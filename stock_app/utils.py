from .models import Stock, Price, UserStock
import yfinance as yf
import pandas as pd

def get_stock_info(symbol):
    try:
        stock = Stock.objects.get(symbol=symbol)
        return stock.company_name, stock.sector, stock.industry
    except Stock.DoesNotExist:
        return 'Unknown', 'Unknown', 'Unknown'


def fetch_new_data(symbol, period, lstart_date, end_date):
    """Fetch updated stock data from Yahoo Finance."""
    ticker_data = yf.Ticker(symbol)
    ticker_df = ticker_data.history(period=period, start=lstart_date, end=end_date)
    return ticker_df

def download_stock_data(symbol, period, start_date, end_date, user=None):
    try:
        # Check if data exists
        existing_prices = Price.objects.filter(stock__symbol=symbol).order_by('-date')

        if existing_prices.exists():
            last_date = existing_prices.first().date
            
            # If the last date is recent enough, skip downloading
            if last_date >= pd.to_datetime(end_date).date():
                return f'Price data for {symbol} is up to date.'
            else:
                # Fetch updated data using the mini function
                ticker_df = fetch_new_data(symbol, period, last_date, end_date)

                if len(ticker_df) == 0:
                    return f'No updated data found for {symbol} from {last_date} to {end_date}.'
                
                # Process and save updated data
                stock = Stock.objects.get(symbol=symbol)
                price_instances = []
                required_fields = ['Open', 'High', 'Low', 'Close', 'Volume']
                for index, row in ticker_df.iterrows():
                    if not all(field in row for field in required_fields):
                        continue
                    price_instance = Price(
                        stock=stock,
                        date=index,
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        volume=row['Volume'],
                    )
                    price_instances.append(price_instance)
                Price.objects.bulk_create(price_instances, 100)
                return f'Updated data fetched successfully for {symbol}.'
        else:
            # Fetch new data from Yahoo Finance
            ticker_df = fetch_new_data(symbol, period, start_date, end_date)
            if len(ticker_df) == 0:
                return f'No data found for {symbol} from {start_date} to {end_date}.'

            # Create or update stock information
            stock, created = Stock.objects.get_or_create(symbol=symbol)
            if created:
                company_name, sector, industry = get_stock_info(symbol)
                stock.company_name, stock.sector, stock.industry = company_name, sector, industry
                stock.save()
                if user:
                    UserStock.objects.get_or_create(user=user, stock=stock)

            # Process and save new data
            price_instances = []
            required_fields = ['Open', 'High', 'Low', 'Close', 'Volume']
            for index, row in ticker_df.iterrows():
                if not all(field in row for field in required_fields):
                    continue
                price_instance = Price(
                    stock=stock,
                    date=index,
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                    volume=row['Volume'],
                )
                price_instances.append(price_instance)
            Price.objects.bulk_create(price_instances, 100)
            return f'New data fetched successfully for {symbol}.'
    except Exception as e:
        return f'An error occurred while fetching data for {symbol}: {e}'