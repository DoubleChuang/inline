# Inline

### run from source
```
pyenv activate inline

export PYTHONPATH=`pwd`:$PYTHONPATH

LINE_TOKEN= \
FINAL_SCREEN_PATH=/final_screen \
INLINE_CONFIG_PATH=/config.json \
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
LINE_TOKEN= 
FINAL_SCREEN_PATH=/final_screen
INLINE_CONFIG_PATH=/config.json
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



### TODO
- [ ] crontab
