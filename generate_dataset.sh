#!/bin/bash

python create_data.py --lattice_size [4,4] --min_temp 0.5 --max_temp 4.5 -b 100 --train
python create_data.py --lattice_size [4,4] --min_temp 0.5 --max_temp 4.5 -b 100 --test

python create_data.py --lattice_size [4,4] --min_temp 0.5 --max_temp 4.5 -b 100 --test --temp_classify

python create_data.py --lattice_size [8,8] --min_temp 0.5 --max_temp 4.5 -b 100 --train
python create_data.py --lattice_size [8,8] --min_temp 0.5 --max_temp 4.5 -b 100 --test

python create_data.py --lattice_size [8,8] --min_temp 0.5 --max_temp 4.5 -b 100 --test --temp_classify

python create_data.py --lattice_size [16,16] --min_temp 0.5 --max_temp 4.5 -b 100 --train
python create_data.py --lattice_size [16,16] --min_temp 0.5 --max_temp 4.5 -b 100 --test

python create_data.py --lattice_size [16,16] --min_temp 0.5 --max_temp 4.5 -b 100 --test --temp_classify

python create_data.py --lattice_size [25,25] --min_temp 0.5 --max_temp 4.5 -b 100 --train
python create_data.py --lattice_size [25,25] --min_temp 0.5 --max_temp 4.5 -b 100 --test

python create_data.py --lattice_size [25,25] --min_temp 0.5 --max_temp 4.5 -b 100 --test --temp_classify

python create_data.py --lattice_size [32,32] --min_temp 0.5 --max_temp 4.5 -b 100 --train
python create_data.py --lattice_size [32,32] --min_temp 0.5 --max_temp 4.5 -b 100 --test

python create_data.py --lattice_size [32,32] --min_temp 0.5 --max_temp 4.5 -b 100 --test --temp_classify