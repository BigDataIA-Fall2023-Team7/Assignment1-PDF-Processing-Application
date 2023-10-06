import os
import pandas as pd
import great_expectations as gx 
import time
from great_expectations.data_context import FileDataContext

class gx_monthly_data:
    def __init__(self, data):
        current_timestamp = time.time()
        self.asset_name = "Monthly_Asset"+"_"+str(current_timestamp)
        self.datasource_name = "Monthly_Datasource"+"_"+str(current_timestamp)
        self.expectation_suite_name = "Monthly_Suite"+"_"+str(current_timestamp)

        self.context = gx.get_context()
        self.datasource = self.context.sources.add_pandas(name=self.datasource_name)
        self.data_asset = self.datasource.add_dataframe_asset(name=self.asset_name)
        self.my_batch_request = self.data_asset.build_batch_request(dataframe=data)
        self.context.add_or_update_expectation_suite(self.expectation_suite_name)
        self.validator = self.context.get_validator(
            batch_request=self.my_batch_request,
            expectation_suite_name=self.expectation_suite_name)

    

    def validate(self):
        mon_columns = ['Loan Sequence Number', 'Monthly Reporting Period', 'Current Actual UPB', 'Current Loan Delinquency Status', 'Loan Age', 'Remaining Months to Legal Maturity', 'Defect Settlement Date', 'Modification Flag', 'Zero Balance Code', 'Zero Balance Effective Date', 'Current Interest Rate', 'Current Deferred UPB', 'Due Date of Last Paid Installment (DDLPI)', 'MI Recoveries', 'Net Sales Proceeds', 'Non MI Recoveries', 'Expenses', 'Legal Costs', 'Maintenance and Preservation Costs', 'Taxes and Insurance', 'Miscellaneous Expenses', 'Actual Loss Calculation', 'Modification Cost', 'Step Modification Flag', 'Deferred Payment Plan', 'Estimated Loan-to-Value (ELTV)', 'Zero Balance Removal UPB', 'Delinquent Accrued Interest', 'Delinquency Due to Disaster', 'Borrower Assistance Status Code', 'Current Month Modification Cost', 'Interest Bearing UPB']

        self.validator.expect_table_column_count_to_equal(32)
        self.validator.expect_table_columns_to_match_ordered_list(mon_columns)

        column_name="Loan Sequence Number"


        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(F|A)\d{2}Q[1-4]\d{7}$")
        self.validator.expect_column_values_to_be_of_type(column_name,"str")
        self.validator.expect_column_value_lengths_to_equal(column_name,12)

        column_name = "Monthly Reporting Period"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(?:19|20)\d{2}(0[1-9]|1[0-2])$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name, 6)

        column_name = "Current Actual UPB"
        self.validator.expect_column_values_to_match_regex(column_name, "^\d{1,5}|\d{1,4}\.\d|\d{1,3}\.\d{2}$") 

        column_name = "Current Deferred UPB"
        self.validator.expect_column_values_to_match_regex(column_name, "^\d{1,5}|\d{1,4}\.\d|\d{1,3}\.\d{2}$") 

        column_name = "Modification Cost"
        self.validator.expect_column_values_to_match_regex(column_name, "^\d{1,5}|\d{1,4}\.\d|\d{1,3}\.\d{2}$") 

        column_name = "Zero Balance Removal UPB"
        self.validator.expect_column_values_to_match_regex(column_name, "^\d{1,5}|\d{1,4}\.\d|\d{1,3}\.\d{2}$") 

        column_name = "Current Month Modification Cost"
        self.validator.expect_column_values_to_match_regex(column_name, "^\d{1,5}|\d{1,4}\.\d|\d{1,3}\.\d{2}$") 

        column_name = "Interest Bearing UPB"
        self.validator.expect_column_values_to_match_regex(column_name, "^\d{1,5}|\d{1,4}\.\d|\d{1,3}\.\d{2}$") 


        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_MON_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name = "Current Loan Delinquency Status"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,3)


        column_name = "Current Loan Delinquency Status"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,3)


        column_name = "Remaining Months to Legal Maturity"


        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,3)

        column_name = "Defect Settlement Date"

        self.validator.expect_column_values_to_match_regex(column_name,"^(?:19|20)\d{2}(0[1-9]|1[0-2])$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name, 6)




        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_MON_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name = "Modification Flag"

        valid_values = ["Y","P",""]

        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name = "Deferred Payment Plan"

        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)


        column_name = "Estimated Loan-to-Value (ELTV)"

        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,999)

        column_name = "Zero Balance Code"

        valid_values = [1,2,3,96,9,15,16]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,2)

        column_name = "Zero Balance Effective Date"

        self.validator.expect_column_values_to_match_regex(column_name,"^(?:19|20)\d{2}(0[1-9]|1[0-2])$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name, 6)

        column_name = "Due Date of Last Paid Installment (DDLPI)"

        self.validator.expect_column_values_to_match_regex(column_name,"^(?:19|20)\d{2}(0[1-9]|1[0-2])$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name, 6)

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_MON_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name = "Current Interest Rate"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,6)

        column_name="Delinquency Due to Disaster"

        valid_values = ['Y','']

        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name  = 'Borrower Assistance Status Code'

        valid_values = ['F','R','T']

        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name = "Current Month Modification Cost"

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_MON_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        name = "Monthly_Data_Run@_"+str(current_timestamp)
        checkpoint_result = checkpoint.run(run_name=name)
        self.context.build_data_docs()

        result_string = str(list(checkpoint_result.run_results.keys()))

        path = result_string.replace("ValidationResultIdentifier::", "") 
        filepath = "./gx/uncommitted/validations/" + path[1:-1] + ".json"
        
        return filepath
