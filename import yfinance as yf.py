from ticker_list import ticker_list
import yfinance as yf
import smtplib
from email.mime.text import MIMEText

class FinancialDataAnalyzer:
    def __init__(self, ticker, email_config):
        self.ticker = ticker
        self.email_config = email_config

    def fetch_stock_data(self, start_date, end_date):
        stock = yf.Ticker(self.ticker)
        data = stock.history(start=start_date, end=end_date)
        return data

    def calculate_sma(self, data, window):
        data['SMA'] = data['Close'].rolling(window=window).mean()
        return data

    def calculate_operating_margin(self, data):
        data['Operating Margin'] = data['Close'].rolling(window=4).mean()
        return data

    def calculate_ev_ebitda_capex(self, data, annual_financial_statement):
        data['EV/EBITDA-Capex'] = annual_financial_statement['Enterprise Value'] / (
                annual_financial_statement['EBITDA'] - annual_financial_statement['Capital Expenditure'])
        return data

    def calculate_ytd_performance(self, data):
        data['YTD Performance'] = (data['Close'][-1] - data['Close'][0]) / data['Close'][0] * 100
        return data

    def calculate_revenue_growth(self, data):
        data['Revenue Growth'] = (data['Revenue'].iloc[-1] - data['Revenue'].iloc[0]) / data['Revenue'].iloc[0] * 100
        return data

    def calculate_net_income_growth(self, data):
        data['Net Income Growth'] = (data['Net Income'].iloc[-1] - data['Net Income'].iloc[0]) / data[
            'Net Income'].iloc[0] * 100
        return data

    def calculate_short_interest(self, data):
        data['Short Interest'] = data['Short Interest'] / data['Shares Outstanding'] * 100
        return data

    def send_email(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_config['sender']
        msg['To'] = self.email_config['recipient']

        smtp_server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
        smtp_server.starttls()
        smtp_server.login(self.email_config['username'], self.email_config['password'])
        smtp_server.send_message(msg)
        smtp_server.quit()

# Example usage
if __name__ == "__main__":
    ticker_list = ["GOOGL", "AMZN", "AAPL"]
    ticker = "AAPL"  # Example stock symbol
    start_date = "2023-01-01"  # Example start date
    end_date = "2023-06-01"  # Example end date
    window = 50  # Example window for SMA calculation

    email_config = {
        'sender': 'sender@example.com',
        'recipient': 'recipient@example.com',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'username': 'your_username',
        'password': 'your_password'
    }
    
    if __name__ == "__main__":
   
    start_date = "2023-01-01"
    end_date = "2023-06-01"

    email_config = {
        'sender': 'sender@example.com',
        'recipient': 'recipient@example.com',
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'username': 'your_username',
        'password': 'your_password'
    }

    analyzer = FinancialDataAnalyzer(ticker_list, email_config)

    for ticker in ticker_list:
        data = analyzer.fetch_stock_data(ticker, start_date, end_date)

        weight_ticker, last_close = analyzer.calculate_weight(ticker, data)
        operating_margin_ticker, avg_operating_margin = analyzer.calculate_operating_margin(ticker, data)
        ev_ebitda_capex_ticker, ev_ebitda_capex = analyzer.calculate_ev_ebitda_capex(ticker)
        ytd_performance_ticker, ytd_performance = analyzer.calculate_ytd_performance(ticker, data)
        revenue_growth_ticker, revenue_growth = analyzer.calculate_revenue_growth(ticker, data)
        net_income_growth_ticker, net_income_growth = analyzer.calculate_net_income_growth(ticker, data)
        short_interest_ticker, short_interest = analyzer.calculate_short_interest(ticker)

        # Format the output data as desired
        output_data = f"Stock: {ticker}\n"
        output_data += f"Weight: {weight_ticker} - {last_close}\n"
        output_data += f"Operating Margin: {operating_margin_ticker} - {avg_operating_margin}\n"
        output_data += f"EV / (EBITDA - Capex): {ev_ebitda_capex_ticker} - {ev_ebitda_capex}\n"
        output_data += f"YTD Performance: {ytd_performance_ticker} - {ytd_performance}%\n"
        output_data += f"Revenue Growth: {revenue_growth_ticker} - {revenue_growth}%\n"
        output_data += f"Net Income Growth: {net_income_growth_ticker} - {net_income_growth}%\n"
        output_data += f"Short Interest: {short_interest_ticker} - {short_interest}%\n\n"

        # Send the output data via email
        email_subject = f"Stock Analysis: {ticker}"
        analyzer.send_email(email_subject, output_data)
