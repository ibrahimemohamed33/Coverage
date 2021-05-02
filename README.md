# Metagenome-Centric Algorithm

This project is still a work in progress yet an introduction is necessary.

  

## Goal of the Project

A central problem in analyzing an environment’s sample of metagenomes is understanding a specific gene’s abundance and importance within a sample without relying on unreliable heuristics. One common yet effective approach would be to see if the gene’s coverage values surpass a benchmark that is found in other identified genes. For example, a microbiologist could use a heatmap and determine a gene’s abundance or role from the patterns in coverage values.  

Unfortunately, this method is susceptible to protean variables that can potentially undermine some of the intrinsic structure. A machine learning, metgenome-centric classification algorithm that leverages the available data on what is "core" or not is an immediate solution to this problem. With _Anvi'o_, there is an established infrastructure with advanced visualization and analytical resources. In addition to these rich tools, _Anvi’o_ already utilizes a hierarchical clustering algorithm that leverages a newick-tree format, and in a general sense, clusters related genes. Therefore, the algorithm should primarily focus on the gene’s data, as well as use anvio’s resources to organize and cluster the data.

Ideally, the algorithm should approximate a function that relies on a few inputs and outputs a single string. The outputs are still subject to debate because contemporary research has not yet established the proper labels for classifying a gene; however, the inputs should consist of the gene and its associated coverage values. The name, or even gene itself, is superfluous to the algorithm’s design, since the function attempts to classify the gene based on its coverage values.

  

This algorithm should return key classifiers that categorize the gene as "core," "variable," "absent," or "non-specific." Moreover, the coverage values within a metagenome (as opposed to a gene) should be properly normalized so a sample’s read counts are not misrepresented.






Throughout the rest of this outline, we'll use an example dataset which has already been classified by Evan Kiefl *et al.* A link to the *.txt* file is attached in the directory `./Data/classified_values.txt` but will be attached as a separate [link](https://www.dropbox.com/s/xlws1vxys2fngcz/classified_values.txt?dl=0).

  

## Brief Demonstration of the Code

  
There are multiple aspects to the code below that involves managing files; generating mock data that approximates real-world, metagenomic data; and implementing an IsoMap embedding onto lower dimensions to account for the wide diversity of datasets. Throughout the README, I will demonstrate some examples of how one should utilize these functions in a way that is conducive to training and testing the metagenome-centric classifier algorithm. It is important to stress from the outset, however, that this project is a work in progress. Thus, some of the functionality or goals have not come to fruition.



### Generating Mock Data and Managing Files

First, it is necessary to go to the directory "code" and import the necessary python modules. 
```bash
cd ./code; ipython3
```

```python
from mock_training_data import MockData
from coverage import Coverage
```

For users who only want to use the class <code>Coverage</code> , you can skip this part but for those who want to understand how the Mock Data is generated, keep reading. First, we instantiate the <code> MockData </code> class as shown below:
```python
mock = MockData(
folder_name='New_Folder', 
directory= os.path.abspath('../generated_scripts/'), 
create_folder=True, 
rows=1000, 
columns=1000
)     
mock.generate_data(index='gene_callers_id')
```
A quick note is that I chose to place <code>mock</code> within the absolute path of my folder <code>generated_scripts</code> because it's the easiest to deal with in terms of file management. For those who will run these scripts, I strongly recommend you input the absolute path of where you want to place the generated mock data.

The parameters that govern MockData relate to where and how the data should be generated. The parameter <code>folder_name</code> relates to the name of the new folder for the mock data. If the folder already exists within your directory, then the function will still generate the new data; this little parameter was added for those who like to separate the mock data with the real data. Similarly, the parameters <code>directory</code> and <code>create_folder</code> relate to where the new folder should be placed, and whether the user wants to create a folder. 

The parameters <code>rows</code> and <code>columns</code> relate to the number of genes and metagenome samples within the dataset, respectively. When calling on <code>mock.generate_data()</code>, we see the mock data in action. 
![image1](/images/image1.png) 

Moreover, the mock data is classified based on the method used by Evan Kiefl *et al.* with "1" and "0" representing a core and accessory gene, respectively. However, after some time this algorithm, after manually classifying and training more data through *anvi'o*, should supplant Evan's approach. 

The importance of generating mock data relates to the overall need of training data to properly manage and build a classifier algorithm. While the mock data isn't expected to fully encapsulate the wide range of complexity within biological systems, it should somewhat approximate it. 

### Utilizing the Coverage Class

It is important not only to generate the mock data and prepare it for both *anvi'o* and the algorithm, but it's also important to consider the cases where a user has their own data. Moreover, the mock data is rather messy and needs some cleaning before we can utilize *anvi'o*'s remarkable capabilities.

We import the necessary module within the directory <code>Coverage/code</code> and instantiate it with the necessary parameters. The function can take on two types of datasets: mock and real, configured data.


### Mock Data
For those interested in generating mock data using the <code>Coverage</code> class, then we input the commands below. It's important to set the value <code>mock</code> to <code>True</code> and <code>train</code> as true. This is because the mock data, as mentioned before, is primarily used to train and not test the data. Moreover, the <code>Coverage</code>  class leverages the <code>MockData</code> class in doing so.
```python
from coverage import Coverage as C
m = Coverage(
directory=os.path.abspath('../generated_scripts', 
folder_name='Another_Folder',
mock=True, 
create_folder=True, 
rows=400, 
columns=100
)
```

From here, we have two *.txt* files in our newly generated folder "Another_folder," as shown below:
![image2](/images/image2.png) 

Now, we can input these files into *anvi'o* and determine whether the mock data approximates expected data from real-life datasets. For more information on anvio, please see the [link](https://merenlab.org/tutorials/infant-gut/) attached.

When inputting these files, we see the following dendrogram below:
![image3](/images/image3.png) 

The lines in the outer layer of the dendrogram is an attempt at classifying the mock data using bagging and other aggregating techniques on data manually classified by Evan's team. 

### Real Data
Here, we'll be working with real life training data and the wonders the `Coverage` class can do in preparing the larger, classifier algorithm. When inputting the following lines of code:
```python
from coverage import Coverage as C
directory='../data/classified_values.txt'

m = C(
directory=directory,
separator='\t',
mock=False, 
coverage_values_file='classified_values.txt',
file_included_in_directory=True,
export_file=True, 
create_folder=False
)
```
This prepares the dataset for anvio, which, in turn, leads to the following dendrogram:
![image4](/images/image4.png)

TO BE CONTINUED