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

#Function to get the name of the pdf processed file    
def get_output_filename(pdfProcessor):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%m_%d_%Y_%H_%M_%S")
    return pdfProcessor + "ProcessedOutput" + formatted_datetime + ".mmd"


#To set the page configurations
st.set_page_config(page_title="Asn1-Part1", page_icon='1️⃣', layout="wide", initial_sidebar_state="auto", menu_items=None)


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

if st.session_state.input_pdf_processor == "Nougat":
    #Input Nougat API Server URL Textbox
    nougatAPIServerURL = st.text_input("Link to Nougat API Server", value="", max_chars=None, key="nougatAPIServerURL", type="default", help="Enter the link to the Nougat API Server")

#Process Button
if st.button("Process!", key="process_button", type='primary'):
    if input_pdf_link!='':
        if re.search(pdf_link_validator, input_pdf_link):
            input_pdf_processor = st.session_state.input_pdf_processor
            try:
                cleanData=""
                downloaded_pdf_file = requests.get(input_pdf_link)
                if downloaded_pdf_file.status_code == 200:
                    content_type = downloaded_pdf_file.headers.get("Content-Type")
                    if 'application/pdf' in content_type.lower():
                        
                        if input_pdf_processor == "Nougat":

                            if nougatAPIServerURL!='':
                            
                                #Record Start time
                                start_time = time.time()

                                nougatAPIHeaders = {
                                    "Accept":"application/json"
                                }
                                nougatAPIInputPDF = {'file':downloaded_pdf_file.content}

                                st.success("Sending the PDF at '{}' for processing using '{}' processor!".format(input_pdf_link, input_pdf_processor), icon='✅')
                                processedPdfData = requests.post(nougatAPIServerURL + "/predict", headers=nougatAPIHeaders, files=nougatAPIInputPDF)
                                
                                if processedPdfData.status_code == 200:
                                    #preprocess rules for creating mmd file
                                    #1. Unstrigify -> One header label
                                    #2. \n\n -> Actual newline character * 2
                                    #3. \n -> Actual newline character * 1
                                    #4. \\ -> \

                                    cleanData = processedPdfData.content[1:-1].decode().replace(r"\n\n",'\n\n').replace(r"\n",'\n').replace('\\\\', '\\')

                                    outputFileName = get_output_filename("Nougat")

                                    # Record the end time
                                    end_time = time.time()

                                    st.success("Processing complete!".format(input_pdf_link, input_pdf_processor), icon='✅')
                                elif processedPdfData.status_code == 404:
                                    e = RuntimeError("Connection to Nougat API Server lost! Check if the server is active or if the URL is correct")
                                    st.exception(e)
                                else:
                                    e = RuntimeError(str(processedPdfData.status_code) + " - " + processedPdfData.reason + "got from the API server")
                                    st.exception(e)
                                    
                                
                                # Calculate and display the processing time
                                if cleanData:
                                    processing_time = end_time - start_time
                                    st.subheader("Processing Time:")
                                    st.write(f"Time taken: {processing_time:.2f} seconds")
                                    st.download_button(label="Download the Processed File", data=cleanData, file_name=outputFileName)

                            else:
                                st.error("Empty Link: Please enter the URL to Nougat API Server", icon='❗️')

                        elif input_pdf_processor == "PyPDF":
                            
                            st.success("Sending the PDF at '{}' for processing using '{}' processor!".format(input_pdf_link, input_pdf_processor), icon='✅')
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
                        e = RuntimeError("File not in pdf format")
                        st.exception(e)
                else:
                    e = RuntimeError("File couldn't be found")
                    st.exception(e)
            except Exception as e:
                raise e

        
        else:
            st.error("Invalid Link: Please check your link {Input format : <http | https>://<server-location>.pdf</>}", icon='❗️')
    else:
        if input_pdf_link == "":
            st.error("Empty Link: Please enter a link to pdf in the textbox", icon='❗️')



