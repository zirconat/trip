import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Trips & Visits",
    page_icon=":airplane:",
    layout="wide"
)

st.title(" ✈️ Trips & Visits")
st.write(
    "Displays trips and visits for WY24/25"
)

@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    return data

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info("Please upload a file to begin", icon="⚠️")
    st.stop()

df = load_data(uploaded_file)
st.dataframe(df)