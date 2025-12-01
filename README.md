# week2-challenge

## Task 1: Data Collection and Preprocessing

### Data Collection
We used the `google-play-scraper` Python library to collect user reviews from the Google Play Store for three Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Awash Bank
- Amhara Bank

For each bank, we targeted at least 400 reviews, collecting the following fields:
- Review text
- Rating
- Date
- Bank name
- Source (Google Play)

The scraping script (`Scripts/scraper.py`) fetches the latest reviews, handles retries, and saves the raw data to `data/raw/reviews_raw.csv`.

### Preprocessing
The preprocessing script (`Scripts/preprocessing.py`) performs the following steps:
- Removes duplicates and handles missing data (critical columns: review text, rating, bank name)
- Normalizes date formats to `YYYY-MM-DD`
- Cleans review text (removes extra whitespace, trims)
- Validates ratings (ensures values are between 1 and 5)
- Adds text length and date breakdown columns
- Saves the cleaned data to `data/processed/reviews_processed.csv`

#### Data Quality
- Data retention rate: 100%
- Final dataset: 983 reviews (400 CBE, 400 Awash, 183 Amhara Bank)
- <5% missing data in critical fields

---
Proceeding to Task 2: Sentiment and Thematic Analysis.