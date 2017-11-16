import csv
from math import sqrt
from pymongo import MongoClient
import math
import random

dataset = {}

def get_items_news_table(score_list, total):
    result = {}
    count = 0
    for tup in score_list:
        category = tup[0]
        number = tup[1]
        # 10 is set as the limit
        limit = round(number/total*10)
        client = MongoClient()
        db = client.newsRecommender
        out = db.news.find({"CATEGORY":category}).limit(limit)
        for item in out:
            #print(item)
            if count>=10:
                break
            result.setdefault(item['URL'], ())
            #result[item['URL']].setdefault(item['TITLE'])
            result[item['URL']] = (item['TITLE'], item['CATEGORY'])
            count += 1
    return result

# this fetches 10 news at random -
def get_news_table_random(result, samples):
    #result = {}
    client = MongoClient()
    db = client.newsRecommender
    total = db.news.count()
    #samples = 10
    for i in range(samples):
        random_num = math.floor(random.random()*total)
        doc = db.news.find().skip(random_num).limit(1).next()
        result[doc['URL']] = (doc['TITLE'], doc['CATEGORY'])
        #result.setdefault(doc['URL'], ())
        #result[doc['URL']] = (doc['TITLE'], doc['CATEGORY'])

    return result

def create_dataset_from_clicks():
    global dataset

    #res = searchInDBWithLimit(db,"category","t",1)
    client = MongoClient()
    db = client.newsRecommender
    res = db.clicks.find()
    #print(res)
    for doc in res:
        #print(doc)
        dataset.setdefault(doc['USERNAME'], {})
        dataset[doc['USERNAME']].setdefault(doc['URL'], (doc['CATEGORY'], doc['TITLE']))

def similarity(person1,person2):
    # To get both rated items
    both_person_category = {}
    for url in dataset[person1]:
        if url in dataset[person2]:
            both_person_category[url] = 1
    number_of_common_category = len(both_person_category)
    # Checking for number of ratings in common
    if number_of_common_category == 0:
        return 0
    # else  - jaccard similarity   ===> agreement_count / total_count
    total_count = len(dataset[person1]) + len(dataset[person2]) - number_of_common_category
    similarity = number_of_common_category / total_count
    return similarity

def get_category_count(person):
    b_category_count = 0
    e_category_count = 0
    m_category_count = 0
    t_category_count = 0
    total_category_count = 0
    for url in dataset[person]:
        if dataset[person][url][0] == 'b':
            b_category_count += 1
        elif dataset[person][url][0] == 'e':
            e_category_count += 1
        elif dataset[person][url][0] == 'm':
            m_category_count += 1
        elif dataset[person][url][0] == 't':
            t_category_count += 1
        total_category_count += 1
    return (b_category_count, e_category_count, m_category_count, t_category_count, total_category_count)

# return type for this function is - {"URL":("TITLE", "CATEGORY")}
def user_recommendations(person):
    global dataset

    final_recommendation = {}

    create_dataset_from_clicks()
    # if the person has not yet clicked anything yet, choose 10 news at random
    if dataset.get(person) == None:
        final_recommendation = get_news_table_random(final_recommendation, 10)
        return final_recommendation
    # Gets recommendations for a person by using a weighted average of every other user's rankings
    totals = {}
    simSums = {}
    rankings_list = []
    category_count = get_category_count(person)
    url_title = {}
    for other in dataset:
        # don't compare me to myself
        if other == person:
            continue
        sim = similarity(person,other)
    # ignore scores of zero or lower
        if sim<=0:
            continue
        for url in dataset[other]:
            # only score items i haven't seen yet
            url_category = dataset[other][url][0]
            title = dataset[other][url][1]
            #print(dataset[other][url])
            if url not in dataset[person]:     # or dataset[person][url] == 0:
                # Similarity * score
                #print(dataset[person][url])
                #title = dataset[person][url][1]
                totals.setdefault(url,0)
                url_title.setdefault(url, ())
                url_title[url] = (title, url_category)
                # working on assigning weights - for now just assuming the similarity
                #totals[url] += dataset[other][url]* sim
                # 1 approach - see the category and the number of times this person has visited that category
                result = 1
                denominator = (category_count[4] + 4)
                # applied laplace smoothing techniques -
                if url_category == 'b':
                    result = (category_count[0] + 1) / denominator
                elif url_category == 'e':
                    result = (category_count[1] + 1) / denominator
                elif url_category == 'm':
                    result = (category_count[2] + 1) / denominator
                elif url_category == 't':
                    result = (category_count[3] + 1) / denominator
                totals[url] += result * sim
                # sum of similarities
                simSums.setdefault(url,0)
                simSums[url]+= sim
    # Create the normalized list
    #print(totals.items())
    rankings = [(total/simSums[url],url) for url,total in totals.items()]
    #print(rankings)
    rankings.sort()
    rankings.reverse()
    # returns the recommended items
    recommendataions_list = [recommend_item for score,recommend_item in rankings]

    count = 0
    for item in recommendataions_list:
        # get only top-10 recommendations
        if count==10:
            break
        final_recommendation[item] = url_title[item]
        count += 1
    #print(final_recommendation)
    #print(recommendataions_list)
    if len(recommendataions_list) == 0:
        mydict = {}
        mydict['b'] = category_count[0]
        mydict['e'] = category_count[1]
        mydict['m'] = category_count[2]
        mydict['t'] = category_count[3]
        score_list = sorted(mydict.items(), key=lambda kv: kv[1], reverse=True)
        final_recommendation = get_items_news_table(score_list, category_count[4])
    if len(final_recommendation)<10:
        final_recommendation = get_news_table_random(final_recommendation, 10-len(final_recommendation))
    # not yet handled the recommendation length > 10
    #elif len(final_recommendation)>10:
    return final_recommendation

# run  - user_recommendations(username)
recommended_result = user_recommendations('jain')
print(recommended_result)
