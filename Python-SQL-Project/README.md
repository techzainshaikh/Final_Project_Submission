# 🐍 CoinGecko API to SQL Server Data Pipeline 📊

This project builds an end-to-end data pipeline that extracts cryptocurrency data from the **CoinGecko API**, processes it using **Python**, stores it into a **Microsoft SQL Server** database, and makes it available for **reporting and visualization**.

<br/>

## 📌 Project Architecture

![Pipeline Architecture](./Copy%20of%20External%20Stage.jpg)

### 🔁 Flow Overview

1. 🦎 **CoinGecko** – Source of real-time cryptocurrency market data.
2. 🔗 **API Integration** – Retrieves structured JSON data from CoinGecko's RESTful API.
3. 🐍 **Python ETL Script** – Extracts, transforms, and loads (ETL) data using:
   - `requests` for API calls  
   - `pandas` for data processing  
   - `pyodbc` or `sqlalchemy` for database interaction
4. 🗃️ **Microsoft SQL Server** – Stores historical data for analytics and reporting.

---

## 🚀 Features

- ✅ Automated data ingestion from CoinGecko API  
- ✅ Clean and transform data using Python  
- ✅ Store and update data in SQL Server  
- ✅ Ready for reporting and visualization  
- ✅ Scalable and modular design

---

## 🧰 Technologies Used

| Technology        | Purpose                            |
|-------------------|------------------------------------|
| 🦎 CoinGecko API  | Real-time crypto data              |
| 🐍 Python         | Data extraction and transformation |
| 🗃️ SQL Server     | Data storage                       |

## 📊 Sample Visualization

Once the data is in SQL Server, you can connect tools like Power BI or Excel to generate insightful dashboards like:

- Market Capitalization Trends  
- Top Gainers & Losers  
- Price Volatility Heatmap  
- Coin Popularity Rankings  

## 🤝 Contributing

Contributions are welcome!  
Feel free to fork this repo and submit a pull request with improvements, bug fixes, or new features.

## 🙏 Acknowledgements

- [CoinGecko API](https://www.coingecko.com/en/api)
- [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/)
- [Python Community](https://www.python.org/)
