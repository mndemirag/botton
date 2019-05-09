var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const gheService = require('./ghe-service');

var reposRouter = require('./routes/repos');

var app = express(); 

gheService.init();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/repos', reposRouter);

module.exports = app;
