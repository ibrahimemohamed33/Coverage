import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Coverage:
    def __init__(self, directory, f, index='gene_callers_id', 
                 norm=True, sort=False, filter=0, _sep='\t'):
        '''
        Initializes the Coverage class that is used to ...

        Inputs:
            directory (str): the desired directory of your data
            f (str): the file containing the data
            norm (bool): if values within a metagenome sample should be 
            normalized, where the norm is defined as 
                            a_i/(\sum \limits_{j = 1}^n a_j)

            index (str): the preferred column name to index

        '''

        if not (type(directory) == type(f)) and isinstance(norm, bool):
            raise Exception("""Directory, index, and file need to be a string
                                and norm should be boolean value""")
        
        self.directory = directory
        self.file = f
        self.norm = norm
        self.sort = sort

        self.dataframe = self.load_dataframe(index, _sep)
        self.filtered_sample = self.filter_samples(filter)

    def load_dataframe(self, index, _sep):
        '''
        Loads the dataframe and includes coverage values of genes within samples
        Inputs:
            index (str): the preferred column that indexes the dataframe
        '''
        
        path = os.path.join(self.directory, self.file)
        df = pd.read_csv(path, sep = _sep).set_index(index)
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
        criteria = df.median() >= filter
        return df[criteria.index[criteria]]


    def export(self, name='data.txt'):
        t = self.dataframe.transpose()
        t.columns = 'gene_' + t.columns.astype(str)
        df = t.transpose()
        df.to_csv(name, path_or_buf= self.directory, sep='\t')


    def plot_values(self, x_axis, metagenome, kind, labels, color):
        x_label, y_label, title = labels
        x_start = self.dataframe.iloc[:1].index[0]
        x_end = self.dataframe.iloc[:1].index[-1]

        plot = sns.relplot(x=x_axis, y=metagenome, data=self.dataframe, kind=kind,
                    color=color)

        plot.set(xlim = (x_start, x_end)).set_axis_labels(x_label, y_label)
        plt.title(title)
    

    def create_heatmap(self, size=(5,5), cmap='RdYlGn', interval=(0.0002, 0.002)):
        minimum, maximum = interval
        length, width = size
        fig = plt.gcf()
        fig.set_size_inches(length, width)

        sns.heatmap(data=self.dataframe, vmax=maximum, vmin=minimum, 
                    cmap=cmap).invert_yaxis()

