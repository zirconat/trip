import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# subheader name
st.subheader("📊 Interactive Dashboard")

#About Dashboard
with st.expander("**About Dashboard**"):
    st.info("Display key statistics of all engagements based on FIEP.")
    st.markdown("How to use")
    st.warning("Select your desired filter in the dropdown box. The charts will automatically update based on your selected filters. To view the datasets, click on 'Data preview'")

# Load data - read .xlsx into Pandas dataframe
df = pd.read_excel("Trip and visit WY24_25 Database.xlsx")
# df['Year'] = df['Year'].astype('int') # enable when using slider for year below

# Hide filter options
with st.expander("Select filter"):
    # Del Lead selection - Create dropdown menu for Del Lead selection
    del_lead_list = df["Del Lead"].unique()
    del_lead_selection = st.multiselect('Select Del Lead', del_lead_list, ['Director', 'BB', 'Chief', 'HOD', 'Working'])

    # Year selection - Create dropdown menu for Year selection
    year_list = df["Year"].unique()
    year_selection = st.multiselect('Select Year', year_list, [2024, 2025])

    # Year selection - Create slider for year range selection
    #year_list = df['Year'].unique()
    #year_selection = st.slider('Select your duration',2021,2030, (2022, 2024))
    #year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

    # Subset data - Filter dataframe based on selection
    df_selection = df[df['Del Lead'].isin(del_lead_selection) & df['Year'].isin(year_selection)]
    df_selection.drop(columns=["Month", "Year"], axis = 1, inplace= True)

# Hide dataframe in dropdown menu
with st.expander("Data preview"):
    st.info("You may download a copy of the table in .csv format. Click the download icon at the top right of the table.")
    st.warning("To edit any data, double-click on the desired cell. Please ensure no columns are empty.")
    #Editable dataframe - Allow users to make live edits to the dataframe
    df_editor = st.data_editor(
        df_selection, 
        use_container_width=True,
        column_config={
            "Confluence Link": st.column_config.LinkColumn("Confluence Link"), # enable clickable links in dataframe
            "Departure Date": st.column_config.DateColumn( # change date format
                "Departure Date",
                format= "DD MMM YYYY"
            ),
            "Return Date": st.column_config.DateColumn( # change date format
                "Return Date",
                format= "DD MMM YYYY"
            ),
        },
    hide_index= True
)
    
# Data prep for charting
df_cleaned = pd.merge(df_editor, df)

df_cleaned