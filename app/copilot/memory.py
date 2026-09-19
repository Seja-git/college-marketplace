import os

from dotenv import load_dotenv
from mem0 import MemoryClient


load_dotenv()


MEM0_API_KEY = os.getenv("MEM0_API_KEY")


if not MEM0_API_KEY:
    raise ValueError(
        "MEM0_API_KEY not found in .env file"
    )


memory = MemoryClient(
    api_key=MEM0_API_KEY
)


def add_user_memory(
    user_id: int,
    user_message: str
):
    """
    Store useful long-term information about a marketplace user.
    """

    result = memory.add(
        user_message,
        user_id=str(user_id)
    )

    return result



def get_user_memories(
    user_id: int
):
    """
    Retrieve long-term memories associated
    with the current marketplace user.
    """

    result = memory.search(
        query=(
            "shopping preferences, preferred products, "
            "budget preferences, categories, brands, "
            "condition preferences and marketplace behavior"
        ),
        filters={
            "user_id": str(user_id)
        }
    )

    memories = []

    # Mem0 may return a dictionary containing the results
    if isinstance(result, dict):

        results = result.get(
            "results",
            []
        )

    else:

        results = result

    for item in results:

        # Result is already a string
        if isinstance(item, str):

            memories.append(item)

        # Result is a dictionary
        elif isinstance(item, dict):

            memory_text = item.get(
                "memory"
            )

            if memory_text:
                memories.append(
                    memory_text
                )

    return memories


def should_store_memory(
    message: str
) -> bool:
    """
    Decide whether a user message is likely to contain
    a useful long-term marketplace preference.
    """

    keywords = [
        "i prefer",
        "i usually",
        "i like",
        "i don't like",
        "i dislike",
        "my budget",
        "i mostly buy",
        "i am interested in",
        "i'm interested in",
        "i want products",
        "i prefer products"
    ]

    message_lower = message.lower()

    return any(
        keyword in message_lower
        for keyword in keywords
    )