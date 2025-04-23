import logging
import zmq
import random
import time
import uuid
from datetime import datetime
from ssmts.config.constants import TradeType
from ssmts.data.loaders.stock_loader import StockLoader
from ssmts.data.store.stock_registry import StockRegistry

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
print("Debugging: Logger initialized.")
logger.info("TradePublisher initialized.")

class TradePublisher:
    def __init__(self, address="tcp://localhost:5555", batch_size=5, total_trades= 10, interval=1):
        StockLoader.load()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(address)
        self.batch_size = batch_size
        self.total_trades = total_trades
        self.interval = interval

    def generate_trade(self):
        """
        Generates a random trade with required fields.
        """
        _stocks = StockRegistry.get_all()

        stock = random.choice(list(_stocks.keys()))
        action = random.choice([t.value for t in TradeType])
        trade_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        trade = {
            "tradeId": trade_id,
            "timestamp": timestamp,
            "indicator": action,
            "stockId": stock,
            "price": round(random.uniform(10, 1000), 2),
            "quantity": random.randint(1, 100)
        }
        return trade

    def publish_trades(self):
        """
        Publishes a batch of trades at a specified interval.
        """
        for _ in range(self.total_trades):
            trades = [self.generate_trade() for _ in range(self.batch_size)]
            for trade in trades:
                self.socket.send_string(f'{trade}')
                logger.info(f"Published trade: {trade}")
            time.sleep(self.interval)

if __name__ == "__main__":
    logger.info("Starting TradePublisher...")
    publisher = TradePublisher()
    try:
        publisher.publish_trades()
    except KeyboardInterrupt:
        logger.info("Shutting down publisher...")
    
