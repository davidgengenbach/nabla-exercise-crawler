#!/usr/bin/env sh

NUMBER_EXERCISES=$1

if [ -z "$NUMBER_EXERCISES" ]
then
    NUMBER_EXERCISES=1
fi

for i in `seq 1 $NUMBER_EXERCISES`
do
    echo "Excercise $i/$NUMBER_EXERCISES"
    python3 crawler.py 2> /dev/null
    python3 update_output.py
    echo ""
done

http-server output -o || open 'http://127.0.0.1:8080/'