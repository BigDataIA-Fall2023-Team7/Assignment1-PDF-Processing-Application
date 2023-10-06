import pandas as pd
import os
import time
import boto3
import io
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()


class aws_config:
    def __init__(self):
        try:
            self.s3client = boto3.client('s3',
                region_name='us-east-1',
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
            )
            filename = "file"  # You should define 'file' variable somewhere
            s3_key = f"uploaded_data/file_layout.xlsx"
            s3_response = self.s3client.get_object(Bucket=os.environ.get('BUCKET_NAME'), Key=s3_key)
            content = s3_response['Body'].read()

            self.org_columns = []
            self.monthly_columns = []

            # Columns for origination dataset
            org_df = pd.read_excel(io.BytesIO(content), sheet_name=0)
            metadata_df = org_df.copy()  # Copy the DataFrame
            metadata_df.columns = metadata_df.iloc[0]
            metadata_df = metadata_df[1:]
            self.org_columns = metadata_df["ATTRIBUTE NAME"].tolist()

            # Columns for monthly dataset
            monthly_df = pd.read_excel(io.BytesIO(content), sheet_name=1)
            metadata_df = monthly_df.copy()  # Copy the DataFrame
            metadata_df.columns = metadata_df.iloc[0]
            metadata_df = metadata_df[1:]
            self.monthly_columns = metadata_df["ATTRIBUTE NAME"].tolist()
        except Exception as e:
            # Handle the exception here, you can log the error or take appropriate action.
            print(f"An error occurred: {str(e)}")

    def save_data(self,uploaded_file, type):
        current_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        filename = current_timestamp+'_'+uploaded_file.name
        s3_key = f"uploaded_data/{type}/{filename}"

        if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(uploaded_file)
        else:
            last_dot_csv_index = filename.rfind(".csv")
            if last_dot_csv_index != -1:
            # Replace ".csv" with ".xlsx"
                new_file_name = filename[:last_dot_csv_index] + ".xlsx"
            df = pd.read_csv(uploaded_file)

        if type == "Origination Data":
            df.columns = self.org_columns
            # date_columns = ['First Payment Date', 'Maturity Date']
            # for col in date_columns:
            #     df[col] = pd.to_datetime(df[col], errors = 'coerce', format="%Y%m")
            #     df[col] = df[col].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isna(x) else None)
        else:
            df.columns = self.monthly_columns
            # date_columns = ['Monthly Reporting Period', 'Defect Settlement Date', 'Zero Balance Effective Date', 'Due Date of Last Paid Installment (DDLPI)']
            # for col in date_columns:
            #     df[col] = pd.to_datetime(df[col], errors = 'coerce', format="%Y%m")
            #     df[col] = df[col].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isna(x) else None)

        output_stream = io.BytesIO()
        with pd.ExcelWriter(output_stream, engine="openpyxl", mode="xlsx") as writer:
            df.to_excel(writer, index=False)

        output_stream.seek(0)
        self.s3client.upload_fileobj(output_stream,os.environ.get('BUCKET_NAME'), s3_key)
        
        # s3_response = self.s3client.get_object(Bucket=os.environ.get('BUCKET_NAME'), Key = s3_key)
        # content =  s3_response['Body'].read()

        # if filename.endswith('.csv'):
        #     df = pd.read_csv(io.BytesIO(content))
        # elif filename.endswith(('.xls', '.xlsx')):
        #     df = pd.read_excel(io.BytesIO(content))
        # else:
        #     df = pd.DataFrame()

        if type == "Origination Data":
            # df.columns = self.org_columns
            date_columns = ['First Payment Date', 'Maturity Date']
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors = 'coerce', format="%Y%m")
                df[col] = df[col].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isna(x) else None)
        else:
            # df.columns = self.monthly_columns
            date_columns = ['Monthly Reporting Period', 'Defect Settlement Date', 'Zero Balance Effective Date', 'Due Date of Last Paid Installment (DDLPI)']
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors = 'coerce', format="%Y%m")
                df[col] = df[col].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isna(x) else None)
        return df 

    def save_report(self,report_html,data_type, report_type):
        output = []

        current_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        filename = 'report_'+current_timestamp+'.html'
        s3_key = f"reports/{data_type}/{report_type}/{filename}"
        self.s3client.put_object(Bucket=os.environ.get('BUCKET_NAME'), Key=s3_key, Body = report_html)

        return s3_key



