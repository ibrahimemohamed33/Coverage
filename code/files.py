import os 
import uuid

from shutil import move 

class FileManage:
    def __init__(self, 
                destination, 
                is_create_folder=False,
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

        self.destination = destination
        self.folder = folder + '/'

        self.working_directory = os.getcwd()
        self.home = os.path.expanduser('~')
        self.file_name = self.generate_unique_name('.txt')
        self.additional_layer = self.additional_layer_string()

        self.path = self.create_folder(destination=destination, 
                                       folder=self.folder, 
                                       is_create_folder=is_create_folder)


    def generate_unique_name(self, file_extension):
        '''
        Generates a unique name for the mockdata file

        Input:
            file_extension (str): the preferred file extension (e.g. .txt, .csv)
        '''
        return str(uuid.uuid4()) + file_extension


    def additional_layer_string(self):
        '''
        Creates the name for the additional layer file
        '''
        return 'additional_layer_' + self.file_name.replace('.csv', '.txt')


    def create_folder(self, destination, folder, is_create_folder):
        '''
        Creates and moves the folder into preferred destination

        Inputs:
            destination (str): destination to manage and move files
            folder (str): name of folder
        '''

        os.chdir(self.working_directory)
        if not is_create_folder:
            os.chdir('../')
            destination = 'generated_scripts/'
        else:
            os.chdir(self.home)
            rho = lambda string: destination.replace(string, '')
            destination = rho('~/') if '~' in destination else rho(self.home + '/')

        new_path = os.path.join(destination, folder)

        if not os.path.isdir(new_path):
            os.mkdir(new_path)
            print("Your new directory '%s' was created succesfully :)" %(new_path))
        
        else:
            print("Your directory '%s' already exists but don't worry, the files"
                " will still be placed within it" %(new_path))
        return new_path


    def move_file(self): 
        '''
        Moves the file into directory
        '''

        move(self.file_name, self.path)
        move(self.additional_layer, self.path)
