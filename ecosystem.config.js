module.exports = {
  apps : [{
    name: 'selenium-proxy:deu-web-pop',
    script: 'index.py',
    args: '--batch=deu-web-pop --vdisplay=1',
    exec_mode: 'fork',
    instances: 1
  }, {
    name: 'selenium-proxy:deu-web-ban',
    script: 'index.py',
    args: '--batch=deu-web-ban --vdisplay=1',
    exec_mode: 'fork',
    instances: 1
  }, {
    name: 'selenium-proxy:deu-mob-pop',
    script: 'index.py',
    args: '--batch=deu-mob-pop --vdisplay=1',
    exec_mode: 'fork',
    instances: 1
  }, {
    name: 'selenium-proxy:deu-mob-ban',
    script: 'index.py',
    args: '--batch=deu-mob-ban --vdisplay=1',
    exec_mode: 'fork',
    instances: 1
  }]
};
