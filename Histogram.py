from bibtexparser.bparser import BibTexParser
import matplotlib.pyplot as plt
import sys

ReqFields = {'inproceedings':['author','booktitle','pages','publisher','title','year'],
             'article':['author','journal','number','pages','title','volume','year'],
             'techreport':['author','institution','title','year'],
             'incollection':['author','booktitle','pages','publisher','title','year'],
             'book':['author','publisher','title','year']
             'inbook':['author','booktitle','pages','publisher','title','year'],
             'proceedings':['editor','publisher','title','year'],
             'phdthesis':['author','school','title','year'],
             'mastersthesis':['author','school','title','year'],
             'electronic':['author','title','url','year'],
             'misc':['author','howpublished','title','year']}

try:
    inputfile = sys.argv[1]
except Exception as err:
    print(err)
    print('Histogram.py <inputfile>')
    sys.exit(2)

with open(inputfile, 'r') as bib_file:
    parser = BibTexParser(bib_file.read())
    bib_dict = parser.get_entry_dict()

bib_err = []
bib_year = []
for doc in bib_dict.keys():
    try:
        Test = Bib
        for field in ReqFields[doc['type']]:
            
        bib_year.append(int(bib_dict[doc]['year']))

    except:
        bib_err.append(doc)

print('{0} contains errors in:{1}'.format(inputfile, bib_err))

plt.hist(bib_year, bins=max(bib_year)-min(bib_year))
plt.title("Histogram of References")
plt.xlabel("Year Published")
plt.ylabel("Number of References")
plt.show()

def BibCheck(Fields, Ref):
    try:
        for f in Fields:

    except:
        
