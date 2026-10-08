import json
import os
from dotenv import load_dotenv
from common.LoadModel import LoadModel
from common.LoadChromaConn import LoadChromaConn
from common.LoadRerankerModel import LoadRerankerModel
from chat.utils.PrintLogUtil import print_log
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda,RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from chat.utils import BM25Rank
from chat.dao import HistoryDao
from chat.utils import SummaryList
from chat.dao import SummaryDao
from common.LoadAgent import ChatAgent

load_dotenv()

def intent(question, history_list=None, summary_list=None):
    llm = LoadModel().llm()
    history_list = history_list or []
    summary_list = summary_list or []
    prompt = f"""
        # 角色
        你是一个严格的 JSON 输出接口，负责两步任务：
        第一步：结合历史对话，把用户问题中的指代词消解成具体对象；
        第二步：判断消解后的用户意图属于 chat / agent / rag 三者中的哪一类。

        # 输入
        【历史摘要记录】（多轮对话的压缩摘要）
        {summary_list}

        【历史对话片段】（最近几轮的原始问答）
        {history_list}

        【用户当前问题】
        {question}

        # 第一步：指代消解规则
        1. 识别用户问题中的指代词、省略句，例如：
           - 指代：这、那、它、这个、那个、这个期刊、上面说的、前面提到的
           - 省略：那再算一下、还要多久、换成别的呢（缺主语）
           - 延续：继续、还有吗、换成……呢
           - 追问：为什么、具体呢、有例外吗
        2. 结合【历史摘要记录】优先、【历史对话片段】辅助，把指代词替换成历史中出现过的具体对象。
        3. 若无法从历史中确定指代对象，保持原句不动。
        4. 消解后的问题必须是一句完整、可独立理解的话。

        # 第二步：三类意图判定规则

        ## 类别一：rag（SCI 期刊知识问答）
        满足以下任一：
        1. 明确出现 SCI、SCIE、Web of Science、WoS、JCR、影响因子、分区、一区/二区、预警名单、特刊、专刊等关键词。
        2. 涉及 SCI 期刊的投稿、选刊、审稿、录用、见刊、检索、版面费、撤稿、评价等行为。
        3. 询问某期刊是否为 SCI/SCIE、是否被 WoS 收录、影响因子或分区。
        4. 核心目标为 SCI 论文发表、SCI 检索、SCI 选刊、SCI 期刊评价。
        5. 消解指代后，问题指向了历史中讨论过的 SCI 期刊话题。

        ## 类别二：agent（发送邮件 / 通知 / 消息）
        满足以下任一：
        1. 明确表达"发邮件 / 发通知 / 发消息 / 通知某人 / 告诉某人 / 给某人发邮件"。
        2. 涉及邮件主题、正文、收件人的描述。
        3. 指代消解后，问题指向了"把某内容发给某人"。

        ## 类别三：chat（普通闲聊）
        满足以下任一：
        1. 与 SCI 期刊、发邮件都无关（寒暄、生活、情感、编程、娱乐等）。
        2. 询问天气、时间、心情、身份等日常话题。
        3. 消解后依然无法归入 rag 或 agent。

        # 输出要求（必须严格遵守）
        - 只输出一个 JSON 对象，不输出任何解释、分析、思考、前后缀、代码块。
        - 输出必须能被 json.loads() 直接解析。
        - 不要使用 ```json 代码块包裹。
        - 字段固定为 "intent" 和 "resolved_question"。
        - "intent" 值只能是 "chat" / "agent" / "rag" 三者之一（小写字符串）。
        - "resolved_question" 为消解后的完整问题字符串；若无需消解，则原样返回用户问题。

        # 输出格式（唯一合法）
        {{"intent": "rag", "resolved_question": "消解后的完整问题"}}
        {{"intent": "agent", "resolved_question": "消解后的完整问题"}}
        {{"intent": "chat", "resolved_question": "消解后的完整问题"}}

        # 示例
        Q: 这个期刊是 SCI 几区？
        A: {{"intent": "rag", "resolved_question": "这个期刊是 SCI 几区？"}}

        Q: 帮我推荐几个容易中的 SCI 期刊。
        A: {{"intent": "rag", "resolved_question": "帮我推荐几个容易中的 SCI 期刊。"}}

        Q: 帮我给张三发封邮件，主题是会议通知。
        A: {{"intent": "agent", "resolved_question": "帮我给张三发封邮件，主题是会议通知。"}}

        Q: 通知老板明天开会。
        A: {{"intent": "agent", "resolved_question": "通知老板明天开会。"}}

        Q: 今天天气怎么样？
        A: {{"intent": "chat", "resolved_question": "今天天气怎么样？"}}

        Q: 你好呀。
        A: {{"intent": "chat", "resolved_question": "你好呀。"}}

        Q: 那它的影响因子是多少？（历史在讨论某 SCI 期刊）
        A: {{"intent": "rag", "resolved_question": "那本 SCI 期刊的影响因子是多少？"}}

        # 现在判断
        用户当前问题：{question}
        输出：
    """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": question},
    ]
    rs = llm.invoke(messages)
    try:
        return json.loads(rs.content)
    except json.JSONDecodeError:
        print("intent 解析失败：", rs.content)
        return {"intent": "chat", "resolved_question": question}

def chat(question:str,historyId:int, token):
    history_list = []
    summary_list = []
    history_pair = []
    if  historyId:
        history_talk = HistoryDao.query_history_by_historyid(historyId)
        history_list = SummaryList.build_history_text(history_talk)
        s_list = history_list[:-4]
        if s_list:
            summary_list = SummaryDao.query_summary_memory(historyId)
        # summary = SummaryList.summary(history_list)
        # summary_list = json.loads(summary.content)["summary_list"]
        history_pair = history_list[-4:]
    intents = intent(question,history_list=history_pair,summary_list=summary_list)
    print(intents)
    is_sci = intents["intent"]
    if is_sci == "rag":
        vector = LoadChromaConn().load_chroma_conn()
        rerank_model = LoadRerankerModel().load_reranker_model()
        llm = LoadModel().llm()
        def reranker_res(doc):
            print_log(docs=doc, title="召回结果：")
            data = []
            for sentence in doc:
                data.append((question, sentence.page_content))
            reranker_scores = rerank_model.compute_score(data)[:5]
            index_docs = [i for i in range(len(reranker_scores))]
            index_docs.sort(key=lambda x: reranker_scores[x], reverse=True)
            res = [data[i] for i in index_docs][:5]
            print_log(docs=res,title="重排序结果：")
            return res
        qa_prompt = """
            你是一个专业的知识库问答助手。请优先依据【参考上下文】回答，并结合【历史对话片段】和【历史摘要】理解多轮语境。
            
            【回答优先级】
            1. 【参考上下文】是回答事实的唯一依据。
            2. 【历史对话片段】和【历史摘要】只用于理解指代、省略、追问关系和用户意图，不能作为新的事实来源。
            3. 若历史/摘要与参考上下文冲突，以参考上下文为准。
            4. 若参考上下文没有足够信息，直接回复：“根据当前参考资料，未找到相关信息”。不要编造、推测或使用外部知识。
            
            【历史与摘要的使用方式】
            - 当用户问题中出现“它、这个、上述、继续、那呢、刚才说的”等指代或省略时，请结合历史/摘要还原用户真正想问的内容，再基于参考上下文回答。
            - 历史/摘要中已确认且与参考上下文一致的信息，可用于保持回答连贯；但关键事实仍必须由参考上下文支持。
            - 不要输出内部还原过程，除非用户明确要求。
            
            【回答规范】
            - 直接回答问题，简洁聚焦，不要开场白、寒暄、总结或无关背景。
            - 若【参考上下文】中片段带有编号，请在关键事实、数据、定义或结论后标注来源，如 [片段1]；综合多个片段时标注 [片段1][片段3]。
            - 若上下文存在矛盾，优先采用更具体、更新的内容，并简要说明差异。
            - 若只能部分回答，只回答有依据的部分，并明确说明剩余部分无依据。
            - 代码、命令、专有名词保持原文大小写与格式。
            - 保持客观中立，不进行主观评价或情感渲染。
            
            【历史对话片段】
            {history}
            
            【历史摘要】
            {summary}
            
            【参考上下文】
            {context}
            
            【用户问题】
            {question}
        """
        prompt = PromptTemplate(template=qa_prompt,input_variables=["history","summary","context","question"])
        qa_chain = (
            RunnableParallel({
                "history": RunnableLambda(lambda _: history_pair),
                "summary": RunnableLambda(lambda _: summary_list),
                "context": RunnableLambda(hybird) | RunnableLambda(reranker_res),
                "question": RunnablePassthrough()
            })
            | prompt
            | llm
            | StrOutputParser()
        )
        for c in qa_chain.stream(question):
            if c:
                yield c
        new_summary = SummaryList.summary(history_list)
        print(f"摘要内容是：{new_summary}")
        try:
            new_summary_list = json.loads(new_summary.content).get("summary_list", [])
        except (json.JSONDecodeError, AttributeError):
            new_summary_list = []
        # new_summary_list = json.loads(new_summary.content)["summary_list"]
        SummaryDao.save_summary_memory(historyId,new_summary_list)
    elif is_sci == "agent":
        agent = ChatAgent()
        for rs in agent.chat(question, token, history_pair, summary_list):
            yield rs
        new_summary = SummaryList.summary(history_list)
        print(f"摘要内容是：{new_summary}")
        try:
            new_summary_list = json.loads(new_summary.content).get("summary_list", [])
        except (json.JSONDecodeError, AttributeError):
            new_summary_list = []
        # new_summary_list = json.loads(new_summary.content)["summary_list"]
        SummaryDao.save_summary_memory(historyId,new_summary_list)
    elif is_sci == "chat":
        llm = LoadModel().llm()
        prompt = f"""
            你是一个自然、友好的中文对话助手。你的目标是像正常聊天一样回答用户当前问题，同时合理利用历史信息保持上下文连贯。
            【可用信息】
            1. 你的内部知识：通用知识、常识、推理、创作、建议、闲聊等。
            2. 【历史摘要对话记录】：对之前多轮对话的压缩记忆，用于了解用户偏好、已确认事实、任务状态、决定和未解决问题。
            3. 【历史对话记录片段】：上一轮对话的片段，用于理解当前问题的指代和上下文。

            【使用原则】
            - 历史信息是辅助，不是回答范围的限制。不要因为历史摘要或历史片段里没有写，就拒绝回答普通问题。
            - 即使【历史摘要对话记录】和【历史对话记录片段】为空，或与当前问题无关，也要像正常聊天一样回答当前问题。
            - 如果当前问题是通用知识、闲聊、解释、建议、创作、观点等，直接使用你的内部知识正常回答。
            - 如果当前问题涉及用户个人信息、偏好、之前决定、任务状态、已确认事实，优先以历史摘要或历史片段为准，不要用内部知识编造或覆盖。
            - 如果历史信息与内部知识冲突，涉及用户个人事实时以历史信息为准；通用知识问题以准确知识为准。
            - 如果历史中没有相关信息，不要编造用户个人事实；但可以正常提供通用回答，必要时简短说明“我这边没有相关记录”。
            - 不要在回答中罗列、复述或展示【历史摘要对话记录】或【历史对话记录片段】。除非用户明确要求回顾历史。
            - 不要输出“无法回答”后再列出摘要。

            【指代与上下文】
            - 遇到“它”“这个”“那件事”“继续”“还有吗”等指代或省略表达时，优先从【历史对话记录片段】和【历史摘要对话记录】中找指代对象。
            - 省略：如"那再算一下""还要多久"等缺主语的问法，需结合上一条摘要补全，以及【历史对话记录片段】回答。
            - 延续：如"继续""还有吗""换成……呢"等，需接续上一条摘要的主题。
            - 追问：如"为什么""具体呢""有例外吗"等，需围绕最近一条相关摘要展开。
            - 能找到就自然接续回答。
            - 找不到时，如果当前问题可以独立理解，就按独立问题正常回答；如果无法独立理解，简短询问澄清，例如“你指的是哪件事？”不要列摘要，也不要直接拒绝回答。

            【回答风格】
            - 像正常聊天一样自然、直接、简洁。
            - 不要机械地说“根据摘要”“根据历史记录”等内部机制，除非用户明确问“你记得什么”。
            - 数字、专名、时间等如果来自历史，保持与历史一致。
            - 不要输出开场白、寒暄或无关背景，除非用户就是在闲聊。

            【输出格式】
            直接输出回答文本，不要 JSON，不要 Markdown 代码块，不要输出思考过程。

            【历史对话记录片段】
            {history_pair}

            【历史摘要对话记录】
            {summary_list}

            【当前问题】
            {question}
            """
        for c in llm.stream(prompt):
            if c.content:
                yield c.content
        new_summary = SummaryList.summary(history_list)
        try:
            new_summary_list = json.loads(new_summary.content).get("summary_list", [])
        except (json.JSONDecodeError, AttributeError):
            new_summary_list = []
        # new_summary_list = json.loads(new_summary.content)["summary_list"]
        SummaryDao.save_summary_memory(historyId,new_summary_list)

def hybird(question: str):
    b = BM25Rank.bm25_rank(question)
    v = BM25Rank.vector_rank(question)
    return BM25Rank.fuse(v, b)

if __name__ == '__main__':
    q = "sci中有哪些适合深度学习投递的期刊"
    q1 = "我叫zs,我今年18岁"
    q2 = "我今年几岁"
    q3 = "给3335281906@qq.com发送邮件，通知他今晚上加班到10点"
    for c in chat(q3,1):
        print(c,end="")