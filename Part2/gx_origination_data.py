import os
import pandas as pd
import great_expectations as gx 
import time
from great_expectations.data_context import FileDataContext

class gx_origination_data:
    def __init__(self, data):
        current_timestamp = time.time()
        self.asset_name = "Origination_Asset"+"_"+str(current_timestamp)
        self.datasource_name = "Origination_Datasource"+"_"+str(current_timestamp)
        self.expectation_suite_name = "Origination_Suite"+"_"+str(current_timestamp)

        self.context = gx.get_context()
        self.datasource = self.context.sources.add_pandas(name=self.datasource_name)
        self.data_asset = self.datasource.add_dataframe_asset(name=self.asset_name)
        self.my_batch_request = self.data_asset.build_batch_request(dataframe=data)
        self.context.add_or_update_expectation_suite(self.expectation_suite_name)
        self.validator = self.context.get_validator(
            batch_request=self.my_batch_request,
            expectation_suite_name=self.expectation_suite_name)

    

    def validate(self):
        org_columns = ['Credit Score', 'First Payment Date', 'First Time Homebuyer Flag', 'Maturity Date', 'Metropolitan Statistical Area (MSA) Or Metropolitan Division', 'Mortgage Insurance Percentage (MI %)', 'Number of Units', 'Occupancy Status', 'Original Combined Loan-to-Value (CLTV)', 'Original Debt-to-Income (DTI) Ratio', 'Original UPB', 'Original Loan-to-Value (LTV)', 'Original Interest Rate', 'Channel', 'Prepayment Penalty Mortgage (PPM) Flag', 'Amortization Type (Formerly Product Type)', 'Property State', 'Property Type', 'Postal Code', 'Loan Sequence Number', 'Loan Purpose', 'Original Loan Term', 'Number of Borrowers', 'Seller Name', 'Servicer Name', 'Super Conforming Flag', 'Pre-HARP Loan Sequence Number', 'Program Indicator', 'HARP Indicator', 'Property Valuation Method', 'Interest Only (I/O) Indicator', 'Mortgage Insurance Cancellation Indicator']
        # mon_columns = ['Loan Sequence Number', 'Monthly Reporting Period', 'Current Actual UPB', 'Current Loan Delinquency Status', 'Loan Age', 'Remaining Months to Legal Maturity', 'Defect Settlement Date', 'Modification Flag', 'Zero Balance Code', 'Zero Balance Effective Date', 'Current Interest Rate', 'Current Deferred UPB', 'Due Date of Last Paid Installment (DDLPI)', 'MI Recoveries', 'Net Sales Proceeds', 'Non MI Recoveries', 'Expenses', 'Legal Costs', 'Maintenance and Preservation Costs', 'Taxes and Insurance', 'Miscellaneous Expenses', 'Actual Loss Calculation', 'Modification Cost', 'Step Modification Flag', 'Deferred Payment Plan', 'Estimated Loan-to-Value (ELTV)', 'Zero Balance Removal UPB', 'Delinquent Accrued Interest', 'Delinquency Due to Disaster', 'Borrower Assistance Status Code', 'Current Month Modification Cost', 'Interest Bearing UPB']

        self.validator.expect_table_column_count_to_equal(32)
        self.validator.expect_table_columns_to_match_ordered_list(org_columns)

        column_name = "Credit Score"

        column_type = "Numeric"
        column_length = 4

        # Addind expectations for the column
        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(9999|([3-7][0-9][0-9]|8[0-4][0-9]|850))$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')

        column_name = "First Payment Date"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(?:19|20)\d{2}(0[1-9]|1[0-2])$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name, 6)   

        column_name = "First Time Homebuyer Flag"

        valid_values = ["Y","N","9"]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)


        column_name = "Maturity Date"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(?:19|20)\d{2}(0[1-9]|1[0-2])$")
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name, 6)


        column_name = "Metropolitan Statistical Area (MSA) Or Metropolitan Division"

        self.validator.expect_column_values_to_match_regex(column_name, r"^\d{1,5}\.\d{1}$") 

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_OD_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name ="Mortgage Insurance Percentage (MI %)"

        self.validator.expect_column_values_to_match_regex(column_name,"^(0|999|([1-4]\d|5[0-5]))$")
        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,3)

        column_name="Number of Units"

        valid_values = [1,2,3,4,99]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,2)

        column_name="Original Combined Loan-to-Value (CLTV)"


        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_between(column_name,1,999)

        column_name="Original Debt-to-Income (DTI) Ratio"


        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(999|[1-9]|[1-5]\d|6[0-5])$")
        self.validator.expect_column_values_to_be_of_type(column_name,"int")


        column_name="Original UPB"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,12)

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_OD_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name = "Original Interest Rate"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,6)

        column_name="Channel"

        valid_values = ['R','B','C','T','9']

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="Prepayment Penalty Mortgage (PPM) Flag"

        valid_values = ['Y','N']

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="Amortization Type (Formerly Product Type)"

        valid_values = ['FRM','ARM']

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')


        column_name="Property State"

        valid_values = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
            "GU","HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC",
            "SD", "TN", "TX", "UT", "VI", "VT", "VA", "WA", "WV", "WI", "WY"
        ]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,2)

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_OD_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name="Property Type"

        valid_values = ["CO", "PU", "MH", "SF", "CP", "99"]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,2)


        column_name="Postal Code"


        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(0[5]|\d{3}00)$")
        self.validator.expect_column_values_to_be_of_type(column_name,"int")

        column_name="Loan Sequence Number"


        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(F|A)\d{2}Q[1-4]\d{7}$")
        self.validator.expect_column_values_to_be_of_type(column_name,"str")
        self.validator.expect_column_value_lengths_to_equal(column_name,12)


        column_name="Loan Purpose"

        valid_values = ["P", "C", "N", "R","9"]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)



        column_name = "Original Loan Term"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,3)
        self.validator.expect_column_values_to_be_of_type(column_name,"int")


        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_OD_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name = "Number of Borrowers"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_match_regex(column_name,"^(0[1-9]|10|99)$")
        self.validator.expect_column_values_to_be_of_type(column_name,"int")

        column_name = "Seller Name"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,60)
        self.validator.expect_column_values_to_be_of_type(column_name,"str")

        column_name = "Servicer Name"

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_value_lengths_to_be_between(column_name,1,60)
        self.validator.expect_column_values_to_be_of_type(column_name,"str")

        column_name="Super Conforming Flag"

        valid_values = ["Y", ""]

        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="Pre-HARP Loan Sequence Number"

        self.validator.expect_column_values_to_match_regex(column_name,"^(F|A)\d{2}Q[1-4]\d{7}$")
        self.validator.expect_column_values_to_be_of_type(column_name,"str")
        self.validator.expect_column_value_lengths_to_equal(column_name,12)

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_OD_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )

        column_name="Program Indicator"

        valid_values = ["H", "F", "R", "9"]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="HARP Indicator"

        valid_values = ["Y", ""]

        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'float')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="Property Valuation Method"

        valid_values = [1,2,3,4,9]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'int')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="Interest Only (I/O) Indicator"

        valid_values = ["Y", "N"]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_values_to_be_of_type(column_name, 'str')
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        column_name="Mortgage Insurance Cancellation Indicator"

        valid_values = ["Y", "N",7]

        self.validator.expect_column_values_to_not_be_null(column_name)
        self.validator.expect_column_values_to_be_in_set(column_name, valid_values)
        self.validator.expect_column_value_lengths_to_equal(column_name,1)

        self.validator.save_expectation_suite(discard_failed_expectations=False)

        current_timestamp = time.time()
        checkpoint_name = "Checkpoint_OD_COL_"+column_name+"_"+str(current_timestamp)
        checkpoint = self.context.add_or_update_checkpoint(
            name = checkpoint_name,
            validations=[
                {
                    "batch_request": self.my_batch_request,
                    "expectation_suite_name": self.expectation_suite_name,
                },
            ],
        )
        name = "Origin_Data_Run@_"+str(current_timestamp)
        checkpoint_result = checkpoint.run(run_name=name)
        self.context.build_data_docs()

        result_string = str(list(checkpoint_result.run_results.keys()))

        path = result_string.replace("ValidationResultIdentifier::", "") 
        filepath = "./gx/uncommitted/validations/" + path[1:-1] + ".json"

        

        return filepath
