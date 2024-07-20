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

#@st.cache_data
#def load_data(path: str):
  #  data = pd.read_excel(path)
   # return data

#df = load_data("./Trip and visit WY24_25 Database.xlsx")
#st.dataframe(df)