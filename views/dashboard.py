import streamlit as st
import pandas as pd
import altair as alt
from streamlit_option_menu import option_menu
import time

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

def main():
    st.markdown("""
            <style>
            .subheader {
                text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)    

st.subheader("📊 Dashboard")    
with st.expander("Data preview"):
    df_formatted(df)
    
# filter for completed trips/visits
completed_df = df[df['Status'] == 'Completed']

# calculate total and completed trips/visits
total_df = len(df)
completed_df_count = len(completed_df)

# Calculate completion rate
completion_rate = completed_df_count / total_df * 100

# display completion rate
st.metric(label = "**Overall Status**", value = f"{completion_rate:}% engagements completed")
    
# display progress bar
progress_bar = st.progress(0)
for i in range(total_df):
    time.sleep(0.1)
    progress_bar.progress(i+1)
    
col = st.columns((1, 2, 1), gap = 'medium')

with col[0]:
    st.subheader("**Engagement Count**")
    col01, col02 = st.columns(2)
           
    with col01:
        total = df['Del Lead'].count()
        st.metric(label= "**Total Engagements**", value=total, delta= 100) 
        
    with col02:
        # filter for Home
        visit_filtered = df[df['Type'] == 'Home']
        visit_total = visit_filtered.groupby(['Type']).size().reset_index(name='count')
        vist_total = visit_total['count']
        st.metric(label="**Visits (Home)**", value = vist_total)

        # filter for away
        trip_filtered = df[df['Type'] == 'Away']
        trip_total = trip_filtered.groupby(['Type']).size().reset_index(name='count')
        trip_total = trip_total['count']
        st.metric(label="**Trips (Away)**", value = trip_total)

with col[1]:
    del_df = df.groupby(['Del Lead']).size().reset_index(name='count')
    del_total = del_df['count'].sum()
    del_df['Percentage']=del_df['count'] / del_total * 100

    # create base chart
    del_chart = alt.Chart(del_df).mark_arc(outerRadius=80, innerRadius=60).encode(
        theta = alt.Theta('Percentage:Q', stack = True),
        color = 'Del Lead',
        tooltip = ['Del Lead', 'count']
    ).interactive()
    st.subheader("**Breakdown by Lead**")        
    st.altair_chart(del_chart, use_container_width=True, theme='streamlit')
        
with col[2]:
    st.subheader("**Status**")
    col21, col22, col23 = st.columns(3)
        
    with col21:
        # filter for Completed
        completed_filtered = df[df['Status'] == 'Completed']
        if not completed_filtered.empty:
            completed_total = completed_filtered.groupby(['Status']).size().reset_index(name='count')
            completed_total = completed_total['count'].iloc[0]
            st.metric(label="**Completed**", value = completed_total)
        else:
            st.metric(label="**Completed**", value = 0)
            
        # filter for Cancelled
        cancelled_filtered = df[df['Status'] == 'Cancelled']
        if not cancelled_filtered.empty:
            cancelled_total = cancelled_filtered.groupby(['Status']).size().reset_index(name='count')
            cancelled_total = cancelled_total['count']
            st.metric(label="**Cancelled**", value = cancelled_total)
        else:
            st.metric(label="**Cancelled**", value = 0)

        # filter for New
        new_filtered = df[df['Status'] == 'New']
        if not new_filtered.empty:
            new_total = new_filtered.groupby(['Status']).size().reset_index(name='count')
            new_total = new_total['count']
            st.metric(label="**New**", value = new_total)
        else:
            st.metric(label="**New**", value = 0)
                   
    with col22:
        # filter for In progress
        inpro_filtered = df[df['Status'] == 'In progress']
        if not inpro_filtered.empty:
            inpro_total = inpro_filtered.groupby(['Status']).size().reset_index(name='count')
            inpro_total = inpro_total['count']
            st.metric(label="**In Progress**", value = inpro_total)
        else:
            st.metric(label="**In Progress**", value = 0)

        # filter for Modified
        modified_filtered = df[df['Status'] == 'Modified']
        if not modified_filtered.empty:
            modified_total = modified_filtered.groupby(['Status']).size().reset_index(name='count')
            modified_total = modified_total['count']
            st.metric(label="**Modified**", value = modified_total)
        else:
            st.metric(label="**Modified**", value = 0)

    with col23:
        # filter for Scheduled
        scheduled_filtered = df[df['Status'] == 'Scheduled']
        if not scheduled_filtered.empty:
            scheduled_total = scheduled_filtered.groupby(['Status']).size().reset_index(name='count')
            scheduled_total = scheduled_total['count']
            st.metric(label="**Scheduled**", value = scheduled_total)
        else:
            st.metric(label="**Scheduled**", value=0)

        # filter for Postponed
        postponed_filtered = df[df['Status'] == 'Postponed']
        if not postponed_filtered.empty:
            postponed_total = postponed_filtered.groupby(['Status']).size().reset_index(name='count')
            postponed_total = postponed_total['count']
            st.metric(label="**Postponed**", value = postponed_total)
        else:
            st.metric(label="**Postponed**", value = 0)

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
st.altair_chart(chart)

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