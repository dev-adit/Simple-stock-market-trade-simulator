import logging
import zmq
import time

from ssmts.config.constants import TradeType
from ssmts.data.store.trade_registry import TradeRegistry
from ssmts.data.store.trade_snapshot_registry import TradeSnapShotRegistry
from ssmts.models.trade import Trade

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
print("Debugging: Logger initialized.")

IDEAL_THRESHOLD = 10  # Ideal threshold for trade messages

class TradeSubscriber:
    """
    A class to subscribe and process trades from a ZeroMQ socket.
    It validates the trades and retries processing in case of failure.
    This can be instantiate and used to consume trades from a publisher
    """
    def __init__(self, address="tcp://localhost:5555", snapShotPubAddress="tcp://localhost:5556", max_retries=3, retry_interval=1):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket.setsockopt(zmq.RCVTIMEO, 5000)  # Set a timeout for receiving messages

        self.snapShotContext = zmq.Context()
        self.snapShotSocket = self.snapShotContext.socket(zmq.PUB)
        self.snapShotSocket.bind(snapShotPubAddress)

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.address = address
        
        logger.info(f"Connected to {address} and subscribed to trade messages.")
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        logger.info(f"Connected to {address} and subscribed to trade messages.")

        TradeRegistry.register()
        TradeSnapShotRegistry.register()

    def validate_trade(self, trade):
        required_fields = {"tradeId", "timestamp", "indicator", "stockId", "price", "quantity"}
        if not all(field in trade for field in required_fields):
            logger.error(f"Trade validation failed: Missing fields in trade {trade}")
            return False
        if trade["indicator"] not in [t.value for t in TradeType]:
            logger.error(f"Trade validation failed: Invalid trade type {trade['indicator']}")
            return False
        if trade["price"] <= 0 or trade["quantity"] <= 0:
            logger.error(f"Trade validation failed: Invalid price or quantity in trade {trade}")
            return False
        logger.info(f"Trade validation passed for trade {trade.get('tradeId')}")
        return True

    def process_trade(self, trade):
        retry = 0
        while retry <= self.max_retries:
            try:
                TradeRegistry.add(trade.tradeId, trade)
                logger.info(f"Trade {trade.tradeId} added to TradeRegistry.")
                # Simulate processing the trade (e.g., storing in a database)
                # In a real-world scenario, this could involve more complex logic
                return
            except Exception as e:
                retry += 1
                logger.error(f"Failed to process trade {trade}. Retrying {retry}/{self.max_retries}. Error: {e}")
                time.sleep(self.retry_interval)
        else:
            logger.error(f"Failed to process trade after {self.max_retries} retries: {retry}")

    def consume_trades(self):
        ideal_count = 0
        while True:
            time.sleep(1)  # Sleep for a second before polling again
            try:
                socks = dict(self.poller.poll(1000))  # Poll for messages with a timeout of 50 second
                if self.socket in socks and socks[self.socket] == zmq.POLLIN:
                    logger.info("Trade data received.")
                    trade_data = self.socket.recv_string()
                    trade_data = eval(trade_data)
                    logger.info(f"Received trade: {trade_data.get('tradeId')} for stock {trade_data.get('stockId')}")
                    if self.validate_trade(trade_data):
                        trade = Trade.from_dict(trade_data)
                        ### Process the trade ###
                        self.process_trade(trade)
                        ### Update the TradeSnapShotRegistry with the trade ###
                        TradeSnapShotRegistry.update_trade(trade.stockId, trade)
                        logger.info(f"Trade {trade.tradeId} for Stock {trade.stockId} updated in TradeSnapShotRegistry.")
                        ### Send the updated snapshot to the snapshot publisher ###
                        snapshot = TradeSnapShotRegistry.get(trade.stockId)
                        self.snapShotSocket.send_string(f'{snapshot.to_dict()}') ### this can also be persisted to a file/database
                        logger.info(f"Snapshot sent for Stock {trade.stockId}.")
                    else:
                        logger.error(f"Invalid trade discarded: {trade_data.get('tradeId')}")
                else:
                    logger.warning("No trade data received. Polling again...")
                    time.sleep(3)
                    ideal_count += 1
                    if ideal_count > IDEAL_THRESHOLD:
                        logger.warning("No trade data received for a while. Exiting...")
                        self.shutdown()
                        logger.info("Total Trade Logged:")
                        logger.info(TradeRegistry.get_all())
                        break
                    continue
            except KeyboardInterrupt:
                logger.info("Shutting down subscriber...")
                break
            except zmq.Again:
                logger.warning("No message received within the timeout period.")
            except zmq.ZMQError as e:
                logger.error(f"ZMQ error: {e}")
            except ValueError as ve:
                logger.error(f"Value error: {ve}")
            except Exception as e:
                logger.error(f"Error while consuming trades: {e}")
                

    def shutdown(self):
        self.socket.close()
        self.context.term()
        logger.info("TradeSubscriber shutdown complete.")

if __name__ == "__main__":
    logger.info("Starting TradeSubscriber...")
    subscriber = TradeSubscriber()
    subscriber.consume_trades()