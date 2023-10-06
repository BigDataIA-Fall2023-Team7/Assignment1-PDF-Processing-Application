import streamlit as st
import os

def list_files_and_directories(path):
    for root, dirs, files in os.walk(path):
        print(f"Current directory: {root}")
        
        # List all directories in the current directory
        for directory in dirs:
            print(f"Directory: {os.path.join(root, directory)}")
        
        # List all files in the current directory
        for file in files:
            print(f"File: {os.path.join(root, file)}")

# Specify the directory you want to start from
start_directory = "."
list_files_and_directories(start_directory)

