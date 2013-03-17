#!/usr/bin/env python
"""PinboardEvernoteSync.py

Pinboard is great. Evernote too. 

Make love, not war, use both and keep them in sync.

"""

__version__ = "1.0"
__license__ = "WTFPL"
__copyright__ = "Copyright 2013, Olivier Thereaux"
__author__ = "Olivier Thereaux <http://olivier.thereaux.net/>"

import os
import socket
import subprocess
import re
import pinboard
import time
import hashlib
import binascii
import cgi
import urllib
import urllib2
import json
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

def canhaslynx():
    # test whether lynx is installed 
    # strongly inspired by http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    lynx_exe = None
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe_file = os.path.join(path, "lynx")
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            lynx_exe = exe_file
    return lynx_exe

def getsummaryfromreadability(href, readability_token):
    readability_query = 'https://readability.com/api/content/v1/parser?url='+href+'&token='+readability_token
    readable_text = urllib.urlopen(readability_query).read()
    return '<p>'+json.loads(readable_text)['excerpt'].encode("utf-8")+'</p>'
    
def getsummaryfromlynx(lynx_exe, href):
    clean_href = href
    try: #python 3.3 and above
        from shlex import quote
        clean_href = quote(clean_href)
    except: 
        _find_unsafe = re.compile(r'[^\w@%+=:,./-]').search
        if _find_unsafe(clean_href):
            clean_href =  "'" + clean_href.replace("'", "'\"'\"'") + "'"
    lynx_args = [lynx_exe,'-dump','-display_charset=utf-8','-assume_charset=utf-8','-nomargins','-hiddenlinks=ignore','-nonumbers',clean_href]
    try:
        lynx_dump = cgi.escape(subprocess.check_output(lynx_args, stderr=open('/dev/null', 'w')))
        return '<pre>'+lynx_dump+'</pre>'
    except:
        return ''

def save2evernote(pinbookmark, bookmark_guid, lynx_exe, readability_token):
    note = Types.Note()
            # ourNote.notebookGuid = parentNotebook.guid
    note.title = pinbookmark["description"].encode("utf-8")
    attributes = Types.NoteAttributes(sourceURL = pinbookmark["href"])
    note.attributes = attributes
    note.notebookGuid = bookmark_guid
    page_dump = ''
    if lynx_exe:
        # print "Can Has Lynx"
        page_dump = getsummaryfromlynx(lynx_exe, pinbookmark["href"])
    if page_dump == "": #lynx failed, or no present. Try readability
        # print "Lynx no worky"
        if readability_token != None:
            # print "Using Readability instead"
            page_dump = getsummaryfromreadability(pinbookmark["href"], readability_token)
    note.content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
%s
<hr />
%s
</en-note>''' % (pinbookmark["extended"].encode("utf-8"), page_dump)
    note.created = 1000*int(time.mktime(pinbookmark[u'time_parsed']))
    return note_store.createNote(note)
    
# initialise clients with tokens
pinboard_username = None
pinboard_pass = None
evernote_token = None
readability_token = None

from conf import *
client = EvernoteClient(token=evernote_token, sandbox=False)
user_store = client.get_user_store()
# p = pinboard.open(token=pinboard_token) # FIXME
p = pinboard.open(pinboard_username, pinboard_pass)
note_store = client.get_note_store()

# look for notebook "Bookmarks". If there is none, create it
notebooks = note_store.listNotebooks()
bookmark_notebook_guid = None
for notebook in notebooks:
    if notebook.name == "Bookmarks":
        bookmark_notebook_guid = notebook.guid
if bookmark_notebook_guid == None:
    new_notebook = Types.Notebook()
    new_notebook.name = "Bookmarks" 
    bookmark_notebook_guid = note_store.createNotebook(new_notebook).guid

#Is Lynx installed?
lynx_exe = canhaslynx()

# retrieve all pinboard posts
# pinboard_posts =  p.posts(fromdt="2013-03-10") # FIXME look only for entries newer than a given timestamp
# pinboard_posts =  p.posts(todt="2011-08-09") # FIXME look only for entries newer than a given timestamp
pinboard_posts =  p.posts()
for post in pinboard_posts:
    note_filter = NoteStore.NoteFilter(words='sourceURL:"'+post["href"].encode("utf-8")+'"')
    try:
        existing_notes = note_store.findNotes(note_filter, 0, 1)
    except socket.error:
        print "Evernote server timeout, waiting to re-try"
        time.sleep(5)
        existing_notes = note_store.findNotes(note_filter, 0, 1)
        # if this bombs again, let it crash. for now.
    if len(existing_notes.notes) > 0:
            print "Skipping post: ", post["href"], " already in Evernote"
            pass        
    else:
        try:
            created_note = save2evernote(post, bookmark_notebook_guid, lynx_exe=lynx_exe, readability_token=readability_token)
            print "Successfully created a new note with GUID: ", created_note.guid, " for bookmark: ", post['href']
        except Exception,e:
            print "Could not create a note for: ", post['href'], e
            pass