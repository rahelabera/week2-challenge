"""
Task 4: Insights and Recommendations
This script generates insights, visualizations, and recommendations from the processed review data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
from config import DATA_PATHS

# Load data
DATA_FILE = DATA_PATHS['sentiment_results']
df = pd.read_csv(DATA_FILE)

# 1. Sentiment Distribution Plot
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='sentiment_label', hue='bank_name', order=['positive', 'neutral', 'negative'])
plt.title('Sentiment Distribution by Bank')
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.legend(title='Bank')
plt.tight_layout()
plt.savefig('Data/processed/sentiment_distribution.png')
plt.close()

# 2. Rating Distribution Plot
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='rating', hue='bank_name', order=[5,4,3,2,1])
plt.title('Rating Distribution by Bank')
plt.xlabel('Rating')
plt.ylabel('Number of Reviews')
plt.legend(title='Bank')
plt.tight_layout()
plt.savefig('Data/processed/rating_distribution.png')
plt.close()

# 3. Word Cloud for Each Bank
for bank in df['bank_name'].unique():
    text = ' '.join(df[df['bank_name'] == bank]['review_text'].astype(str))
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud for {bank}')
    plt.tight_layout()
    plt.savefig(f'Data/processed/wordcloud_{bank.replace(" ", "_").lower()}.png')
    plt.close()

# 4. Insights and Recommendations (printed)
def get_insights(df):
    insights = {}
    for bank in df['bank_name'].unique():
        bank_df = df[df['bank_name'] == bank]
        # Drivers: Most common positive words
        pos_reviews = bank_df[bank_df['sentiment_label'] == 'positive']['review_text']
        drivers = pd.Series(' '.join(pos_reviews).lower().split()).value_counts().head(3).index.tolist()
        # Pain points: Most common negative words
        neg_reviews = bank_df[bank_df['sentiment_label'] == 'negative']['review_text']
        pains = pd.Series(' '.join(neg_reviews).lower().split()).value_counts().head(3).index.tolist()
        # Recommendations (simple rule-based)
        recs = [f"Improve: {pains[0]}" if pains else "Improve app reliability", f"Enhance: {drivers[0]}" if drivers else "Enhance user experience"]
        insights[bank] = {'drivers': drivers, 'pain_points': pains, 'recommendations': recs}
    return insights

insights = get_insights(df)

with open('Data/processed/insights.txt', 'w', encoding='utf-8') as f:
    for bank, info in insights.items():
        f.write(f"Bank: {bank}\n")
        f.write(f"  Drivers: {', '.join(info['drivers'])}\n")
        f.write(f"  Pain Points: {', '.join(info['pain_points'])}\n")
        f.write(f"  Recommendations: {', '.join(info['recommendations'])}\n\n")

print("Insights and visualizations generated in Data/processed/.")
