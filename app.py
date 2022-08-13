### Importing the required packages
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import markdown
import time
from streamlit_metrics import metric, metric_row
import io
st.set_page_config(layout="wide")

my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)
st.write('Done Loading')

import streamlit as st

def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")
    st.cache()
    st.title('Diwan Delivery Analysis')
    col1, col2,col3 = st.columns(3) ### Adding columns to insert the picture in the middle of the screen in column 2

    with col1:
        st.write(' ')
    with col2:
        st.image("https://play-lh.googleusercontent.com/qPmIH0OemtPoTXyEztnpZVW-35sEWvrw99DIX6n1sklf1mDekUxtMzyInpJlTOATsp5B") # Adding Diwan hyper market picture
    with col3:
        st.write(' ')

    head = st.checkbox('First Few Rows') # Making a checkbox for showing df.head
    if st.checkbox('Show all graphs'): # Adding all graph into a single button to see
    st.subheader('All Graphs')
    container1 = st.container()
    g1, g2,g21 = st.columns(3)

        with container1:
            with g1:
                Day
        with g21:
               driver


    container2 = st.container()
    g3, g4, g41 = st.columns(3)

    with container2:
       with g3:
            split_size = st.slider('Top n Drivers', 0, 90, 5)
            dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
            dfd.columns = ['Driver Name', 'count']
            drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
            drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
            drv
        with g41:
            pda
    container3 = st.container()
    g5,g6,g61 = st.columns(3)

    with container3:
        with g5:
            st.pyplot(gh)
        with g61:
            st.pyplot(pdapicker)
    container4 = st.container()
    g7,g8,g81 = st.columns(3)

    with container4:
        with g7:
            stpk
        with g81:
            onmount
    container5 = st.container()
    g9,g10,g01 = st.columns(3)

    with container5:
        with g9:
            onmount2
        with g01:
            n_size = st.slider('Top n Customers', 0, 90, 5)
            dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
            amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
            amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
            amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
            amc
    container6 = st.container()
    g11,g12,g02 = st.columns(3)

    with container6:
        with g11:
            sto
        with g02:
            tc
    container7 = st.container()
    g13,g14,g04 = st.columns(3)

    with container7:
        with g13:
            tdc
        with g04:
            slides = st.slider('Top n Locations', 0, 90, 5)
            addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
            addy.columns = ['Adress', 'count']
            addresss = px.bar(addy, y='Adress', x = 'count', text_auto=True)
            addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
            addresss
            dincome
    if head:
        st.write(df.head())

 ### Adding comments onto the home tab for understanding the dashboard
    st.header('What is the objective of this Dashboard?')
    st.write('In this dashboard, we are trying to analyze Diwan’s Delivery sector, by making visuals to help us understand what is happening on the ground as it brings many managerial insights about how the company is doing throughout the year. This dashboard will go into three various sub-sections in the delivery sector. The three sub-sections that we will be focusing on are:')
    st.write('1-	Employees related analysis')
    st.write('2-	Type of methods used in ordering')
    st.write('3-	Customer analysis and the area they are ordering from')
    st.write('After going through each tab and its respectable analysis we would understand in more detail how this information can enable us to adapt accordingly. Each tab represents a certain sub-section and a quick analysis of what is being presented.')

 ### Adding Tableau dashboard link for secondary dashboard
    st.write('For additional visuals feel free to press the following link')
    link = '[Tableau]https://public.tableau.com/app/profile/salem.gr/viz/DiwanDeliverySectorAnalysis/DiwanDeliverySectorAnalysis'
    st.markdown(link, unsafe_allow_html=True)

 ### Importing the table ive made on the queuing model using csv github
    st.write('The following button has three models depending on demand Diwan should hire accordingly with its following costs')
    df1= pd.read_csv('https://raw.githubusercontent.com/SalemGrayzi/status/main/Queing%20Model.csv')

## defining a code to convert df1 into utf-8
    def convert_df(df1):
        return df1.to_csv().encode('utf-8')

## Converting the csv file to utf-8
    csv = convert_df(df1)

### Creating a download button to get the queuing model
    st.download_button(
        label="Download Queuing Model",
        data=csv,
        file_name='Queuing_Model.csv',
        mime='text/csv',
  )

 ### Word documents from google drive where it has the full report once clicked it downloads
    st.write('For the full analysis press the following link to be redirected to the report')
    link1 = '[Full Report]https://drive.google.com/uc?export=download&id=1xiEgoeXq9oxBc4ZQELjsY36mHyrbHFXV'
    st.markdown(link1, unsafe_allow_html=True)

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")
    st.write('12165')
def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

