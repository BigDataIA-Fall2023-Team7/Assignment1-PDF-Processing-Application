import streamlit as st
import os

a = os.getcwd()
b = os.listdir()

st.write(a)
st.write(b)
