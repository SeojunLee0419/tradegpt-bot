import os
import yfinance as yf
from openai import OpenAI
from dotenv import load_dotenv

# Initialize OpenAI client
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def fetch_tesla_data(start_date, end_date):
    """
    Fetch Tesla stock data from Yahoo Finance.
    """
    print(f"Fetching Tesla stock data from {start_date} to {end_date}...")
    data = yf.download("TSLA", start=start_date, end=end_date)
    return data

def generate_summary(data):
    """
    Generate a summary of Tesla stock data statistics.
    """
    summary = {
        "Highest Price": round(data['High'].max(), 2),
        "Lowest Price": round(data['Low'].min(), 2),
        "Average Close Price": round(data['Close'].mean(), 2),
        "Average Volume": round(data['Volume'].mean(), 2),
    }

    summary_text = (
        f"Tesla Stock Data Summary:\n"
        f"- Highest Price: ${summary['Highest Price']}\n"
        f"- Lowest Price: ${summary['Lowest Price']}\n"
        f"- Average Close Price: ${summary['Average Close Price']}\n"
        f"- Average Volume: {summary['Average Volume']} shares"
    )
    return summary_text

def analyze_with_openai(summary_text):
    """
    Use OpenAI's Chat Completion to analyze Tesla stock data.
    """
    print("Analyzing stock data with OpenAI...")
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a stock market analyst."},
            {"role": "user", "content": f"Analyze this Tesla stock data:\n\n{summary_text}\n\n"
                                         "Provide insights and potential trends based on this information."}
        ],
        model="gpt-4",
    )
    print(f"Got it! {response}")
    print(f"result: {response.choices[0].message.content.strip()}")
    # return response["choices"][0]["message"]["content"].strip()

def main():
    # Define the date range for the analysis
    start_date = "2025-01-01"
    end_date = "2025-01-15"

    # Fetch and summarize Tesla stock data
    data = fetch_tesla_data(start_date, end_date)
    summary_text = generate_summary(data)

    # Display the stock data summary
    print("\n" + summary_text)

    # Analyze stock data with OpenAI
    analysis = analyze_with_openai(summary_text)
    print("\nOpenAI Analysis:")
    print(analysis)

if __name__ == "__main__":
    main()
