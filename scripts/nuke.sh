#!/bin/bash

echo
read -p "Do you REALLY want to nuke the local docker environment? " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

# Don't ask for confirmation as we did already
docker compose down --remove-orphans --volumes
docker compose rm -v --force
