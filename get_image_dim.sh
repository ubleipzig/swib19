#!/bin/bash

file $1 | grep -o -E ', [0-9]{3,}x[0-9]{3,}' | tr -d ','

