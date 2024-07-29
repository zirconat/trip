import streamlit as st
import pandas as pd
#import plotly.express as px
import altair as alt
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui

st.set_page_config(
    page_title=" Trips & Visits",
    page_icon=":airplane:",
    layout="wide"
)

st.title(" ✈️ Trips & Visits Overview")
st.write(
    "An overview of trips and visits for WY2024/2025"
)

# remove streamlit header and footer
hide_st_style = """
                <style>
                header {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# horizontal navigation bar
selected = option_menu(
    menu_title= None,
    options = ["📊 Dashboard", "🎾 Tennis Court"],
    icons= ["chart", "tennis"],
    default_index=0,
    orientation= "horizontal"
)

if selected == "📊 Dashboard":
    # subheader name
    #st.subheader("📊 Interactive Dashboard")

    #About Dashboard -- Do we need this?
    #with st.expander("**About Dashboard**"):
    #    st.info("Display key statistics of all engagements based on FIEP.")
    #    st.markdown("How to use")
    #    st.warning("Select your desired filter in the dropdown box. The charts will automatically update based on your selected filters. To view the datasets, click on 'Data preview'")

    
    # Load data - read .xlsx into Pandas dataframe
    df = pd.read_excel("Trip and visit WY24_25 Database.xlsx")
    # add month & year column
    df['Month'] = df["Departure Date"].dt.month_name()
    df['Year'] = df["Departure Date"].dt.year
    df['Year'] = df['Year'].astype("object")
    #df['Year'] = df['Year'].astype('int') # enable when using slider for year below

    @st.cache_data # cache local data

    # function to format dataframe
    def df_formatted(df_formatted):
        st.dataframe(
            df.drop(columns= ['Month','Year']),
            use_container_width=True,
            hide_index=True,
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
            }
        )
        
    def bb_stats(bb_df):
        # filter data for 'BB'
        bb_filtered = df[df['Del Lead'] == 'BB']

        # Group and cound by type
        bb_df = bb_filtered.groupby(['Type']).size().reset_index(name='count')

        # Calculate total count
        bb_total = bb_df['count'].sum()

        # add column for percentage calculation
        bb_df['Percentage'] = bb_df['count'] / bb_total * 100

        return bb_df
    
    def chief_stats(chief_df):
        # filter data for 'Chief'
        chief_filtered = df[df['Del Lead'] == 'Chief']

        # Group and cound by type
        chief_df = chief_filtered.groupby(['Type']).size().reset_index(name='count')

        # Calculate total count
        chief_total = chief_df['count'].sum()

        # add column for percentage calculation
        chief_df['Percentage'] = chief_df['count'] / chief_total * 100

        return chief_df

    def hod_stats(hod_df):
        # filter data for 'HOD'
        hod_filtered = df[df['Del Lead'] == 'HOD']

        # Group and cound by type
        hod_df = hod_filtered.groupby(['Type']).size().reset_index(name='count')

        # Calculate total count
        hod_total = hod_df['count'].sum()

        # add column for percentage calculation
        hod_df['Percentage'] = hod_df['count'] / hod_total * 100

        return hod_df
    
    def dir_stats(hod_df):
        # filter data for 'HOD'
        dir_filtered = df[df['Del Lead'] == 'Director']

        # Group and cound by type
        dir_df = dir_filtered.groupby(['Type']).size().reset_index(name='count')

        # Calculate total count
        dir_total = dir_df['count'].sum()

        # add column for percentage calculation
        dir_df['Percentage'] = dir_df['count'] / dir_total * 100

        return dir_df

    def working_stats(working_df):
        # filter data for 'HOD'
        working_filtered = df[df['Del Lead'] == 'Working']

        # Group and cound by type
        working_df = working_filtered.groupby(['Type']).size().reset_index(name='count')

        # Calculate total count
        working_total = working_df['count'].sum()

        # add column for percentage calculation
        working_df['Percentage'] = working_df['count'] / working_total * 100

        return working_df
        
    with st.expander("Data preview"):
        df_formatted(df)
    
    col = st.columns((1, 1, 1), gap = 'medium')

    with col[0]:
        total = df['Del Lead'].count()
        st.metric(label= "**Total Engagements**", value=total, delta= 150)

    with col[1]:
        del_df = df.groupby(['Del Lead']).size().reset_index(name='count')
        del_total = del_df['count'].sum()
        del_df['Percentage']=del_df['count'] / del_total * 100

        # create base chart
        del_chart = alt.Chart(del_df).mark_arc(outerRadius=80, innerRadius=60).encode(
            theta = alt.Theta('Percentage:Q', stack = True),
            color = 'Del Lead',
            tooltip = ['Del Lead', 'count']
        )
        st.markdown("**Breakdown by Del Lead**")        
        st.altair_chart(del_chart, use_container_width=True, theme='streamlit')
        
        

    # group data by Year, Month, Del Lead
    group_data1 = df.groupby(['Year','Month', 'Del Lead']).size().reset_index(name='count')
    
    # custom month order for chart
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    # custom filter for chart
    del_filter = alt.selection_multi(fields=['Del Lead'])
        
    # using altair
    chart = alt.Chart(df).mark_bar().encode(
        opacity = alt.condition(del_filter, alt.value(1), alt.value(0.2)),
        x=alt.X('Month:O', title=" ", sort=month_order),
        y=alt.Y('count()', title='No. of Trips & Visits'),
        color='Del Lead',
        tooltip=['Del Lead', 'Type', 'count()'],
    ).add_params(
        del_filter,
    ).facet(
        column='Year',
        #title='Trips & Visits by Group',
    ).properties(
        title = "Engagements by Group",
    ).configure_title(
        anchor = 'middle',
    ).interactive()
    
    #display chart
    st.altair_chart(chart, use_container_width=True)

    # display bb stats
    bb_chart = alt.Chart(bb_stats(df)).mark_arc(outerRadius=80, innerRadius=60).encode(
        theta = alt.Theta('Percentage:Q', stack = True),
        color = 'Type',
        tooltip = ['Type', 'count']
    )
    st.altair_chart(bb_chart, use_container_width=True)
    
    # display chief stats
    chief_chart = alt.Chart(chief_stats(df)).mark_arc(outerRadius=80, innerRadius=60).encode(
        theta = alt.Theta('Percentage:Q', stack = True),
        color = 'Type',
        tooltip = ['Type', 'count']
    )
    st.altair_chart(chief_chart, use_container_width=True)

    # display hod stats
    hod_chart = alt.Chart(hod_stats(df)).mark_arc(outerRadius=80, innerRadius=60).encode(
        theta = alt.Theta('Percentage:Q', stack = True),
        color = 'Type',
        tooltip = ['Type', 'count']
    )
    st.altair_chart(hod_chart, use_container_width=True)

    # display dir stats
    dir_chart = alt.Chart(dir_stats(df)).mark_arc(outerRadius=80, innerRadius=60).encode(
        theta = alt.Theta('Percentage:Q', stack = True),
        color = 'Type',
        tooltip = ['Type', 'count']
    )
    st.altair_chart(dir_chart, use_container_width=True)

    # display working stats
    working_chart = alt.Chart(working_stats(df)).mark_arc(outerRadius=80, innerRadius=60).encode(
        theta = alt.Theta('Percentage:Q', stack = True),
        color = 'Type',
        tooltip = ['Type', 'count']
    )
    st.altair_chart(working_chart, use_container_width=True)
    

    # Hide filter options
    #with st.expander("**Select filter**"):
        # Del Lead selection - Create dropdown menu for Del Lead selection
    #    del_lead_list = df["Del Lead"].unique()
    #    del_lead_selection = st.multiselect('Select Del Lead', del_lead_list, ['Director', 'BB', 'Chief', 'HOD', 'Working'])

    #    # Year selection - Create dropdown menu for Year selection
    #    year_list = df["Year"].unique()
    #    year_selection = st.multiselect('Select Year', year_list, [2024, 2025])

        # Year selection - Create slider for year range selection
        #year_list = df['Year'].unique()
        #year_selection = st.slider('Select your duration',2021,2030, (2022, 2024))
        #year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

        # Subset data - Filter dataframe based on selection
    #    df_selection = df[df['Del Lead'].isin(del_lead_selection) & df['Year'].isin(year_selection)]
    #    df_selection.drop(columns=["Month", "Year"], axis = 1, inplace= True)

    # Hide dataframe in dropdown menu -- do we need this?
    #with st.expander("Data preview"):
    #    st.info("You may download a copy of the table in .csv format. Click the download icon at the top right of the table.")
    #    st.warning("To edit any data, double-click on the desired cell. Please ensure no columns are empty.")
    #    #Editable dataframe - Allow users to make live edits to the dataframe
    #    df_editor = st.data_editor(
    #        df, 
    #        use_container_width=True,
    #        column_config={
    #            "Confluence Link": st.column_config.LinkColumn("Confluence Link"), # enable clickable links in dataframe
    #            "Departure Date": st.column_config.DateColumn( # change date format
    #                "Departure Date",
    #                format= "DD MMM YYYY"
    #            ),
    #            "Return Date": st.column_config.DateColumn( # change date format
    #                "Return Date",
    #                format= "DD MMM YYYY"
    #             ),
    #        },
    #    hide_index= True
    #)

# Page setup
#dashboard_page = st.Page(
 #   page = "views/dashboard.py",
 #   title="Dashboard",
#  icon = "📊",
#   default=True,
#)

#tennis_page = st.Page(
    #page = "views/tennis_court.py",
    #title="Tennis Court",
    #icon = "🎾",
#)

#pg = st.navigation(pages=[dashboard_page, tennis_page])
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