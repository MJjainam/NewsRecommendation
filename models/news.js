var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/newsRecommender');
var db = mongoose.connection;

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

var News = module.exports = mongoose.model('News', newsSchema);

module.exports.getNews = function(callback){
	console.log("in getNews");
	var query = {};
	News.aggregate({$sample:{size:10}}).exec(callback);
}