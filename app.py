######################################import streamlit as st
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
import bokeh
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import markdown
import hydralit_components as hc
import time
from streamlit_metrics import metric, metric_row

#@st.cache

#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy

app = hy.HydraApp(title='Diwan')


my_bar = st.progress(0)
# progress bar continues to complete from 0 to 100
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)
st.write('Done Loading')

st.balloons()

df= pd.read_csv('https://raw.githubusercontent.com/SalemGrayzi/status/main/Statuscsv%20-%20Copy.csv')
df['Address'] =  df['Address'].fillna('بشامون')
df.drop(['Order No_','Phone No_','Receipt No','Company'], axis = 1, inplace = True)
df.drop_duplicates(inplace=True)

df['Handheld Used'] = df['Handheld Used'].map(
                   {True:'Used PDA' ,False:"Didn't Use PDA"})
df['OnlineApp'] = df['OnlineApp'].map(
                   {True:'Application' ,False:'Phone Call'})


######################################
Day=px.histogram(df, y= "Day Name",text_auto=True)
Day.update_layout(yaxis={'categoryorder':'total ascending'})
Day.update_layout(title="Orders per Day in a Year",xaxis_title="",yaxis_title="Day")

######################################
driver=px.histogram(df, y="Driver Name", text_auto=True)
driver.update_layout(yaxis={'categoryorder':'total ascending'})
driver.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")

####################################################################
#split_size = st.slider('Top n Drivers', 0, 90, 5)
#dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
#dfd.columns = ['Driver Name', 'count']
#drv = px.bar(dfd, y='Driver Name', x = 'count')
######################################
vt=df['Handheld Used'].value_counts()
vts=df['Handheld Used'].value_counts().index
pda=go.Figure(data=[go.Pie(labels=vts, values=vt, pull=[0.2, 0])])
pda.update_traces(textposition='inside', textinfo='percent+label')
pda.update_layout(title="Percent of PDA Usage")

######################################
gh = sns.catplot(
    data=df, kind="count",
    x="Status", hue="Handheld Used",
     palette=['tab:blue', 'tab:red'], alpha=.6, height=6,order=df['Status'].value_counts().index
)
gh.fig.suptitle("Order Status with Usage of PDA")
gh.set_axis_labels(x_var="Order Status", y_var="")
######################################
pdapicker = sns.catplot(
    data=df, kind="count",
    y="PickerName", hue="Handheld Used",
     palette=['tab:red', 'tab:blue'], alpha=.6,height=6,order=df['PickerName'].value_counts().index
)
pdapicker.set(title ="Usage of PDA per Picker", ylabel='Picker')

######################################
stpk = px.histogram(df, y="PickerName", color="Status",barnorm = "percent",hover_data=["Status"])
stpk.update_layout(yaxis={'categoryorder':'total ascending'})
stpk.update_layout(title="Picker's Percentage of Order Status",xaxis_title="Percentage",yaxis_title="Picker")

######################################
am=df['Amount'].value_counts()
op=df['OnlineApp'].value_counts()
ops=df['OnlineApp'].value_counts().index
onmount=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df.loc[df['Status'] == 'Delivered'].Amount, pull=[0.2, 0])])
onmount.update_traces(textposition='inside', textinfo='percent+label')
onmount.update_layout(title="Revenue of Ordering Method")
######################################
onmount2=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df.loc[df['Status'] == 'Canceled'].Amount, pull=[0.2, 0])])
onmount2.update_traces(textposition='inside', textinfo='percent+label')
onmount2.update_layout(title="Lost Revenue of Ordering Method")

######################################
#n_size = st.sidebar.slider('Top n Customers', 0, 90, 5)
#dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
#amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
#amc=px.histogram(data_frame=dfna, x='Amount', y='Name')
######################################
sto=px.histogram(df, y="Status", color="OnlineApp",text_auto=True)
sto.update_layout(title="Status of Order per Ordering Method",xaxis_title="",yaxis_title="Status of Order")
######################################
tc=px.line(df, y=df['Time Created'].value_counts(),x=df['Time Created'].value_counts().index)
tc.update_layout(title="Time of Incoming Orders",xaxis_title="Time of Order",yaxis_title="")
######################################
tdc=px.line(df, y=df['Time to deploy'].value_counts(),x=df['Time to deploy'].value_counts().index)
tdc.update_layout(title="Time to Deploy an Order",xaxis_title="Time in Hours and Minutes",yaxis_title="")

######################################
#slides = st.sidebar.slider('Top n Locations', 0, 90, 5)
#addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
#addy.columns = ['Adress', 'count']
#addresss = px.bar(addy, y='Adress', x = 'count')
######################################
dincome = px.histogram(df, y="Day Name",x='Amount', histfunc='avg',text_auto=True)
dincome.update_layout(yaxis={'categoryorder':'total ascending'})
dincome.update_layout(title="Average Revenue Per Day",xaxis_title="Amount",yaxis_title="Day Name")

#15

@app.addapp(is_home=True,icon='🏪')
def Home():
 st.title('Diwan Delivery Analysis')
  metric_row(
    {
        "Revenue Received From Customers": df.loc[df['Status'] == 'Delivered'].Amount.sum(),
        "Lost Sales Due cancelation": df.loc[df['Status'] == 'Canceled'].Amount.sum()
    }
)

 head = st.checkbox('First Few Rows')
 amount = st.checkbox("Amount Received in LBP")
 if st.checkbox('Show all graphs'):
    st.subheader('All Graphs')
    Day
    driver
    split_size = st.slider('Top n Drivers', 0, 90, 5)
    dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
    dfd.columns = ['Driver Name', 'count']
    drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
    drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
    drv
    pda
    st.pyplot(gh)
    st.pyplot(pdapicker)
    stpk
    onmount
    onmount2
    n_size = st.slider('Top n Customers', 0, 90, 5)
    dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
    amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
    amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
    amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
    amc
    sto
    tc
    tdc
    slides = st.slider('Top n Locations', 0, 90, 5)
    addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
    addy.columns = ['Adress', 'count']
    addresss = px.bar(addy, y='Adress', x = 'count', text_auto=True)
    addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
    addresss
    dincome
 if amount:
     st.write("Revenue Received" , df.loc[df['Status'] == 'Delivered'].Amount.sum() , "in LBP from customers" , "and lost sales due to cancelation", df.loc[df['Status'] == 'Canceled'].Amount.sum())
 if head:
     st.write(df.head())
 st.header('This is a header')
 st.subheader('This is a subheader')
 st.markdown("### This is a markdown")
 st.write('sdfhsd ihjsd l')
############################################################################

@app.addapp(title='Employee Related Analysis',icon='💼')
def app2():
 hy.info('Hello from app1')

 PDA1 = hy.selectbox('Employee Related Analysis',
                                    ['None','Pickers','Picker and Order Status','PDA Usage','Drivers','PDA and Status of Order','All'])
 if PDA1 == 'Pickers':
    st.pyplot(pdapicker)
    st.write('this is what pickers are')
 elif PDA1 == 'PDA Usage':
        pda
 elif PDA1 == 'Picker and Order Status':
        stpk
 elif PDA1 == 'Drivers':
#        driver
        split_size = st.slider('Top n Drivers', 0, 90, 5)
        dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
        dfd.columns = ['Driver Name', 'count']
        drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
        drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
        drv
 elif PDA1 == 'PDA and Status of Order':
        st.pyplot(gh)
 elif PDA1 == 'All':
        st.pyplot(pdapicker)
        driver
        split_size = st.slider('Top n Drivers', 0, 90, 5)
        dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
        dfd.columns = ['Driver Name', 'count']
        drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
        drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
        drv
        pda
        stpk
        st.pyplot(gh)
 elif PDA1 == 'None':
        st.write(str(''))
#6
############################################################################

@app.addapp(title='Application or Call Analysis',icon='📲')
def app3():
 hy.info('Hello from app 2')
 App = hy.selectbox('Application or Call Analysis',
                                     ['None', 'App vs. Call Revenues','Status of Delivery Using App','All'])

 if App == 'App vs. Call Revenues':
     onmount
     onmount2
 elif App == 'Status of Delivery Using App':
     sto
 elif App == 'All':
     onmount
     onmount2
     sto
 elif App == 'None':
     st.write(str(''))

#3
############################################################################

@app.addapp(title='Customer Analysis',icon='📈')
def app4():
 hy.info('Hello from app 2')
 App = hy.selectbox('Customer Analysis',
                                     ['None','Days','Revenue Per Customer','deploy','time','Address','Average Revenue Per Day','All'])

 if App == 'Revenue Per Customer':
     n_size = st.slider('Top n Customers', 0, 90, 5)
     dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
     amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
     amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
     amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
     amc
 elif App == 'deploy':
     tdc
 elif App == 'time':
     tc
 elif App == 'Days':
     Day
 elif App == 'Average Revenue Per Day':
     dincome
 elif App == 'Address':
     slides = st.slider('Top n Locations', 0, 90, 5)
     addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
     addy.columns = ['Adress', 'count']
     addresss = px.bar(addy, y='Adress', x = 'count',text_auto=True)
     addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
     addresss
 elif App == 'All':
     n_size = st.slider('Top n Customers', 0, 90, 5)
     dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
     amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
     amc=px.histogram(data_frame=dfna, x='Amount', y='Name',text_auto=True)
     amc.update_layout(title="Revenue of Customers",xaxis_title="",yaxis_title="Name of Customer")
     amc
     tdc
     tc
     Day
     slides = st.slider('Top n Locations', 0, 90, 5)
     addy = df.groupby(['Address']).size().to_frame().sort_values([0], ascending = False).head(slides).reset_index()
     addy.columns = ['Adress', 'count']
     addresss = px.bar(addy, y='Adress', x = 'count',text_auto=True)
     addresss.update_layout(title="Demand per Area",xaxis_title="",yaxis_title="Location")
     addresss
     dincome
 elif App == 'None':
     st.write(str(''))




#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()
