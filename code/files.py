import os 
import uuid

class ConvertPath:
    def __init__(self, path, file, create_folder=True, file_included_in_directory=False):
        '''
        Initializes the ConvertPath Class that will be helpful in navigating
        directories and files
        '''
        self.home = os.path.expanduser('~')
        self.relative_path = path
        self.is_path_OK(self.relative_path, create_folder)
        self.absolute_path = os.path.abspath(path)
        self.extract_file(file, file_included_in_directory)
    
    def is_path_OK(self, path, create_folder):
        self.is_home_directory_OK(path)
        if path is None or not create_folder:
            #stores files in /generated_scripts directory
            self.relative_path = '../generated_scripts'

        converted_path = self.convert_directory(path)
        if not os.path.isdir(os.path.abspath(converted_path)):
            D = lambda string, string1: os.path.join(string, string1)
            raise FileNotFoundError(
                """Unfortunately, the path '%s' you inputted is not a valid path
                name, at least within the directory '%s'. This means
                that your new path '%s' does not exist, nor does the absolute path
                %s exists. You should probably change the way you configure your
                path and that may do the trick
                """
                %(path, os.getcwd(), os.path.abspath(path), D(os.getcwd(), path))
            )

    def is_home_directory_OK(self, path):
        D = lambda string, string1: os.path.join(string, string1)
        converted_path = self.convert_directory(path)
        if not os.path.isdir(converted_path):
            raise FileNotFoundError(
            """
            Unfortunately, the absolute path '%s' you inputted is not a valid path
            name, at least within the directory '%s'. This means
            that your new path '%s' does not exist, nor does the absolute path
            '%s' exists. You should probably change the way you configure your
            path and that may do the trick
            """
            %(path, os.getcwd(), converted_path, D(os.getcwd(), converted_path))
        )
        
    def convert_directory(self, path):
        if path[-1] != '/':
            path += '/'

        if '~' in path:
            path = path.replace('~/', '')

        if self.home in path:
            path = path.replace(self.home + '/', '')

        os.chdir(self.home)
        return os.path.abspath(path)
            

    def extract_file(self, file, file_included_in_directory):
        if file_included_in_directory:
            self.file = os.path.split(self.absolute_path)[-1]
            self.folder_path = os.path.split(self.absolute_path)[-2]
        else:
            self.file = file
            self.folder_path = self.absolute_path
 

class FileManage:
    def __init__(self, 
                destination, 
                create_folder=False,
                folder='folder'):
        '''
        Initializes the FileManage class. This is generally used when creating
        and storing the mock data needed to train the classifying algorithm

        Inputs:
            destination (str): the destination to move and manage files
            folder (str): name of folder
            own_file (bool): whether the user should use their own file
            create_folder (bool): whether the file should create a folder to 
                                  store the data
        '''

        self.folder = folder + '/'

        # generates unique name for the coverage and classifier file
        self.coverage_values_file_name = self.generate_unique_name('.txt')
        # self.classified_values_file_name = self.layer_string()


        self.convert_file = ConvertPath(
                path=destination, file=self.coverage_values_file_name, create_folder=create_folder
            )
        # self.convert_additional = ConvertPath(
        #         path=destination, file=self.classified_values_file_name, create_folder=create_folder
        #     )

        self.home_directory = self.convert_file.home
        self.destination = self.convert_file.absolute_path
        self.path = self.make_folder(destination=self.destination, folder=self.folder)


    def generate_unique_name(self, file_extension):
        return str(uuid.uuid4()) + file_extension

    def layer_string(self):
        return 'classified_' +  self.coverage_values_file_name.replace('.csv', '.txt')


    def make_folder(self, destination, folder):
        '''
        Creates and moves folder into preferred destination
        '''
        
        new_path = os.path.join(destination, folder)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
            print(
                "Your new directory '%s' was created succesfully :)"
                 %(new_path)
            )
        else:
            print(
                """Your directory '%s' already exists but don't worry, the files
                will still be placed within it""" 
                %(new_path)
            )

        return new_path
