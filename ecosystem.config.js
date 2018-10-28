module.exports = {
  apps : [{
    name: 'selenium:deu-mob-ban',
    script: 'index.py',
    args: '--batch=deu-mob-ban --vdisplay=1',
    exec_mode: 'fork',
    instances: 1
  }]
};
