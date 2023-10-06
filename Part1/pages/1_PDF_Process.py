import streamlit as st
import re
import requests
import PyPDF2
import io
import time
import os
import datetime



# Function to extract text from a PDF given a URL
def extract_text_from_pdf_url(pdf_url):
    try:
        # Download the PDF file
        response = requests.get(pdf_url, stream=True)
        f = io.BytesIO(response.content)
        #response.raise_for_status()

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(f)

        # Extract text from specified number of pages
        pages = pdf_reader.pages[:]
        #pages = pdf_reader.pages
        contents = "".join([page.extract_text() for page in pages])

        return contents
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
    
def get_output_filename(pdfProcessor):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%m_%d_%Y_%H_%M_%S")
    return pdfProcessor + "ProcessedOutput" + formatted_datetime + ".mmd"

#To set the page configurations
#st.set_page_config(page_title="Asn1-Part1", page_icon='1️⃣', layout="wide", initial_sidebar_state="auto", menu_items=None)


#-----------------------
# .env file details
# Nougat API Server URL
nougatAPIServerURL = st.secrets["NGROK_API_GATEWAY_URL"]
#-----------------------


#PDF Link Validator - validate links ending without .pdf as some links could have request params
# pdf_link_validator = re.compile(r'https?://\S+\.pdf(/)?$')
pdf_link_validator = re.compile(r'https?://\S+$')

#Streamlit Application starts

#Header
st.header("PDF Processing Application")

#Input PDF Link Textbox
input_pdf_link = st.text_input("Link to PDF", value="", max_chars=None, key="input_pdf_link", type="default", help="Enter the link to the PDF which you want to send for processing!")

#Select Library Choice Radio Button
st.radio("Choose the PDF Processor: ",["Nougat", "PyPDF"], captions=["Recommended for physically scanned documents, mathematical equations, etc.", "Recommended for digitally created documents"],index=0, key="input_pdf_processor")

#Process Button
if st.button("Process!", key="process_button", type='primary'):
    if input_pdf_link!='':
        if re.search(pdf_link_validator, input_pdf_link):
            input_pdf_processor = st.session_state.input_pdf_processor
            downloaded_pdf_file = requests.get(input_pdf_link)
            st.success("Sending the PDF at '{}' for processing using '{}' processor!".format(input_pdf_link, input_pdf_processor), icon='✅')

            if input_pdf_processor == "Nougat":
                #Record Start time
                start_time = time.time()

                nougatAPIHeaders = {
                    "Accept":"application/json"
                }
                nougatAPIInputPDF = {'file':downloaded_pdf_file.content}

                processedPdfData = requests.post(nougatAPIServerURL + "/predict", headers=nougatAPIHeaders, files=nougatAPIInputPDF)
                
                #preprocess rules for creating mmd file
                #1. Unstrigify -> One header label
                #2. \n\n -> Actual newline character * 2
                #3. \n -> Actual newline character * 1
                #4. \\ -> \

                cleanData = processedPdfData.content[1:-1].decode().replace(r"\n\n",'\n\n').replace(r"\n",'\n').replace('\\\\', '\\')

                st.success("Processing complete!".format(input_pdf_link, input_pdf_processor), icon='✅')

                outputFileName = get_output_filename("Nougat")

                # Record the end time
                end_time = time.time()

                # Calculate and display the processing time
                if cleanData:
                    processing_time = end_time - start_time
                    st.subheader("Processing Time:")
                    st.write(f"Time taken: {processing_time:.2f} seconds")
                    st.download_button(label="Download the Processed File", data=cleanData, file_name=outputFileName)

            elif input_pdf_processor == "PyPDF":
                
                #Record Start time
                start_time = time.time()
                
                #Call function to process URL using pypdf for the input pages
                pdf_text = extract_text_from_pdf_url(input_pdf_link)
                
                # Record the end time
                end_time = time.time()

                outputFileName = get_output_filename("PyPDF")
                
                # Calculate and display the processing time
                if pdf_text:
                    processing_time = end_time - start_time
                    st.subheader("Processing Time:")
                    st.write(f"Time taken: {processing_time:.2f} seconds")
                    st.download_button(label="Download the Processed File", data=pdf_text, file_name=outputFileName)

        
        else:
            st.error("Invalid Link: Please check your link {Input format : <http | https>://<server-location>.pdf</>}", icon='❗️')
    else:
        st.error("Empty Link: Please enter a link to pdf in the textbox", icon='❗️')