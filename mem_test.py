from app import create_app

from app.copilot.memory import (
    add_user_memory,
    get_user_memories,
    should_store_memory
)


app = create_app()


with app.app_context():

    user_id = 3

    print("\n==============================")
    print("MEMORY FILTER TEST")
    print("==============================")

    messages = [
        "hello",
        "Find me a Logitech mouse",
        "I usually buy electronics under ₹1500",
        "I prefer Logitech products"
    ]

    for message in messages:

        print(
            message,
            "->",
            should_store_memory(message)
        )


    print("\n==============================")
    print("ADDING TEST MEMORY")
    print("==============================")

    add_user_memory(
        user_id,
        "I usually buy electronics under ₹1500."
    )

    print("Memory added.")


    print("\n==============================")
    print("RETRIEVING MEMORIES")
    print("==============================")

    memories = get_user_memories(
        user_id
    )

    for memory in memories:

        print(
            "-",
            memory
        )