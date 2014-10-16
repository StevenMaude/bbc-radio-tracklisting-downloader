#!/usr/bin/env python
# encoding: utf-8

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

import codecs
import os
import sys

import lxml.html
import mediafile
import requests

from cmdline import parse_arguments


def open_listing_page(trailing_part_of_url):
    """
    Opens a BBC radio tracklisting page based on trailing part of url.
    Returns a lxml ElementTree derived from that page.

    trailing_part_of_url: a string, like the pid or e.g. pid/segments.inc
    """
    base_URL = 'http://www.bbc.co.uk/programmes/'
    print("Opening web page: " + base_URL + trailing_part_of_url)

    try:
        html = requests.get(base_URL + trailing_part_of_url).text
    except (IOError, NameError):
        print("Error opening web page.")
        print("Check network connection and/or programme id.")
        sys.exit(1)

    return lxml.html.fromstring(html)


def get_programme_title(pid):
    """Take BBC programme ID as string; returns programme title as string."""
    print("Extracting title and station...")
    main_page_etree = open_listing_page(pid)
    try:
        title, = main_page_etree.xpath('//title/text()')
    except ValueError:
        title = ''
    return title.strip()


def get_broadcast_date(pid):
    """Take BBC pid (string); extract and return broadcast date as string."""
    print("Extracting first broadcast date...")
    broadcast_etree = open_listing_page(pid + '/broadcasts.inc')
    original_broadcast_date, = broadcast_etree.xpath(
        '(//div[@class="grid__inner"]//span'
        '[@class="broadcast-event__date text-base timezone--date"])'
        '[1]/text()')
    return original_broadcast_date


def extract_listing(pid):
    """Extract listing; return list of tuples (artist, title, label)."""
    print("Extracting tracklisting...")
    listing_etree = open_listing_page(pid + '/segments.inc')
    track_divs = listing_etree.xpath('//div[@class="segment__track"]')

    listing = []
    for track_div in track_divs:
        try:
            artist, = track_div.xpath('.//span[@property="byArtist"]'
                                      '//span[@class="artist"]/text()')
        except ValueError:
            artist = ''
        try:
            title, = track_div.xpath('.//p[@property="name"]/text()')
        except ValueError:
            title = ''
        try:
            label, = track_div.xpath('.//abbr[@title="Record Label"]'
                                     '/span[@property="name"]/text()')
        except ValueError:
            label = ''
        listing.append((artist, title, label))
    return listing


def generate_output(listing, title, date):
    """
    Returns a string containing a full tracklisting.

    listing: list of (artist, track, record label) tuples
    title: programme title
    date: programme date
    """
    listing_string = u'{0}\n{1}\n\n'.format(title, date)
    for entry in listing:
        listing_string += '\n'.join(entry) + '\n***\n'
    return listing_string


def get_output_filename(args):
    """Returns a filename as string without an extension."""
    # If filename and path provided, use these for output text file.
    if args.directory is not None and args.fileprefix is not None:
        path = args.directory
        filename = args.fileprefix
        output = os.path.join(path, filename)
    # Otherwise, set output to current path
    elif args.fileprefix is not None:
        output = args.fileprefix
    else:
        output = args.pid
    return output


def write_listing_to_textfile(textfile, tracklisting):
    """Write tracklisting to a text file."""
    with codecs.open(textfile, 'wb', 'utf-8') as text:
        text.write(tracklisting)


def tag_audio_file(audio_file, tracklisting):
    """
    Adds tracklisting as list to lyrics tag of audio file.
    Returns True if successful, False if not.
    """
    try:
        f = mediafile.MediaFile(audio_file)
        print("Trying to tag {}".format(audio_file))
        # check if tracklisting already added
        if tracklisting in f.lyrics:
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


def output_to_file(filename, tracklisting, action):
    """
    Produce requested output; either output text file, tag audio file or do
    both.

    filename: a string of path + filename without file extension
    tracklisting: a string containing a tracklisting
    action: 'tag', 'text' or 'both', from command line arguments
    """
    if action in ('tag', 'both'):
        audio_tagged = tag_audio(filename, tracklisting)
        if action == 'both' and audio_tagged:
            write_text(filename, tracklisting)
    elif action == 'text':
        write_text(filename, tracklisting)


def write_text(filename, tracklisting):
    """Handle writing tracklisting to text."""
    print("Saving text file.")
    try:
        write_listing_to_textfile(filename + '.txt', tracklisting)
    except IOError:
        # if all else fails, just print listing
        print("Cannot write text file to path: {}".format(filename))
        print("Printing tracklisting here instead.")
        # ignoring errors is a hack to cope with Windows not dealing well
        # with UTF-8
        print(tracklisting.encode(sys.stdout.encoding, errors='ignore'))


def tag_audio(filename, tracklisting):
    """Return True if audio tagged successfully; handle tagging audio."""
    if not(tag_audio_file(filename + '.m4a', tracklisting) or
           tag_audio_file(filename + '.mp3', tracklisting)):
        print("Cannot find or access any relevant M4A or MP3 audio file.")
        print("Trying to save a text file instead.")
        write_text(filename, tracklisting)
        return False
    return True


def main():
    """Get a tracklisting, write to audio file or text."""
    args = parse_arguments()
    pid = args.pid
    title = get_programme_title(pid)
    broadcast_date = get_broadcast_date(pid)
    listing = extract_listing(pid)
    filename = get_output_filename(args)
    tracklisting = generate_output(listing, title, broadcast_date)
    output_to_file(filename, tracklisting, args.action)
    print("Done!")

if __name__ == '__main__':
    main()
