import os
import os.path as op
import re
import argparse

from rulesStructured import *



def newchecker(input_directory):
    """ Checks the ephys-BIDS validity of a data set.

    The specifications that define what is checked by this function is available in the following document:


    Parameters
    ----------
        directory : string
            Name of the root directory containing the data set to be checked

    Returns
    -------
        valid : boolean
            True if the data set follows the ephys-BIDS specification; False if not

        error_list : list
            List of errors (empty if the data set is valid)
    """


    error_list = []

    # walk through the directory tree using the os.walk function
    for ind, (root, dirs, files) in enumerate(os.walk(input_directory)):
        # compute depth of the directory given as input
        if ind == 0:
            # remove ending / or \ if the input directory was given with it at the end
            if root.endswith(os.path.sep):
                root = root[:-1]
            # count the number of / or \ in the directory name to estimate its "depth"
            initial_depth = root.count(os.path.sep)
        # estimate at which level we are
        depth = root.count(os.path.sep) - initial_depth
        #print(depth,root,dirs,files)
        ###
        # extract rules for this level!
        ###
        currentdepth_rules = rules_set[depth]
        ###
        # 1. check whether the rules are followed for the folder at this level ("authorized folders")
        ###
        folder = op.split(root)[1]
        folder_res = [re.compile(x).search(folder) is None for x in currentdepth_rules['authorized_folders']]
        # if none of the authorized rules is respected, raise an error
        if all(folder_res):
            error_list.append("Naming rule not respected for this directory : {}".format(root))
        ###
        # 2. check whether rules are followed for files within the folder at this level ("authorized files")
        ###
        for current_file in files:
            #### ADD generation of regular expressions based on base names and extensions
            file_res = [re.compile(x).search(current_file) is None for x in currentdepth_rules['authorized_files']]
            # if none of the authorized rules is respected, raise an error
            if all(file_res):
                error_list.append("Naming rule not respected for this file : {}".format(current_file))
        ###
        # 3. check whether the "mandatory files" are actually present at this level!
        ###
        if len(currentdepth_rules['mandatory_files']) > 0:
            #### ADD generation of regular expressions based on base names and extensions
            # loop over rules, each rule corresponding to one mandatory file
            for current_mandatoryfile_rule in currentdepth_rules['mandatory_files']:
                file_res = [re.compile(current_mandatoryfile_rule).search(f) is None for f in files]
                # if this mandatory file is missing, raise an error
                if all(file_res):
                    error_list.append("Mandatory file not found for this rule : {}".format(current_mandatoryfile_rule))

    # if there are no errors, the data set is valid!
    valid = len(error_list) == 0

    return valid, error_list



def main():

    """
    Main file of the validator. uses other class methods for checking
    different aspects of the directory path.

    usage: checker.py [-h] [-v] path

            positional arguments:
            directory           Name of the directory that contains the data set to be checked

            optional arguments:
            -h, --help     show this help message and exit
            -v, --verbose  increase output verbosity


    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    parser.add_argument('directory', help='Name of the directory to be checked')
    args = parser.parse_args()

    try:
        directory = args.directory
    except IndexError:
        directory = '.'

    if not directory:
        print('Directory does not exist:', directory)
        exit(1)
    dataset_validity, error_list = newchecker(directory)
    if dataset_validity :
        print("Congratulations!\n" +
              directory +
              " respects the ephys-BIDS specifications")
    else:
        print("Attention!\n" +
              directory +
              " does not respect the ephys-BIDS specifications")
        if args.verbose:
            print("\nHere are the errors that have been identified:")
            for error_message in error_list:
                print("  " + error_message)


if __name__ == '__main__':

    main()
