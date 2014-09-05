from bibtexparser.bparser import BibTexParser
import matplotlib.pyplot as plt
import sys

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
        bib_year.append(int(bib_dict[doc]['year']))
    except:
        bib_err.append(doc)

print('{0} contains errors in:{1}'.format(inputfile, bib_err))

plt.hist(bib_year, bins=max(bib_year)-min(bib_year))
plt.title("Histogram of References")
plt.xlabel("Year Published")
plt.ylabel("Number of References")
plt.show()
