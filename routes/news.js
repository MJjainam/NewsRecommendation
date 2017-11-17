var express = require('express');
var router = express.Router();
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var Token = require('../models/token');
var crypto = require('crypto');

var User = require('../models/user');  //model stores all the logical part. Importing 
//functions assosiated with the user.

var news = require("../models/news");

router.get("/process/:articleID?",function(req,res){
    news.storeClick(req.user.username,req.params.articleID,function(url){
        console.log("inside anonymous function of storeClick");
        console.log("see here now: " +url);
        // res.redirect(url);
    });
    // res.redirect("index");
});

module.exports = router;
