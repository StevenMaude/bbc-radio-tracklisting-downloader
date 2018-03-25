#################################
bbc-radio-tracklisting-downloader
#################################

A Python script that downloads radio tracklistings from BBC's website
and tags MP3 or M4A audio files or outputs to a text file. Licensed
under GPL v3 (see COPYING).

**************
Usage examples
**************

Run ``bbc_tracklist.py`` from the command line.

Required arguments are an action: one of ``tag``, ``text`` or ``both``
and a BBC programme id, the 8 characters that are found at the end of
iPlayer URLs such
as:``http://www.bbc.co.uk/iplayer/episode/<programme id>/<programme name>``
or programme information URLs such as:
``http://www.bbc.co.uk/programmes/<programme id>``, e.g. b03d0wk8

``text`` will save the tracklisting to a text file, ``tag`` will tag an
audio file and (unsurprisingly) ``both`` will perform both of these
actions.

Optional arguments are ``--directory DIRECTORY`` and
``--fileprefix FILEPREFIX``. The ``--fileprefix`` is the filename
prefix: e.g. for ``some_bbc_audio.mp3``, the filename prefix is
``some_bbc_audio``.

If either of these are omitted, output will be to the current path. If
no filename is specified, any audio file you want tagging should be
named as the pid. Any text file generated without a filename will be
called ``pid.txt``.

First, if ``tag`` or ``both`` actions are chosen, the script tries to
tag an M4A file, then an MP3. If it fails to find (or write to) an
appropriate audio file, it falls back to creating a text file.

The script generates an output formatted as:

::

    Programme title
    Programme first broadcast date

    Artist
    Title
    Record label

    ***

get\_iplayer usage
==================

**As of get_iplayer 3.13, there is a `tracklist` feature included, which you
can use directly without needing this package installed at all.**

If downloading a radio programme with
`get\_iplayer <http://www.infradead.org/get_iplayer/html/get_iplayer.html>`_,
adding an argument of the form
``--command "python /home/scripts/bbc_tracklist.py action <pid> --directory <dir> --fileprefix <fileprefix>"``
should result in a text file containing the tracklisting in the same
directory as your downloaded audio file where action is ``text``,
``tag`` or ``both``.

(Change ``/home/scripts`` to point to wherever the script is located.)

In Windows, you may need to quote the placeholders (presumably if there
are spaces in them; thanks `JackDandy <https://github.com/JackDandy>`_)
``bbc_tracklist.py <pid> "<dir>" "<fileprefix>"``

*************************
Installation requirements
*************************

-  Tested on Python 2.7.3 on Windows (Windows 7 64-bit) and Linux
   (Raspbian and Ubuntu 12.04). (I suspect it doesn't work with Python
   versions earlier than this due to improvements in Python's HTMLParser
   introduced in 2.7.3.)
-  Requires ``mediafile``, ``requests`` and ``lxml``.

Install module directly
=======================

``pip install bbc-radio-tracklisting-downloader``
should install the module and its dependencies. However, lxml may be an
issue if you're on Windows (see below); make sure that's installed
first.

``bbc_tracklist`` should be available as a command. (Tested on Linux
only.)

Installing by hand
==================

``pip install -r requirements.txt`` may work for you on Linux.

If you're on Windows and have ``pip`` installed,
``pip install beets requests lxml`` may work.

``lxml`` requires compiling. Previously, the easiest way is to install
it was by downloading the latest installer version for Python 2.7 from
`PyPI <https://pypi.python.org/pypi/lxml>`_. However, the Python wheel
that's available on PyPI might be installed automatically on Windows
when you ``pip install lxml`` (not tested).

Even on Linux, compiling ``lxml`` may require more build dependencies.
See `this discussion <https://stackoverflow.com/questions/6504810>`_ for
details. Otherwise, there may be a version of ``lxml`` in your
distribution's package manager (e.g. ``python-lxml``).

You can then grab a copy of the Python scripts from here or git clone
the repository.

*********************************************
Known issue (don't think there's an easy fix)
*********************************************

-  Printing tracklisting in Windows doesn't play nicely with non-ASCII
   characters; these are ignored. (Printing occurs if directory and
   fileprefix are invalid.) You can try running ``cmd /u`` in a command
   prompt if you find this an issue (not tested).
