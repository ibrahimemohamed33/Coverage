# !/bin/bash -e

source ~/.bash_profile

cd ~/Coverage/code

dir = pwd

echo -n "Welcome! We're going realize the fruits behind these python scripts
         in the context of the metagenome-centric classifier algorithm :)\n\n"


echo -n "Is this be mock or real data? (m/r)"
read MOCK

if [[ $1 -eq "m" ]]
then 

echo -n "Please input a valid number of rows for the mock data \n\n"
read ROWS
export ROWS

echo -n "Please input a valid number of columns for the mock data \n\n"
read COLUMNS
export COLUMNS

echo -n "Please list a valid directory to place the mock data \n\n"
read DIRECTORY
export DIRECTORY


echo -n "Lastly, please input a valid name for the folder you want to 
        store the mock data in \n\n"

read FOLDER
export FOLDER


cat > script.py << 'END_SCRIPT'
    
import os 
from coverage import Coverage as C

ROWS, COLUMNS, DIRECTORY, FOLDER = 'ROWS', 'COLUMNS', 'DIRECTORY', 'FOLDER'


directory = str(os.environ[DIRECTORY])
if directory is None:
    directory = os.path.abspath('../generated_scripts')

rows = int(os.environ[ROWS])
if rows is None:
    rows = 100

columns = int(os.environ[COLUMNS])
if columns is None:
    columns = 100

folder_name = str(os.environ[FOLDER])
if folder_name is None:
    folder_name = 'Practice'

m = C(directory=directory, mock=True, rows=rows, columns=columns, 
coverage_values_file='practice.txt', folder_name=folder_name, export_file=True
)


os.system("export COVERAGE=%s" %m.coverage_values_file)





END_SCRIPT

echo -n "Success! We will now begin running your anvio commands :) \n\n"


else 

    echo -n "Please input a valid directory for the file \n\n"
    read DIRECTORY

    echo -n "Is the file included in the directory? [yes, no]\n\n"
    read FILE_INCLUDED_IN_DIRECTORY

    echo -n "Please input a valid name for the file. If it's included in the
            directory, then simply put the name 'foo.txt' \n\n"
    read FILE

    echo -n "Should we export this file? [yes, no]\n\n"
    read EXPORT
    
    export DIRECTORY, FILE_INCLUDED_IN_DIRECTORY, FILE, EXPORT


cat > script.py << 'END_SCRIPT'

import os
from coverage import Coverage as C


directory = os.environ[DIRECTORY]
if directory is None:
    directory = os.path.abspath('../data/classified_values.txt')

file_included_in_directory = os.environ[FILE_INCLUDED_IN_DIRECTORY]

if file_included_in_directory == 'yes':
    file_included_in_directory = True
else:
    file_included_in_directory = False


coverage_values_file = os.environ[FILE]
if coverage_values_file is None:
    coverage_values_file = 'Untitled.txt'

export_file = os.environ[EXPORT]
if export_file == 'yes':
    export_file = True
else:
    export_file = False



m = C(
directory=directory,
separator='\t',
mock=False, 
coverage_values_file=coverage_values_file,
file_included_in_directory=file_included_in_directory,
export_file=export_file, 
create_folder=False
)

output1 = print(m.coverage_values_file)
output2 = print(m.classified_values_file_name)
    
END_SCRIPT
fi

cd $DIRECTORY


# outputString=`python script.py arg1 arg2 | tail -0`
rm script.py


anvi-matrix-to-newick $COVERAGE \
                         -o tree.txt


anvi-interactive -d $COVERAGE \
                    -p asdf.db \
                    --title "Practice Run" \
                    --tree tree.txt \
                    --manual

cd $dir