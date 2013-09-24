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


def generate_output(listing, title, date):
    """
    Returns a string containing a full tracklisting.

    listing: list of (artist, track, record label) tuples
    title: programme title
    date: programme date
    """
    listing_string = u''
    listing_string += title + '\n' + date + '\n\n'

    for (artist, track, label) in listing:
        listing_string += (artist + '\n')
        listing_string += (track + '\n')
        listing_string += (label + '\n')
        listing_string += '***\n'
    return listing_string


def get_output_filename():
    """
    Returns a filename without an extension.
    """
    # if filename and path provided, use these for output text file
    if len(sys.argv) == 4:
        path = sys.argv[2]
        filename = sys.argv[3]
        output = os.path.join(path, filename)
    # otherwise set output to current path
    else:
        output = pid
    return output


def write_listing_to_textfile(textfile, tracklisting):
    with open(textfile, 'wb+') as text:
        text.write(tracklisting.encode('utf-8'))


def tag_audio_file(audio_file, tracklisting):
    """
    Adds tracklisting as list to lyrics tag of audio file.
    Returns True if successful, False if not.
    """
    try:
        f = mediafile.MediaFile(audio_file)
        # check if tracklisting already added
        if f.lyrics.endswith(tracklisting):
            print ("Tracklisting already present. Not modifying file.")
            return True
        # check if lyrics tag exists already
        elif len(f.lyrics) != 0:
            print("Lyrics tag exists. Appending tracklisting to it.")
            f.lyrics = f.lyrics + '\n\n' + 'Tracklisting' + '\n' + tracklisting
        else:
            print("No tracklisting present. Creating lyrics tag.")
            f.lyrics = 'Tracklisting' + '\n' + tracklisting
            #tag = ''.join(lines)
        f.save()
        print("Saved tag to file:", audio_file)
        return True
    except IOError:
        print("Unable to save tag to file:", audio_file)
        return False


def output_to_file(filename, tracklisting):
    """
    Try tagging to audio file. Failing that fall back to writing to text
    file.

    filename: a string of path + filename without file extension
    tracklisting: a string containing a tracklisting
    """
    # if writing to either type of file fails
    # try writing to text file instead
    if not(tag_audio_file(filename + '.m4a', tracklisting) or
           tag_audio_file(filename + '.mp3', tracklisting)):
        print("Cannot find or access any relevant audio file.")
        try:
            print("Trying to save a text file instead.")
            write_listing_to_textfile(filename + '.txt', tracklisting)
        except IOError:
            # if all else fails, just print listing
            print("Cannot write text file in specified path!")
            print("Just printing tracklisting here instead.")
            print(tracklisting)


# programme id get from command line argument
try:
    pid = sys.argv[1]
except IndexError:
    print("bbc_tracklist.py: Download tracklistings for Radio 1, 6 Music and "
          "maybe other BBC stations..." + '\n')
    print("Usage: bbc_tracklist.py BBC_pid [directory] [filename prefix].")
    print("Only BBC_pid is required, but to specify a file, both "
          "[directory] and [filename prefix] are required.")
    print("If either [directory] or [filename prefix] are omitted, output "
          "will be to the current path.")
    sys.exit()


# open the page, extract the contents and output to text
soup = open_listing_page(pid)
listing, title, date = extract_listing(soup)
filename = get_output_filename()
tracklisting = generate_output(listing, title, date)
output_to_file(filename, tracklisting)

print("Done!")

#if __name__ == '__main__':
#    main()
