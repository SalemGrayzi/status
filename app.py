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

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Home", "About", "Contact"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Home"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Home")
    active_tab = "Home"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Home":
    st.write("Welcome to my lovely page!")
    st.write("Feel free to play with this ephemeral slider!")
    st.slider(
        "Does this get preserved? You bet it doesn't!",
        min_value=0,
        max_value=100,
        value=50,
    )
elif active_tab == "About":
    st.write("This page was created as a hacky demo of tabs")
elif active_tab == "Contact":
    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")
