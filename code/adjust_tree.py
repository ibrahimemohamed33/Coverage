import os
import re

special_newick_characters = r'[(),]+([^;:]+)\b'


class Tree:
    '''
    Instantiates the Tree class which returns the genes that have undergone
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