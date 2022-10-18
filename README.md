# Duck's Docker-Compose

An enhanced Docker-Compse that:

* Finds the docker-compose-file.yaml in the parent directories
* Defaults to Daemon on up
* Adds a "shell" command (future)

## Enhanced docker-compose-file searching

In addition to looking for the docker-compose variants (docker-compose.yml,
docker-compose.yaml, compose.yml, and compose.yaml) in the current directory,
it searches for it in all the parent directories.  If not found, it then tries
the `DOCKER_COMPOSE_FILE` enviroment variable.

## Daemon by default

This may be personal opinion, but for me 99% of the time `docker-compose up`
should be run with the `-d` flag.  This code does that by default.  Specify
the `-D` flag to use the legacy foreground run.  In addition, this can be
disabled by setting the `DOCKER_COMPOSE_UP_IN_FOREGROUND` environment variable.
(The environment variable setting is not yet supported).

## ddc shell (not yet implemented)

The `ddc shell service` command is essentially a shortcut for `docker-compose 
exec service /bin/bash`.  It also has the features that it searches your
`DOCKER_COMPOSE_SHELLS` for available shells in the service.  If not set, it will use
`/bin/zsh:/bin/bash:/bin/sh` as the search value.  In addition, if no service
is supplied, it will use the `DOCKER_COMPOSE_SHELL_SERVICE` environment varaible.

## Installation

```
pip3 install git+https://github.com/bonafideduck/ducks-docker-compose.git@main
```
