from parseratorvariable import ParseratorType, consolidate
from simplecosine.cosine import CosineTextSimilarity
import graphiqparser
import numpy
import functools
import re
import csvkit
import os

CORPORATION = (('corporation name',             ('CorporationName', 
                                                 'ShortForm')),
               ('corporation org',              ('CorporationNameOrganization',)),
               ('corporation type',             ('CorporationLegalType',)),
               ('corporation committee',        ('CorporationCommitteeType',)),
               ('corporation &Co',              ('CorporationNameAndCompany',)),
               ('corporation branch',           ('CorporationNameBranchType', 
                                                 'CorporationNameBranchIdentifier')))

STOP_WORDS = {'the', 'elect', 'to', '&', 'and', 'for', 'of'}

class EmployerType(ParseratorType) :
    type = "Employer"

    def __init__(self, definition) :
        self.components = (('Corporation', self.compareFields, CORPORATION),)

        super(EmployerType, self).__init__(definition)

        self.tagger = graphiqparser.tag

        self.corpus = self.grabCorpus()

        self.corpusCompare = CosineTextSimilarity(self.corpus)

    def grabCorpus(self):
        corpus_filename = os.path.abspath(os.path.dirname(__file__))+'/employer_corpus.csv'

        # make corpus if it doesnt exist
        if not os.path.exists(corpus_filename):
            csv_filename = os.path.abspath(os.path.dirname(__file__))+'/employers.csv'

            with open(csv_filename, 'rU') as f:
                reader = csvkit.DictReader(f)

                words = []
                for row in reader:
                    try:
                        tagged = self.tagger(row['employer'])
                        name = tagged[0].get('CorporationName')
                        name = re.sub(r'\.', '', name)

                        words.extend(name.split())
                    except:
                        pass

            with open(corpus_filename, "w") as outfile:
                corpus_rows = [[w] for w in words]
                writer = csvkit.writer(outfile)
                writer.writerows(corpus_rows)

        # read in corpus
        with open(corpus_filename, 'rU') as f:
            reader = csvkit.reader(f)
            
            corpus=[]
            for row in reader:
                corpus.append(row[0])

        return corpus


    def compareFields(self, parts, field_1, field_2) :


        joinParts = functools.partial(consolidate, components=parts)
        for part, (part_1, part_2) in zip(parts, zip(*map(joinParts, [field_1, field_2]))) :

            part_1 = re.sub(r'\.', '', part_1)
            part_2 = re.sub(r'\.', '', part_2)

            if part == ('CorporationName', 'ShortForm') :
                remainder_1 = ' '.join(word for word in part_1.split()
                                       if word not in STOP_WORDS)
                remainder_2 = ' '.join(word for word in part_2.split()
                                       if word not in STOP_WORDS)
                yield self.corpusCompare(remainder_1, remainder_2)
            elif part == ('CorporationNameOrganization',):
                remainder_1 = ' '.join(word for word in part_1.split()
                                       if word not in STOP_WORDS)
                remainder_2 = ' '.join(word for word in part_2.split()
                                       if word not in STOP_WORDS)
                yield self.compareString(remainder_1, remainder_2)
            else :
                yield self.compareString(part_1, part_2)
