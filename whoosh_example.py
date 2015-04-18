# -*- coding: utf-8 -*-

from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.qparser import QueryParser
from whoosh.index import open_dir, create_in
from whoosh.query import Term, And

my_schema = Schema(id = ID(unique=True, stored=True), 
                   path = ID(stored=True), 
                   source = ID(stored=True),
                   author = TEXT(stored=True), 
                   title = TEXT(stored=True),
                   text = TEXT)


ix = create_in("index", my_schema)
index = open_dir("index")
writer = index.writer()

import io
writer.add_document(id = u'guten01', 
                    path = u'gutenberg/austen-emma.txt',
                    source = u'austen-emma.txt',
                    author = u'Jane Austen',
                    title = u'Emma',
                    text = io.open('gutenberg/austen-emma.txt', encoding='utf-8').read())

writer.add_document(id = u'guten02', 
                    path = u'gutenberg/austen-persuasion.txt',
                    source = u'austen-persuasion.txt',
                    author = u'Jane Austen',
                    title = u'Chapter 1',
                    text = io.open('gutenberg/austen-persuasion.txt', encoding='utf-8').read())

writer.add_document(id = u'guten03', 
                    path = u'gutenberg/blake-poems.txt',
                    source = u'blake-poems.txt',
                    author = u'William Blake',
                    title = u'SONGS OF INNOCENCE AND OF EXPERIENCE and THE BOOK of THEL',
                    text = io.open('gutenberg/austen-persuasion.txt', encoding='utf-8').read())
writer.commit()



#=============Query===========
index = open_dir("index")
searcher = index.searcher()
query = And([Term("text", "song"), Term("text", "wild")])

results = searcher.search(query)
print('# of hits:', len(results))
print('Best Match:', results[0])

parser = QueryParser("text", index.schema)
parser.parse("song wild person")
parser.parse("(song OR wild) AND (song OR austen)")
parser.parse("song wild author:'William Blake'")
