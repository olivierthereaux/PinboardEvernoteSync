#!/usr/bin/env python
"""PinboardEvernoteSync.py

Pinboard is great. Evernote too. 

Make love, not war, use both and keep them in sync.

"""

__version__ = "1.0"
__license__ = "WTFPL"
__copyright__ = "Copyright 2013, Olivier Thereaux"
__author__ = "Olivier Thereaux <http://olivier.thereaux.net/>"

import pinboard
import time
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

def save2evernote(pinbookmark):
    note = Types.Note()
            # ourNote.notebookGuid = parentNotebook.guid
    note.title = pinbookmark["description"]
    attributes = Types.NoteAttributes(sourceURL = pinbookmark["href"])
    note.attributes = attributes
    note.content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>%s</en-note>''' % pinbookmark["extended"]
    print str(int(time.mktime(pinbookmark[u'time_parsed'])))
    note.created = 1000*int(time.mktime(pinbookmark[u'time_parsed']))
    return note_store.createNote(note)
    
# initialise clients with both tokens
try:
    import conf
    client = EvernoteClient(token=evernote_token, sandbox=True)
    user_store = client.get_user_store()
    note_store = client.get_note_store()
    p = pinboard.open(token=pinboard_token)
except:
    print "Please fill in your evernote and pinboard developer tokens"
    print "See conf_sample.py for instructions"
    exit(1)


posts =  p.posts()
    # p.posts(fromdt="") # FIXME look only for entries newer than a given timestamp
for post in posts:
    created_note = save2evernote(post)
    print "Successfully created a new note with GUID: ", created_note.guid, " and modified date: ", created_note.created, created_note.updated
    