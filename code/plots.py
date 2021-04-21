import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from dimension import Embedding
from coverage import Coverage

class Plots:
    def __init__(self, 
                size,
                labels,
                kind,
                directory,
                n_neighbors=5,
                dimension=10,
                rows=100,
                columns=50,
                mock=True,
                embed=False,
                interval=(2e-4, 2e-3),
                color="Blue"):
        '''
        Initializes the Plots class and will be used for graphical depictions
        of coverage values

        Inputs:
            size (tuple): the preferred length and width of heatmap
            labels (tuple): the x and y label, as well as the title
            kind (string): type of plot  ('scatter', 'line')

        '''

        self.x_label, self.y_label, self.title = labels
        self.kind = kind
        self.size = size
        self.interval = interval
        self.color = color

        self.reduced = Embedding(
            n_neighbors=n_neighbors,
            directory=directory,
            path='auto',
            dimension=dimension,
            mock=mock,
            rows=rows,
            columns=columns
        )
        
        if embed:
            self.dataframe = self.reduced.embedded_dataframe
        else:
            self.dataframe = self.reduced.dataframe
        
        self.x_axis = np.array(self.dataframe.index)


    def plot_heatmap(self, cmap = 'RdYlGn'):
        '''
        Plots heatmap using Seaborn

        Inputs:
            size (tuple): the size of the length and width of the heatmap
            cmap (string): the color scale for the heatmap
            interval (tuple): the vmin and vmax 
        Output:
            Seaborn Heatmap
        '''

        height, width = self.size
        vmin, vmax = self.interval
        fig = plt.gcf()
        fig.set_size_inches(height, width)
        
        sns.heatmap(
            data=self.dataframe,
            vmin=vmin,
            vmax=vmax,
            cmap=cmap
        ).invert_yaxis()
    

    def plot_relation(self):
        '''
        Plots metagenome's coverage values using Seaborn

        Inputs:
            kind (string): type of plot  ('scatter', 'line')
            metagenome (int): specific index of metagenome

        '''
        # returns name of the nth gene
        indexed_dataframe = lambda n: self.dataframe.iloc[:1].index[n]
        X_start, X_end = indexed_dataframe(0), indexed_dataframe(-1)
        y_axis = self.dataframe[self.y_label]

        plot = sns.relplot(
            x=self.x_axis,
            y=y_axis,
            data=self.dataframe,
            kind=self.kind,
            color=self.color
        )
                           
        plot.set(xlim=(X_start, X_end)).set_axis_labels(self.x_label, self.y_label)
        plot.fig.subtitle(self.title)   

