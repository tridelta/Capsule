from jieba import posseg as pseg
from .utils import _get_random_id, _get_hash_id, _get_current_timestamp
from . import index
from . import FileService
from typing import List

"""声明"""


class Atom:
    pass


class Quark:
    pass


"""实现"""


class Atom:
    def __init__(self, title, contents: List[Quark]):
        """
        Atom 应有的字段:
          - id          str     唯一标识符
          - title       str     标题
          - last_modify str     最后修改时间
          - contents    list    内容(每个元素都是Quark)
          - tags        list    标签
        """
        self.id = "A-" + _get_random_id()
        self.title = title
        self.last_modify = _get_current_timestamp()
        self.contents = contents
        self.tags = []
        self.info = {}

    def add_tag(self, tag):
        self.tags.append(tag)

    def auto_tag(self):
        # 结巴分词带词性标注
        words = pseg.cut(self.get_full_contents())

        # 定义需要保留的词性(可根据需求调整)
        KEEP_FLAGS = {
            "n",  # 名词
            "v",  # 动词
            "a",  # 形容词
            "nr",  # 人名
            "ns",  # 地名
            "nt",  # 机构团体
            "nz",  # 其他专名
            "eng",  # 英文
        }

        # 过滤停用词性和单字词
        meaningful_words = [
            word.word
            for word in words
            if word.flag in KEEP_FLAGS and len(word.word) > 1
        ]

        # 去重后添加为标签
        self.tags += list(set(meaningful_words))

    def get_full_contents(self):
        contents = []
        for quark in self.contents:
            if quark.type == "text":
                contents.append(f"({quark.created_at})" + quark.content)
            elif quark.transcripts:
                for t in quark.transcripts:
                    contents.append(t["content"])

        return "\n".join(contents)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "last_modify": self.last_modify,
            "contents": [q.id for q in self.contents],
            "tags": self.tags,
            "info": self.info,
        }

    @classmethod
    def from_json(cls, json_obj):
        atom = cls(json_obj["title"], [])
        atom.id = json_obj["id"]
        atom.last_modify = json_obj["last_modify"]
        atom.contents = [index.QUARKS[q_id] for q_id in json_obj["contents"]]
        atom.tags = json_obj["tags"]
        atom.info = json_obj["info"]
        if 0:
            atom.tags = []
            atom.info = []
        return atom


class Quark:
    def __init__(self, content, type="text", transcripts=[]):
        """
        Quark 应有的字段:
          - id          str     唯一标识符
          - type        str     类型
          - content     str     内容
          - transcripts list    对非文本内容的解释，可以有很多个。
          - created_at  str     创建时间

        transcripts 的结构示例（每个元素）:
        {
            type: 'transcript/xxx',
            content: '<str>...'
        }
        """
        self.id = "Q-" + _get_hash_id(content)
        self.type = type
        self.transcripts = transcripts
        self.created_at = _get_current_timestamp()
        # save content
        if self.type == "text":
            self.content = content
        else:
            err = FileService.local.save_quark_content(self.id, content)
            if err != 0:
                raise Exception("Save Quark Content Error: " + str(err))
            self.content = "/quarkcontent/" + self.id

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "transcripts": self.transcripts,
            "created_at": self.created_at,
        }

    @staticmethod
    def load_content(content):
        if content.startswith("/quarkcontent/"):
            quark_id = content[len("/quarkcontent/") :]
            return FileService.local.get_quark_content(quark_id)
        else:
            return content

    @classmethod
    def from_json(cls, json_obj):
        quark = cls(
            Quark.load_content(json_obj["content"]),
            json_obj["type"],
            json_obj["transcripts"],
        )
        quark.id = json_obj["id"]
        quark.created_at = json_obj["created_at"]
        return quark


"""测试"""
if __name__ == "__main__":
    # NOTE FROM BH:az...你这auto tag把所有词都列出来了...没做完?
    atom = Atom(
        "Hello World", [Quark("Hello, World"), Quark("I am Bernie Huang at age 16")]
    )

    atom.auto_tag()
    print(atom.tags)
