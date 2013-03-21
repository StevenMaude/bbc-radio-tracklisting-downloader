## bbc_radio_tracklisting_downloader.py
A Python script that downloads radio tracklistings from BBC's website and outputs to a text file.
Licensed under GPL v3 (see COPYING).
***
### Usage examples
Run bbc_tracklist.py from the command line. The required argument is the BBC programme id, the 8 characters that are found at the end of iPlayer URLs such as:`http://www.bbc.co.uk/iplayer/episode/<programme id>/<programme name>` or programme information URLs such as: `http://www.bbc.co.uk/programmes/<programme id>`. The output is a text file named `<pid>.txt` of the format:

`Programme title`    
`Programme broadcast date`    
  
`Artist`  
`Title`  
`Record label`  
`***`
***
### Dependencies and issues
* Tested on Python 2.7.3 on Windows (Windows 7 64-bit) and Linux (Raspbian).
* Requires [BeautifulSoup 4.1.3](http://www.crummy.com/software/BeautifulSoup/)
* Handling of po:SpeechSegment and po:short_synopsis sections needs testing.
