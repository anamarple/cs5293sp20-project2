# CS 5293, Spring 2020 Project 2

###### The Summarizer

###### Ana Marple

## Intro
-----------
This program allows the user to summarize a subset of academic documents from Kaggle's COVID-19 Open Research Dataset Challenge (CORD-19) (https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge). In a nutshell, this program randomly picks 500 .json files, extracts the meaningful information, clusters the documents using k-means clustering, summarizes each document in each cluster using the text rank (tr) method (latent semantic analysis (lsa) is another option, but for final results the tr method was used), and the summarizations for each cluster are written to a file in the ```output/``` subfolder.

#### Installation
----------------
1. Install the package
```bash
pip install project2
```
2. Go into the shell
```bash
pipenv shell
```
3. Make sure neccessary packages are downloaded
```bash
python setup.py install
```
Note: Python 3.7 was used in the making of this program.

## Folder Structure
----------------------
Below is the tree structure for this project. The main module is main.py, which contains all of the neccessary functions. Many documents in the ```docs/``` subfolder were removed in the tree to save space.

```
├── COLLABORATORS
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── build
│   ├── bdist.linux-x86_64
│   └── lib
│       └── project2
│           ├── __init__.py
│           └── main.py
├── dist
│   └── project2-1.0-py3.7.egg
├── docs
│   ├── 001259ae6d9bfa9376894f61aa6b6c5f18be2177.json
│   ├── ee3cc22161595e877450737882a52950fd179672.json
│   ├── eef61bdfa49b8652fd660b5b8b7e74cf51922505.json
	...
	...	
	...
│   ├── ef586c7c8fe46545e4d236ad74818063b1ac0c10.json
│   ├── efd27ff0ac04dd60838266386aaebb5df80f4fa9.json
│   ├── f06dde80e1f11939bb7306853ca92a8c9382ede4.json
├── output
│   ├── SUMMARY.md
│   ├── cluster_0_lsa.md
│   ├── cluster_10_tr.md
│   ├── cluster_12_tr.md
│   ├── cluster_13_tr.md
│   ├── cluster_14_tr.md
│   ├── cluster_1_lsa.md
│   ├── cluster_1_tr.md
│   ├── cluster_2_tr.md
│   ├── cluster_3_tr.md
│   ├── cluster_4_tr.md
│   ├── cluster_5_tr.md
│   ├── cluster_6_tr.md
│   ├── cluster_7_tr.md
│   ├── cluster_8_tr.md
│   └── cluster_9_tr.md
├── project2
│   ├── __init__.py
│   └── main.py
├── project2.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── requirements.txt
├── setup.cfg
├── setup.py
└── tests
    ├── test_cluster.py
    ├── test_file_reader.py
    ├── test_summarize.py
    └── test_write_summary.py
```

A subset of the .json files in the ```docs/``` folder were used to create and test the program. After reading all documents, the summarizations for each cluster were written in the ```output/``` subfolder with the following naming convention: cluster_clusterNo_method.md where the options for method are tr, lsa, and test (created when running pytest). The 'best' summarization result was renamed to SUMMARY.md.

#### Usage
------------
The command used to execute the program was:
```bash
	pipenv run python project2/main.py 
```

## Tasks
-------------------

### 1. Look at the format of the file
I had a difficult time being able to 'prepare about 5000 documents' without storing the files in my github version control. I first tried to use the Jupyter notebook provided by Kaggle to generate a list of all of the names of the files so that my function could randomly pick 5000 names from that list, and then from that list randomly pick 10% of the files to download (500 total) using the Kaggle command line API. I don't know if it was a security issue, but the list of document names I had retrived were not 'found' in the kaggle dataset. Thus, I resorted to downloading as many files as I could on my githib version initially (about 27k out of the 45k) and using the function I talk about next to randomly pick 500 files to keep, and delete the rest.

### 2. Choose documents
The doc_chooser() function obtains 500 (10% of 5000) documents randomly from the documents mentioned above, and the rest were delete. This function only needed to be ran once at the beginning of the project, and the call to this function has been commented out accordingly. Documents that were picked were moved to the ```docs/``` subfolder.

### 3. Write a files reader
The file_reader() function takes the location and glob of the files to read. After browsing through the format of the .json files on Kaggle's website, I decided the only relevant information to store for each file would be the text, and to ignore all of the references information, etc. Ideally, the text information to download would be from the Abstract section, since that is a summary of the document itself. However, not all documents had a non-empty Abstract section. This file_reader function goes through each .json file, check if it has a non-empty abstract and if so adds the text of the Abstract. If the Abstract section is empty, the text from the Body Text section is added instead. The text sections for each section were all merged together before being added to a dataframe as 'text.' The 'paper_id' of the document was stored in the dataframe as well.

### 4. Cluster Documents
The k-means clustering method was used to cluster the documents. The cluster() function took in the dataframe mentioned in the previous section. Then, the 'text' part was vectorized using sklearn's CountVectorizer and preprocessed by removing all stop words. There is a commented out section in the function that determines the optimal number of clusters by using the 'elbow method' and computing the silhouette coefficient. The 'elbow method' levels out starting at the optimal number of clusters, and the silhouette coefficient represents the distance between neighboring clusters. After comparing values and considering the time it takes to compare the values, *the optimal number of clusters was found to be 14, and 2 for testing. The user must change the number of clusters in the code after viewing the numbers from the elbow method and silhouette score!!!*

### 5. Summarize document clusters
There are two functions that could be used to summarize the documents. The first (and one used to generate the final results seen in output/SUMMARY.md) was text rank (tr). The summarize_tr() function took in the dataframe and number of clusters generated from the previous task and tokenized each document by sentence using nltk's sent_tokenize. Each tokenized sentence was then vectorized using CountVectorizer, and used to build a document-term frequency matrix and then similarity matrix. Using networkx's pagerank method, the scores of each sentence were calulated and ranked. The top 4 sentences of each document (top 1 if the length of the document was less than 4 sentences itself) were used to summarize that document. The second method was latent semantic analysis (lsa) had the same process as the tr method up to the building a document-term frequency matrix part. Then, scipy's svds method was used instead to get the sentence weights per topic and rank them. Due to more time being available to invest in the first method, I chose the tr method to summarize the documents.


### 6. Write summarized clusters to a file
The write_summary() function takes in the dataframe mentioned in the previous section, the number of clusters, and the method used. The summarizations for each cluster were written in the ```output/``` subfolder with the following naming convention: cluster_clusterNo_method.md where the options for method are tr, lsa, and test (created when running pytest). The 'best' summarization result was renamed to SUMMARY.md.

## Testing
------------
There are five tests to diagnose the program, all located in the ```tests/``` folder. There is a 'test_cluster.py' to test that the documents were categorized into different clusters. The 'test_write_summary.py' makes sure that an output file was properly created and with the right naming convention. The 'test_summarize.py' contains two tests that tests each summarization method (tr and lsa). The 'test_file_reader.py' tests that it correctly reads in files and creates the initial dataframe populated by the 'text' and 'paper_id' data from the documents.

Command to run pytest:
```bash pytest -p no:warnings -s```


#### References
------
https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge#json_schema.txt
'Text Analytics with Python' book by Dipanjan Sarkar
# cs5293sp20-project2
