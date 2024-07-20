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

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is None:
    st.info("Please upload a file through the sidebar to begin", icon="⚠️")
    st.stop()

df = load_data(uploaded_file)

with st.expander("Data preview"):
    st.dataframe(df)

with st.sidebar:
    st.header("Filter:")
    country = st.sidebar.multiselect(
        "Select the country:",
        options=df["Country"].unique(),
        default=df["Country"].unique()
    )
    service = st.sidebar.multiselect(
        "Select the service:",
        options=df["Service"].unique(),
        default=df["Service"].unique()
    )
    status = st.sidebar.multiselect(
        "Select the status:",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )
    level = st.sidebar.multiselect(
        "Select the level:",
        options=df["Level"].unique(),
        default=df["Level"].unique()
    )