

def print_log(docs=None, title="召回的结果"):
    print(f"{title}:")
    for index, doc in enumerate(docs,start=1):
        print(f"第{index}个文档: {doc}")