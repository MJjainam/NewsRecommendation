
# coding: utf-8

# In[1]:


import csv
from math import sqrt


# In[2]:


dataset = {}


# In[3]:


def load_data(input_name):
    global dataset
    
    input_file = open(input_name, 'rU')
    flag = True
    for line in input_file:
        # executing flag for the first time to eliminate the first row that tells the column names in CSV file
        if flag==True:
            flag = False
            continue
        row = str(line)
        row = row.split(',')
        #print(row)
        # to remove '\n' in the end - 
        row[3] = row[3][:-1]
        dataset.setdefault(row[0], {})
        dataset[row[0]].setdefault(row[1], (row[2], row[3]))
        print(row[3])


# In[4]:


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


# In[7]:


dataset


# In[6]:


load_data('testData.csv')
#similarity('jain', 'nish')


# In[8]:


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
    
    


# In[32]:


def user_recommendations(person):
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
                url_title.setdefault(url, "")
                url_title[url] = title
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
    final_recommendation = []
    for item in recommendataions_list:
        final_recommendation.append((item,url_title[item]))
    #print(final_recommendation)
    #print(recommendataions_list)
    if len(recommendataions_list) == 0:
        mydict = {}
        mydict['b'] = category_count[0]
        mydict['e'] = category_count[1]
        mydict['m'] = category_count[2]
        mydict['t'] = category_count[3]
        print(sorted(mydict.items(), key=lambda kv: kv[1], reverse=True))
        
    return final_recommendation


# In[36]:


recommended_result = user_recommendations('jatin')


# In[37]:


dataset['jain']['google'][1]


# In[35]:


recommended_result


# In[ ]:




