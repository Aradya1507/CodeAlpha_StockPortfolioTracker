import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data
def fetch_stock_data(symbol):
    stock_data = yf.download(symbol)
    return stock_data

# Initialize portfolio
portfolio = pd.DataFrame(columns=["Symbol", "Shares", "Average Price"])

st.title("Stock Portfolio Tracker")

# Add stock
stock_symbol = st.text_input("Enter Stock Symbol:")
shares = st.number_input("Enter Number of Shares:", min_value=1)

if st.button("Add Stock"):
    if stock_symbol and shares > 0:
        stock_data = fetch_stock_data(stock_symbol)
        if not stock_data.empty:
            avg_price = stock_data['Close'].iloc[-1]
            portfolio = portfolio.append({"Symbol": stock_symbol, "Shares": shares, "Average Price": avg_price}, ignore_index=True)
            st.success(f"Added {shares} shares of {stock_symbol} at ${avg_price:.2f} each.")
        else:
            st.error("Invalid stock symbol.")

# Remove stock
remove_symbol = st.text_input("Enter Stock Symbol to Remove:")
if st.button("Remove Stock"):
    if remove_symbol in portfolio['Symbol'].values:
        portfolio = portfolio[portfolio['Symbol'] != remove_symbol]
        st.success(f"Removed {remove_symbol} from portfolio.")
    else:
        st.error("Stock not found in portfolio.")

# Display portfolio
if not portfolio.empty:
    st.write("Current Portfolio:")
    st.dataframe(portfolio)

    # Calculate total investment value
    total_value = sum(portfolio['Shares'] * portfolio['Average Price'])
    st.write(f"Total Investment Value: ${total_value:.2f}")

    # Plot stock trends
    for symbol in portfolio['Symbol']:
        data = fetch_stock_data(symbol)
        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label=symbol)
        plt.title(f"{symbol} Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        st.pyplot(plt)
else:
    st.write("Your portfolio is empty.")
    # Option to clear the portfolio
if st.button("Clear Portfolio"):
    st.session_state.portfolio = pd.DataFrame(columns=["Symbol", "Shares", "Average Price"])
    st.success("Portfolio cleared.")