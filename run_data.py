"""
Module for FX market data processing and order book maintenance.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict

from orderbook import OrderBook

def read_market_data(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file with market data and return a DataFrame.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with parsed market data
    """
    df = pd.read_csv(file_path)
    
    # Convert time column to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # Sort by time
    df = df.sort_values('time')
    
    return df


def update_order_book(order_book: OrderBook, row: pd.Series) -> None:
    """
    Update the order book with a new row of market data.
    
    Args:
        order_book: OrderBook instance to update
        row: DataFrame row with market data
    """
    # Extract bid prices and quantities
    bid_prices = [
        float(row['BI_price_1']), float(row['BI_price_2']), float(row['BI_price_3']),
        float(row['BI_price_4']), float(row['BI_price_5'])
    ]
    bid_quantities = [
        float(row['BI_quantity_1']), float(row['BI_quantity_2']), float(row['BI_quantity_3']),
        float(row['BI_quantity_4']), float(row['BI_quantity_5'])
    ]
    
    # Extract offer prices and quantities
    offer_prices = [
        float(row['OF_price_1']), float(row['OF_price_2']), float(row['OF_price_3']),
        float(row['OF_price_4']), float(row['OF_price_5'])
    ]
    offer_quantities = [
        float(row['OF_quantity_1']), float(row['OF_quantity_2']), float(row['OF_quantity_3']),
        float(row['OF_quantity_4']), float(row['OF_quantity_5'])
    ]
    
    # Update the order book
    order_book.update_bids(bid_prices, bid_quantities)
    order_book.update_offers(offer_prices, offer_quantities)
    # Convert pandas Timestamp to Python datetime
    time_value = row['time']
    if hasattr(time_value, 'to_pydatetime'):
        order_book.last_update_time = time_value.to_pydatetime()  # type: ignore
    else:
        order_book.last_update_time = time_value  # type: ignore


def process_file(file_path: str, order_books: Dict[str, OrderBook]) -> None:
    """
    Process a market data file and update the order books.
    
    Args:
        file_path: Path to the CSV file
        order_books: Dictionary of order books by security
    """
    print(f"Processing file: {file_path}")
    
    # Read market data
    df = read_market_data(file_path)
    
    # Process each row
    for idx, row in df.iterrows():
        security = str(row['security'])
        
        # Create order book if it doesn't exist
        if security not in order_books:
            order_books[security] = OrderBook(security)
        
        # Update order book
        update_order_book(order_books[security], row)

        # call the strategy
    
    print(f"  - Processed {len(df)} rows")
    print(f"  - Securities found: {list(order_books.keys())}")


def run(data_dir: str = "data") -> Dict[str, OrderBook]:
    """
    Main function that processes all data files and updates the order books.
    
    Args:
        data_dir: Directory containing CSV data files
        
    Returns:
        Dictionary with updated order books by security
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Directory {data_dir} does not exist")
    
    # Dictionary to maintain order books by security
    order_books: Dict[str, OrderBook] = {}
    
    # Find CSV files in the directory
    csv_files = sorted(data_path.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return order_books
    
    print(f"Found {len(csv_files)} CSV files")
    print("-" * 60)
    
    # Process each file
    for csv_file in csv_files:
        try:
            process_file(str(csv_file), order_books)
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
    
    print("-" * 60)
    print(f"\nProcessing completed.")
    print(f"Total securities processed: {len(order_books)}")
    
    # Show order books summary
    print("\nOrder Books Summary:")
    for security, ob in order_books.items():
        print(f"  {ob}")
    
    return order_books


if __name__ == "__main__":
    # Execute processing
    order_books = run()
    
    # Example usage: show statistics
    if order_books:
        print("\n" + "=" * 60)
        print("Final Statistics:")
        print("=" * 60)
        
        for security, ob in order_books.items():
            best_bid = ob.get_best_bid()
            best_offer = ob.get_best_offer()
            spread = ob.get_spread()
            
            print(f"\nSecurity: {security}")
            print(f"  Best Bid: {best_bid}")
            print(f"  Best Offer: {best_offer}")
            print(f"  Spread: {spread}")
            print(f"  Bid Levels: {len(ob.bids)}")
            print(f"  Offer Levels: {len(ob.offers)}")
            print(f"  Last Update: {ob.last_update_time}")

