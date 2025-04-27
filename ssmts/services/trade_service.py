
import threading
import time

from ssmts.services.consumer.trade_sub import TradeSubscriber
from ssmts.services.producer.trade_pub import TradePublisher

LOCK = threading.Lock()

ZMQ_TRADE_PUB_ADDRESS = "tcp://localhost:5555"
ZMQ_TRADE_SNAPSHOT_SUB_ADDRESS = "tcp://localhost:5556"


if __name__ == "__main__":
    # Initialize the TradePublisher and TradeSubscriber
    subscriber = TradeSubscriber(address=ZMQ_TRADE_PUB_ADDRESS, snapShotPubAddress=ZMQ_TRADE_SNAPSHOT_SUB_ADDRESS)
    publisher = TradePublisher(address=ZMQ_TRADE_PUB_ADDRESS, batch_size=5, total_trades=10, interval=1)

    # Start the subscriber in a separate thread
    subscriber_thread = threading.Thread(target=subscriber.consume_trades)
    subscriber_thread.start()

    time.sleep(2)  # Give some time for the subscriber to start

    # Start the publisher in a separate thread
    publisher_thread = threading.Thread(target=publisher.publish_trades)
    publisher_thread.start()

    # Wait for both threads to finish
    publisher_thread.join()
    subscriber_thread.join()