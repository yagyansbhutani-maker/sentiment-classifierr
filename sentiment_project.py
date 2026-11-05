import csv
import anthropic

client = anthropic.Anthropic()  # reads your key automatically
MODEL = "claude-haiku-5-5"

# Your answer key: (review, correct label)
REVIEWS = [
    ("Amazing food, will come back!", "Positive"),
    ("Worst service ever.", "Negative"),
    ("It was okay, nothing special.", "Neutral"),
    ("Battery lasts all day, love it.", "Positive"),
    ("Arrived broken and support ignored me.", "Negative"),
    ("Average movie, some good parts, some boring.", "Neutral"),
    ("Great, it stopped working after one day.", "Negative"),
    ("Fast delivery but the quality is poor.", "Neutral"),
    ("Best purchase I've made this year.", "Positive"),
    ("Not bad at all.", "Positive"),
]

# Prompt A: simple instruction only
PROMPT_A = (
    "Classify the review as Positive, Negative, or Neutral. "
    "Reply with only the label.\n"
    "Review: {review}"
)

# Prompt B: same instruction plus examples
PROMPT_B = (
    "Classify the review as Positive, Negative, or Neutral. "
    "Reply with only the label.\n"
    'Examples: "Amazing food" = Positive. "Worst service ever" = Negative. '
    '"It was okay" = Neutral.\n'
    "Review: {review}"
)


def classify(prompt_template, review):
    """Send one review to the AI and return its one-word answer."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt_template.format(review=review)}],
    )
    answer = response.content[0].text.strip().replace(".", "")
    return answer.capitalize()


def main():
    rows = []
    score_a = 0
    score_b = 0

    for review, correct in REVIEWS:
        a = classify(PROMPT_A, review)
        b = classify(PROMPT_B, review)
        score_a += a == correct
        score_b += b == correct
        rows.append([review, correct, a, b])
        print(f"{review[:40]:40} | {correct:8} | A: {a:8} | B: {b:8}")

    total = len(REVIEWS)
    print()
    print(f"Prompt A score: {score_a}/{total} ({score_a / total:.0%})")
    print(f"Prompt B score: {score_b}/{total} ({score_b / total:.0%})")

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Review", "Correct", "Prompt A", "Prompt B"])
        writer.writerows(rows)
    print("\nSaved results to results.csv")

    with open("results_table.md", "w", encoding="utf-8") as f:
        f.write("| # | Review | Correct | Prompt A | Prompt B |\n")
        f.write("|---|---|---|---|---|\n")
        for i, (review, correct, a, b) in enumerate(rows, start=1):
            f.write(f"| {i} | {review} | {correct} | {a} | {b} |\n")
        f.write(f"\n**Prompt A score:** {score_a}/{total}  \n")
        f.write(f"**Prompt B score:** {score_b}/{total}\n")
    print("Saved README-ready table to results_table.md")


if __name__ == "__main__":
    main()
