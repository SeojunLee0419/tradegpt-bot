import yfinance as yf
import pandas_ta as ta
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    try:
        # Set the date range (Last 180 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)

        # Download stock data from Yahoo Finance
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)

        # Check if data is empty
        if df.empty:
            print(f"[Warning] No data available for {ticker}.")
            return

        # Calculate RSI (Relative Strength Index)
        df['RSI'] = ta.rsi(df['Close'], length=14)

        # Remove NaN values (RSI is NaN for the first 14 days)
        df.dropna(subset=['RSI'], inplace=True)

        # Format date and select relevant columns
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        df = df[['Date', 'Close', 'RSI', 'Volume']]

        # Round numerical values
        df['Close'] = df['Close'].round(2)
        df['RSI'] = df['RSI'].round(2)

        # Add Buy/Sell signals based on RSI levels
        # df['Signal'] = df['RSI'].apply(analyze_rsi)

        # Save data as a CSV file (named after the stock ticker)
        # filename = f"data/{ticker}_data.csv"
        # df.to_csv(filename, index=True)

        # Output text file to save print statements
        output_filename = f"data/{ticker}_Summary.txt"
        with open(output_filename, 'w') as file:
            # Write to the file and also print to the console
            output_text = f"{ticker} Last 30 Trading Days:\n"
            output_text += df.tail(30).to_string(index=False)

            # Write the output to the file
            file.write(output_text)

            # Also print to the console
            print(output_text)

        print(f"\n{ticker} Last 30 Trading Days:")
        print(df.tail(30))

    except Exception as e:
        print(f"[Error] An issue occurred while processing {ticker} data: {e}")

def analyze_rsi(rsi):
    if rsi < 30:
        return "Buy"
    elif rsi > 70:
        return "Sell"
    return "--"

# Example usage: Fetch data for multiple stocks
tickers = ["AAPL", "TSLA", "GOOG", "NVDA", "AXON", "CRWD", "META"]
for ticker in tickers:
    fetch_stock_data(ticker)
