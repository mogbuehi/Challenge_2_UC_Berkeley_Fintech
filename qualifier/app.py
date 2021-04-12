"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

"""
import csv
import sys
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def save_csv(csv_string, data_dict_or_list):
    """ 
    Args: `csv_string` is a string object that contains the .csv file name you wish to save the data as. `data_dict_or_list`
    is an iterable (list or string) that will be written to the .cvs file. 
    """
    csvpath = Path(csv_string)
    with open (csvpath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data_dict_or_list:
            csvwriter.writerow(row)
    return csvwriter


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    
    print(f"Found {len(bank_data_filtered)} qualifying loans")
    
    print(bank_data_filtered)
    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!
    save_prompt = questionary.confirm(""" Would you like to save your data? 
       Note that if neither yes or no is selected, data will be saved by default""").ask()
    if save_prompt:
        file_name = questionary.text('Provide the file name you would like to save as (with .csv suffix)').ask()
        save_csv (file_name, qualifying_loans)
    

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_csv('data/daily_rate_sheet.csv')
    

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )
    # Add a header to qualifying loans data (list of lists)
    header = ['Lender', 'Max Loan', 'Max LTV', 'Max DTI', 'Min Credit', 'Interest Rate']
    qualifying_loans.insert(0, header)

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)

