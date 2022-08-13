### Importing the required packages
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import markdown
from streamlit_metrics import metric, metric_row
st.set_page_config(layout="wide")

my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)
st.write('Done Loading')

df= pd.read_csv('https://raw.githubusercontent.com/SalemGrayzi/status/main/Statuscsv.csv')

### Filling missing values in Adress column with the mode
df['Address'] =  df['Address'].fillna('بشامون')

###Droping columns that dont add value to the analysis
df.drop(['Order No_','Phone No_','Receipt No','Company'], axis = 1, inplace = True)

### Dropping dublicates in the dataset
df.drop_duplicates(inplace=True)

### Changing Boolean values into their respectable names
df['Handheld Used'] = df['Handheld Used'].map(
                   {True:'Used PDA' ,False:"Didn't Use PDA"})
df['OnlineApp'] = df['OnlineApp'].map(
                   {True:'Application' ,False:'Phone Call'})

### In the bellow section it conatains all the graphs made

###################################### Graph to get orders per day in a year
st.cache()
Day=px.histogram(df, x= "Day Name",text_auto=True,category_orders={'Day Name':["Monday","Tuesday","Wednesday", "Thursday", "Friday", "Saturday","Sunday"]})
Day.update_layout(title="Orders per Day in a Year",xaxis_title="Day",yaxis_title="")

###################################### Graph to get number of order per driver
st.cache()
driver=px.histogram(df, y="Driver Name", text_auto=True)
driver.update_layout(yaxis={'categoryorder':'total ascending'})
driver.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")

#################################################################### This graph was sent into its area due to filtering reasoning
#split_size = st.slider('Top n Drivers', 0, 90, 5)
#dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
#dfd.columns = ['Driver Name', 'count']
#drv = px.bar(dfd, y='Driver Name', x = 'count')

###################################### Graph to find the percent of PDA usage
st.cache()
vt=df['Handheld Used'].value_counts()
vts=df['Handheld Used'].value_counts().index
pda=go.Figure(data=[go.Pie(labels=vts, values=vt, pull=[0.2, 0])])
pda.update_traces(textposition='inside', textinfo='percent+label')
pda.update_layout(title="Percent of PDA Usage")
hp,hp1 = (df['Handheld Used'].value_counts() /
                      df['Handheld Used'].value_counts().sum()) * 100

###################################### Order status depending on which order method was used
st.cache()
gh = sns.catplot(
    data=df, kind="count",
    x="Status", hue="Handheld Used",
     palette=['tab:red', 'tab:blue'], alpha=.6, height=6,order=df['Status'].value_counts().index
)
gh.fig.suptitle("Order Status with Usage of PDA")
gh.set_axis_labels(x_var="Order Status", y_var="")

###################################### A graph illustrating which picker is using a PDA
st.cache()
pdapicker = sns.catplot(
    data=df, kind="count",
    y="PickerName", hue="Handheld Used",
     palette=['tab:blue', 'tab:red'], alpha=.6,height=6,order=df['PickerName'].value_counts().index
)
pdapicker.set(title ="Usage of PDA per Picker", ylabel='Picker')

###################################### Fidning the percentage of order status based on each picker
st.cache()
stpk = px.histogram(df, y="PickerName", color="Status",barnorm = "percent",hover_data=["Status"])
stpk.update_layout(yaxis={'categoryorder':'total ascending'})
stpk.update_layout(title="Picker's Percentage of Order Status",xaxis_title="Percentage",yaxis_title="Picker")

###################################### Percentage of revenue based on order methods
st.cache()
am=df['Amount'].value_counts()
op=df['OnlineApp'].value_counts()
ops=df['OnlineApp'].value_counts().index
onmount=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df.loc[df['Status'] == 'Delivered'].Amount, pull=[0.2, 0])])
onmount.update_traces(textposition='inside', textinfo='percent+label')
onmount.update_layout(title="Revenue of Ordering Method")



###################################### Percentage of lost sales based on order methods
st.cache()
onmount2=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df.loc[df['Status'] == 'Canceled'].Amount, pull=[0.2, 0])])
onmount2.update_traces(textposition='inside', textinfo='percent+label')
onmount2.update_layout(title="Lost Sales of Ordering Method")
os,os1 = (df.groupby('OnlineApp')['Status'].count() /
                      df['OnlineApp'].value_counts().sum()) * 100


#################################################################### This graph was sent into its area due to filtering reasoning
#n_size = st.sidebar.slider('Top n Customers', 0, 90, 5)
#dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
#amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
#amc=px.histogram(data_frame=dfna, x='Amount', y='Name')

###################################### ORder status based on order methods
st.cache()
sto=px.histogram(df, y="Status", color="OnlineApp",text_auto=True)
sto.update_layout(title="Status of Order per Ordering Method",xaxis_title="",yaxis_title="Status of Order")

###################################### Time of incoming orders in a day
st.cache()
df['Time Created'] = pd.to_datetime(df['Time Created'], format='%I:%M:%S %p')
tc=px.histogram(x=df['Time Created'])

#,category_orders={'':["7:00:00 AM","8:00:00 AM","9:00:00 AM", "10:00:00 AM", "11:00:00 AM", "12:00:00 PM","1:00:00 PM","2:00:00 PM","3:00:00 PM","4:00:00 PM","5:00:00 PM","6:00:00 PM","7:00:00 PM","8:00:00 PM","9:00:00 PM","10:00:00 PM","11:00:00 PM","12:00:00 PM","1:00:00 AM","2:00:00 AM","3:00:00 AM","4:00:00 AM","5:00:00 AM","6:00:00 AM"]})

#tc=px.line(df, y=df['Time Created'].value_counts(),x=df['Time Created'].value_counts().index,
#    category_orders={'Time Created':["7:00:00 AM","8:00:00 AM","9:00:00 AM", "10:00:00 AM", "11:00:00 AM", "12:00:00 PM",
#    "1:00:00 PM","2:00:00 PM","3:00:00 PM","4:00:00 PM","5:00:00 PM","6:00:00 PM","7:00:00 PM","8:00:00 PM","9:00:00 PM",
#    "10:00:00 PM","11:00:00 PM","12:00:00 PM","1:00:00 AM","2:00:00 AM","3:00:00 AM","4:00:00 AM","5:00:00 AM","6:00:00 AM"]})
#tc.update_layout(title="Time of Incoming Orders",xaxis_title="Time of Order",yaxis_title="")

###################################### Time it takes for an order to deploy
st.cache()
tdc=px.line(df, y=df['Time to deploy'].value_counts(),x=df['Time to deploy'].value_counts().index)
tdc.update_layout(title="Time to Deploy an Order",xaxis_title="Time in Hours and Minutes",yaxis_title="")


#################################################################### This graph was sent into its area due to filtering reasoning
#slides = st.sidebar.slider('Top n Locations', 0, 90, 5)
#addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
#addy.columns = ['Adress', 'count']
#addresss = px.bar(addy, y='Adress', x = 'count')

###################################### Average revenue per day
st.cache()
dincome = px.histogram(df, y="Day Name",x='Amount', histfunc='avg',text_auto=True,category_orders={'Day Name':["Monday","Tuesday","Wednesday", "Thursday", "Friday", "Saturday","Sunday"]})
dincome.update_layout(title="Average Revenue Per Day",xaxis_title="Amount",yaxis_title="Day Name")

st.cache()
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
