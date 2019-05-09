const express = require('express');
const router = express.Router();
const {getRepos, getPRs, mergePR} = require('../ghe-service');

// List of all repos
router.get('/', (req, res, next) => {
  res.json({
    repos: getRepos(),
  });
});

// List of all mergeable PRs for a specific repo
router.get('/:repoId/pulls', (req, res, next) => {
  const repoId = req.params.repoId;
  const repo = getRepos().find(repo => repo.id === repoId);

  if (!repo) {
    return res.json({
      error: 'Unknown repo',
    });
  }

  res.json({
    repo: repoId,
    pull_requests: getPRs(repoId),
  }); 
});

// Merge a PR for a repo
router.put('/:repoId/pulls/:prId/merge', (req, res, next) => {
  const {repoId, prId} = req.params;

  if (!getPRs(repoId).find(pr => pr.id === parseInt(prId))) {
    return res.json({
      error: 'Unknown PR number',
    });
  }
  
  mergePR(repoId, prId, result => {
    res.json(result);
  });
 
});

module.exports = router;
