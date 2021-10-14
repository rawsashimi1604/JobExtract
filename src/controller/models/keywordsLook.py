from __future__ import annotations

"""
    KeywordsLook Module. Contains KeywordsLookModel Object, utility object used to help with storage of keywords to search for.
"""

class KeywordsLookModel:
    '''
        KeywordsLookModel Object, utility object used to help with storage of keywords to search for.

        Class Attributes:
            None
    '''
    def __init__(self) -> KeywordsLookModel:
        '''
            Constructor for JobsModel Class.
            Parameters:
                None
            Returns:
                KeywordsLookModel => Constructs KeywordsLookModel Class
        '''
        self.dependenceKeywords = '''customer team partner people relationship communication support contact understanding responsibility care group communicate staff manner help follow share partner support home assist family serve consultant'''.split(
            " ")

        self.independenceKeywords = ['job', 'solution', 'operate', 'knowledge', 'comply', 'degree', 'legislation', 'technology', 'write', 'deliver', 'sell', 'learn', 'software', 'performance', 'project', 'service', 'healthcare', 'perform', 'compliance', 'emergency', 'risk', 'bachelor', 'issue', 'retail', 'conflict', 'accounting', 'forecast', 'negotiation', 'achieve',
                                     'jurisdiction', 'quality', 'information', 'territory', 'training', 'report', 'tool', 'presentation', 'problem', 'success', 'implement', 'individual', 'engineering', 'order', 'result', 'negotiate', 'specialist', 'deal', 'operation', 'promote', 'study', 'qualification', 'program', 'self', 'execute', 'initiative', 'task', 'win', 'wealth', 'education']

        self.allKeywords = self.dependenceKeywords + self.independenceKeywords
        