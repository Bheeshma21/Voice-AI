from rag.retriever import retrieve


class ProductAgent:

    def handle(self, query):

        context = retrieve(query)

        return context