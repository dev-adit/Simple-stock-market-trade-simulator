
#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status

echo "Starting services..."

mkdir -p logs # Create logs directory if it doesn't exist

export PYTHONPATH=$(pwd)
echo "starting trade consumer..."
nohup python -m debugpy --listen 5678 -m ssmts.services.consumer.trade_sub > logs/trade_consumer.log 2>&1 & # Start the debugger in the background
echo "starting trade producer..."
nohup python -m debugpy --listen 5679 -m ssmts.services.producer.trade_pub > logs/trade_producer.log 2>&1 & 
echo "starting market metrics..."
nohup python -m debugpy --listen 5680 -m ssmts.services.market_metrics > logs/RESTer_market_metrics.log 2>&1 & 
DEBUG_PID=$! # Get the PID of the debugger
sleep 5 # Wait for the debugger to start

echo "opening flask RESTer in browser..."
python -m webbrowser -t "http://localhost:5000" # Open the Flask RESTer in the default web browser
echo "Debugger started with PID: $DEBUG_PID"
