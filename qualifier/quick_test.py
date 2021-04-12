import csv
from pathlib import Path


def save_csv(csv_string, data_dict_or_list):
    """ 
    Args: `csv_string` is a string object that contains the .csv file name you wish to save the data as. `data_dict_or_list`
    is an iterable (list or string) that will be written to the .cvs file. 
    """
    csvpath = Path(csv_string)
    with open (csvpath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data_dict_or_list:
            csvwriter.writerow(row.values())
    return csvwriter
test_data = [{'hi': [1, 2, 3]}]

save_csv('test.csv', test_data)