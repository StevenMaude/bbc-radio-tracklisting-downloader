## bbc_radio_tracklisting_downloader.py
A Python script that downloads radio tracklistings from BBC's website and outputs to a text file.
Licensed under GPL v3 (see COPYING).
***
### Usage examples
Run `bbc_tracklist.py` from the command line. The required argument is the BBC programme id, the 8 characters that are found at the end of iPlayer URLs such as:`http://www.bbc.co.uk/iplayer/episode/<programme id>/<programme name>` or programme information URLs such as: `http://www.bbc.co.uk/programmes/<programme id>`. 

Optional arguments are <directory> and <filename>. If either of these are omitted, output will be to the current path.

The output is a text file named `<pid>.txt` of the format:
`Programme title`    
`Programme broadcast date`    
  
`Artist`  
`Title`  
`Record label`  
`***`
***
### get_iplayer usage
If downloading a radio programme with [get_iplayer](http://www.infradead.org/get_iplayer/html/get_iplayer.html), adding an argument of the form `--command "/home/get_iplayer/bbc_tracklist.py <pid> <dir> <fileprefix>" should result in a text file containing the tracklisting in the same directory as your downloaded audio file. (Change /home/get_iplayer to point to wherever the script is located.
***
### Dependencies and issues
* Tested on Python 2.7.3 on Windows (Windows 7 64-bit) and Linux (Raspbian).
* Requires [BeautifulSoup 4.1.3](http://www.crummy.com/software/BeautifulSoup/)
* po:short_synopsis sections not handled yet.
