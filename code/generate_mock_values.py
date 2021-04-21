import numpy as np
import pandas as pd
import os

classifiers = ['Core', 'Accessory']
probabilities = [0.54, 0.46]

class Values:
    def __init__(self, drop=False, directory='~/Coverage/data/classified_values.txt'):
        '''
        Initializes the Values class to store all possible coverage values for 
        core and accessory genes.  
        '''
        self.df = self.load_dataframe(directory)
        self.normalize_dataframe()
        self.core_dataframe = self.load_adjusted_dataframes(core=True)
        self.accessory_dataframe = self.load_adjusted_dataframes(core=False)
        if drop:
            self.df, _ = self.drop_classifier()
  

    def load_dataframe(self, directory):
        '''
        Uses pandas to load and read the .csv/.txt file
        '''
        return pd.read_csv(directory, sep='\t').set_index('gene_callers_id')
    
    def load_adjusted_dataframes(self, core=True):
        '''
        Returns the manually classified core or accessory dataframes 
        '''
        # filters the dataframe based on whether an entry is core
        F = lambda n: self.df['Classification'] == n
        filtered = F(1) if core else F(0)
        return self.df[filtered].drop('Classification', axis=1)

    def drop_classifier(self, dataframe=None):
        '''
        Helper function that drops the 'Classification' column
        '''
        if dataframe is None:
            dataframe = self.df
    
        if 'Classification' in dataframe.columns:
            classifiers = dataframe['Classification']
            df = dataframe.drop('Classification', axis=1)

        return df, classifiers

    def normalize_dataframe(self):
        '''
        Normalizes the sample's reads
        '''
        if 'Classification' in self.df.columns:
            dropped, classifiers = self.drop_classifier()
            self.df = dropped/dropped.sum()
            self.df['Classification'] = classifiers
        else:
            self.df = self.df/self.df.sum()


class MockValues:
    def __init__(self, columns):
        '''
        Initializes the MockValues class that generates the new, mock values
        for the MockData class.

        Inputs:
            columns (int): number of columns

        '''
        self.all_values = Values()
        self.core = self.all_values.core_dataframe.to_numpy().flatten()
        self.accessory = self.all_values.accessory_dataframe.to_numpy().flatten()
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

        if self.gene_class == 'Core':
            alpha, beta = self.core, 1
        else:
            alpha, beta = self.accessory, 0
        # Generates random values from core or accessory values
        p = np.random.choice(alpha, size=columns)
        return list(p), beta
