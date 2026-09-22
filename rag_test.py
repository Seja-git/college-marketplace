from app.copilot.rag import (
    retrieve_knowledge,
    get_rag_context
)


print("\n==============================")
print("RAG TEST")
print("==============================")


queries = [
    "What should I check before buying a used product?",
    "How should I create a good listing?",
    "How should I negotiate the price?",
    "What should users know about marketplace safety?"
]


for query in queries:

    print("\n------------------------------")
    print("QUERY:")
    print(query)

    results = retrieve_knowledge(
        query,
        top_k=2
    )

    for result in results:

        print(
            "\nSOURCE:",
            result["source"]
        )

        print(
            "SCORE:",
            result["score"]
        )


print("\n==============================")
print("RAG CONTEXT")
print("==============================")

context = get_rag_context(
    "What should I check before buying a used laptop?",
    top_k=2
)

print(context)