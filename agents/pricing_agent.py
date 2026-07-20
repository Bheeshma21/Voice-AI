from rag.retriever import retrieve


class PricingAgent:

    def handle(self, query):

        context = retrieve(query)

        return context