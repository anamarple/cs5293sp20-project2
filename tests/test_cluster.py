from project2 import main
  
loc = 'docs/'
fileNames = '*5.json' #test on .json files that end in 5

#Tests cluster() function
def test_cluster():

    text = main.file_reader(loc, fileNames)

    (clustered_text, clusters) = main.cluster(text)
    
    assert(clusters >= 2)                         
