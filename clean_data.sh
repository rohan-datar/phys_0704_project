#!/bin/bash

# This script will clean the data from the raw data directory
rm -f ./data/binary_class/test/less_than_critical/*
rm -f ./data/binary_class/test/greater_than_critical/*
rm -f ./data/binary_class/train/less_than_critical/*
rm -f ./data/binary_class/train/greater_than_critical/*

rm -rf ./data/temp_class/test/*
rm -rf ./data/temp_class/train/*