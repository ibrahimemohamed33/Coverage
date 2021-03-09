import os 
import uuid

from shutil import move 

class FileManage:
    def __init__(self, directory, folder='folder'):

        self.file_name = str(uuid.uuid4()) + '.csv'
        self.home = os.path.expanduser('~')
        self.directory = directory
        self.folder = folder + '/'
        self.path = self.create_folder(directory, folder)


    def create_folder(self, directory, folder):
        os.chdir(self.home)
        if '~' in directory:
            directory = directory.replace('~', self.home)

        directory = directory.replace(self.home + '/', '')
        new_path = os.path.join(directory, folder)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)

        print("Your new directory '%s' was successfully created :)" %(new_path))
        return new_path

    def move_file(self): 
        move(self.file_name, self.path)

