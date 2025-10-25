#!/bin/bash

filename="${1##*/}"
filename="${1%.*}"
filename="$filename.mp3"
ffmpeg -i "$1" -q:a 0 -map a "data/$filename"

cp "data/$filename" "data/recordings/$filename"