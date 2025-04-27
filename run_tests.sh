#!/bin/bash

cd "$(dirname "$0")" || exit 1

export PYTHONPATH=$(pwd)
echo "pythonpath: $PYTHONPATH"
echo "Running tests..."
python3 -m unittest discover -s ssmts/tests -p "test_*.py" -v || { echo "Tests failed"; exit 1; }