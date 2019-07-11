#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

/usr/bin/python -u $DIR/main.py >> $DIR/log.txt 2>&1