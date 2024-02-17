from datasets import load_dataset

tr_news = load_dataset("mc4", "tr")

print(tr_news[0])