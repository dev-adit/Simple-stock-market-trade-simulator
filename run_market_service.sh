
#!/bin/bash

export PYTHONPATH=.
export FLASK_APP=ssmts/services/market_metrics.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_EXTRA_FILES=/ssmts/services/market_metrics.py


echo "Starting Flask server..."
flask run --host=0.0.0.0 --port=5000 & # Run the Flask server in the background
FLASK_PID=$! # Get the PID of the Flask server
sleep 5 # Wait for the server to start
echo "Flask server started with PID: $FLASK_PID"