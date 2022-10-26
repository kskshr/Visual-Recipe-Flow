#!/bin/zsh

## download recipe texts and cooking videos
while read line; do
    recipe_id=${line:t}
    d=./data/recipes/${recipe_id}
    mkdir -p ${d}

    wget ${line} -O ${d}/source.txt
    sleep 5s

    video_url=$(cat ${d}/source.txt | grep -Eo "https[^ ]*mp4" | head -n1)
    wget ${video_url} -O ${d}/video.mp4
    sleep 5s

    mkdir -p ${d}/frames
    python scripts/sample_frames.py ${d}
done < ./data/recipe_urls.txt

## extract ingredients and instructions from a source file
python scripts/parser.py 

## tokenize words
python scripts/tokenize.py


