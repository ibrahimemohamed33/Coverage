import os
from test_embedding import new_data


print("Embedded Dataframe before:\n")
print(new_data.embedded_dataframe)
print("Embedded Dataframe After:\n")
new_data.adjusted_dataframe_and_classification()
print(new_data.embedded_dataframe)

path_to_excel = '/Applications/Microsoft Excel.app'
path_to_file = os.path.join(new_data.directory, new_data.embedded_coverage_values_file)
string = "open -a '%s' '%s'" %(path_to_excel, path_to_file)
os.system(string)

