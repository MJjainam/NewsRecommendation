var express = require('express');
var router = express.Router();

var news = require("../models/news");


// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
	res.header('Cache-Control', 'no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0');
	news.getNews(req.user,function(err,news){
		res.render('index',{news:news});
	});
});

// router.get('/newsList', function (req, res) {
// 	console.log("kakakkka");
// 	User.getNewsList(function (newsList) {
// 		// console.log(newsList);
// 		res.render('user-list', { newsList: newsList });

// 	});
// 	// var userList = db.collection('users');
// 	// userList.find().toArray(function (err, users) {
// 	// console.log(users);
// 	// });
// 	// res.render('user-list');
// });

function ensureAuthenticated(req, res, next){
	if(req.isAuthenticated()){
		return next();
	} else {
		//req.flash('error_msg','You are not logged in');
		res.redirect('/users/login');
	}
}

module.exports = router;