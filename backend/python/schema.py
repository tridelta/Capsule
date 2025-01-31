import jieba
from utils import _get_random_id

class Atom:
    def __init__(self, title, contents):
        self.id = "0x" + _get_random_id()
        self.title = title
        self.contents = contents
        self.tags = []
        self.transcriptions = []
    
    def add_tag(self, tag):
        self.tags.append(tag)

    def auto_tag(self):
        # 结巴分词带词性标注
        words = pseg.cut(self.contents)
        
        # 定义需要保留的词性（可根据需求调整）
        KEEP_FLAGS = {
            'n',  # 名词
            'v',  # 动词
            'a',  # 形容词
            'nr', # 人名
            'ns', # 地名
            'nt', # 机构团体
            'nz', # 其他专名
            'eng' # 英文
        }

        # 过滤停用词性和单字词
        meaningful_words = [
            word.word for word in words 
            if word.flag in KEEP_FLAGS 
            and len(word.word) > 1
        ]

        # 去重后添加为标签
        self.tags += list(set(meaningful_words))

    