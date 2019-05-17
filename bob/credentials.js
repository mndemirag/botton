const fs = require('fs');

let credentials = JSON.parse(fs.readFileSync('credentials.json'));

const getUser = (req) => {
  return credentials[req.header('Authorization')];
};

const getFirstToken = () => {
  return credentials[Object.keys(credentials)[0]].auth_token;
};

module.exports = {
  getUser,
  getFirstToken
};
