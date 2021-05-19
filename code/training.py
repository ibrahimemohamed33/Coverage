import os
import sys

import pandas as pd
import colorful as cf

from manual import AdjustClassification

# for nice formatting
cf.use_style('monokai')
class Train:
    '''
    Runs anvio and shell commands to manually classify the data
    '''
    def __init__(self, directory, coverage_values_file, classified_values_file,
                tree_file, title, override=False, export=True):

        self.directory = directory
        self.coverage_values_file = coverage_values_file
        self.classified_values_file = classified_values_file
        self.tree_file = tree_file
        self.train = True

        self.adjusted_dataframe_and_classification(title, override=override, export=export)


    def is_tree_file_OK(self):
        '''
        determines if the user has a tree file to perform the hierarchal 
        clustering
        '''
        if not os.path.exists(os.path.join(self.directory, self.tree_file)):
            raise FileNotFoundError(
                """You did not go through the anvio interface to create a newick
                tree format. If you did, then you probably did not name your 
                tree_file parameter the same name as '%s', which can be a 
                problem. Worst case scenario, you restart the process and look
                at the necessary documentation at INSERT_LINK to create the 
                newick tree
                """
                %(self.tree_file)
            )
    
    def run_anvi_newick_matrix(self):
        '''
        Checks whether the environment contains anvio and if it does, it would
        run important commands on the shell that will load up the dendrogram
        necessary for manually classifying and training the data
        '''
        environment = os.getenv('CONDA_DEFAULT_ENV')
        os.chdir(self.directory)

        if 'anvio' not in environment: 
            raise EnvironmentError(
                """ Your default environment '%s' is not related to anvio and
                thus makes it difficult to perform this algorithm. To install
                anvio, please refer to the site:

                https://merenlab.org/2016/06/26/installation-v2/
                """
                %(environment)
            )
            sys.exit()
            
        os.system("clear")
        print(cf.blue("Now running Anvio's matrix-to-newick command...\n"))
        os.system(
            """ anvi-matrix-to-newick %s \
                         -o %s
            """
			%(self.coverage_values_file, self.tree_file)
	    ) 

        print("""Finished! If you look at thme directory %s, your tree file will appear as '%s'"""
            %(self.directory, self.tree_file))

    def launch_anvi_interactive(self, title, override):
        '''
        Launches anvio's interactive's dendrogram
        '''
        if override:
            self.tree_file = 'tree.txt'

        string = """ anvi-interactive -d %s \
                    -p asdf.db \
                    --title '%s' \
                    --tree %s \
                    --manual
                """ %(self.coverage_values_file, title, self.tree_file)

        os.system(string)

    def adjusted_dataframe_and_classification(self, title, override, export):
        '''
        Adjusts training data so that the coverage values are clustered, 
        using anvio clustering algorithm, and the dataframe is sorted 
        Overall, this eases the process of manually inputting the data.
        This is, however, only useful for inputting training data into the model.
        '''
        self.run_anvi_newick_matrix()
        self.is_tree_file_OK()

        self.F = AdjustClassification(tree_file=self.tree_file,
                                    directory=self.directory,
                                    coverage_values_file=self.coverage_values_file,
                                    classified_values_file=self.classified_values_file)
    
        self.dataframe = self.F.dataframe.reindex(self.F.genes)
        self.dataframe['Classification'] = 0
        self.dataframe.to_csv(self.coverage_values_file, sep='\t')
        
        print(cf.green("""Now we will open up the excel file so you can input the 
            classified values \n\n\n"""))

        print(cf.green("Opening up '%s' on an Excel spreadsheet\n" %(self.coverage_values_file)))
        path_to_excel = '/Applications/Microsoft Excel.app'
        path_to_file = os.path.join(self.directory, self.coverage_values_file)
        string = "open -a '%s' '%s'" %(path_to_excel, path_to_file)
        os.system(string)

        print(cf.blue("""Now launching anvi-interactive. When you are done
        manually classifying the data, make sure to press CTRL + C to exit
        out. If the data is already classified, simply press CTRL + C\n"""))

        self.launch_anvi_interactive(title, override)

        print(cf.green("""Finished! By now, you must have a column
        in your Excel spreadsheet labeled 'Classification' and manually
        inputted the classifying data for each gene. """))

        if export:
            self.export_classifier()
            
    def export_classifier(self):
        '''
        Adjusts the classification values after user manually inputs it.
        It's very important to run this function AFTER you input the classification
        variables and save the file.
        '''

        self.F.export_classifier(self.classified_values_file)
        self.convert_data()

    def convert_data(self):
        '''
        Using the sorted data and manually classified values, this adjusts the
        data before it is used to train the model.
        '''
        if self.train:
            self.adjusted_dataframe_and_classification()

        if self.classified_values_dataframe is not None:
            self.classified_values = self.classified_values_dataframe.to_numpy()