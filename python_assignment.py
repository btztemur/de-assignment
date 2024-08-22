import pandas as pd
from datetime import  timedelta
import json

    
# method for evaluating number of loans for the last 180 days
def claims_last_180_days(contracts, application_date):
    # if there are not contracts, returns -3
    if pd.isna(contracts):
        return -3
    # parses json
    parsed = json.loads(contracts)
    count = 0
    # evaluating date which was 180 ago before application date
    cutoff_date = application_date - timedelta(days=180)
    # checks if contracts  were list of json objects or signle object
    if isinstance(parsed,list):
        # if it was list, it works with for loop
        for claim in parsed:
            claim_date = pd.to_datetime(claim.get('claim_date', None), format='%d.%m.%Y', errors='coerce')
            if pd.notna(claim_date) and claim_date > cutoff_date:
                count += 1
    else:
        # otherwise with dict
        claim_date = pd.to_datetime(parsed.get('claim_date', None), format='%d.%m.%Y', errors='coerce')
        if pd.notna(claim_date) and claim_date > cutoff_date:
            count += 1
    return count

# method  for evaluating sum of exposue of loans without TBC loans
def sum_exposure_without_tbc_loans(contracts):
    # list of banks for exclusion
    excluded_banks = ['LIZ', 'LOM', 'MKO', 'SUG', None]
    # if there are no contracts, returns -3
    if pd.isna(contracts):
        return -3
    parsed = json.loads(contracts)
    total_exposure = 0
    # checks if contracts  were list of json objects or signle object
    if isinstance(parsed,list):
        # if it was list, it works with for loop
        for claim in parsed:
            # checks the condition for feature, whether it has bank keyword, not inexcluded banks, whether contract_date is not none
            if 'bank' in claim and claim['bank'] not in excluded_banks and claim.get('contract_date', None):
                loan_summa = claim.get('loan_summa', 0)
                # parsing logic
                if isinstance(loan_summa, (int, float)):
                    total_exposure += int(loan_summa)
                elif isinstance(loan_summa, str) and loan_summa.isdigit():
                    total_exposure += int(loan_summa)
                else:
                    total_exposure += 0  
    else:
        # otherwise with dict
        # checks the condition
        if 'bank' in parsed and parsed['bank'] not in excluded_banks and parsed.get('contract_date', None):
                loan_summa = parsed.get('loan_summa', 0)
                # parsing logic
                if isinstance(loan_summa, (int, float)):
                    total_exposure += int(loan_summa)
                elif isinstance(loan_summa, str) and loan_summa.isdigit():
                    total_exposure += int(loan_summa)
                else:
                    total_exposure += 0  
    if total_exposure!=0:
        return total_exposure
    else:
        # if total exposure is equal to 0, returns -1
        return -1

# method for calculating days from the last loan
def days_since_last_loan(contracts, application_date):
    if pd.isna(contracts):
        return -3
    loans = json.loads(contracts)
    # space for getting last loan date
    last_loan_date = None
    if isinstance(loans,list):
        for loan in loans:
            # checks whether  summa and contract_date are not null 
            if pd.notna(loan.get('summa', None)) and loan.get('contract_date', None):
                loan_date = pd.to_datetime(loan['contract_date'], format='%d.%m.%Y', errors='coerce')
                if last_loan_date is None or (loan_date > last_loan_date):
                    last_loan_date = loan_date
    else:
        # performs the same logic for single json object
        if pd.notna(loans.get('summa', None)) and loans.get('contract_date', None):
                loan_date = pd.to_datetime(loans['contract_date'], format='%d.%m.%Y', errors='coerce')
                if last_loan_date is None or (loan_date > last_loan_date):
                    last_loan_date = loan_date
    if last_loan_date is not None:
        return (application_date - last_loan_date).days
    # returns -1 if no loans at all
    return -1

df = pd.read_csv('data_copy.csv')
# converting application date int date_time, so it would be easy to work with days
df["application_date"] = pd.to_datetime(df["application_date"], errors='coerce')
df["application_date"] = df["application_date"].dt.tz_localize(None)

# applying methods on columns
df["tot_claim_cnt_l180d"] = df.apply(lambda x: claims_last_180_days(x['contracts'], x['application_date']), axis=1)
df['exposure_without_tbc'] = df['contracts'].apply(sum_exposure_without_tbc_loans)
df['day_sinlastloan'] = df.apply(lambda x: days_since_last_loan(x['contracts'], x['application_date']), axis=1)


df.to_csv('contract_features.csv', index=False)