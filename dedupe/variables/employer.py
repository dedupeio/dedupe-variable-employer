from parseratorvariable import ParseratorType, consolidate
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

        self.expanded_size = (1 + 1 + 2 * self.n_parts + 1)

    def compareFields(self, parts, field_1, field_2) :


        joinParts = functools.partial(consolidate, components=parts)
        for part, (part_1, part_2) in zip(parts, zip(*map(joinParts, [field_1, field_2]))) :

            part_1 = re.sub(r'[.,]', '', part_1)
            part_2 = re.sub(r'[.,]', '', part_2)

x            if part == ('CorporationNameOrganization',
                          'CorporationName',
                          'ShortForm'):
                remainder_1 = ' '.join(word for word in part_1.split()
                                       if word not in STOP_WORDS)
                remainder_2 = ' '.join(word for word in part_2.split()
                                       if word not in STOP_WORDS)
                yield self.compareString(remainder_1, remainder_2)
            else :
                yield self.compareString(part_1, part_2)

    def comparator(self, field_1, field_2) :
        distances = numpy.zeros(self.expanded_size)
        i = 0

        if not (field_1 and field_2) :
            return distances
        
        distances[i] = 1
        i += 1

        try :
            parsed_variable_1, variable_type_1 = self.tagger(field_1) 
            parsed_variable_2, variable_type_2  = self.tagger(field_2)
        except Exception as e :
            if self.log_file :
                import csv
                with open(self.log_file, 'a') as f :
                    writer = csv.writer(f)
                    writer.writerow([e.original_string.encode('utf8')])
            distances[i] = 1
            distances[-1] = self.compareString(field_1, field_2)
            return distances

        i += 1

        variable_type = self.variable_types[variable_type_1]

        for j, dist in enumerate(variable_type['compare'](parsed_variable_1, 
                                                          parsed_variable_2), 
                                 i) :
            distances[j] = dist

        unobserved_parts = numpy.isnan(distances[i:j+1])
        distances[i:j+1][unobserved_parts] = 0
        unobserved_parts = (~unobserved_parts).astype(int)
        distances[(i + self.n_parts):(j + 1 + self.n_parts)] = unobserved_parts

        return distances

