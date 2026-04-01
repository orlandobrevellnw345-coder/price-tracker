



import pandas as pd
from datetime import datetime
import os

DATA_FILE = "data/prices.csv"

def init_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["url", "title", "price", "target_price", "timestamp"])
        df.to_csv(DATA_FILE, index=False)

def add_product(url, target_price=0):
    init_data()
    title = get_product_title(url)  # from scraper.py
    price = get_product_price(url)
    
    if price is None:
        return False, "Could not fetch price"
    
    new_row = {
        "url": url,
        "title": title,
        "price": price,
        "target_price": target_price,
        "timestamp": datetime.now().isoformat()
    }
    
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return True, f"Added: {title} at ${price}"

def get_price_history():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

def check_price_drops():
    df = get_price_history()
    if df.empty:
        return []
    # Group by URL and check latest vs target
    alerts = []
    for url, group in df.groupby("url"):
        latest = group.iloc[-1]
        if latest["target_price"] > 0 and latest["price"] <= latest["target_price"]:
            alerts.append(latest)
    return alerts
