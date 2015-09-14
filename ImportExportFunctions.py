import json
import csv

__author__ = 'donnalley'


# FUNCTIONS FOR EXPORTING DATA #####################
def write_to_txt(data, output_file):
    try:
        with open(output_file, 'w') as outfile:
            for line in data:
                outfile.write(line + '\n')
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


def write_to_csv(data, output_file):
    try:
        with open(output_file, 'wb') as myCSVFile:
            csv_writer = csv.writer(myCSVFile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            for data in data:
                csv_writer.writerow(data)
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


def write_json(data, output_file):
    try:
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=True)
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


###################################################

# FUNCTIONS FOR IMPORTING DATA ####################
def open_json(input_file):
    with open(input_file, 'r') as infile:
        input_data = json.load(infile)
    return input_data

###################################################
