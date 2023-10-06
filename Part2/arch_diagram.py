from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users
from diagrams.generic.storage import Storage
from diagrams.custom import Custom

with Diagram("Architecture Diagram", show=False, direction="LR"):
    user = Users("User")
    
    uploaded_file = Custom("Streamlit", "./images/streamlit.png")
    # Custom("Great Expectations", "./images/great_expectations.png")
    user >>uploaded_file

    with Cluster("AWS S3"):
        s3_bucket = S3("S3 Bucket")
        uploaded_file >> s3_bucket

    with Cluster("Data Processing"):
        ge = Custom("Great Expectations", "./images/great_expectations.png")
        ydp = Custom("YDataProfiling", "./images/ydata-profiling.png")
        s3_bucket >> ge
        s3_bucket >> ydp
    
    st = Custom("Streamlit", "./images/streamlit.png")
    report = Storage("Report")

    ge >> st 
    ydp >> st
    st >> report

