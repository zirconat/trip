import streamlit as st
import pandas as pd
#import random
#import plotly.express as px
from IPython.display import HTML

st.set_page_config(
    page_title=" Trips & Visits",
    page_icon=":airplane:",
    layout="wide"
)

st.title(" ✈️ Trips & Visits Overview")
st.write(
    "An overview of trips and visits for WY2024/2025"
)

# Page setup
dashboard_page = st.Page(
    page = "views/dashboard.py",
    title="Dashboard",
    icon = "📊",
    default=True,
)

tennis_page = st.Page(
    page = "views/tennis_court.py",
    title="Tennis Court",
    icon = "🎾",
)

pg = st.navigation(pages=[dashboard_page, tennis_page])
pg.run()
#pg.run()
#@st.cache_data
#def load_data(file):
#    data = pd.read_excel(file)
#    return data

#uploaded_file = st.file_uploader("Choose a file to begin")

#if uploaded_file is None:
#    st.info("Please upload a file", icon="⚠️")
#    st.stop()

#df = load_data(uploaded_file)

# assign excel file
#df = pd.read_excel("./Trip and visit WY24_25 Database.xlsx")

# multi tab pages
#tab1, tab2, tab3 = st.tabs(["Dashboard", "Tennis Court", "Testing"])

#with tab1:
#    df_clean = df
#    df_clean.drop(columns=['Month', 'Year'], axis=1, inplace=True) #remove month and year reference columns
#    df_clean.dropna(inplace=True) # remove blanks
    
    # hide table in preview
#    with st.expander("Data preview"):
        # edit table config
#        st.data_editor(
#            df_clean,
#            column_config={
#                "Confluence Link": st.column_config.LinkColumn("Confluence Link"), # enable clickable links in dataframe
#                "Departure Date": st.column_config.DateColumn( # change date format
#                    "Departure Date",
#                    format= "DD MMM YYYY"
#                    ),
#                "Return Date": st.column_config.DateColumn( # change date format
#                    "Return Date",
#                    format= "DD MMM YYYY"
#                    ),
#        },
#        hide_index=True, #hide df index
#        disabled=True # disable user editing
#    )

#with tab2:
#    df_clean.groupby(['Status']) # doesn't work correctly now. displays the cleaned df instead but with index visible
#    df_clean

#with st.sidebar:
#    st.header("Filter:")
#    country = st.sidebar.multiselect(
#        "Select the country:",
#        options=df["Country"].unique(),
#       default=df["Country"].unique()
#    )
#    service = st.sidebar.multiselect(
#        "Select the service:",
#        options=df["Service"].unique(),
#        default=df["Service"].unique()
#    )
#    status = st.sidebar.multiselect(
#        "Select the status:",
#        options=df["Status"].unique(),
#        default=df["Status"].unique()
#    )
#    level = st.sidebar.multiselect(
#        "Select the level:",
#        options=df["Level"].unique(),
#        default=df["Level"].unique()
#    )

#df_selection = df.query(
#    "Country == @country & Service == @service & Status == @status & Level == @level"
#)