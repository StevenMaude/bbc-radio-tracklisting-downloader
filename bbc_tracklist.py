#!/usr/bin/env python

# bbc_radio_tracklisting_downloader: Download radio tracklistings from
# BBC's website and outputs to a text file.

# Copyright 2013 Steven Maude

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

## maybe iterate over directory and subdirectories and try to download all
## tracklistings for mp3s?
from __future__ import print_function
from bs4 import BeautifulSoup
import os
import urllib
import sys
#import time
import mediafile


def open_listing_page(pid):
    """
    Opens a BBC radio tracklisting page based on pid. Returns a BeautifulSoup
    object derived from that page.

    pid: programme id
    """
    base_URL = 'http://www.bbc.co.uk/programmes/'
    print("Opening web page: " + base_URL + pid)
    ## change to with statement here?
    # get html
    try:
        html = urllib.urlopen(base_URL + pid)
        soup = BeautifulSoup(html.read())
    except (IOError, NameError) as e:
        print("Error opening web page.")
        print("Check network connection and/or programme id.")
        sys.exit()

    html.close()
    return soup


def extract_listing(soup):
    """
    Returns listing, a list of (artist, track, record label) tuples,
    programme title (string) and programme date (string).

    soup: BeautifulSoup object.
    """
    print("Extracting data...")
    try:
        # get radio station as string
        station = soup.find('a', class_='logo-area masterbrand-logo'
                            ).find(class_='title').get_text()

        # get programme title
        title = (soup.title.get_text()).strip()

        # get programme date
        date = soup.find(datatype="xsd:date").get_text()

        # figure out how to convert this object into a datetime one
        #time.strptime(date, "%a %d %b %Y")

        ##print(title)
        ##print(date)
        ##print('***')
        # po:short_synopsis?
        # handle po:SpeechSegment?
        # e.g. b01pzszx
        # don't know how to get the titles as well
        # could do
        # hit = soup.findAll(['li', 'h3'])
        # but duplicates artists, tracks and labels then...
        # hit = soup.findAll('li')
        hits = soup.findAll(typeof=['po:MusicSegment', 'po:SpeechSegment'])

    except AttributeError:
        print("Error processing web page.")
        print("Bad programme id?")
        sys.exit()

    # store (artist, track, record label) in listing as list of tuples
    listing = []

    for each in hits:
        #artist = None
        #track = None
        #label = None
        artist = each.find(class_="artist")
        track = each.find(class_="title")
        label = each.find(class_="record-label")

        if artist is not None:
            art = artist.get_text()
        else:
            art = ''

        if track is not None:
            trk = track.get_text()
        else:
            art = ''

        if label is not None:
            lbl = label.get_text()
        else:
            lbl = ''

        listing.append((art, trk, lbl))
        #print(each)
        # group_title = each.find('h3')
        #if group_title != None:
        #    print(group_title.get_text())
        #    print(group_title)
        #if artist != None:
        #    print(artist.get_text())
        #if track != None:
        #    print(track.get_text())
        #if label != None:
        #    print(label.get_text())
        #if artist != None or track != None or label != None:
        #    print('***')
    return listing, title, date


def write_tracklisting_to_text(listing, pid, title, date, output):
    """
    Write tracklisting to a text file.

    listing: list of (artist, track, record label) tuples
    pid: programme id
    title: programme title
    date: date of programme broadcast
    output: output filename
    """
    # handle this invalid filename
    try:
        with open(output, 'w') as textfile:
            write_output(textfile, listing, title, date)
    except IOError:
        print("Cannot write output. Check write permissions.")
        sys.exit()


def generate_output(listing, title, date):
    """
    Returns a string containing a full tracklisting.

    listing: list of (artist, track, record label) tuples
    title: programme title
    date: programme date
    """
    listing_string = ''

    for (artist, track, label) in listing:
        listing_string += (artist + ' - ' + track).encode('utf-8')
        listing_string += (artist + '\n').encode('utf-8')
        listing_string += (track + '\n').encode('utf-8')
        listing_string += (label + '\n').encode('utf-8')
        listing_string += '***'.encode('utf-8')
        listing_string += '\n'.encode('utf-8')
    return


def write_output(textfile, listing, title, date):
    """
    Writes artist, track, label to text file.

    textfile: file object
    listing: list of (artist, track, record label) tuples
    title: programme title
    date: programme date
    """
    textfile.write(title + '\n')
    textfile.write(date + '\n\n')
    #written_first_entry = False
    for (artist, track, label) in listing:
        # encode handles unicode characters
        #line = (artist + ' - ' + track).encode('utf-8')
        textfile.write((artist + '\n').encode('utf-8'))
        textfile.write((track + '\n').encode('utf-8'))
        textfile.write((label + '\n').encode('utf-8'))
        textfile.write('***'.encode('utf-8'))
        textfile.write('\n'.encode('utf-8'))


def get_output_path():
    """
    Returns a file path
    """
    # if filename and path provided, use these for output text file
    if len(sys.argv) == 4:
        path = sys.argv[2]
        filename = sys.argv[3] + '.txt'
        output = os.path.join(path, filename)
    # otherwise set output to current path
    else:
        output = pid + '.txt'
    return output


def tag_audio_file(audio_file, tracklisting):
    """
    Adds tracklisting as list to lyrics tag of audio file.
    Returns True if successful, False if not.
    """
    try:
        f = mediafile.MediaFile(audio_file)
        #tag = ''.join(lines)
        f.lyrics = tracklisting
        f.save()
        return True
    except IOError:
        print("Unable to save tag to file.")
        return False


# programme id get from command line argument
try:
    pid = sys.argv[1]
except IndexError:
    print("bbc_tracklist.py: Download tracklistings for Radio 1, 6 Music and "
          "maybe other BBC stations..." + '\n')
    print("Usage: tlist.py BBC_pid [directory] [filename].")
    print("Only BBC_pid is required, but to specify a path, both "
          "[directory] and [filename] are required.")
    print("If either [directory] or [filename] are omitted, output "
          "will be to the current path.")
    sys.exit()


# open the page, extract the contents and output to text
soup = open_listing_page(pid)
listing, title, date = extract_listing(soup)
output = get_output_path()
#print (output)

# need a function which outputs either to tags or text file failing that
write_tracklisting_to_text(listing, pid, title, date, output)

print("Done!")

#if __name__ == '__main__':
#    main()
