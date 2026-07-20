from rag.retriever import retrieve


class OrderAgent:

    def handle(self, query):

        context = retrieve(query)

        return context