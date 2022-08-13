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

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
# Contents of ~/my_app/streamlit_app.py
import streamlit as st

def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

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

