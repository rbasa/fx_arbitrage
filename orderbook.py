"""
Module with the OrderBook class to maintain the order book state.
"""

from typing import List, Tuple, Optional
from datetime import datetime
from collections import OrderedDict


class OrderBook:
    """
    Class to maintain the order book state.
    """
    
    def __init__(self, security: str):
        """
        Initialize an order book for a given security.
        
        Args:
            security: Security identifier
        """
        self.security = security
        # Bid side: price -> quantity (ordered from highest to lowest price)
        self.bids: OrderedDict[float, float] = OrderedDict()
        # Offer side: price -> quantity (ordered from lowest to highest price)
        self.offers: OrderedDict[float, float] = OrderedDict()
        self.last_update_time: Optional[datetime] = None
    
    def update_bids(self, prices: List[float], quantities: List[float]):
        """
        Update the bid side of the order book.
        
        Args:
            prices: List of bid prices (up to 5 levels)
            quantities: List of bid quantities (up to 5 levels)
        """
        # If all prices are 0, there are no changes in the data
        if all(p == 0.0 for p in prices):
            return
        
        # Update only levels that have price > 0 and quantity > 0
        for price, qty in zip(prices, quantities):
            if price > 0.0 and qty > 0.0:
                self.bids[price] = qty
            elif price > 0.0 and qty == 0.0:
                # If price exists but quantity is 0, remove that specific level
                if price in self.bids:
                    del self.bids[price]
        
        # Reorder bids from highest to lowest price
        self.bids = OrderedDict(sorted(self.bids.items(), reverse=True))
    
    def update_offers(self, prices: List[float], quantities: List[float]):
        """
        Update the offer side of the order book.
        
        Args:
            prices: List of offer prices (up to 5 levels)
            quantities: List of offer quantities (up to 5 levels)
        """
        # If all prices are 0, there are no changes in the data
        if all(p == 0.0 for p in prices):
            return
        
        # Update only levels that have price > 0 and quantity > 0
        for price, qty in zip(prices, quantities):
            if price > 0.0 and qty > 0.0:
                self.offers[price] = qty
            elif price > 0.0 and qty == 0.0:
                # If price exists but quantity is 0, remove that specific level
                if price in self.offers:
                    del self.offers[price]
        
        # Reorder offers from lowest to highest price
        self.offers = OrderedDict(sorted(self.offers.items()))
    
    def get_best_bid(self) -> Optional[Tuple[float, float]]:
        """
        Return the best bid (price, quantity).
        
        Returns:
            Tuple (price, quantity) of the best bid or None if there are no bids
        """
        if not self.bids:
            return None
        price = next(iter(self.bids))
        return (price, self.bids[price])
    
    def get_best_offer(self) -> Optional[Tuple[float, float]]:
        """
        Return the best offer (price, quantity).
        
        Returns:
            Tuple (price, quantity) of the best offer or None if there are no offers
        """
        if not self.offers:
            return None
        price = next(iter(self.offers))
        return (price, self.offers[price])
    
    def get_spread(self) -> Optional[float]:
        """
        Calculate the spread (difference between best offer and best bid).
        
        Returns:
            Spread or None if both sides of the book are not available
        """
        best_bid = self.get_best_bid()
        best_offer = self.get_best_offer()
        
        if best_bid is None or best_offer is None:
            return None
        
        return best_offer[0] - best_bid[0]
    
    def __repr__(self) -> str:
        """Order book representation."""
        best_bid = self.get_best_bid()
        best_offer = self.get_best_offer()
        spread = self.get_spread()
        
        return (f"OrderBook(security={self.security}, "
                f"best_bid={best_bid}, best_offer={best_offer}, "
                f"spread={spread})")

