import streamlit as st
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

# Function that generates the flow/pipeline diagram
def generate_diagram():
    with Diagram("PDF Processing Flow", show=False, direction="TB", outformat="png"):
        user = Custom("User", "./images/user.png")
        app = Custom("Streamlit App", "./images/streamlit.png")
        storage = Server("Streamlit Cloud Storage")
        pdf_processor_check = Server("PDF Processor Check")
        py_pdf_processor = Custom("PyPDF Processor", "./images/pypdf2.png")
        nougat_processor = Server("Nougat Processor")
        ngrok_agent = Custom("Ngrok Agent", "./images/ngrok.png")
        colab_ngrok_service = Custom("Google Colab ngrok Service", "./images/colab.png")
        nougat_api = Server("Nougat API")

        # Create the connections between elements
        user >> Edge(label="Http/Https PDF link") >> app
        app >> Edge(label="Download PDF") >> storage
        storage >> Edge(label="Validate PDF") >> pdf_processor_check
        pdf_processor_check >> Edge(label="PyPDF Processor") >> py_pdf_processor
        py_pdf_processor >> Edge(label="Send PDF Link") >> user  
        pdf_processor_check >> Edge(label="Nougat Processor") >> nougat_processor
        nougat_processor >> Edge(label="Send to Ngrok Agent") >> ngrok_agent
        ngrok_agent >> Edge(label="Forward Request") >> colab_ngrok_service
        colab_ngrok_service >> Edge(label="Forward Request") >> nougat_api
        nougat_api >> Edge(label="Return MMD File") >> user

# Create a new page for the flow diagram
if st.button("Show Flow Diagram"):
    st.subheader("PDF Processing Flow Diagram")
    generate_diagram()
    diagram_image_path = "./pdf_processing_flow.png"
    st.image(diagram_image_path)
