#!/usr/bin/env bash

GAME_DIR=./games

function extract() {
    game=$1
    echo "extracting $1..."
    zipfile=$(jq --raw-output ".$game.zipfile" < games.json)
    cd $GAME_DIR
    if [ ! -d "$game" ]; then
        unzip -d "$game" "$zipfile"
    fi
}

games=$(jq --raw-output "keys[]" < games.json)
for game in $games; do
    extract $game
done
