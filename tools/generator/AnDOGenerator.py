import pandas as pd
import argparse
import os
import sys

# columns required
COLUMNS = ["experiments_name", "subjects_names",
           "years", "months", "days",
           "sessions_numbers", "comments"
           ]


def create_Struct(csv_file, pathToDir):
    """
    Create structure with csvfile given in argument
    This file must follows format where :

    first row ==> experiments_name,subjects_names,years,mouths,days,sessions_numbers,comments

    Args:
        csv_file ([csv file ]): [Csv file that contains a list of directories to create ]
        pathToDir ([Path to directory]): [Path to directory where the directories will be created]
    """

    dirnames = []
    df = pd.read_csv(csv_file)

    # Formating   months and  days , cannot format years
    df["months"] = df.months.map("{:02}".format)
    df["days"] = df.days.map("{:02}".format)


    header = df.columns.values.tolist()
    # Check is the header contains the right names
    if header != COLUMNS:
        print("Failed : Csv does not have the expected columns please " \
            + " check the documentation at 'https://github.com/INT-NIT/AnDOChecker/tools/' ")
        exit(1)
    if df.isnull().values.any():
        number_of_null_values = df.isnull().sum().sum()
        print("There are " +str(number_of_null_values)+" null values in the cvs file")
        exit(1)
    list_of_information = list()

    for index, row in df.iterrows():

        my_list = [
            row["experiments_name"], row["subjects_names"],
            row["years"], row["months"], row["days"],
            row["sessions_numbers"], row["comments"]
        ]
        list_of_information.append(my_list)

    for _, information in enumerate(list_of_information):

        # Check if digits or not and addapt the string
        if information[5] < 10:
            num_sessions = "_00"+str(information[5])
        else:
            num_sessions = "_0"+str(information[5])
        
        # Check if years format is correct 
        if  len(str(information[2])) < 4 :
            print("Error date format not valid at row "+ str(_))
            exit(1)

        dirnames.append("exp-"+str(information[0])+"/"+"sub-"+str(information[1])+"/"+'ses-'+str(
            information[2])+str(information[3])+str(information[4])+num_sessions+"_"+str(information[6])+"/derivatives")
        dirnames.append("exp-"+str(information[0])+"/"+"sub-"+str(information[1])+"/"+'ses-'+str(
            information[2])+str(information[3])+str(information[4])+num_sessions+"_"+str(information[6])+"/metadata")
        dirnames.append("exp-"+str(information[0])+"/"+"sub-"+str(information[1])+"/"+'ses-'+str(
            information[2])+str(information[3])+str(information[4])+num_sessions+"_"+str(information[6])+"/rawdata")

    for directory in dirnames:

        try:
            # Create the directories is they do not exist
            os.makedirs(pathToDir+str(directory))
        except OSError:
            # Error handling when directory already exists
            print("Creation of the directory %s failed, already exist" % directory)
        else:
            print("Successfully created the directory %s " % directory)


def main():
    """
    usage: AnDO_Creator.py [-h] pathToCsv pathToDir

    positional arguments:
    pathToCsv   Path to your folder
    pathToDir   Path to your csv file

    optional arguments:
    -h, --help  show this help message and exit
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('pathToCsv', help='Path to your folder')
    parser.add_argument('pathToDir', help='Path to your csv file')
   
    # Create two argument groups
    
    args = parser.parse_args()

  
         # Check if directory exists
    if not os.path.isdir(args.pathToDir):
            print('Directory does not exist:', args.pathToDir)
            exit(1)
    create_Struct(args.pathToCsv, args.pathToDir)
    


if __name__ == '__main__':

    main()