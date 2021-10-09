class KeywordsLookModel:
    def __init__(self):
        self.dependenceKeywords = '''customer team partner people relationship communication support contact understanding responsibility care group communicate staff manner help follow share partner support home assist family serve consultant'''.split(
            " ")

        self.independenceKeywords = ['job', 'solution', 'operate', 'knowledge', 'comply', 'degree', 'legislation', 'technology', 'write', 'deliver', 'sell', 'learn', 'software', 'performance', 'project', 'service', 'healthcare', 'perform', 'compliance', 'emergency', 'risk', 'bachelor', 'issue', 'retail', 'conflict', 'accounting', 'forecast', 'negotiation', 'achieve',
                                     'jurisdiction', 'quality', 'information', 'territory', 'training', 'report', 'tool', 'presentation', 'problem', 'success', 'implement', 'individual', 'engineering', 'order', 'result', 'negotiate', 'specialist', 'deal', 'operation', 'promote', 'study', 'qualification', 'program', 'self', 'execute', 'initiative', 'task', 'win', 'wealth', 'education']

        self.allKeywords = self.dependenceKeywords + self.independenceKeywords

    def __repr__(self):
        pass

    def __str__(self):
        pass
