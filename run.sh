#!/usr/bin/env sh

for i in `seq 1 20`
do
    python3 crawler.py
    python3 update_output.py
done


