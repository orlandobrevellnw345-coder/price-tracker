





























import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from scraper import get_product_price, get_product_title
from tracker import add_product, get_price_history, check_price_drops

st.set_page_config(page_title="Simple Price Tracker", layout="wide")
st.title("🛒 Simple Price Tracker")

tab1, tab2, tab3 = st.tabs(["Add Product", "Dashboard", "History"])

with tab1:
    url = st.text_input("Product URL (e.g., Amazon link)")
    target = st.number_input("Target price (alert when below)", min_value=0.0, value=0.0)
    
    if st.button("Track this product"):
        if url:
            success, msg = add_product(url, target)
            st.success(msg) if success else st.error(msg)

with tab2:
    st.subheader("Price Alerts")
    alerts = check_price_drops()
    if alerts:
        for alert in alerts:
            st.warning(f"Price drop! {alert['title']} is now ${alert['price']} (target: ${alert['target_price']})")
    else:
        st.info("No alerts yet.")

    st.subheader("Current Prices")
    df = get_price_history()
    if not df.empty:
        latest = df.groupby("url").last().reset_index()
        st.dataframe(latest[["title", "price", "target_price"]])

with tab3:
    df = get_price_history()
    if not df.empty:
        st.dataframe(df)
        
        # Simple chart for a selected product
        urls = df["url"].unique()
        selected_url = st.selectbox("Select product for chart", urls)
        product_df = df[df["url"] == selected_url].copy()
        product_df["timestamp"] = pd.to_datetime(product_df["timestamp"])
        
        fig = px.line(product_df, x="timestamp", y="price", title="Price History")
        st.plotly_chart(fig)
    else:
        st.info("No data yet. Add some products!")
