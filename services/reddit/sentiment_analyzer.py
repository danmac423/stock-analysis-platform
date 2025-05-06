from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
        )
        self.labels = ["negative", "neutral", "positive"]

    def analyze(self, text: str) -> str:
        if not text or text.strip() in ("[removed]", "[deleted]"):
            return "neutral"
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        scores = outputs.logits.softmax(dim=1).numpy()[0]
        return self.labels[scores.argmax()]