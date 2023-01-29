# New Taipei City Traffic Adjudication Office Bot
A bot to help you get case status and send to line chat from New Taipei City Traffic Adjudication Office.

[![Docker Image CI](https://github.com/DoubleChuang/New-Taipei-City-Traffic-Adjudication-Office-Bot/actions/workflows/docker-image.yml/badge.svg)](https://github.com/DoubleChuang/New-Taipei-City-Traffic-Adjudication-Office-Bot/actions/workflows/docker-image.yml)

### run from source
```
docker run -d --name=selenium-hub --rm -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.2.0
docker run -d --name=selenium-hub4_8 --rm -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.8.0-20230123

pyenv activate inline
export PYTHONPATH=`pwd`:$PYTHONPATH
CASE_ID= \
ACDT_DATE= \
LINE_TOKEN= \
CHROME_REMOTE_URL=http://127.0.0.1:4444/wd/hub \
python3 inline/__main__.py
```

## docker-compose
#### Build inline docker image
```
./scripts/build.sh
```

#### Create a .env file by referring to the example below
Refer to [.env.sample](.env.sample) to write environment variables

```
CASE_ID=
ACDT_DATE=1110912
LINE_TOKEN=
CHROME_REMOTE_URL=http://selenium-hub:4444/wd/hub
FINAL_SCREEN_PATH=/final_screen
```
> If you have not adjusted the container name and binding port, you do not need to adjust **CHROME_REMOTE_URL**

#### Create and start containers
```
docker-compose up -d
```

#### Stop and remove containers, networks
```
docker-compose down
```


### reference

[chromium driver](https://chromedriver.chromium.org/downloads)


### TODO
- [ ] crontab
