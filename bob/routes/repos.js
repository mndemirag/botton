const fs = require('fs');
const express = require('express');
const router = express.Router();
const {getRepos, getPRs, mergePR} = require('../ghe-service');

const GENERIC_ERROR_MESSAGE = '-- error --';

let credentials = JSON.parse(fs.readFileSync('credentials.json'));  

const getUser = (req) => {
  return credentials[req.get('Uid')];
};

// List of all repos
router.get('/', (req, res, next) => {
  const user = getUser(req);
  if (!user) return res.json({ message: 'Not authorized' });

  res.json({
    user: user.name,
    repos: getRepos(),
  });
});

// List of all mergeable PRs for a specific repo
router.get('/:repoId/pulls', (req, res, next) => {
  const user = getUser(req);
  if (!user) return res.json({ message: 'Not authorized' });

  const repoId = req.params.repoId;
  const repo = getRepos().find(repo => repo.id === repoId);

  if (!repo) {
    return res.json({
      message: GENERIC_ERROR_MESSAGE,
    });
  }

  res.json({
    user: user.name,
    repo: repoId,
    pull_requests: getPRs(repoId),
  }); 
});

// Merge a PR for a repo
router.put('/:repoId/pulls/:prId/merge', (req, res, next) => {
  const user = getUser(req);
  if (!user) return res.json({ message: 'Not authorized' });

  const {repoId, prId} = req.params;

  if (!getPRs(repoId).find(pr => pr.id === parseInt(prId))) {
    return res.json({ message: GENERIC_ERROR_MESSAGE });
  }
  
  mergePR(repoId, prId, user.auth_token, (result = {}) => {
    if (result.merged) {
      return res.json({ message: 'Success: all done' });
    }
    
    return res.json({ message: GENERIC_ERROR_MESSAGE })
  });
 
});

module.exports = router;
