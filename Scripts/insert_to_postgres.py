"""
PostgreSQL Insertion Script
Task 3: Store Cleaned Data in PostgreSQL

This script creates the required tables and inserts the processed review data into a PostgreSQL database.
"""
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import os
from config import DATA_PATHS

# Database connection parameters (edit as needed or use environment variables)
DB_NAME = os.getenv('POSTGRES_DB', 'bank_reviews')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'postgres')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

# Table creation SQL
BANKS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100)
);
"""
REVIEWS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50)
);
"""

# Load processed data
reviews_path = DATA_PATHS['sentiment_results']
df = pd.read_csv(reviews_path)

# Connect to PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
with engine.connect() as conn:
    # Create tables
    conn.execute(text(BANKS_TABLE_SQL))
    conn.execute(text(REVIEWS_TABLE_SQL))

    # Insert banks and get their IDs
    bank_names = df['bank_name'].unique()
    bank_id_map = {}
    for bank in bank_names:
        # Insert or get bank_id
        result = conn.execute(text("INSERT INTO banks (bank_name, app_name) VALUES (:name, :app) ON CONFLICT (bank_name) DO UPDATE SET bank_name=EXCLUDED.bank_name RETURNING bank_id"), {"name": bank, "app": bank})
        bank_id = result.scalar() or conn.execute(text("SELECT bank_id FROM banks WHERE bank_name=:name"), {"name": bank}).scalar()
        bank_id_map[bank] = bank_id

    # Prepare review records
    review_records = []
    for _, row in df.iterrows():
        review_records.append({
            'review_id': str(row['review_id']),
            'bank_id': bank_id_map[row['bank_name']],
            'review_text': row['review_text'],
            'rating': int(row['rating']),
            'review_date': row['review_date'],
            'sentiment_label': row['sentiment_label'],
            'sentiment_score': float(row['sentiment_score']),
            'source': row['source']
        })

    # Insert reviews
    for rec in review_records:
        try:
            conn.execute(text("""
                INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
                VALUES (:review_id, :bank_id, :review_text, :rating, :review_date, :sentiment_label, :sentiment_score, :source)
                ON CONFLICT (review_id) DO NOTHING
            """), rec)
        except Exception as e:
            print(f"Error inserting review {rec['review_id']}: {e}")

print("Data insertion complete. Verify your PostgreSQL database for results.")
