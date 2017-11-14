var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/newsRecommender');
var db = mongoose.connection;
var spawn = require("child_process").spawn;	

var newsSchema = mongoose.Schema({
	ID: {
		type: Number,
		index: true,
		unique: true
	},
	TITLE: {
		type: String
	},
	URL:{
		type: String
	},
	PUBLISHER: {
		type: String
	},
	CATEGORY:{
		type: String
	},
	STORY:{
		type: String
    },
    HOSTNAME:{
        type:String
    },
    TIMESTAMP:{
        type: Number
    }
});

var clickSchema = mongoose.Schema({
	USERNAME:{
		type:String
	},
	URL:{
		type:String
	},
	CATEGORY:{
		type:String
	},
	TITLE:{
		type:String
	},
	ID:{
		type:String,
	}
});

var News = module.exports = mongoose.model('News', newsSchema);
var Clicks = module.exports = mongoose.model('Clicks',clickSchema);
module.exports.getNews = function(user,callback){

	var process = spawn('python3',["./user_based_recommender/user_recommender.py", user.username]);
	
	News.aggregate({$sample:{size:10}}).exec(callback);
}

module.exports.storeClick = function(username,articleID){
	var query = {ID:articleID};
	News.findOne(query,function(err,news){
		console.log(news.PUBLISHER);
		var clickJson = {
			USERNAME:username,
			URL:news.URL,
			CATEGORY:news.CATEGORY,
			TITLE:news.TITLE,
			ID: news.ID
		};
		db.collection('clicks').insert(clickJson);
		return news.url;
	});

}