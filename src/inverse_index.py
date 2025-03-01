import thulac
import math

thulac_model = thulac.thulac(seg_only=True, filt=True)


def _word_split(text):
    return thulac_model.cut(text)


class InverseIndex:
    def __init__(self):
        self.i_index = {}
        self.doc_count = 0

    def add_document(self, doc_id: str, doc: str):
        words = _word_split(doc)
        for w in words:
            word, tag = w
            if word not in self.i_index:
                self.i_index[word] = set()
            self.i_index[word].add(doc_id)
        self.doc_count += 1

        return words

    def get(self, word: str):
        if word in self.i_index:
            return self.i_index[word]
        return set()

    def idf(self, word: str):
        if word in self.i_index:
            return math.log(self.doc_count / len(self.i_index[word]))
        return 0
    
    def to_json(self):
        return {
            "i_index": self.i_index,
            "doc_count": self.doc_count
        }
    
    @classmethod
    def from_json(cls, json_obj):
        index = cls()
        index.i_index = json_obj["i_index"]
        index.doc_count = json_obj["doc_count"]
        return index


if __name__ == "__main__":
    index = InverseIndex()
    index.add_document("doc1", "我爱北京天安门")
    index.add_document("doc2", "天安门上太阳升")
    index.add_document("doc3", "我爱北京天安门")
    index.add_document("doc4", "太阳升，北京天安门")
    print(index.get("天安门"))
    print(index.idf("天安门"))
    print(index.get("北京"))
    print(index.idf("北京"))
    print(index.get("我"))