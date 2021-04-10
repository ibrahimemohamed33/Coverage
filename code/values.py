import numpy as np
import pandas as pd
import os

classifiers = ['Core', 'Accessory']
probabilities = [0.54, 0.46]

class Values:
    def __init__(self, drop=True, directory=None):
        '''
        Initializes the Values class to store all possible coverage values for 
        core and accessory genes.  
        '''
        if directory is None:
            #Directory that stores the coverage values
            directory = '~/Coverage/code/core.txt'

        self.df = self.load_dataframe(directory)
        self.normalize_dataframe()
        self.core_dataframe = self.load_adjusted_dataframes(core=True)
        self.accessory_dataframe = self.load_adjusted_dataframes(core=False)
        if drop:
            self.df = self.drop_classifier()[0]
  

    def load_dataframe(self, directory):
        return pd.read_csv(directory, sep='\t').set_index('gene_callers_id')
    
    def load_adjusted_dataframes(self, core=True):
        # filters the dataframe based on whether an entry is core
        _filter = (self.df["Core"] == 1) if core else (self.df["Core"] == 0)

        return self.df[_filter].drop("Core", axis=1)

    def drop_classifier(self, dataframe=None):
        if dataframe is None:
            dataframe = self.df
    
        if 'Core' in dataframe.columns:
            core = dataframe["Core"]
            df = dataframe.drop("Core", axis=1)

        return df, core

    def normalize_dataframe(self):
        '''
        Normalizes the sample's reads
        '''
        if 'Core' in self.df.columns:
            dropped, core = self.drop_classifier()
            self.df = dropped/dropped.sum()
            self.df["Core"] = core
        else:
            self.df = self.df/self.df.sum()


class MockValues:
    def __init__(self, columns):
        '''
        Initializes the Probability class

        Inputs:
            columns (int): number of columns

        '''

        self.all_values = Values()
        self.core = self.all_values.core_dataframe
        self.accessory = self.all_values.accessory_dataframe

        self.gene_class = np.random.choice(classifiers, size=1, p=probabilities)[0]
        self.values, self.classifier = self.return_values(columns)


    def return_values(self, columns):
        '''
        Returns randomly generated coverage values based on gene's classification

        Inputs:
            columns (int): number of columns
        Returns:
            randomly generated values, classified variable (lst, int)

        '''

        flattened_core_values = self.core.to_numpy().flatten()
        flattened_accessory_values = self.accessory.to_numpy().flatten()
        
        if self.gene_class == 'Core':
            alpha, beta = flattened_core_values, 1
        else:
            alpha, beta = flattened_accessory_values, 0

        # Generates random values from core or accessory values
        p = np.random.choice(alpha, size=columns)
        return list(p), beta
