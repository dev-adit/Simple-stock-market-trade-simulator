# Simple Stock Market Simulator 
A simple Trade simulator comes with an ability to consume and ingest trades real time and provide real time trade / stock metrics

# Requirements:
For a given stock,
    i. Given any price as input, calculate the dividend yield
    ii. Given any price as input, calculate the P/E Ratio
    iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and
        traded price
    iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes
b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks

**Pre-requisites:**

Before Setting up the project, ensure you have the following installed on your system:

* Python (3.8+ recommended)
* Pip (Python package manager)


# Step 1: Install Python and Pip

1. Download and install Python from the official website: https://www.python.org/downloads/
2. During installation, make sure to check the box that says "Add Python to PATH".
3. After installation, open a command prompt or terminal and run the following command to check if Python is installed correctly:
```bash
python --version
```
4. To check if Pip is installed, run the following command:
```bash
pip --version
```

# Step 2: Install Git
* Install Git from the official website: https://git-scm.com/downloads
* Follow the installation instructions for your operating system.
* After installation, open a command prompt or terminal and run the following command to check if Git is installed correctly:
```bash
git --version
```

# Step 3: Clone the Repository
1. Open a command prompt or terminal and navigate to the directory where you want to clone the repository.
2. Run the following command to clone the repository:
```bash
git clone
git@github.com:dev-adit/Simple-stock-market-trade-simulator.git
OR
https://github.com/dev-adit/Simple-stock-market-trade-simulator.git
```
3. Navigate into the cloned directory:
```bash
cd Simple-stock-market-trade-simulator
```
# Step 4: Install Dependencies
pip install -r requirements.txt


# Step 5: Run the Application

* Option 1: Run Via Launch Task (VsCode or IDE):
1. Open the project in your preferred IDE (e.g., Visual Studio Code).
2. CTRL + Shift + D to open the Run and Debug panel.
3. Select the "Start/ Debug All Services" option from the dropdown menu.

This would start the real time trade publisher, consumer and the web server.

* Option 2: Run Via Command Line:
1. Open a command prompt or terminal and navigate to the directory where you cloned the repository.
2. Run the following command to start the application:
```bash
./start_services.sh
```

# Step 6: Use, Test & verify logs
1. got to the logs directory and check the logs for the publisher and consumer.
2. You can also check the web server logs to verify if the application is running correctly.

3. Open a web browser and navigate to `http://localhost:5000` to access the web interface.
4. You can also use tools like Postman or curl to send requests to the API endpoints.


# step 7: stop the application
1. Open a command prompt or terminal and navigate to the directory where you cloned the repository.
2. Run the following command to stop the application:
```bash
./stop_services.sh
```

# Idea behind the project:
The project is a simple stock market simulator that allows users to perform various operations related to stocks and trades. The main features of the project include:

* We already have a pre-defined stocks data & set of formulas that our application would serve the service.
* Our application should be able to :
    * A. Consume incoming trade data/payload:
        * Assuming it can be flowing in from another internal application real time.
        * scalable enough to handle other consumption mechanism
    * B. *Store provide central trade storage (in memory)
        * Should maintain data integrity
        * Should serve as a single golden source for any data publish/ service
    * C. Serve real-time data metrics
        * based on static stocks
        * real-time trade consumption
* Provide unit-test Coverage

Following are main components in our application:
* 1. Trae Publisher: This component is responsible for publishing trade data to the message queue (Kafka).
* 2. Trade Consumer: This component is responsible for consuming trade data from the message queue and processing it.
* 3. Web Server & snapshot consumer: This component is responsible for serving the web interface and providing API endpoints for interacting with the application.

Data Registries (mocks db/ in memory db):
* 1. Stock Registry: This component is responsible for storing stock data and providing access to it.
* 2. Trade Registry: This component is responsible for storing trade data and providing access to it.
* 3. Trade SnapShot Registry: This component is responsible for storing trade snapshots and providing access to it.

# Flow:

Static Stock Data & Calculations
        |
    1   |---> Trade Publisher Service (ZMQ PUB) ---> Message Socket (ZMQ) ---> Trade Consumer (ZMQ SUB) ---> Trade Registry
        |
    2   |---> Trade Consumer Service (ZMQ PUB) ---> Generate Trade SnapShot ---> Trade Snapshot Registry ---> Message Socket (ZMQ PUB)
        |
   3.1  |---> Metric Service Main Thread (Consume SnapShots) ---> Trade Snapshot Registry
        |
   3.2  |---> Metric Service background thread ---> Web Server Thread (Flask) ---> Stock Registry/ Trade Snapshot Registry ---> Web Server (Flask) ---> Web API (HTML/JS/CSS)


# API Endpoints:
1. GET /stocks: Returns a list of all stocks in the system.
2. GET /stocks/<stockId>: Returns details of a specific stock by its stockId.
3. GET /calculate/peRatio/<stockId>/<stock_price>: Returns the P/E ratio for a specific stock by its stockId and price.
4. GET /calculate/dividendYield/<stockId>/<stock_price>: Returns the dividend yield for a specific stock by its stockId and price.
5. GET /gbce-all-share-index: Returns the GBCE All Share Index using the geometric mean of prices for all stocks. 
6. GET /trade/volume-weighted-stock-price: Returns the volume-weighted stock price based on trades in the past 15 trades.



Stock Data is static and is stored in the `StockRegistry`. The stock data is used to calculate the dividend yield and P/E ratio.
The stock data is also used to calculate the GBCE All Share Index.
Trade Data is stored in the `TradeRegistry`.
Trade data are snapped into the `TradeSnapShotRegistry`.
The trade snapshot data is used to calculate the volume-weighted stock price.

**You can test if the real time trades are impacting the stock price by using the following endpoints:**
**GET /trade/volume-weighted-stock-price/<stockId>**
**The Price would keep changing based on the trades that are being consumed in real time.**

