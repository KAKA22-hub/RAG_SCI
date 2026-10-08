from common.LoadModel import LoadModel
from chat.dao import HistoryDao
import json

def build_history_text(history_list:list):
    history_text = []
    for item in history_list:
        history_text.append(
            {"role":"user","content":item["question"]}
        )
        history_text.append(
            {"role": "system", "content": item["answer"]}
        )
    return history_text

def summary(history_text:list):
    local_llm = LoadModel().local_load()
    prompt = f"""
        你是一个专业的对话记录摘要助手。你的所有输出必须且只能基于下方【参考上下文】中提供的问答记录，用于把整段对话压缩成可长期保存、可复原脉络的摘要。
        
        【输入说明】
        【参考上下文】是一段 Python 列表的字符串表示形式，列表中的元素是字典，每个字典包含 role 和 content 两个字段：
        - role 为 "user" 时，content 是用户提出的 question。
        - role 为 "system" 时，content 是助手给出的 answer。
        - 列表按问答先后顺序交替排列（user、system、user、system……）。
        - 你只能读取 role 和 content 的内容；列表中出现的单引号、双引号、括号、转义符等仅是字符串表示形式，不属于内容本身。
        
        【核心目标】
        把整段对话中所有用户问题的意图、所有助手回答的关键信息完整抽取出来，形成一份可用于长期记录的摘要。摘要要能让人在不看原文的情况下，复原这段对话问了什么、答了什么、结论是什么。
        
        【核心原则】
        1. 完整覆盖：每一轮有效问答都必须在摘要中有对应记录，不得跳过、不得只保留部分轮次。
        2. 忠实原文：摘要必须完全来源于【参考上下文】中 user 与 system 的内容，严禁使用外部知识、常识或训练数据补充、推测或编造内容。
        3. 保留关键信息：每轮摘要需尽量保留该轮的核心要素，包括主题、主体、时间、地点、目标、任务、决定、结论、重要数字、专有名词、法律条款编号、片段引用等。
        4. 精炼表达：删除寒暄、重复、语气词、无信息量的修饰，但保留所有有实际意义的内容；不得逐字复制整段长文，要压缩成要点式表达。
        5. 保持原意：不得对上下文内容进行过度解读、主观评价或情感渲染，保持客观中立。
        6. 明确说明：若【参考上下文】中不包含有效问答信息（如仅有寒暄、空转对话），请如实输出"无有效咨询内容"。
        
        【摘要规范】
        - 每一轮有效问答（一个 user 加一个 system）原则上生成一条摘要；若某轮答案很长、信息点很多，可拆成多条。
        - 每条摘要推荐格式为："用户询问了 X；助手答复了 Y，关键点包括 A、B、C。"
        - 摘要必须同时体现"用户问了什么"与"助手答了什么"，并保留该轮的核心结论、数字、专名、条件、例外、限制。
        - 对于法律、医疗、技术等专业内容，保留条款编号、片段引用编号（如 [片段1]）、金额、期限、比例等关键限定词。
        - 若多轮问答属于同一主题或存在连续追问，可合并为一条，但必须保留各轮新增的信息点。
        - 若上下文存在矛盾信息，优先采用更具体、更新的内容，并注明差异（如"最初为……，后更新为……"）。
        - 若某轮问答为寒暄或空转（如"你好""在吗""请提供问题"），可合并说明或忽略，不单独成条。
        - 数字、专名、时间词等保持原文大小写与格式不变，不要擅自换算相对时间。
        - 摘要条数不设固定上限，以完整覆盖对话内容为准；建议 3-20 条，长对话可适当增加。
        - 每条摘要长度不限，以把该轮关键信息说清为准，建议 30-150 字。
        
        【输出格式要求】
        1. 只输出合法 JSON，不要包含任何 Markdown 代码块。
        2. 所有内容中禁止使用反斜杠 \ 。如需表达路径或公式，用文字代替（如"二分之一"而不是"\frac{1}{2}"）。
        3. 如遇必须转义的字符，用双反斜杠 \\ 表示。
        只输出一个合法 JSON 对象，不要 Markdown，不要代码块，不要解释，不要输出思考过程。
        格式必须为：{{"summary_list": ["摘要内容1", "摘要内容2"]}}
        summary_list 必须是字符串数组，不要输出对象数组，不要输出额外字段。
        若【参考上下文】中无任何有效问答内容，输出：{{"summary_list": []}}
        再次强调：输出必须以 {{ 开头，以 }} 结尾，绝对不能有任何前缀、后缀、代码块标记、说明文字。
        
        【错误示例（禁止输出）】
        ```json
        {{"summary_list": ["用\\frac{{1}}{{2}}表示的路径C:\\Users"]}}

        【参考上下文】
        {history_text}
    """
    summary = local_llm.invoke(prompt)
    return summary

if __name__ == '__main__':
    history_list = HistoryDao.query_history_by_list(1)
    h = build_history_text(history_list)
    # print(h)
    summary_list = summary(h)
    s = json.loads(summary_list.content)
    print(s)
