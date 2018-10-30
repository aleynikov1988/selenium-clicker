
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM joyzoursky/python-chromedriver:3.6-xvfb

# install PM2
RUN wget -qO- https://deb.nodesource.com/setup_8.x | bash - \
&& apt-get install -y nodejs \
&& npm i pm2 -g

WORKDIR /app
ADD . /app

# Using pip:
RUN python -m pip install -r requirements.txt
# CMD [ "pm2-runtime", "start", "ecosystem.config.js" ]
CMD [ "python", "index.py", "--batch=deu-mob-ban", "--vdisplay=1"]
