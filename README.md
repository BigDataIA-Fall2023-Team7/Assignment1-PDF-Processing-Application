# Freddie Mac Single Family Dataset Quality Evaluation Tool

## Objective
The objective of this project is to build a tool that allows users to evaluate the quality of the Freddie Mac Single Family dataset. Users can upload a CSV or XLS file containing either Origination or Monthly performance data and assess whether it adheres to the published schema. The tool will use Pandas Profiling to summarize the data and display the results to the user. Additionally, it will run Great Expectations to perform data quality checks, including schema validation, data validity, absence of missing data, and other custom tests.

## Team Members
- Uddhav Zambare
- Aditya Kawale
- Nidhi Singh

## Links
- [Freddie Mac Single Family Dataset](https://www.freddiemac.com/research/datasets/sf_singlefamily.html)
- [Great Expectations](https://greatexpectations.io/)
- [Pandas Profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/)
- [Streamlit](https://streamlit.io/)
- [Amazon S3](https://aws.amazon.com/s3/)

## Architecture Diagram
![Architecture Diagram](insert_diagram_link_here)

## How to Run the Project
To run the project, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```
   cd project-directory
   ```

3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required dependencies from the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file with the necessary environment variables, such as AWS credentials.

6. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

7. Access the tool through your web browser at `http://localhost:8501`.

## Undertaking
By using this tool, we aim to simplify the process of evaluating the quality of Freddie Mac Single Family dataset files. The tool leverages the power of Pandas Profiling and Great Expectations to provide comprehensive data analysis and validation reports to ensure data quality and adherence to the schema. This project will help data engineers and analysts assess and trust the data they work with, ultimately improving data-driven decision-making processes.

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or contribute to this project. Your feedback is valuable in enhancing the tool's functionality and usability.