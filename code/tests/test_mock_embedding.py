import os 
import sys 

sys.path.insert(0,'../')

import dimension



# Tests local variables
n_neighbors = 10
directory = os.path.abspath('../../data/test_data')
mock = True
path = 'D'
file_name = 'classified_values.txt'
index = 'gene_callers_id'
create_folder = True
folder_name = 'folder'
tree_file = 'tree.txt'
train=True


separator = None
norm = True
rows = 1000
columns = 120



new_data = dimension.Embedding(n_neighbors=n_neighbors, 
                                mock=mock,
                                create_folder=create_folder,
                                directory=directory, 
                                path=path,
                                train=train,
                                file_name=file_name,
                                tree_file=tree_file)

print("Below is the embedded_dataframe\n")
print(new_data.embedded_dataframe)

print("Your coverage values file\n")
print(new_data.coverage_values_file)

print(
    """Your classified values file. Since you indicated this is your training
    data, you will need to manually classify the values within this file\n"""
    )
print(new_data.classified_values_file)


