import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mock_training import MockData

class Coverage:
    def __init__(self, directory, f='Untitled.csv', index='gene_callers_id', 
                 norm=True, sort=False, filter=0, separator=None, mock=False,
                 folder_name='folder', rows=100, columns=100):
        '''
        Initializes the Coverage class

        Inputs:
            directory (str): the desired directory of your data
            f (str): the name of the file
            norm (bool): if values within a metagenome sample should be 
            normalized, where the norm is defined as 
                            a_i/(\sum \limits_{j = 1}^n a_j)

            index (str): the preferred column name to index
        '''

        if not (type(directory) == type(f)) and isinstance(norm, bool):
            raise Exception("""Directory, index, and file need to be a string
                                and norm should be boolean value""")
        
        self.norm = norm
        self.sort = sort

        if mock:
            self.mock = MockData(directory=directory, rows=rows, 
                                 columns=columns, folder_name=folder_name)

            self.mock.generate_data(index)
            self.folder = folder_name
            self.file = self.mock.file
            self.directory = self.mock.directory

        else:
            self.file = f
            self.directory = directory
        
        self.dataframe = self.load_dataframe(index, separator,mock=mock)
        self.filtered_sample = self.filter_samples(filter)
        self.export()

    def load_dataframe(self, index, _sep, mock=False):
        '''
        Loads the dataframe and includes coverage values of genes within samples
        Inputs:
            index (str): the preferred column that indexes the dataframe
        '''
        
        path = os.path.join(self.directory, self.file)
        df = pd.read_csv(path, sep=_sep).set_index(index)
        if self.norm:
            df = df/df.sum()
        if self.sort:
            df = df.sort_values(by=list(df.columns),axis=0) 
        return df
    

    def filter_samples(self, filter=0):
        '''
        Filters samples in a pandas dataframe based on filter value

        Input:
            filter (float): preferred filter value
            output (bool): whether the filtered dataframe should be outputted
        '''

        df = self.dataframe
        criteria = (df.median() >= filter)
        return df[criteria.index[criteria]]


    def export(self):
        '''
        Exports the dataframe into a .txt file for anvi'o

        Inputs:
            export_directory (str): desired directory

        '''

        name = self.file.replace('.csv', '.txt')
        t = self.dataframe.transpose()
        t.columns = 'gene_' + t.columns.astype(str)
        df = t.transpose()
        df.to_csv(os.path.join(self.directory, name), sep='\t')


    def plot_values(self, x_axis, metagenome, kind, labels, color):
        '''
        Plots the dataframe's coverage values using seaborn

        Inputs:
            x_axis (str): the parameter to compare the gene's coverage values. This 
                          is typically the gene's id or name        
            metagenome (str): the name of the metagenome to plot
            kind (scatter, line): type of plot
            labels (tuple): the title of the x-axis, y-axis, and overall title
            color (str): preferred color of the plot

        Output:
            a relational plot

        '''

        x_label, y_label, title = labels
        x_start = self.dataframe.iloc[:1].index[0]
        x_end = self.dataframe.iloc[:1].index[-1]

        plot = sns.relplot(x=x_axis, y=metagenome, data=self.dataframe, kind=kind,
                    color=color)

        plot.set(xlim = (x_start, x_end)).set_axis_labels(x_label, y_label)
        plt.title(title)
    

    def create_heatmap(self, size=(5,5), cmap='RdYlGn', interval=(0.0002, 0.002)):
        '''
        Uses seaborn to create and plot a heatmap 

        Input:
            size (tuple): size of heatmap
            cmap (string): color scale
            interval (tuple): the vmin and vmax values
        Output:
            seaborn heatmap
        '''

        minimum, maximum = interval
        length, width = size
        fig = plt.gcf()
        fig.set_size_inches(length, width)

        sns.heatmap(data=self.dataframe, vmax=maximum, vmin=minimum, 
                    cmap=cmap).invert_yaxis()

