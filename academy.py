from urllib.request import urlopen
from lxml.etree import parse, HTMLParser
import re
import sqlite3

html = HTMLParser()

class Academy:
  """An Academy is a way to ask whether a word exists."""

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
    self.cursor.execute('CREATE TABLE Word(word TEXT NOT NULL PRIMARY KEY, is_valid INT)')
    self.db.commit()

  def __init__(self):
    # Init online dict (Get session key)
    self.site = 'http://atilf.atilf.fr'
    page = urlopen(self.site + '/Dendien/scripts/generic/showps.exe?p=main.txt;java=no;host=interface_academie8.txt')
    self.session = re.search(';s=(\\d+)', str(page.readall())).group(1)

    # Init database
    self.db = sqlite3.connect('words.db')
    self.cursor = self.db.cursor()
    if not self.is_db_installed():
      self.install_db()

  def save_db(self, word, is_valid):
    """save_db(self, word, is_valid)
    Add a new line to the database."""
    self.cursor.execute('INSERT OR REPLACE INTO Word (word, is_valid) VALUES (?, ?)', [word, is_valid])
    self.db.commit()
    

  def check_online(self, word):
    """check_online(self, word)
    Ask an online dictionnary whether `word` exists."""
    
    data = b'var0=&var2=' + word.encode('cp1252') + b'&var3=*!!*&var5=*!!*'
    page = urlopen(self.site + '/Dendien/scripts/generic/cherche.exe?15;s=' + self.session, data)

    return b'Aucun document' not in page.readall()

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

    res = self.check_db(word)
    if res == None:
      res = self.check_online(word)
      self.save_db(word, res)

    return res
  

