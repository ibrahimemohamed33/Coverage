import numpy as np
import pandas as pd

class Values:
    def __init__(self):
        '''
        Initializes the Values class to store all possible coverage values for 
        core and accessory genes.  
        '''
        
        self.core_values = np.array([])
        self.accessory_values = np.array([])


    def add(self, gene_class, lst):
        '''
        Appends the core and accessory coverage values

        Inputs:
            gene_class (str): the gene's classification
            lst (list): list of coverage values for a specific classified gene
        '''
        if gene_class == 'Core':
            self.core_values = np.append(self.core_values, lst)
        else:
            self.accessory_values = np.append(self.accessory_values, lst)


class Probability:
    def __init__(self, columns, core_file=None, dataframe=None):
        '''
        Initializes the Probability class

        Inputs:
            columns (int): number of columns
            core_file (str): file containing the index of core genes
            dataframe (dataframe): dataframe containing a gene's coverage values

        '''

        if core_file is not None and dataframe is not None:
            self.core = [int(x.strip()) for x in open(core_file).readlines()]
            self.accessory = [x for x in dataframe.index if x not in self.core]
            self.core_dataframe = dataframe[dataframe.index.isin(self.core)]
            self.accessory_dataframe = dataframe[dataframe.index.isin(self.accessory)]
        
        self.gene_class = np.random.choice(
            ['Core', 'Accessory'], size=1, p=[0.54, 0.46]
            )[0]
        self.all_values = Values()
        self.values = self.return_values(columns, core_file, dataframe)
        self.all_values.add(self.gene_class, self.values)


    def generate_values(self, core_file=None, dataframe=None):
        '''
        Generates the random coverage values depending on the gene's class

        Inputs:
            core_file (str): file containing the index of core genes
            dataframe (dataframe): dataframe containing a gene's coverage values

        '''

        if core_file is not None and dataframe is not None:
            core_values = self.core_dataframe.values.flatten()
            accessory_values = self.accessory_dataframe.values.flatten()
            self.all_values.add("Core", core_values)
            self.all_values.add("Accessory", accessory_values)
            alpha = core_values if self.gene_class == 'Core' else accessory_values
        else:
            alpha = None

        all_core_values = self.all_values.core_values
        all_accessory_values = self.all_values.accessory_values
        beta = all_core_values if self.gene_class == 'Core' else all_accessory_values
        
        return alpha, beta


    def return_values(self, columns,  core_file=None, dataframe=None):
        '''
        Returns the generated coverage values

        Inputs:
            columns (int): number of columns
            core_file (str): file containing the index of core genes
            dataframe (dataframe): dataframe containing a gene's coverage values

        '''

        alpha, beta = self.generate_values(core_file, dataframe)

        if (dataframe is None and core_file is None) and (len(beta) == 0):
            p = np.random.choice(a=beta, size=columns)
        else:
            p = np.random.choice(a=alpha, size=columns)

        return p 
