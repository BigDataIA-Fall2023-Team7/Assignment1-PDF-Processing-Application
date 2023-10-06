import streamlit as st
import os


st.write(os.getcwd())
st.write(os.listdir())
st.write(os.listdir('./Part2'))
st.write(os.listdir('./Part2/gx/uncommitted/validations'))



def list_files_and_directories(path):
    for root, dirs, files in os.walk(path):
        st.write(f"Current directory: {root}")
        
        # List all directories in the current directory
        for directory in dirs:
            st.write(f"Directory: {os.path.join(root, directory)}")
        
        # List all files in the current directory
        for file in files:
            st.write(f"File: {os.path.join(root, file)}")

# Specify the directory you want to start from
start_directory = "./Part2"
list_files_and_directories(start_directory)

