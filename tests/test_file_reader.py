from project2 import main

loc = 'docs/'
fileNames = '*5.json' #test on .json files that end in 5

#Tests file_reader function
def test_file_reader():

    df = main.file_reader(loc, fileNames)
    print(df)

    #assert df is not empty
    assert(len(df) > 0)
