
from http import HTTPStatus
import threading
import time
from flask import Flask, request, jsonify

from ssmts.data.loaders.stock_loader import StockLoader
from ssmts.services.consumer.trade_snapshot_sub import TradeSnapshotSubscriber
from  ssmts.services.trade_service import ZMQ_TRADE_SNAPSHOT_SUB_ADDRESS
from ssmts.utility.stock_utils import StockUtils


app = Flask(__name__)

@app.before_first_request
def load_data():
    """
    Load data into the application before the first request.
    This is where you can initialize your data store or perform any setup needed.
    """
    StockLoader.load() ### Load stock data into the registry (central store)
    print("Stock data loaded into the registry.")

@app.before_request
def before_request():
    """
    This function runs before each request.
    You can use it to perform any setup needed for each request.
    """
    # Example: Check if the request is valid or authenticate the user
    request.start_time = time.time()  # Store the start time of the request
    print(f"Request started at: {request.start_time}")


@app.after_request
def after_request(response):
    """
    This function runs after each request.
    You can use it to perform any cleanup or logging needed after the request is processed.
    """
    response_time = time.time() - request.start_time
    print(f"Request completed in: {response_time} seconds")
    return response


@app.route('/', methods=['GET'])
def index():
    """
    Index route for the application.
    You can use this to provide a welcome message or documentation for your API.
    """
    return jsonify({"message": "Welcome to the Stock Market Trading System API!"}), HTTPStatus.OK


@app.route('/calculate/peRatio/<stock_id>/<stock_price>', methods=['GET'])
def calculate_pe_ratio(stock_id, stock_price):
    """
    Calculate the Price-to-Earnings (P/E) ratio for a given stock ID and stock price.
    
    :param stock_id: The ID of the stock.
    :param stock_price: The current stock price.
    :return: JSON response with the P/E ratio.
    """
    try:
        # Assuming StockUtils is already imported and available
        pe_ratio = StockUtils.calculate_pe_ratio(stock_id, float(stock_price))
        return jsonify({"pe_ratio": pe_ratio}), HTTPStatus.OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

@app.route('/calculate/dividendYield/<stock_id>/<stock_price>', methods=['GET'])
def calculate_dividend_yield(stock_id, stock_price):
    """
    Calculate the dividend yield for a given stock ID and stock price.
    
    :param stock_id: The ID of the stock.
    :param stock_price: The current stock price.
    :return: JSON response with the dividend yield.
    """
    try:
        # Assuming StockUtils is already imported and available
        dividend_yield = StockUtils.calculate_dividend_yield(stock_id, float(stock_price))
        return jsonify({"dividend_yield": dividend_yield}), HTTPStatus.OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
        

@app.route('/GBCE/index', methods=['GET'])
def calculate_gbce_index():
    """
    Calculate the GBCE All Share Index.
    
    :return: JSON response with the GBCE All Share Index.
    """
    try:
        # Assuming StockUtils is already imported and available
        gbce_index = StockUtils.calculate_all_share_index()
        return jsonify({"gbce_index": gbce_index}), HTTPStatus.OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@app.route('/vwsp/<stock_id>', methods=['GET'])
def calculate_vwsp(stock_id):
    """
    Calculate the Volume Weighted Stock Price (VWSP) for a given stock ID.
    This should be updated realtime based on the incoming trades and snapshot
    
    :param stock_id: The ID of the stock.
    :return: JSON response with the VWSP.
    """
    try:
        # Assuming StockUtils is already imported and available
        vwsp = StockUtils.calculate_vwsp(stock_id)
        return jsonify({"Volume Weighted Stock Price": vwsp}), HTTPStatus.OK
    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

if __name__ == '__main__':

    # Initialize the TradeSnapshotSubscriber
    subscriber = TradeSnapshotSubscriber(address=ZMQ_TRADE_SNAPSHOT_SUB_ADDRESS)

    # Start the subscriber in a separate thread
    subscriber_thread = threading.Thread(target=subscriber.consume_snapshots)
    subscriber_thread.start()

    time.sleep(5)  # Give some time for the subscriber to start

    # Run the Flask application
    publisher_thread = threading.Thread(target=app.run(debug=True, host='0.0.0.0', port=5000))
    publisher_thread.start()

    # Wait for both threads to finish
    publisher_thread.join()
    subscriber_thread.join()
    