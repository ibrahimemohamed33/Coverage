import os
import sys

from manual import AdjustClassification 

class Train:
    '''
    Class is helpful for running and training the data itself
    '''
    def __init__(self, directory, coverage_values_file, 
                classified_values_file, tree_file, title):

        self.directory = directory
        self.coverage_values_file = coverage_values_file
        self.classified_values_file = classified_values_file
        self.tree_file = tree_file

    def is_tree_file_OK(self):
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

        print("Now running Anvio's matrix-to-newick command\n")
        os.system(
            """ anvi-matrix-to-newick %s \
                         -o %s
            """
			%(self.coverage_values_file, self.tree_file)
	    ) 
        print(
            """Finished! If you look at thme directory %s, your tree file will appear as '%s'"""
            %(self.directory, self.tree_file)
        )

    def launch_anvi_interactive(self, title="Practice Run"):
        string = """ anvi-interactive -d %s \
                    -p asdf.db \
                    --title '%s' \
                    --tree %s \
                    --manual
                """ %(self.embedded_coverage_values_file, title, self.tree_file)

        os.system(string)

    def adjusted_dataframe_and_classification(self):
        '''
        Adjusts training data so that the coverage values are clustered, 
        using anvio clustering algorithm, and the dataframe is sorted 
        Overall, this eases the process of manually inputting the data.
        This is, however, only useful for inputting training data into the model.
        '''
        self.run_anvi_newick_matrix()

        if self.train:
            self.is_tree_file_OK()
            self.F = AdjustClassification(
                                    tree_file=self.tree_file, 
                                    directory=self.directory,
                                    coverage_values_file=self.embedded_coverage_values_file,
                                    classified_values_file=self.classified_values_file)
            
            self.embedded_dataframe = self.F.dataframe

            print(
                """Now we will open up the excel file so you can input the 
                classified values \n"""
                )

            print("Opening up the Excel spreadsheet\n")
            path_to_excel = '/Applications/Microsoft Excel.app'
            path_to_file = os.path.join(self.directory, self.embedded_coverage_values_file)
            string = "open -a '%s' '%s'" %(path_to_excel, path_to_file)
            os.system(string)

            print("Now launching anvio-interactive\n")
            self.launch_anvi_interactive()

            print("""
            Finished! When you are done, make sure to execute the command
            export_classifier, as outlined in the documentation file in 
            INSERT_LINK \n
            """)
            
    def export_classifier(self):
        '''
        Adjusts the classification values after user manually inputs it
        '''
        self.F.export_classifier(self.classified_values_file)
        self.convert_data()

    def convert_data(self):
        '''
        Using the sorted data and manually classified values, this adjusts the
        embedded data before it is used to train the model.
        You will need to run this in your ipython shell after instantiating
        the Embedding class. 
        '''
        if self.train:
            self.adjusted_dataframe_and_classification()

        numpy = lambda dataframe: dataframe.to_numpy()
        self.coverage_values = numpy(self.embedded_dataframe)
        if self.classified_values_dataframe is not None:
            self.classified_values = numpy(self.classified_values_dataframe)
    

    