#!/bin/bash

mkdir -p archive

timestamp=$(date +"%Y%m%d-%H%M%S")

if [ -f "grades.csv" ]; then
    new_name="grades_$timestamp.csv"
    mv grades.csv archive/$new_name
    touch grades.csv
    echo "$timestamp | grades.csv -> archive/$new_name" >> organizer.log
    echo "Archive complete."
else
    echo "grades.csv not found."
fi
