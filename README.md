# Pinboard-Evernote Sync

## What is it?

Pinboard is great. Evernote too. 

Make love, not war, use both and keep them in sync.

## How it works

The script will:

1. retrieve all your bookmarks from pinboard 
2. if there is no entry in Evernote (in any notebook) with the same URL, create one in the notebook "Bookmarks"
  * The notebook will be created if you don't have it yet


## How to use it

1. Get your pinboard API Token here: https://pinboard.in/settings/password
2. Get an Evernote developer token at: https://www.evernote.com/api/DeveloperToken.action
3. Create a conf.py file with the two tokens. The file conf_sample.py will show you how
4. install https://github.com/evernote/evernote-sdk-python
5. install https://github.com/mgan59/python-pinboard
6. [Optional] install lynx, if you want a nice text dump of the pages in your bookmark note
7. Run PinboardEvernoteSync.py whenever you feel like syncing your accounts
8. goto 7

## TODO

* Reverse sync: If there are notes in your evernote "Bookmarks" notebook which are not in your Pinboard account, add an entry there
* Keep a timestamp of the last sync to avoid processing ALL entries each time
* Add an option to choose the notebook rather than the "Bookmarks" default
* Help lynx with HTTPS content