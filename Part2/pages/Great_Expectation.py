import streamlit as st
import time
import tempfile
from io import BytesIO
import streamlit.components.v1 as components

filepath = "./gx/uncommitted/data_docs/local_site/index.html"

st.set_page_config(layout="wide")

with open(filepath, "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=800, width=1400, scrolling=True)