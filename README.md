# Pinboard-Evernote Sync

## What is it?

Sync Pinboard and Evernote bookmarks.

## How it works

The script will:

1. retrieve all your bookmarks from pinboard 
2. if there is no entry in Evernote (in any notebook) with the same URL, create one in the notebook "Bookmarks"
  * The notebook will be created if you don't have it yet
3. Add all your pinboard bookmarks into evernote 
  * If you have lynx installed, the script will save a text dump of the page into Evernote
  * If you have phantom.JS installed, the script will also save a screenshot of the page into Evernote
4. Add all your evernote bookmarks into Pinboard 

## How to use it

1. Get your pinboard API Token here: https://pinboard.in/settings/password
2. Get an Evernote developer token at: https://www.evernote.com/api/DeveloperToken.action
3. Create a conf.py file with your credentials (tokens or passwords). The file conf_sample.py will show you how
4. install https://github.com/evernote/evernote-sdk-python
5. install https://github.com/mgan59/python-pinboard
6. [Optional] install lynx, if you want a nice text dump of the pages in your bookmark note
7. [Optional] get a Readability parser key if you want to use it instead of lynx
8. [Optional] install phantomJS from http://phantomjs.org/ if you want to keep a screenshot of each bookmarked site in evernote
9. Run PinboardEvernoteSync.py whenever you feel like syncing your accounts
10. goto 9

## TODO

* Sync tags
* Add an option to choose the Evernote notebook. Currently only uses the "Bookmarks" default
