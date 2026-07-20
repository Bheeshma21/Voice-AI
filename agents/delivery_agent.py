from rag.retriever import retrieve


class DeliveryAgent:

    def handle(self, query):

        context = retrieve(query)

        return context