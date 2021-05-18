import os
import sys
sys.path.insert(0,'../')
import compare



m = compare.Compare(n_neighbors=10, 
                    directory=os.path.abspath('../../data/test_data/'), 
                    mock=False, path='D', 
                    file_name='classified_values.txt', 
                    create_folder=False, 
                    export_file=True, 
                    folder_name='folder', 
                    separator=None, 
                    norm=True, 
                    rows=100, 
                    columns=100, 
                    coverage_tree_file='tree.txt', 
                    embedding_tree_file='tree1.txt')


os.system('source delete.sh')