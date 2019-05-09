const request = require('request');

// These are all the repos that will show up
// (hardcoding since we have TONS of useless repos in the first-aid scope)
// display_name has 16-char cap
const REPOSITORIES = [
  {
    display_name: 'support-site',
    id: 'support-site',
  },
  {
    display_name: 'susi-frontend',
    id: 'support-site-frontend',
  },
  {
    display_name: 'susi-backend',
    id: 'support-site-backend',
  },
  {
    display_name: 'susi-router',
    id: 'support-site-router',
  },
  {
    display_name: 'botton (meta!)',
    id: 'botton-demo',
  }
];

const BASE_URL = 'https://ghe.spotify.net/api/v3/';

// base config when communicating with GHE API
const requestConfig = { 
  json: true,
  headers: {
    'Authorization': `token ${process.env.AUTHTOKEN}`,
  },
};

const repoPRs = {};

// Get all current repos. More useful in the potential future where we have dynamic repos
const getRepos = () => {
  return REPOSITORIES;
};

// Get all PRs for a specific repo
const getPRs = repoId => {
  return repoPRs[repoId] || [];
}

// Merge a specific PR in a specific repo. 
const mergePR = (repoId, prId, callback) => {
  const url = `${BASE_URL}repos/first-aid/${repoId}/pulls/${prId}/merge`;
  request(url, {
    ...requestConfig, 
    method: 'PUT',
    body: { merge_method: 'squash' },
  }, (err, res, body) => {
    if (err) { console.log(err); return; }
    callback(body);
  });
};

// Run once to setup automatic reload of GHE data
const init = () => {
  if (!process.env.AUTHTOKEN) {
    console.error('Error: env var AUTHTOKEN is missing');
    process.exit(1);
  }

  updatePRdata();
  setInterval(updatePRdata, 10000);
};

const updatePRdata = () => {
  console.log('--- Updating PR data');

  REPOSITORIES.forEach(repoId => {
    const url = `${BASE_URL}repos/first-aid/${repoId.id}/pulls`;
    
    request(url, requestConfig, (err, res, body) => {
      if (err) { console.log(err); return; }
      
      // Remove open and locked PRs
      const PRs = body.filter(pr => {
          if (pr.state !== 'open') return false;
          if (pr.locked) return false;
          return true;
        });

      // Simply flush the current info about PRs
      repoPRs[repoId.id] = [];
      
      // Fetch extra info for every open PR for this repo
      PRs.forEach(pr => {
        const url = `${BASE_URL}repos/first-aid/${repoId.id}/pulls/${pr.number}`;
        request(url, requestConfig, (err, res, pr) => {
          if (err) { console.log(err); return; }
          
          if (!pr.mergeable) return;
          if (pr.mergeable_state !== 'clean') return; 
            
          // Store only the part of the PR object that we need
          repoPRs[repoId.id].push({
            id: pr.number,
            title: pr.title,
          });
        });
      });
    });
  });
};

module.exports = {
  init, 
  getRepos,
  getPRs,
  mergePR,
};
