#! /usr/bin/env python3
from bibtexparser.bparser import BibTexParser
import matplotlib.pyplot as plt
import sys

REQ = 0
OPT = 1
Fields = {'article':[['author','title','journal','year'],
                     ['volume','number','pages','month','note']],
          'book':[['author','title','publisher','year'],
                  ['volume','number','series','address','edition','month','note']],
          'booklet':[['title','year'],
                     ['author','howpublished','address','month','note']],
          'conference':[['author','title','booktitle','year'],
                        ['editor','volume','number','series','pages','address','month','publisher','note']],
          'inbook':[['author','editor','title','chapter','pages','publisher','year'],
                    ['volume','number','series','type','address','edition','month','note']],
          'incollection':[['author','title','booktitle','publisher','year'],
                          ['editor','volume','number','series','type','chapter','pages','address','edition','month','note']],
          'inproceedings':[['author','title','booktitle','year'],
                           ['editor','volume','number','series','pages','address','organization','publisher','month','note']],
          'manual':[['title','year'],
                    ['author','organization','address','edition','month','note']],
          'mastersthesis':[['author','title','school','year'],
                           ['type','address','month','note']],
          'misc':[[],
                  ['author','title','howpublished','year','month','note']],
          'phdthesis':[['author','title','school','year'],
                       ['address','month','keywords','note']],
          'proceedings':[['title','year'],
                         ['editor','volume','number','series','address','organization','publisher','month','note']],
          'techreport':[['author','title','institution','year'],
                        ['type','number','address','month','note']],
          'unpublished':[['author','title','note'],
                         ['year','month']],
          'patent':[[],
                    []],
          'collection':[[],
                        []],
          'electronic':[[],
                        []]}


def parse_and_validate(inputfile):
    with open(inputfile, 'r') as bib_file:
        parser = BibTexParser(bib_file.read())
        bib_dict = parser.get_entry_dict()

    bib_err = []
    bib_opt = []
    bib_year = []

    for doc in bib_dict.keys():
        doctype = bib_dict[doc]['type']
        for field in Fields[doctype][REQ]:
            try:
                bib_dict[doc][field]
            except:
                bib_err.append(doc)
        for field in Fields[doctype][OPT]:
            try:
                bib_dict[doc][field]
            except:
                bib_opt.append(doc)
        try:
            bib_year.append(int(bib_dict[doc]['year']))
        except:
            pass

    return bib_err, bib_opt, bib_year


def plot_years(bib_year):
    plt.hist(bib_year, bins=max(bib_year)-min(bib_year))
    plt.title("Histogram of References")
    plt.xlabel("Year Published")
    plt.ylabel("Number of References")
    plt.show()


def main():
    try:
        inputfile = sys.argv[1]
        print('Parsing {}'.format(inputfile))
    except Exception as err:
        print(err)
        print('Histogram.py <inputfile>')
        sys.exit(2)

    err, opt, year = parse_and_validate(inputfile)

    if len(err) == 0:
        print('{0} contains no errors'.format(inputfile))
    else:
        print('{0} contains errors in:{1}'.format(inputfile, err))

    if len(opt) != 0:
        print('{0} entrys are missing optional fields'.format(len(opt)))

    plot_years(year)

if __name__ == '__main__':
    main()
