import os 
import pandas as pd
import numpy as np

def join_file(__file__): # Make sure file is a string
    return os.path.join(r'~/Coverage/data/12_SUMMARY/bin_by_bin/ALL_SPLITS', __file__)

df = pd.read_csv(join_file('ALL_SPLITS-gene_non_outlier_coverages.txt'), sep = '\t').set_index('gene_callers_id')
df_sigma = pd.read_csv(join_file('ALL_SPLITS-gene_non_outlier_coverage_stds.txt'), sep = '\t').set_index('gene_callers_id')

df.to_csv('Coverage.csv')
df_sigma.to_csv('Coverage_Sigma.csv')
