import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Coverage:
    def __init__(self, directory, file, *args):
        '''
        Initializes the Coverage class that is used to ...

        Inputs:
            directory (str): the desired directory of your data
            file (str): the file containing the data
        '''
        self.directory = directory
        self.file = file
        self.args = args


    def load_dataframe(self, index, norm=False, sort=False, output=True):
        '''
        Loads the dataframe and includes coverage values of genes within samples
        Inputs:
            index (str): the preferred column that indexes the dataframe
            norm (bool): if values should be normalized, where the norm is
            defined to be 
                            a_i/(a_1 + ... + a_i + ... + a_n)
            sort (bool): sorts the dataframe by genes with high coverage values
            output (bool): if the function should return the dataframe
        '''
        self.index = index
        try:
            isinstance(self.file, str)
        except:
            form = type(self.file)
            Exception('Your file is a {} and needs to be a string :/'.format(form))

        path = os.path.join(self.directory, self.file)
        df = pd.read_csv(path,sep = '\t').set_index(self.index)
        if norm:
            df = df/df.sum()
        if sort:
            df = df.sort_values(by=list(df.columns),axis=0)
        self.dataframe = df
        if output:
            return self.dataframe
    

    def export(self, name):
        t = self.dataframe.transpose()
        t.columns = 'gene_' + t.columns.astype(str)
        df = t.transpose()
        df.to_csv(name, sep='\t')
    

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

    def filter_samples(self, filter=None):
        df = self.load_dataframe(self.index)
        self.dataframe = df.loc[:, df.median() > filter]




