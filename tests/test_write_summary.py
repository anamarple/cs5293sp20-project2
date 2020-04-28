from project2 import main
import os

loc = 'docs/'
fileNames = '*5.json' #test on .json files that end in 5

#Tests write_summary function
def test_write_summary():

    text = main.file_reader(loc, fileNames)
    (clustered_text, clusters) = main.cluster(text)
    (summary, clusters) = main.summarize_tr(clustered_text, clusters)
    main.write_summary(summary, clusters, 'test')

    assert(os.path.exists('output/cluster_0_test.md'))
