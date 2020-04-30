class ExperimentError(Exception):
    def __init__(self, arg):
        names = arg
        self.strerror = ("\nError1 type experiment folder error] at : " +
                         names[0] + "\n " +
                         "\ndoes not respect the naming convention for a "
                         "subject directory,"
                         "which is (exp-NAME) Check for "
                         "structural/naming issues")
class SubError(Exception):
    def __init__(self, arg):
        names = arg
        self.strerror = ("\nError 2 type [Subject folder error] at : " +
                         names[1] +
                         "\n \ndoes not respect the naming convention for a"
                         " subject directory,"
                         " which is (sub-GUID) Check for structural"
                         "/naming issues")


class SessionError(Exception):
    def __init__(self, arg):
        names = arg
        self.strerror = ("\nError 3 type [Date folder error] at : " +
                         names[2] + "\n" +
                         "\nIt does not respect the naming convention for "
                         "a session directory,"
                         
                         "which is (yymmdd_xxx_a_bbbb_cccc,) with : "+ "\n"+
                         
                         "yymmdd is the date in the format year, month, date (6 digits, for instance 200430 for April 30, 2020)"+ "\n\n"+
                         
                         "xxx is the number of the session acquired on that date (3 digits, for instance 001 for the first session)"+ "\n\n"+
                         
                         "a is a single letter that designate the species (m for ???, o for ???, r for ???, s for ???)"+ "\n\n"+
                         
                         "bbbb is a string containing the user friendly identifier (UFID) of the animal"+ "\n\n"+
                         
                         "cccc is a string of which the use is to be decided by the research group / user "+"\n\n"+
                         
                         "(for instance to add extra info on the version of the experimental protocol, on the type of preparation etc.)"+ "\n")
class SourceError(Exception):
    def __init__(self, arg):
        names = arg
        self.strerror = ("\nError 4 type [Source folder error] at : " +
                         names[3] + "\n " +
                         "\ndoes not respect the naming convention for a "
                         "subject directory,"
                         "which is (source) Check for "
                         "structural/naming issues")
        
class SourceNotFound(Exception):
    def __init__(self, arg):
        names = arg
        self.strerror = ("\nError 5 type [Source folder error] at : " 
                         "Folder source not found")
                         

