from Tests.check import checkpoint

sen = input("Enter a sentence: ")
replacements = checkpoint(sen)
print("Suggestions for replacements:")
for mistake, suggestions in replacements.items():
    print(f"Mistake: {mistake}")
    for rank, suggestion in enumerate(suggestions, 1):
        print(f"    Rank {rank}: {suggestion}")