from parseratorvariable import ParseratorType
import graphiqparser
import numpy

CORPORATION = (('corporation name',             ('CorporationName', 
                                                 'ShortForm')),
               ('corporation org',              ('CorporationNameOrganization',)),
               ('corporation type',             ('CorporationLegalType',)),
               ('corporation committee',        ('CorporationCommitteeType',)),
               ('corporation &Co',              ('CorporationNameAndCompany',)),
               ('corporation branch',           ('CorporationNameBranchType', 
                                                 'CorporationNameBranchIdentifier')),
               ('client corporation name',      ('ProxiedCorporationName', 
                                                 'ProxiedShortForm')),
               ('client corporation org',       ('ProxiedCorporationNameOrganization',)),
               ('client corporation type',      ('ProxiedCorporationLegalType',)),
               ('client corporation committee', ('ProxiedCorporationCommitteeType',)),
               ('client corporation &Co',       ('ProxiedCorporationNameAndCompany',)),
               ('client corporation branch',    ('ProxiedCorporationNameBranchType', 
                                                 'ProxiedCorporationNameBranchIdentifier')))


class EmployerType(ParseratorType) :
    type = "Employer"

    def __init__(self, definition) :
        self.components = (('Corporation', self.compareFields, CORPORATION),)

        super(EmployerType, self).__init__(definition)

        self.tagger = graphiqparser.tag

