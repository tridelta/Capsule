import json
import re


def summerize_atom(atom, ask_ai: callable):
    prompt = """
请阅读以下内容，并总结出有关信息：
- 内容类型，即这个内容在陈述什么？一个事件？一个人物？还是其他？
- 建议的标题
- 内容标签，使用**不多于10个**文章中的词/概括总结的词语来描述内容。要求能完全概括，且尽量使用常用词汇，尽量少包含专有名词。更具有概括性的标签在前，更不具有概括性的在后。
- 有关的事件（文段中出现的事件专有名词/事件概要）
- 有关的人物（文段中的明确人名/外号）
总结之后，请以纯json形式输出有关信息。请不要输出除json以外的内容（e.g. '```')
你的输出（json）格式如下：
{
  "type": "event/people/other",
  "title": "suggested title",
  "tags": ["tag1(from doc or summerized)", "tag2", "...", "tag10"],
  "rel_events": ["event name 1", "..."],
  "rel_people": ["people name 1", "..."]
}

内容文段如下：
"""
    contents = atom.get_full_contents()
    prompt += f"<TITLE: {atom.title}>" + contents

    result = ask_ai(prompt)

    # Remove any code block markers or non-JSON content
    result = re.sub(r"```json|```", "", result).strip()

    # Parse the JSON to validate it
    json_result = json.loads(result)
    return json_result
