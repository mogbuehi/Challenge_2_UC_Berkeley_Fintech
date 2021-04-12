# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
from pathlib import Path
import csv


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath) as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Came with starter code, Skip the CSV Header: 
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
        
    return data

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