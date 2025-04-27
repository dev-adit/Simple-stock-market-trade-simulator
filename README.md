# Simple-stock-market-trade-simulator
A simple Trade simulator comes with an ability to consume and ingest trades real time and providing real time trade / stock metrics

Requirement:
    a. For a given stock,
        i. Given any price as input, calculate the dividend yield
        ii. Given any price as input, calculate the P/E Ratio
        iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and
            traded price
        iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes
    b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks

Requirements to run:
python==3.11
flask==3.0.3
pyzmq==26.0.0

Setps to Run:
<TBD>


Idea:
1. We already have a pre-defined stocks data & set o formulas that our application would serve the service.
2. Our application should be able to :
    a. Consume incoming trade data/payload:
        i. Assuming it can be flowing in from another internal application real time.
        2. scalable enough to handle other consumption mechanism
    b. Store provide central trade storage (in memory)
        i. Should maintain data integrity
        2. Should serve as a single golden source for any data publish/ service
    c. serve real-time data metrics
        i.  based on static stocks
        ii. real-time trade consumption
3. Provide unit-test Coverage