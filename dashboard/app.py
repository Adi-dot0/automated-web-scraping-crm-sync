import os
import sqlite3

import pandas as pd
import streamlit as st

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE, "scraping.db")

st.set_page_config(page_title="Scraping & CRM Sync Monitor", layout="wide")
st.title("Web Scraping & CRM Synchronization - Monitoring Dashboard")

if not os.path.exists(DB_PATH):
    st.warning("No data yet. Run `python main.py` first to scrape and store records.")
    st.stop()

conn = sqlite3.connect(DB_PATH)
records = pd.read_sql("SELECT * FROM scraped_records", conn)
syncs = pd.read_sql("SELECT * FROM sync_history ORDER BY sync_id DESC", conn)
dupes = pd.read_sql("SELECT * FROM duplicate_log ORDER BY id DESC", conn)
conn.close()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total records in DB", len(records))
col2.metric("Sync runs", len(syncs))
col3.metric("Last sync status", syncs.iloc[0]["sync_status"] if len(syncs) else "-")
col4.metric("Duplicates logged", len(dupes))

st.subheader("Records by rating")
if len(records):
    st.bar_chart(records["rating"].value_counts().sort_index())

st.subheader("Price summary")
if len(records):
    st.write(records["price"].describe())

st.subheader("Scraped records")
st.dataframe(records, use_container_width=True)

st.subheader("Sync history")
st.dataframe(syncs, use_container_width=True)
