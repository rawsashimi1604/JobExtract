from __future__ import annotations

"""
    Keywords Module. Contains KeywordsModel Object, utility object used to help with storage of keywords in CSV.
"""

class KeywordsModel:
    '''
        KeywordsModel Object, utility object used to help with storage of keywords in CSV.

        Class Attributes:
            keyword : str => Keyword
            count : str => Keyword Count
            type_ : str => Keyword Type
    '''
    def __init__(self, keyword: str, count: str, type_: str) -> KeywordsModel:
        '''
            Constructor for KeywordsModel Class.
            Parameters:
                keyword : str => Keyword
                count : str => Keyword Count
                type_ : str => Keyword Type
            Returns:
                KeywordsModel => Constructs KeywordsModel Class
        '''
        self.keyword = keyword
        self.count = count
        self.type_ = type_

        self.parameters = [
            "keyword",
            "count",
            "type_"
        ]

        self.objectValues = [
            self.keyword,
            self.count,
            self.type_
        ]

    def __repr__(self) -> str:
        '''
            Print for Object
            Parameters:
                None
            Returns:
                str => Print message
        '''
        return f"<KeywordsModel object => keyword: {self.keyword}, count: {self.count}, type_: {self.type_}>\n"

    def __str__(self) -> str:
        '''
            Print for Object
            Parameters:
                None
            Returns:
                str => Print message
        '''
        return f"KeywordsModel attritutes: <KeywordsModel object => keyword: {self.keyword}, count: {self.count}, type_: {self.type_}>\n"

    def updateValues(self) -> None:
        '''
            Updates object values
            Parameters:
                None
            Returns:
                None
        '''
        self.objectValues = [
            self.keyword,
            self.count,
            self.type_
        ]
