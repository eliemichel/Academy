from urllib.request import urlopen, HTTPError
from urllib.parse import quote
from lxml.etree import parse, HTMLParser
import re
import sqlite3

html = HTMLParser()

wikitionnary_base = 'https://fr.wiktionary.org/wiki/'
wikipedia_base = 'https://fr.wikipedia.org/wiki/'

class Academy:
  """An Academy is a way to ask whether a word exists.
  It uses Wiktionnary and Wikipedia (for proper nouns) to
  determine whether the word exists.
  Edit urls to use it in another language than French!
  Example of use:
  ac = Academy()
  ac.check('word')"""

  def is_db_installed(self):
    """is_db_installed(self)
    Check whether the database has been installed"""
    c = self.cursor
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Word'")
    return c.fetchone() != None

  def install_db(self):
    """install_db(self)
    Initialize database tables (Word)"""
    print("Installing...")
    self.cursor.execute('CREATE TABLE Word(word TEXT NOT NULL PRIMARY KEY, is_valid INT, origin TEXT)')
    self.db.commit()

  def __init__(self):
    # Init database
    self.db = sqlite3.connect('words.db')
    self.cursor = self.db.cursor()
    if not self.is_db_installed():
      self.install_db()

  def save_db(self, word, is_valid, origin):
    """save_db(self, word, is_valid)
    Add a new line to the database."""
    self.cursor.execute('INSERT OR REPLACE INTO Word (word, is_valid, origin) VALUES (?, ?, ?)', [word, is_valid, origin])
    self.db.commit()
    

  def check_wikitionnaire(self, word):
    """check_wikitionnaire(self, word)
    Ask the Wikitionnaire whether `word` exists."""
    
    try:
        page = urlopen(wikitionary_base + quote(word))
        res = 'Le Wiktionnaire ne possède pas d’article avec ce nom exact'.encode() not in page.readall()
    except HTTPError as e:
        res = False
        if e.code != 404:
            print('[Warning] Unexpected HTTP Status: %d (for %s)' % (e.code, word))

    if res:
      self.save_db(word, res, 'wikitionnaire')

    return res

  def check_wikipedia(self, word):
    """check_wikitionnaire(self, word)
    Ask the Wikipedia whether `word` exists."""
    
    try:
        page = urlopen(wikipedia_base + quote(word))
        res = "Wikipédia ne possède pas d'article avec ce nom.".encode() not in page.readall()
    except HTTPError as e:
        res = False
        if e.code != 404:
            print('[Warning] Unexpected HTTP Status: %d (for %s)' % (e.code, word))

    if res:
      self.save_db(word, res, 'wikipedia')

    return res

  def check_online(self, word):
    """check_online(self, word)
    Ask an online dictionnary whether `word` exists."""
    
    res = self.check_wikitionnaire(word)
    if not res:
      res = self.check_wikipedia(word)
    if not res:
      self.save_db(word, res, 'online')

    return res



  def check_db(self, word):
    """check_db(self, word)
    Ask the local dayabase whether `word` exists."""
    c = self.cursor
    c.execute('SELECT is_valid FROM Word WHERE word=?', [word])
    res = c.fetchone()
    if res == None:
      return res
    else:
      return res[0]


  def check(self, word):
    """check(self, word)
    Return true if and only if `word` exists."""

    # Check local data
    res = self.check_db(word)
    if not res:
      res = self.check_db(word.lower())

    # Ask online
    if res == None:
      res = self.check_online(word)
      if not res:
        res = self.check_online(word.lower())

    return res

  def white_list(self, filename):
    """white_list(self, filename)
    Add words from `filename` to the db.
    One word per line."""
    pass # TODO

  

