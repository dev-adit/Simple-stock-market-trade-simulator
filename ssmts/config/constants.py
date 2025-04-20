import enum


class StockType(enum.Enum):
    COMMON = "common"
    PREFERRED = "preferred"

DEFAULT_STOCKS = [
    {'stockId': 'STK1', 'symbol': 'TEA', 'stockType': StockType.COMMON.value, 'lastDivident': 0.0, 'fixedDivident': 0.0, 'parValue': 100.0},
    {'stockId': 'STK2', 'symbol': 'POP', 'stockType': StockType.COMMON.value, 'lastDivident': 8.0, 'fixedDivident': 0.0, 'parValue': 100.0},
    {'stockId': 'STK3', 'symbol': 'ALE', 'stockType': StockType.COMMON.value, 'lastDivident': 23.0, 'fixedDivident': 0.0, 'parValue': 60.0},
    {'stockId': 'STK4', 'symbol': 'GIN', 'stockType': StockType.PREFERRED.value, 'lastDivident': 8.0, 'fixedDivident': 2.0, 'parValue': 100.0},
    {'stockId': 'STK5', 'symbol': 'JOE', 'stockType': StockType.COMMON.value, 'lastDivident': 13.0, 'fixedDivident': 0.0, 'parValue': 250.0},
]