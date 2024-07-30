import streamlit as st
import pandas as pd
#from streamlit_option_menu import option_menu


st.set_page_config(
    page_title=" Trips & Visits",
    page_icon=":airplane:",
    layout="wide"
)

st.title(" ✈️ Trips & Visits Overview")
st.write("An overview of trips and visits for WY2024/2025")

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

# remove streamlit header and footer
hide_st_style = """
                <style>
                header {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# horizontal navigation bar
#selected = option_menu(
#    menu_title= None,
#    options = ["📊 Dashboard", "🎾 Tennis Court", "🔍 Compare"],
#    icons= ["chart", "tennis"],
#    default_index=0,
#    orientation= "horizontal"
#)

#if selected == "📊 Dashboard":
    # subheader name
    #st.subheader("📊 Interactive Dashboard")

    #About Dashboard -- Do we need this?
    #with st.expander("**About Dashboard**"):
    #    st.info("Display key statistics of all engagements based on FIEP.")
    #    st.markdown("How to use")
    #    st.warning("Select your desired filter in the dropdown box. The charts will automatically update based on your selected filters. To view the datasets, click on 'Data preview'")
