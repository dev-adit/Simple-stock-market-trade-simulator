#!/bin/bash

cd "$(dirname "$0")" || exit 1

export PYTHONPATH=.
echo "pythonpath: $PYTHONPATH"
echo "Running tests..."
python3 -m unittest discover -s ssmts/tests -p "test_*.py" -v || exit 1