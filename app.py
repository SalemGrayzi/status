######################################import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from pandas_profiling import ProfileReport
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import bokeh
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import markdown
import hydralit_components as hc

#@st.cache

#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy

app = hy.HydraApp(title='Simple Multi-Page App')




st.balloons()

df= pd.read_csv('https://raw.githubusercontent.com/SalemGrayzi/status/main/Statuscsv.csv')
df.drop(['Order No_','Phone No_','Receipt No','Company'], axis = 1, inplace = True)
df.dropna()
df.drop_duplicates()
#df['Amount'] = df.apply(lambda x: "{:,}".format(x['Amount']), axis=1)
df['Handheld Used'] = df['Handheld Used'].map(
                   {True:'Used PDA' ,False:"Didn't Use PDA"})
df['OnlineApp'] = df['OnlineApp'].map(
                   {True:'Application' ,False:'Phone Call'})


#st.checkbox('First Few Rows',st.write(df.head()))
######################################
Day=px.histogram(df, y= "Day Name",text_auto=True)
######################################
driver=px.histogram(df, y="Driver Name", text_auto=True)
driver.update_layout(yaxis={'categoryorder':'total ascending'})
####################################################################
split_size = st.sidebar.slider('Top n Drivers', 0, 90, 5)
dfd = df.groupby(['Driver Name']).size().to_frame().sort_values([0], ascending = False).head(split_size).reset_index()
dfd.columns = ['Driver Name', 'count']
drv = px.bar(dfd, y='Driver Name', x = 'count')
######################################
vt=df['Handheld Used'].value_counts()
vts=df['Handheld Used'].value_counts().index
pda=go.Figure(data=[go.Pie(labels=vts, values=vt, pull=[0.2, 0])])
pda.update_traces(textposition='inside', textinfo='percent+label')
######################################
gh = sns.catplot(
    data=df, kind="count",
    x="Status", hue="Handheld Used",
     palette=['tab:blue', 'tab:red'], alpha=.6, height=6,order=df['Status'].value_counts().index
)
######################################
pdapicker = sns.catplot(
    data=df, kind="count",
    y="PickerName", hue="Handheld Used",
     palette=['tab:red', 'tab:blue'], alpha=.6, height=6,order=df['PickerName'].value_counts().index
)
######################################
stpk = px.histogram(df, y="PickerName", color="Status",barnorm = "percent",hover_data=["Status"])
stpk.update_layout(yaxis={'categoryorder':'total ascending'})
######################################
am=df['Amount'].value_counts()
op=df['OnlineApp'].value_counts()
ops=df['OnlineApp'].value_counts().index
onmount=go.Figure(data=[go.Pie(labels=df['OnlineApp'], values=df['Amount'], pull=[0.2, 0])])
onmount.update_traces(textposition='inside', textinfo='percent+label')
######################################
n_size = st.sidebar.slider('Top n Customers', 0, 90, 5)

dfna = df.groupby("Name", as_index=False).sum().sort_values("Amount", ascending=False).head(n_size)
amc=go.Figure(go.Bar(x=dfna["Amount"], y=dfna["Name"]))
amc=px.histogram(data_frame=dfna, x='Amount', y='Name')
######################################
sto=px.histogram(df, y="Status", color="OnlineApp",text_auto=True)
######################################
tc=px.line(df, y=df['Time Created'].value_counts(),x=df['Time Created'].value_counts().index)
######################################
tdc=px.line(df, y=df['Time to deploy'].value_counts(),x=df['Time to deploy'].value_counts().index)
######################################



#PDA = st.sidebar.selectbox('Employee Related Analysis',
#                                    ['None','Pickers','Picker and Order Status','PDA Usage','Drivers','All'])
#if PDA == 'Pickers':
#    st.pyplot(pdapicker)
#elif PDA == 'PDA Usage':
#    pda
#elif PDA == 'Picker and Order Status':
#    stpk
#elif PDA == 'Drivers':
#    driver
#    drv
#elif PDA == 'All':
#    st.pyplot(pdapicker)
#    driver
#    drv
#    pda
#    stpk
#elif PDA == 'Correlation':
#    heat=sns.heatmap(df.corr()[['Amount']].sort_values('Status', ascending=False), annot = True)
#    heat.figure
#elif PDA == 'None':
#    st.write(str(''))

#App = st.sidebar.selectbox('Application or Call Analysis',
#                                    ['None', 'App vs. Call Revenues','Status of Delivery Using App','All'])

#if App == 'App vs. Call Revenues':
#    onmount
#elif App == 'Status of Delivery Using App':
#    sto
#elif App == 'All':
#    onmount
#    sto
#elif App == 'None':
#    st.write(str(''))



# Revenue and days needed to put in a selectbox


chart_visual = st.sidebar.selectbox('Select Desired Graph',
                                    ['None','Days','Drivers','PDA Usage',
                                    'Pickers','Picker and Order Status', 'App vs. Call Revenues',
                                    'Revenue Per Customer','Status of Delivery Using App','PDA and Status of Order'])

if chart_visual == 'Days':
    Day
elif chart_visual == 'Drivers':
#    driver
    drv
elif chart_visual == 'PDA Usage':
    pda
elif chart_visual == 'Weekday/weekend':
    weeks
elif chart_visual == 'Pickers':
    st.pyplot(pdapicker)
elif chart_visual == 'Picker and Order Status':
    stpk
elif chart_visual == 'App vs. Call Revenues':
    onmount
elif chart_visual == 'Revenue Per Customer':
    amc
elif chart_visual == 'Status of Delivery Using App':
    sto
elif chart_visual == 'PDA and Status of Order':
    st.pyplot(gh)
elif chart_visual == 'None':
    st.write(str(''))



@app.addapp(is_home=True,icon='🏪')
def Home():
 hy.info('Hello from app1')
 st.title('Diwan Delivery Analysis')
 head = st.checkbox('First Few Rows')
 amount = st.checkbox("Amount Received in LBP")

 if amount:
     st.write("Amount received" , df['Amount'].sum(axis=0) , "in LBP from customers")
 if head:
     st.write(df.head())

@app.addapp(title='Employee Related Analysis',icon='💼')
def app2():
 hy.info('Hello from app1')
 PDA1 = hy.selectbox('Employee Related Analysis',
                                    ['None','Pickers','Picker and Order Status','PDA Usage','Drivers','PDA and Status of Order','All'])
 if PDA1 == 'Pickers':
    st.pyplot(pdapicker)
 elif PDA1 == 'PDA Usage':
        pda
 elif PDA1 == 'Picker and Order Status':
        stpk
 elif PDA1 == 'Drivers':
#        driver
        split_size
        drv
 elif PDA1 == 'PDA and Status of Order':
        st.pyplot(gh)
 elif PDA1 == 'All':
        st.pyplot(pdapicker)
        driver
        split_size
        drv
        pda
        stpk
        st.pyplot(gh)
#elif PDA == 'Correlation':
#    heat=sns.heatmap(df.corr()[['Amount']].sort_values('Status', ascending=False), annot = True)
#    heat.figure
 elif PDA1 == 'None':
        st.write(str(''))

@app.addapp(title='Application or Call Analysis',icon='📲')
def app3():
 hy.info('Hello from app 2')
 App = hy.selectbox('Application or Call Analysis',
                                     ['None', 'App vs. Call Revenues','Status of Delivery Using App','All'])

 if App == 'App vs. Call Revenues':
     onmount
 elif App == 'Status of Delivery Using App':
     sto
 elif App == 'All':
     onmount
     sto
 elif App == 'None':
     st.write(str(''))

@app.addapp(title='Customer Analysis',icon='📈')
def app4():
 hy.info('Hello from app 2')
 App = hy.selectbox('Customer Analysis',
                                     ['None','Days','Revenue Per Customer','deploy','time','All'])

 if App == 'Revenue Per Customer':
     amc
 elif App == 'deploy':
     tdc
 elif App == 'time':
     tc
 elif App == 'Days':
     Day
 elif App == 'All':
     amc
     tdc
     tc
     Day
 elif App == 'None':
     st.write(str(''))




#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()

if st.sidebar.checkbox('Show all graphs'):
    st.subheader('All Graphs')
    Day
    driver
    drv
    pda
    st.pyplot(gh)
    st.pyplot(pdapicker)
    stpk
    onmount
    amc
    sto
    tc
    tdc
