module.exports = {
  apps : [{
    name: 'selenium-proxy',
    script: 'index.py',
    exec_mode: 'fork',
    instances: 2
  }]
};
