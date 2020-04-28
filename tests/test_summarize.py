from project2 import main
  
loc = 'docs/'
fileNames = '*5.json' #test on .json files that end in 5


#Tests summarize_tr() function
def test_summarize_tr():    
    
    text = main.file_reader(loc, fileNames)
    (clustered_text, clusters) = main.cluster(text)

    (summary, clusters) = main.summarize_tr(clustered_text, clusters)
    
    assert('Summarized' in summary.columns)


#Tests summarize_lsa() function
def test_summarize_lsa():
    
    text = main.file_reader(loc, fileNames)
    (clustered_text, clusters) = main.cluster(text)
    
    (summary, clusters) = main.summarize_lsa(clustered_text, clusters)

    assert('Summarized' in summary.columns)
