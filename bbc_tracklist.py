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
import contextlib
import urllib
import sys
import time

##def main():
base_URL = 'http://www.bbc.co.uk/programmes/'

# programme id
# get from command line argument
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

#html.close()
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

except AttributeError:
    print("Error processing web page.")
    print("Bad programme id?")
    sys.exit()

# store (artist, track, record label) in listing as list of tuples
listing = []

# see http://stackoverflow.com/questions/15484134
# could handle <h3 class="group title"> too, but don't know if really
# necessary; I think it distracts a little from the listing...
# soup.findAll('h3', class_='group-title')
for each in soup.findAll(typeof=['po:MusicSegment', 'po:SpeechSegment']):
    if each['typeof'] == 'po:MusicSegment':
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
            trk = ''

        if label != None:
            lbl = label.get_text()
        else:
            lbl = ''

        listing.append((art, trk, lbl))
    elif each['typeof'] == 'po:SpeechSegment':
        artist = each.find(class_="artist")
        track = each.find(class_="title")
        ##label = each.find(class_="record-label")

        if artist != None:
            art = artist.get_text()
        else:
            art = ''

        if track != None:
            trk = track.get_text()
        else:
            trk = ''
        # need to check this is always the case
        # may not exist in some cases, so maybe need a try/except KeyError here
        if each.p['property'] == 'po:short_synopsis':
            # better way to check
            syn = each.p.get_text()
        else:
            syn = ''

        listing.append((art, trk, syn))

# also need to handle writing output to file
with open(pid + '.txt', 'w') as textfile:
    textfile.write(title + '\n')
    textfile.write(date + '\n\n')
    written_first_entry = False
    # could check whether music or speech
    # then remove gap as appropriate...
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
