import os
import logging
import streamlit as st
import time
import tempfile
from io import BytesIO
from dotenv import load_dotenv
from aws_config import *
from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file
from streamlit_pandas_profiling import st_profile_report
import streamlit.components.v1 as components

load_dotenv()
aws = aws_config()

logClient = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
                        )

st.set_page_config(layout="wide")

def log(message: str):
    logClient.put_log_events(
        logGroupName = "Assignment01-Logs",
        logStreamName = "Run-Logs",
        logEvents = [
            {
                'timestamp' : int(time.time() * 1e3),
                'message' : message
            }
        ]
    )


# @st.cache
def dataPreview(df,data_type, profile_type):
    context =  "<h3 style='text-align: center;'>" + data_type + " Preview</h3>"
    st.markdown(context, unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown("<h3 style='text-align: center;'>Dataset Summary</h1>", unsafe_allow_html=True)
    if profile_type == 'Regular Exploratory Data Analysis (EDA)':
        regularProfiling(df, data_type)
    else:
        timeseriesProfiling(df, data_type)

def downloadReport(report_html):
    st.download_button(
    label="Download Report",
    data=report_html,
    file_name="report.html",
    key="download_button"
    )

def get_html(profile):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, 'report.html')
    print(temp_file_path)
    log(f"Converting report into file")
    # profile.to_file("report.html")
    # HtmlFile = open("./report.html", 'r', encoding='utf-8')
    # report_html = HtmlFile.read()

    # Read the content of the temporary file

    profile.to_file(temp_file_path)
    with open(temp_file_path, 'rb') as temp_file:
        report_html = temp_file.read()

    return report_html

# @st.cache
def regularProfiling(df, data_type):
    # st.markdown("<h6 style='text-align: Left;'>Dataset Summary</h6>", unsafe_allow_html=True)
    st.write(f"Data Type: {data_type}")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Number of Columns: {df.shape[1]}")
    
    log('Regular report initialized')
    profile = ProfileReport(df, title="Regular Exploratory Data Analysis (EDA)", explorative=True)
    log('Regular report generated')

    st.write("### Data Quality Report")
    # report_html = profile.to_file(output_file=BytesIO()).getvalue()

    report_html = get_html(profile)

    filepath = aws.save_report(report_html, data_type, 'Regular')
    components.html(report_html, height=700, width=1400, scrolling=True)
    downloadReport(report_html)

def timeseriesProfiling(df,data_type):
    st.markdown("<h6 style='text-align: Left;'>Dataset Summary</h6>", unsafe_allow_html=True)
    st.write(f"Data Type: {data_type}")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Number of Columns: {df.shape[1]}")

    if data_type == 'Origination Data':
        print("originatiion data")
        sort_by = "First Payment Date"
    else:
        type_schema = {
        "Current Actual UPB": "timeseries"
        }
        sort_by = "Monthly Reporting Period"

    profile = ProfileReport(
    df,
    tsmode=True,
    # type_schema=type_schema,
    sortby=sort_by,
    title="Time-Series Exploratory Data Analysis (EDA)",
    )
    
    log(f"Profile Generated for Time Series")

    st.write("### Data Quality Report")
    report_html = get_html(profile)
    filepath = aws.save_report(report_html, data_type, 'TimeSeries')
    components.html(report_html, height=700, width=1400, scrolling=True)
    downloadReport(report_html)

def data_process(uploaded_file, data_type, profile_type):
    if uploaded_file is None:
        st.sidebar.warning("Please Upload a pdf file")
    else:
        if data_type is None:
            st.sidebar.warning("Select type of data")
        else:
            df = aws.save_data(uploaded_file, data_type)
            log("Data Saved")
            dataPreview(df, data_type, profile_type)
            
def main():
    uploaded_file = st.sidebar.file_uploader("Upload a CSV/XLS file", type=["csv", "xls", "xlsx"])
    data_type = st.sidebar.radio("Select data type:", ["Origination Data", "Monthly Performance Data"], index = None)
    # profile_type = st.sidebar.selectbox("Select type of profiling:",['Regular Exploratory Data Analysis (EDA)', 'Time-Series Exploratory Data Analysis (EDA)'], index = None)    
    profile_type = 'Regular Exploratory Data Analysis (EDA)'
    if st.sidebar.button('Process Data') is False:
        st.markdown("<h1 style='text-align: center;'>Freddie Mac Single Family Dataset Quality Evaluation</h1>", unsafe_allow_html=True)
    else:
        data_process(uploaded_file, data_type, profile_type)

                
if __name__ == "__main__":
    log(f"Streamlit started")
    main()
    log(f"Streamlit ended")