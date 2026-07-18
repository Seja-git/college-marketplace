#for recommendation

# from utils.recommendation import recommend

# result=recommend(25)
# print(result)

# from utils.semantic_search import search

# print(search("ardino uno"))


from utils.description_generator import generate_description


description = generate_description(
    title="Arduino Uno R3",
    category="Electronics",
    condition="Excellent",
    price=650,
    details="""
Used for one semester.
USB cable included.
Reason for selling: Course completed.
"""
)

print("=" * 60)
print("Generated Description")
print("=" * 60)
print(description)