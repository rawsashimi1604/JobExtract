'''
    Module containing all logic related code

    Files:
        cleaner.py:
            Cleaner Module. Contains Cleaner Object, used for cleaning rawData files and export to cleanedData folder.
        crawler.py: 
            Crawler Module. Contains Crawler Object, used for crawling data from sg.linkedin.com
            Requires Google Chrome Web Driver to use.
            Put WebDriver into PATH Environment before using.
        merger.py: 
            Merger Module. Contains Merger Object, used for merging CSV files with identical columns
        counter.py: 
            Counter Module. Contains Counter Object, used for counting keywords in data, and returning a CSV file containg keywords and count
        augmentor.py:
            Augmentor Module. Contains Augmentor Object, augmenting new columns of data, mainly numerical to help with graph analysis.
        processor.py:
            Processor Module. Contains Processor Object, used for processing raw data into processed data.


    Additional Modules:
        models: 
            Module containing all utility models
'''