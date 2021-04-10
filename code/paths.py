import os 
import uuid

from shutil import move 


class FileManage:
    def __init__(self, 
                directory, 
                create_folder=False,
                folder='folder'):
        '''
        Initializes the FileManage class

        Inputs:
            directory (str): directory to manage and move files
            folder (str): name of folder
        '''
        self.directory = directory
        self.folder = folder + '/'
        self.home = os.path.expanduser('~')

        self.file_name = self.generate_unique_name('.csv')
        self.additional_layer = self.layer_string()
        if create_folder:
            self.path = self.create_folder(directory, folder)
    
    def generate_unique_name(self, file_extension):
        '''
        Generates a unique name for the mockdata file

        Input:
            file_extension (str): the preferred file extension (e.g. .txt, .csv)
        '''

        unique_string = str(uuid.uuid4())
        return unique_string + file_extension


    def layer_string(self):
        '''
        Creates the name for the additional layer file
        '''

        p = 'additional_layer_'
        return p + self.file_name.replace('.csv', '.txt')



    def create_folder(self, directory, folder):
        '''
        Creates and moves the folder into preferred directory

        Inputs:
            directory (str): directory to manage and move files
            folder (str): name of folder
        '''

        os.chdir(self.home)
        if '~' in directory:
            directory = directory.replace('~', self.home)
            
        new_path = os.path.join(directory.replace(self.home + '/', ''), folder)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)

        print("Your new directory '%s' was successfully created :)" %(new_path))
        return new_path

    def move_file(self): 
        '''
        Moves the file into directory
        '''

        move(self.file_name, self.path)
        move(self.additional_layer, self.path)
