# -*- coding: utf-8 -*-
import json
import csv

__author__ = 'donnalley'


# FUNCTIONS FOR EXPORTING DATA #####################
def write_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as myCSVFile:
            csv_writer = csv.writer(myCSVFile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            for row in data:
                csv_writer.writerow(row)
    except IOError:
        print("I/O error")
    return


def write_json(data, output_file):
    try:
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=True)
    except IOError:
        print("I/O error")
    return


###################################################

# FUNCTIONS FOR IMPORTING DATA ####################
def open_json(input_file):
    with open(input_file, 'r') as infile:
        input_data = json.load(infile)
    return input_data

###################################################
