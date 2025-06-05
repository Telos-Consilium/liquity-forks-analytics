import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Liquity Forks Peg Monitor", layout="wide")

TOKENS = {"feUSD": "felix-feusd", "USDQ": "quill-usdq", "Orki": "orki-usdk", "USDaf": "asymmetry-usdaf"}


def fetch_prices():
    ids = ",".join(TOKENS.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()


def calculate_peg_distance(price):
    return ((price - 1) / 1) * 100


st.title("🎯 Stablecoin Peg Monitor")

data = fetch_prices()

df_data = []
for symbol, coin_id in TOKENS.items():
    if coin_id in data:
        price = data[coin_id]["usd"]
        peg_distance = calculate_peg_distance(price)
        df_data.append(
            {
                "Token": symbol,
                "Price": f"${price:.4f}",
                "Peg Distance": f"{peg_distance:+.2f}%",
                "Status": "🟢" if abs(peg_distance) < 1 else "🟡" if abs(peg_distance) < 5 else "🔴",
            }
        )

df = pd.DataFrame(df_data)

col1, col2 = st.columns([2, 1])

with col1:
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.metric("Tokens Tracked", len(df))
    stable_count = len([x for x in df_data if abs(float(x["Peg Distance"].replace("%", "").replace("+", ""))) < 1])
    st.metric("Within 1% Peg", f"{stable_count}/{len(df)}")

st.button("🔄 Refresh", key="refresh")
