import streamlit as st
import pandas as pd
# from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Daily NSE Scanner", layout="wide")

st.title("📊 Daily NSE Pattern Scanner")
st.caption("Auto-updated after GitHub Actions run")

# 🔁 auto refresh every 2 minutes
# st_autorefresh(interval=120_000, key="refresh")

# 🔥 READ DIRECTLY FROM GITHUB
CSV_URL = "https://raw.githubusercontent.com/bhavya-1204/pattern-stock-fetching/master/latest_output.csv"

try:
    df = pd.read_csv(CSV_URL)

    if not df.empty:
        st.success(f"Patterns found: {len(df)}")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Scanner ran, but no patterns found.")

except Exception as e:
    st.error("Unable to fetch latest output yet.")
