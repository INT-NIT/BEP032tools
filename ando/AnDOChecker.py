import os
import os.path as op
import re
import argparse

from AnDO.ando import rulesStructured as Rs


def is_valid(input_directory):
    """ Checks the ephys-BIDS validity of a data set.

    The specifications that define what is checked by this function is available in the following document:


    Parameters
    ----------
        input_directory : string
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
        currentdepth_rules = Rs.rules_set[depth]
        ###
        # 1. check whether the rules are followed for the folder at this level ("authorized folders")
        #
        ###
        if len(currentdepth_rules['mandatory_folders']) > 0:
            # loop over rules, each rule corresponding to one mandatory folder
            for current_mandatoryfolder_rule in (currentdepth_rules['mandatory_folders']):
                # create the list of regexp
                list_of_mandatory_folders = (
                    get_list_of_rules_with(current_mandatoryfolder_rule))
                for each_file in list_of_mandatory_folders:
                    dir_res = [re.compile(each_file).search(d) is not None for d in dirs]
                    if not any(dir_res):
                        error_list.append(
                            "Mandatory folder not found for this rule : {}".format(current_mandatoryfolder_rule))
        folder = op.split(root)[1]
        folder_res = [re.compile(x).search(folder) is None
                      for x in get_list_of_rules_with(currentdepth_rules['authorized_folders'])]

        # if none of the authorized rules is respected, raise an error
        if all(folder_res):
            error_list.append("Naming rule not respected for this directory : {}".format(root))
        ###
        # 2. check whether rules are followed for files within the folder at this level ("authorized files")
        ###
        for current_file in files:
            file_res = list()
            for rules in currentdepth_rules['authorized_metadata_files']:
                file_res.extend(([re.compile(x).search(current_file) is not None for x in
                                  get_list_of_rules_with(rules, Rs.AUTHORIZED_METADATA_EXTENSIONS)]))

            for rules in currentdepth_rules['authorized_data_files']:
                file_res.extend([re.compile(x).search(current_file) is not None for x in
                                 get_list_of_rules_with(rules, Rs.AUTHORIZED_DATA_EXTENSIONS)])
                # if none of the authorized rules is respected, raise an error

            if not any(file_res):
                error_list.append("Naming rule not respected for this file : {}".format(current_file))
        ###
        # 3. check whether the "mandatory files" are actually present at this level!
        ###
        if len(currentdepth_rules['mandatory_files']) > 0:
            #### ADD generation of regular expressions based on base names and extensions
            # loop over rules, each rule corresponding to one mandatory file
            for current_mandatoryfolder_rule in (currentdepth_rules['mandatory_files']):
                    list_of_mandatory_folders = (get_list_of_rules_with
                                               (current_mandatoryfolder_rule, current_mandatoryfolder_rule[1]))
                    for each_file in list_of_mandatory_folders:
                        file_res = [re.compile(each_file).search(f) is not None for f in files]

                        if any(file_res) == False:
                            error_list.append("Mandatory file not found for this rule : {}".
                                              format(current_mandatoryfolder_rule))

    # if there are no errors, the data set is valid!
    valid = len(error_list) == 0

    return valid, error_list


def get_list_of_rules_with(file_name_regexp, file_ext_regexp=None):
    """
    Function that create rules base on the regexp in rulesStructured.py

    Parameters
    ----------

        file_name_regexp: list
            list of filenames
        file_ext_regexp: list
            list of extensions

    Returns
    -------
        list_of_rules : list
            Concatenate every extension with is respective file

    Examples
    -------
    if :
    file_name_regexp = [
        ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys'],
        ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels'],
        ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_contacts'],
        ]

    and :
    file_ext_regexp = ['.tsv', '.json']

    then :
    list_of_rules = [
        'sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys.tsv',
        'sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys.json',
        'sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels.tsv',
        'sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels.json',
        ]
    """
    list_of_rules = list()
    if file_ext_regexp is None:
        list_of_rules = file_name_regexp
    else:
        if len(file_name_regexp) == 2:
            for filename in file_name_regexp[:-1]:
                for extension in file_ext_regexp:
                    list_of_rules.append(filename + str(extension))
        else:
            for filename in file_name_regexp:
                for extension in file_ext_regexp:
                    list_of_rules.append(filename + str(extension))

    return list_of_rules


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
    dataset_validity, error_list = is_valid(directory)
    if dataset_validity:
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
