"""
Sentiment and Thematic Analysis Script
Task 2: Sentiment and Theme Extraction

This script computes sentiment scores using VADER and extracts keywords/themes using TF-IDF and spaCy.
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import os
from config import DATA_PATHS

# Load spaCy English model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import subprocess
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
    nlp = spacy.load('en_core_web_sm')

class SentimentThemeAnalyzer:
    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['processed_reviews']
        self.output_path = output_path or DATA_PATHS['sentiment_results']
        self.df = None
        self.analyzer = SentimentIntensityAnalyzer()

    def load_data(self):
        self.df = pd.read_csv(self.input_path)
        print(f"Loaded {len(self.df)} reviews for analysis.")

    def compute_sentiment(self):
        print("\n[1/3] Computing sentiment scores with VADER...")
        def get_sentiment(row):
            text = str(row['review_text'])
            score = self.analyzer.polarity_scores(text)
            compound = score['compound']
            if compound >= 0.05:
                label = 'positive'
            elif compound <= -0.05:
                label = 'negative'
            else:
                label = 'neutral'
            return pd.Series({'sentiment_score': compound, 'sentiment_label': label})
        sentiment_df = self.df.apply(get_sentiment, axis=1)
        self.df = pd.concat([self.df, sentiment_df], axis=1)
        print("Sentiment analysis complete.")

    def extract_keywords(self, top_n=10):
        print("\n[2/3] Extracting keywords with TF-IDF...")
        tfidf = TfidfVectorizer(max_features=top_n, stop_words='english')
        keywords = {}
        for bank in self.df['bank_name'].unique():
            texts = self.df[self.df['bank_name'] == bank]['review_text'].astype(str)
            tfidf_matrix = tfidf.fit_transform(texts)
            feature_names = tfidf.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            top_keywords = [feature_names[i] for i in scores.argsort()[::-1][:top_n]]
            keywords[bank] = top_keywords
        self.keywords = keywords
        print("Keywords extracted per bank:")
        for bank, kw in keywords.items():
            print(f"  {bank}: {', '.join(kw)}")

    def extract_themes(self):
        print("\n[3/3] Grouping keywords into themes...")
        # Simple rule-based grouping for demonstration
        theme_map = {
            'login': 'Account Access Issues',
            'error': 'Account Access Issues',
            'slow': 'Transaction Performance',
            'transfer': 'Transaction Performance',
            'ui': 'User Interface & Experience',
            'interface': 'User Interface & Experience',
            'support': 'Customer Support',
            'help': 'Customer Support',
            'feature': 'Feature Requests',
            'request': 'Feature Requests',
        }
        themes = {}
        for bank, kw_list in self.keywords.items():
            bank_themes = set()
            for kw in kw_list:
                for key, theme in theme_map.items():
                    if key in kw:
                        bank_themes.add(theme)
            if not bank_themes:
                bank_themes.add('Other')
            themes[bank] = list(bank_themes)
        self.themes = themes
        print("Themes identified per bank:")
        for bank, th in themes.items():
            print(f"  {bank}: {', '.join(th)}")

    def save_results(self):
        self.df.to_csv(self.output_path, index=False)
        print(f"\nResults saved to: {self.output_path}")

    def run(self):
        self.load_data()
        self.compute_sentiment()
        self.extract_keywords()
        self.extract_themes()
        self.save_results()

if __name__ == "__main__":
    analyzer = SentimentThemeAnalyzer()
    analyzer.run()
