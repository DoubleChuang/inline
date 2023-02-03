# Inline
[![Docker Image CI](https://github.com/DoubleChuang/inline/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/DoubleChuang/inline/actions/workflows/docker-image.yml)
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
> If you do not want to take a screenshot when bot finishes, you can leave `FINAL_SCREEN_PATH` empty
> If you do not want to line notifications, leave `LINE_TOKEN` empty

#### Create and start containers
```
docker-compose up -d
```

#### Stop and remove containers, networks
```
docker-compose down
```
