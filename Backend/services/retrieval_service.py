from services.index_service import get_index

def retrieve_docs(question, top_k=5):
    index = get_index()
    retriever = index.as_retriever(similarity_top_k=top_k)
    return retriever.retrieve(question)