#!/bin/bash

python create_data.py --min_temp 0.5 --max_temp 4.5 -b 100 --train
python create_data.py --min_temp 0.5 --max_temp 4.5 -b 100 --test

python create_data.py --min_temp 0.5 --max_temp 4.5 -b 100 --test --temp_classify