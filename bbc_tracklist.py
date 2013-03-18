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

from __future__ import print_function
from bs4 import BeautifulSoup
import urllib
import sys
import time

##def main():
base_URL = 'http://www.bbc.co.uk/programmes/'
## iterate over directory and subdirectories and try to download all
## tracklistings for mp3s?

# programme id
# gets from command line argument
try:
    pid = sys.argv[1]
except IndexError:
    print(  "tlist.py: Download tracklistings for Radio 1, 6 Music and maybe"
            " other BBC stations...")
    print("Usage: tlist.py <BBC pid>")
    sys.exit()

print("Opening web page: " + base_URL + pid)
# get html
# change to with statement here?
try:
    with contextlib.closing(urllib.urlopen(base_URL + pid)) as html:
        soup = BeautifulSoup(html.read())
except (IOError, NameError) as e:
    print("Error opening web page.")
    print("No network connection?")
    sys.exit()

print("Extracting data...")

try:
    # get radio station as string
    station = soup.find('a', class_='logo-area masterbrand-logo'\
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

    if artist != None:
        art = artist.get_text()
    else:
        art = ''

    if track != None:
        trk = track.get_text()
    else:
        art = ''

    if label != None:
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

# also need to handle writing output to file
with open(pid + '.txt', 'w') as textfile:
    textfile.write(title + '\n')
    textfile.write(date + '\n\n')
    written_first_entry = False
    for (artist, track, label) in listing:
        # encode handles unicode characters
        line = (artist + ' - ' + track).encode('utf-8')
        textfile.write((artist + '\n').encode('utf-8'))
        textfile.write((track + '\n').encode('utf-8'))
        textfile.write((label + '\n').encode('utf-8'))
        textfile.write('***'.encode('utf-8'))
        textfile.write('\n'.encode('utf-8'))

print("Done!")

#if __name__ == '__main__':
#    main()