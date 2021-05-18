import sys
sys.path.insert(0,'../')

import os
import coverage

epsilon = coverage.epsilon

n_neighbors = 10
directory = os.path.abspath('../../data/test_data')
mock = False
path = 'auto'
file_name='classified_values.txt'
index='gene_callers_id' #your index should almost always be the gene_callers_id
separator=None
_filter = epsilon
export_file = True
tree_file = 'tree.txt'
norm=True

# unnecessary if you are never working with mock data
create_folder = False
folder_name = 'folder'
rows = 100
columns = 100

import dimension

m = dimension.Embedding(n_neighbors=n_neighbors,
                        directory=directory,
                        separator=separator,
                        mock=mock,
                        file_name=file_name,
                        create_folder=create_folder,
                        export_file=export_file,
                        folder_name=folder_name,
                        norm=norm,
                        _filter=_filter,
                        rows=rows,
                        columns=columns)

import training

coverage_values_file = m.embedded_coverage_values_file
directory = m.directory
classified_values_file = m.embedded_classified_values_file
tree_file = 'tree.txt'
title = 'Practice Run'

t = training.Train(directory=directory, 
                    coverage_values_file=coverage_values_file,
                    classified_values_file=classified_values_file,
                    tree_file=tree_file,
                    title=title)

