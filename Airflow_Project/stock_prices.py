import pandas as pd
import yfinance as yf
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import pyodbc

def create_connection():
    conn_str = (
        r"DRIVER={SQL Server};"
        r"SERVER=KHR;"
        r"DATABASE=BikeStore;"
        r"Trusted_Connection=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        print("✅ Connected to SQL Server successfully!")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to SQL Server: {e}")
        return None

def create_table_if_not_exists(table_name):
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='stock_prices' and xtype='U')
    CREATE TABLE {table_name} (
        trade_date DATETIME,
        close_price FLOAT,
        high_price FLOAT,
        low_price FLOAT,
        open_price FLOAT,
        volume BIGINT,
        symbol VARCHAR(10),
        close_change FLOAT,
        close_pct_change FLOAT
    )
    """
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("✅ Table ensured: stock_prices")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()


def insert_data_to_db(table_name, values):
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    insert_query = f"""
    INSERT INTO {table_name} (
        trade_date, close_price, high_price, low_price, open_price,
        volume, symbol, close_change, close_pct_change
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    try:
        cursor.executemany(insert_query, values)
        conn.commit()
        print(f"✅ Inserted {len(values)} rows into {table_name}")
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()

def get_sp500_symbols():
    sp_500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    tables = pd.read_html(sp_500_url)
    sp_500 = tables[0]
    return sp_500['Symbol'].tolist()

def get_finance_data (symbols,start_date,end_date, interval):
    result ={}
    for symbol in symbols:
        data = yf.download(tickers = symbol,start=start_date,end = end_date, interval=interval )
        if not data.empty:
            result[symbol] = data
    return result 
    
def transform_data(data, symbol):
    data.columns = [col[0] for col in data.columns]
    data = data.reset_index()

    # data = data[data["Close"] != 0]
    data["symbol"] = symbol
    data['close_change'] = data['Close'].diff().fillna(0)
    data['close_pct_change'] = data['Close'].pct_change().fillna(0) * 100
    return data[['Date', 'Close', 'High', 'Low', 'Open', 'Volume', 'symbol', 'close_change', 'close_pct_change']]

def ingest_yfinance_data(symbol_data, table_name, interval):
    values = []
    for symbol in symbol_data:
        try:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            data_dict = get_finance_data([symbol], start_date, end_date, interval)
            if symbol in data_dict:
                data = transform_data(data_dict[symbol], symbol)
                if not data.empty:
                    values.extend([tuple(x) for x in data.to_numpy()])
        except Exception as e:
            print(e)
            # error_logger.error(f"{symbol} transformation error: {str(e)}")
    if values:
        print(values)
        # insert_data_to_db(table_name, values)


def main(interval):
    table_name = "stock_prices"
    symbols = get_sp500_symbols()
    print(len(symbols))
    # create_table_if_not_exists(table_name)
    ingest_yfinance_data(symbols ,table_name, interval)


default_args = {
    'owner': 'zain',
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id='stock_prices_dag',
    default_args=default_args,
    description='Getting stock prices from yfinance',
    schedule_interval='0 22 * * *',
    start_date=datetime(2023, 4, 26),
    catchup=False,
    tags=['stock_daily'],
) as dag:

    # Define the task using the Basherator
    stock_prices_task = PythonOperator(
    task_id='get_stock_prices',
    python_callable=main,
    op_args=['1d'],

    )
    stock_prices_task