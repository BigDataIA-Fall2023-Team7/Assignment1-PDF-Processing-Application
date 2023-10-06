# Assignment1-PDF-Processing-Application

## Abstract 📝
Streamlit application that processes PDFs either via Nougat or PyPDF python libraries. The objective of is to analyze and compare Nougat and PyPDF based on various use cases and different input PDFs.

## Team Members 👥
- Aditya Kawale
  - NUID
  - Email
- Nidhi Singh
  - NUID 002925684
  - Email singh.nidhi1@northeastern.edu
- Uddhav Zambare
  - NUID
  - Email

---
## Links 📎
* 📕 Codelab Doc - [link](https://codelabs-preview.appspot.com/?file_id=)
* 📊 Streamlit Application for PDF Processing - [link]()
* 📊 Streamlit Application for Data Profiling - [link]()
* 📕 Colab Notebook - [link]()
* 📊 Input Data - [link](https://www.sec.gov/forms)
* 📊 Output Data - [link]()
* 🔧 Tools Used - [link]()

---
## Architecture 👷🏻‍♂️

### For PDF Processing
![alt text](img/pdf_processing_flow_(colored).png)

1. User gives Http/Https PDF link to Streamlit App on Streamlit Cloud
2. Streamlit Cloud App downloads the pdf on its own storage and validates if it is truly a pdf file
3. If the check passes, it checks the PDF Processor.
4. If the PDF Processor is PyPDF it processes the PDF on Streamlit Cloud itself
5. If the PDF Processor is Nougat it sends the downloaded PDF to Ngrok Agent which is accessible via public internet
6. Once the Ngrok Agent gets the request, it forwards it to Google Colab ngrok service
7.  Ngrok service forwards the request to Nougat API running on port 8503
8. Nougat API processes the PDF and returns the MMD file via HTTP to streamlit application
9. User downloads MMD files from Streamlit

### For Data Profiling
![alt text]()

---

## Source Code References 💻

1. Branch: **streamlit-pdf-processing** - [link]()
2. Branch: **streamlit-great-expectations** - [link]()

---


## Individual Contribution ⚖️

| **Developer** 	|          **Deliverables**          	|
|:-------------:	|:----------------------------------:	|
|      Aditya      	| Streamlit Component 1              	|
|      Nidhi      	| FastAPI Endpoint - Feeds           	|
|      Uddhav      	| Technical Documentation            	|
                       	|


## Undertaking 👮🏻‍♂️

> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

**Contribution**: 🤝
*   Aditya &ensp; &emsp;: `%`
*   Nidhi : `%`
*   Nidhi : `%`
