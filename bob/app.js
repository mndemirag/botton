var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const credentials = require('./credentials');
const gheService = require('./ghe-service');

const reposRouter = require('./routes/repos');

const app = express();

gheService.init(credentials.getFirstToken());

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/repos', reposRouter);

module.exports = app;
