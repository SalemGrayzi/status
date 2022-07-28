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

df= pd.read_csv('https://raw.githubusercontent.com/SalemGrayzi/status/main/Statuscsv.csv')
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
     palette=['tab:red', 'tab:blue'], alpha=.6, height=6,order=df['Status'].value_counts().index
)
gh.fig.suptitle("Order Status with Usage of PDA")
gh.set_axis_labels(x_var="Order Status", y_var="")
######################################
pdapicker = sns.catplot(
    data=df, kind="count",
    y="PickerName", hue="Handheld Used",
     palette=['tab:blue', 'tab:red'], alpha=.6,height=6,order=df['PickerName'].value_counts().index
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
 col1, col2,col3 = st.columns(3)

 with col1:
     st.write(' ')

 with col2:
     st.image("https://play-lh.googleusercontent.com/qPmIH0OemtPoTXyEztnpZVW-35sEWvrw99DIX6n1sklf1mDekUxtMzyInpJlTOATsp5B")
 with col3:
    st.write(' ')

 head = st.checkbox('First Few Rows')
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
 if head:
     st.write(df.head())
 st.header('What is the objective of this Dashboard?')
 st.write('In this dashboard, we are trying to analyze Diwan’s Delivery sector, by making visuals to help us understand what is happening on the ground as it brings many managerial insights about how the company is doing throughout the year. This dashboard will go into three various sub-sections in the delivery sector. The three sub-sections that we will be focusing on are:')
 st.write('1-	Employees related analysis')
 st.write('2-	Type of methods used in ordering')
 st.write('3-	Customer analysis and the area they are ordering from')
 st.write('In the first section, we are going to be talking about how the pickers are utilizing the PDA equipment as well as how it might affect an order status. Here we will find the distribution of PDA usage across the pickers to find the percentage of if they are using said equipment or not. After finding the percentage of usage of PDA we turn our heads to find the proportions of each picker if their orders were canceled or delivered as this might arise some issues that some pickers might be falling behind whether it’s their service or an issue they are facing for higher cancelation rates.')
 st.write('In the second section, we focus on which ordering method is bringing in the most revenue and causing lost opportunity sales. The two methods are using the phone to order, or the application. Finally, we would like to find which ordering method has a higher probability of lost sales, and which generates the most revenue.')
 st.write('Finally, the last section covers the customers. In this section, we will be looking at overall lost sales and generated revenues, and several other pieces of information that are valuable to understanding Diwan’s customers. Here we look at revenues generated by each customer and which day generates the most. An important part is analyzing which days are the highest demand, and the area they are coming from. Last but not least is finding the distribution of the time of incoming orders to understand during which time has the biggest workload on the pickers, and see how long it takes to deploy an order.')


 st.write('For additional visuals feel free to press the following link')
 link = '[GitHub]https://public.tableau.com/app/profile/salem.gr/viz/DiwanDeliverySectorAnalysis/DiwanDeliverySectorAnalysis'
 st.markdown(link, unsafe_allow_html=True)
############################################################################

@app.addapp(title='Employee Related Analysis',icon='💼')
def app2():

 PDA1 = hy.selectbox('Employee Related Analysis',
                                    ['None','Pickers','Picker and Order Status','PDA Usage','Drivers','PDA and Status of Order','All'])
 if PDA1 == 'Pickers':
    st.pyplot(pdapicker)
    st.write('Here we can see each picker that is using a PDA or not. as we can see many of the pickers are not using the PDA in thier daily operations.')
 elif PDA1 == 'PDA Usage':
        pda
        st.write('From this graph we can analyze that 44.3% of pickers are using PDAs compared to 55.7% of them not using PDA. This shows that we should find a way to push the usage of PDAs across the pickers.')
 elif PDA1 == 'Picker and Order Status':
        stpk
        st.write('In this graph we can see the proportions of each picker from their total orders based on cancelation, and completed orders. The Blue shows the orders that have been completed comapared to red which shows the cancelations. As we can see there are couple of pickers that have a higher probability of their orders being canceled this is why we need to get to the buttom of the issue to fix it.')
 elif PDA1 == 'Drivers':
#        driver
        split_size = st.slider('Top n Drivers', 0, 90, 5)
        dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
        dfd.columns = ['Driver Name', 'count']
        drv = px.bar(dfd, y='Driver Name', x = 'count',text_auto=True)
        drv.update_layout(title="Number of Orders per Driver",xaxis_title="",yaxis_title="Driver")
        drv
        st.write('This graph shows the number of orders each driver has done throughout the year, with a filter where you can look at the top # of drivers based on the number of orders.')
 elif PDA1 == 'PDA and Status of Order':
        st.pyplot(gh)
        st.write('This graph is very important as it shows us how does PDA affect the order status. As we can see orders that were canceled with the usage of PDA has a much lower ratio compared to not using PDAs. Eventhough delivered orders are similar to each other but with cancelation there is a big difference between them.')

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
 col1, col2 = st.columns(2)
 col1.metric(label="Revenue in LBP", value=df.loc[df['Status'] == 'Delivered'].Amount.sum(), delta_color="inverse")
 col2.metric(label="Lost Sales in LBP", value=df.loc[df['Status'] == 'Canceled'].Amount.sum(), delta_color="inverse")
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
