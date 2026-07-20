from agents.graph import build_graph


app = build_graph()


result = app.invoke(
    {
        "query": "What is cancellation policy?",
        "response": ""
    }
)


print(result["response"])