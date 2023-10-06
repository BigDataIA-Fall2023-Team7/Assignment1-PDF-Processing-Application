import streamlit as st
import re
import requests
import PyPDF2
import io
import time
import os
import datetime

    #To set the page configurations
    #st.set_page_config(page_title="Asn1-Part1", page_icon='1️⃣', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(layout="wide")
st.header("Welcome to PDF Processor Application")


