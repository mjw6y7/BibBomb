#! /usr/bin/env python3
import bibtexparser
import matplotlib.pyplot as plt
import itertools
import os
import re
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

def parse(inputfile):
    with open(inputfile, 'r') as bib_file:
        return bibtexparser.loads(bib_file.read())

def parse_and_validate(inputfile):
    bib_database = parse(inputfile)
    bib_err = {}
    bib_opt = {}
    bib_year = []

    for doc in bib_database.entries:
        doctype = doc['ENTRYTYPE']
        for field in Fields[doctype][REQ]:
            try:
                doc[field]
            except:
                if doc['ID'] in bib_err:
                    bib_err[doc['ID']].append(field)
                else:
                    bib_err[doc['ID']] = [field]
        for field in Fields[doctype][OPT]:
            try:
                doc[field]
            except:
                if doc['ID'] in bib_opt:
                    bib_opt[doc['ID']].append(field)
                else:
                    bib_opt[doc['ID']] = [field]
        try:
            bib_year.append(int(doc['year']))
        except:
            pass

    return bib_err, bib_opt, bib_year


def check_citekeys(inputfile):
    """Check citekeys using this guide:

    Textual representation: **AaBCCd**

    - **Aa**
      - First two initials in first author's last name.

    - **B**
      - First initial in second author's last name (if there is one).

    - **CC**
      - Last two digits of year the paper was published.

    - **d**
      - In case there is already a paper in the database that already
        has this same ID, append an "a" or "b" (or "c" or "d"...) to
        the end of the ID.

    """
    citekey_re = re.compile(r"@[a-zA-Z]+\s*\{\s*(\w+),")
    with open(inputfile) as f:
        all_keys = sorted(citekey_re.findall(f.read()))

    bib_database = parse(inputfile)
    format_re = re.compile(r"[A-Z][a-z][A-Z]?\d{2}[a-z]?")
    format_err = []
    for doc in bib_database.entries:
        if format_re.match(doc['ID']) is None:
            format_err.append(doc['ID'])

    duplicate_err = {}
    for key, copies in itertools.groupby(all_keys):
        num_copies = len(list(copies))
        if num_copies > 1:
            duplicate_err[key] = num_copies

    return format_err, duplicate_err


def plot_years(bib_year):
    plt.hist(bib_year, bins=max(bib_year)-min(bib_year))
    plt.title("Histogram of References")
    plt.xlabel("Year Published")
    plt.ylabel("Number of References")
    plt.show()


def main(args):
    for inputfile in args.bib_file:
        print('\nChecking {}'.format(inputfile), file=sys.stderr)

        if not os.path.exists(inputfile):
            print('\tCannot open {}. Skipping...'.format(inputfile), file=sys.stderr)
            continue

        print('\tParsing {}'.format(inputfile), file=sys.stderr)
        err, opt, year = parse_and_validate(inputfile)

        if not args.field_lst and not args.opt_lst and not args.key_dup_lst and not args.key_bad_lst:
            print('\tDisabled entry output. Enable with --list\n', file=sys.stderr)

        if len(err) == 0:
            print('\t{0} contains no errors'.format(inputfile), file=sys.stderr)
        elif args.field_lst:
            print('\t{0} contains errors in:'.format(inputfile), file=sys.stderr)
            for e in sorted(err):
                print('{}:\t{}'.format(e, err[e]))

        if len(opt) == 0:
            print('\t{0} contains no missing optional fields'.format(inputfile), file=sys.stderr)
        elif args.opt_lst:
            print('\t{0} has missing optional fields in:'.format(inputfile), file=sys.stderr)
            for o in sorted(opt):
                print('{}:\t{}'.format(o, opt[o]))

        format_errs, key_errs = None, None
        if args.keys or args.key_dup_lst or args.key_bad_lst:
            format_errs, key_errs = check_citekeys(inputfile)
            if len(format_errs) == 0 and len(key_errs) == 0:
                print('\t{0} contains no citekey errors'.format(inputfile), file=sys.stderr)
            else:
                if args.key_dup_lst:
                    print('\t{0} contains duplicated keys in:'.format(inputfile), file=sys.stderr)
                    for k in sorted(key_errs):
                        print('{} x{}'.format(k, key_errs[k]))
                if args.key_bad_lst:
                    print('\t{0} contains badly formatted keys in:'.format(inputfile), file=sys.stderr)
                    for f in sorted(format_errs):
                        print(f)

        if args.plot:
            print('\tPlotting histogram for {}'.format(inputfile), file=sys.stderr)
            plot_years(year)

        print('\t{} entries are missing required fields'.format(len(err)), file=sys.stderr)
        print('\t{} entries are missing optional fields'.format(len(opt)), file=sys.stderr)
        if key_errs or format_errs:
            print('\t{} entries have badly formatted citekeys'.format(len(format_errs)), file=sys.stderr)
            print('\t{} entries have a duplicated citekey'.format(len(key_errs)), file=sys.stderr)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Check your BibTeX files')
    parser.add_argument('bib_file', type=str, nargs='+',
                        help='BibTeX files to check')
    parser.add_argument('--plot', action='store_true',
                        help='Plot a histogram of pulication years')
    parser.add_argument('--keys', action='store_true',
                        help='Check citation keys')
    parser.add_argument('--list-missing-fields', dest="field_lst", action='store_true',
                        help='List entries with missing required fields')
    parser.add_argument('--list-optional-fields', dest="opt_lst", action='store_true',
                        help='List entries with missing optional fields')
    parser.add_argument('--list-duplicate-keys', dest="key_dup_lst", action='store_true',
                        help='List entries with duplicate keys')
    parser.add_argument('--list-bad-keys', dest="key_bad_lst", action='store_true',
                        help='List entries with badly formatted keys')

    main(parser.parse_args())
