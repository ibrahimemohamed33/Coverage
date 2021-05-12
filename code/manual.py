import os
import re
import pandas as pd


class ExtractGenes:
    '''
    Instantiates the ExtractGenes class which returns the genes that have undergone
    the hierarchical clustering in anvio. This class ease the task of manually
    classifying genes.
    '''
    def __init__(self, directory, tree_file):
        self.file = tree_file
        self.directory = os.path.abspath(os.path.join(directory, self.file))
    
    def extract_genes(self):
        '''
        extracts the genes from the newick tree format and returns them as a 
        clean list
        '''
        special_newick_characters = r'[(),]+([^;:]+)\b'

        formatted_tree = str(
            open(self.directory).readlines()
            )
        
        res = re.findall(
            special_newick_characters, formatted_tree
        )

        gene_list = [x for x in res if x != '0']
        return gene_list

    def return_index(self, gene):
        '''
        returns the index of a specific gene within the clustered list
        '''
        return self.extract_tree_elements().index(gene)

    def extract_list_of_genes(self, gene1, gene2):
        '''
        returns the list of genes between gene 1 and gene 2. This is helpful
        when having to manually classify a large cluster of genes that share
        similar properties
        '''
        gene_list = self.extract_tree_elements()

        gene1_index = self.return_index(gene1)
        gene2_index = self.return_index(gene2)

        adjusted_list = gene_list[gene1_index: gene2_index + 1]
        
        return adjusted_list


class AdjustDataframe:
    '''
    Instantiates the AdjustDataframe class which sorts the dataframe in the
    .txt file for manual classification. 
    '''
    def __init__(self, tree_file, directory, coverage_values_file=None):

        self.tree = ExtractGenes(directory=directory, tree_file=tree_file)
        self.coverage_values_file = os.path.join(directory, coverage_values_file)
        self.dataframe = pd.read_csv(self.coverage_values_file, sep='\t').set_index('gene_callers_id')

        self.genes = self.tree.extract_genes()
        self.adjust(coverage_values_file)
    
    def adjust(self, coverage_values_file):
        self.dataframe = self.dataframe.reindex(self.genes)
        self.dataframe.to_csv(
           self.coverage_values_file, sep='\t'
        )

