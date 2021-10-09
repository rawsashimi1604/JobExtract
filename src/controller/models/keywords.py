class KeywordsModel:
    def __init__(self, keyword, count, type_):
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

    def __repr__(self):
        return f"<KeywordsModel object => keyword: {self.keyword}, count: {self.count}, type_: {self.type_}>\n"

    def __str__(self):
        return f"KeywordsModel attritutes: <KeywordsModel object => keyword: {self.keyword}, count: {self.count}, type_: {self.type_}>\n"

    def updateValues(self):
        self.objectValues = [
            self.keyword,
            self.count,
            self.type_
        ]
