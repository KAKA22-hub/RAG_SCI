import jieba
from neo4j_graphrag.components.graph_pruning import PrunedItem
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from common.LoadChromaConn import LoadChromaConn

STOP_WORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
    "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会",
    "着", "没有", "看", "好", "自己", "这", "那", "他", "她", "它", "们",
    "这个", "那个", "什么", "哪", "怎么", "吗", "呢", "吧", "啊", "哦",
    "还", "被", "把", "让", "从", "对", "与", "但", "而", "或", "所",
    "为", "以", "及", "可", "可以", "能", "能够", "应该", "需要", "已经",
    "虽然", "如果", "因为", "所以", "只是", "还是", "不过", "然后",
    "之", "其", "中", "等", "等等", "即", "使", "向", "将", "按", "当",
    "于", "由", "比", "除了", "关于", "以及", "并且", "此外", "另外",
    "过", "着", "来", "去", "做", "作", "像", "如", "如同", "由于",
])

def tokenize(text):
    data = []
    tokens = list(jieba.lcut(text))
    for item in tokens:
        if item in STOP_WORDS or len(item.strip()) == 0:
            continue
        data.append(item)
    return data

def bm25_rank(question):
    vector = LoadChromaConn().load_chroma_conn()
    data = vector.get()
    ids = data['ids']
    documents = data['documents']
    metadatas = data['metadatas']
    bm25_docs = [Document(id=ids[index], page_content=documents[index], metadata=metadatas[index]) for index in
                 range(len(ids))]

    tokenizer = [tokenize(doc) for doc in documents]
    q_tokenizer = tokenize(question)
    bm25 = BM25Okapi(tokenizer)
    bm25_scores = bm25.get_scores(q_tokenizer)
    bm25_indies = sorted(range(len(bm25_scores)),key= lambda x: bm25_scores[x], reverse=True)[:10]
    res = [bm25_docs[index] for index in bm25_indies]
    return res

def vector_rank(question):
    vector = LoadChromaConn().load_chroma_conn()
    vector_retriever = vector.as_retriever(search_kwargs={"k":10})
    rank = vector_retriever.invoke(question)
    return rank

def fuse(v_data,b_data):
    docs = {}
    res = []
    for item in v_data:
        docs[item.id] = item.page_content
    for item in b_data:
        docs[item.id] = item.page_content
    doc = [Document(id=key, page_content=value) for (key, value) in docs.items()]
    return doc

if __name__ == '__main__':
    q = "大类分区为一区的计算机相关期刊有哪些？"
    bm25 = bm25_rank(q)
    r = vector_rank(q)
    res = fuse(bm25,r)
    print(res)
