#!/bin/bash

cd ../sql

psql -h ischool.berkeley.edu -p 5432 -d censusmapper -U censusmapper < db_creation.sql

cd ../python

./db_insert_measures.py
./db_insert_colors.py

