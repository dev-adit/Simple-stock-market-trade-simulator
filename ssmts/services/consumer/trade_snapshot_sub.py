
# -*- coding: utf-8 -*-

import zmq
import logging

from ssmts.data.loaders.stock_loader import StockLoader
from ssmts.data.store.stock_registry import StockRegistry
from ssmts.data.store.trade_snapshot_registry import TradeSnapShotRegistry
from ssmts.models.trade import Trade

from ssmts.models.trade_snapshot import TradeSnapShot
from datetime import datetime

from ssmts.utility.stock_utils import StockUtils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TradeSnapshotSubscriber is responsible for subscribing to trade messages from a publisher.
# It uses ZeroMQ to receive messages and processes them by adding them to the TradeSnapshotRegistry.
# It can be instantiated and used to consume trades from a publisher.
# It also handles the connection to the publisher and manages the subscription to trade messages.
# It uses a polling mechanism to check for incoming messages and processes them accordingly.
# It also handles timeouts and errors during message consumption.
# It can be used to create a snapshot of trades and store them in the TradeSnapshotRegistry.
# It can be extended to include additional functionality such as filtering messages or processing them in a specific way.
# It can also be used to create a snapshot of trades and store them in the TradeSnapshotRegistry.

class TradeSnapshotSubscriber:
    def __init__(self, address="tcp://localhost:5556"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket.setsockopt(zmq.RCVTIMEO, 5000)
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.address = address
        logger.info(f"Connected to {address} and subscribed to trade messages.")
        StockLoader.load()  # Load stock data into the registry (central store)
    
    def consume_snapshots(self):
        while True:
            try:
                socks = dict(self.poller.poll(1000))  # Poll for incoming messages
                if self.socket in socks and socks[self.socket] == zmq.POLLIN:
                    message = self.socket.recv_string()
                    snapshot = eval(message)
                    logger.info(f"Received trade snapshot in metrics service")
                    # Process the trade message here
                    snapshot = TradeSnapShot.from_dict(snapshot)  # Deserialize the trade message
                    TradeSnapShotRegistry.add(snapshot.stockId, snapshot)
                    vwsp = StockUtils.calculate_vwsp(snapshot.stockId)
                    StockRegistry.update_stock_price(snapshot.stockId, price=vwsp) #realtime update of stock price
                    logger.info(f"Trade snapshot {snapshot.stockId} updated/added in TradeSnapShotRegistry.")
            except zmq.Again as e:
                logger.warning(f"Polling timed out: {e}")
            except Exception as e:
                logger.error(f"Error while consuming trades: {e}")