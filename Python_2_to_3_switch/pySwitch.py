"""
Package util
---------------
"""
__date__ = "$Date: 2020/11/15 10:51:13CET $"
__author__ = "Shinde Sumit"
__version__ = "$Revision: 1.27 $"
__copyright__ = "Copyright 2020 ,Continental AG"
__maintainer__ = "$Author: Shinde, Sumit (uic07134) $"

import os

class convert_py2_to_py3(object):

    '''

    Example:
       1. -----------------------Convert entire repo-------------------------------
        1. Initialise the class with repo/sandbox path
        2. Use the method switch._py2_to_py3()
           This will convert all the available python files in the repo 2.7 --> 3.x

        2. -----------------------Convert only perticular python script-------------

        In this case just pass the filepath as a list (argument) to switch._py2_to_py3()
        e.g.    switch._py2_to_py3([r"D:\Sandboxes\FRS 2_7\VSC_Validation\sense\frs\base\frs_readers.py"])

    '''

    def __init__(self, directory, overwrite_py2_files=True):
        self.directory=directory
        self.overwrite_py2_files=overwrite_py2_files
        self.check_repo_path()

    def create_py2_to_py3_file(self,*args):

        code = '''import sys\nfrom lib2to3.main import main\nsys.exit(main("lib2to3.fixes"))'''
        with open("2to3.txt", "w") as output:
            output.write(code)
        os.replace(r"2to3.txt", r"2to3.py")

    def get_all_py_files_from_directory(self,*args):
        if self.check_repo_path():
            pyfiles = []
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    if file.endswith('.py'):
                        pyfile=os.path.join(root, file)
                        print (pyfile)
                        pyfiles.append(pyfile)
            if len(pyfiles)==0:
                print ("Given repo/sandbox does not contain any valid python file")
            else:
                print("\n Total no of python files found =", len(pyfiles))
            return  pyfiles

    def _py2_to_py3(self, pyfiles=[],*args):

        self.create_py2_to_py3_file()

        if len(pyfiles)==0:
            pyfiles=self.get_all_py_files_from_directory(self.directory)
        else:
            pyfiles=pyfiles
        if self.overwrite_py2_files:
            for pyfile in pyfiles:
                print (pyfile)
                os.system(r"C:\LegacyApp\Python36\python.exe "+str(os.path.join(os.getcwd(), r'2to3.py')) +str(' -w ')+ str(pyfile))
        else:
            for pyfile in pyfiles:
                os.system(r"C:\LegacyApp\Python36\python.exe "+str(os.path.join(os.getcwd(), r'2to3.py')) +str(' ')+ str(pyfile))

        if os.path.isfile(r"2to3.py") :
            os.remove(r"2to3.py")

    def check_repo_path(self, *args):
        if not os.path.exists(self.directory):
            print ("Given repo/sandbox path is not valid")
            return False
        else:
            return True

if __name__ == "__main__":

    sandbox=r'D:\Sandboxes\trial\VSC_Validation\sense\frs'                      #give_path_of_repo/sandbox

    switch= convert_py2_to_py3(sandbox, overwrite_py2_files=True)               #initialise the class() #overwrite_py2_files to

    get_all_py_files= switch.get_all_py_files_from_directory()                  # optional: get list of all the python files present in the repo/sandbox

    switch._py2_to_py3()                                                        # overwrite py2 files to py3 ()

