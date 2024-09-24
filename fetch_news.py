import spacy
from geopy.geocoders import Nominatim
from pymongo import MongoClient
import requests
import os
import re
import streamlit as st
import pandas as pd
from spacy.training import Example

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Configuration
api_key = os.getenv('NEWS_API_KEY', 'NEWS_API')
news_url = (
    f'https://newsapi.org/v2/everything?q=("natural+disaster"+OR+earthquake+OR+tsunami+OR+landslide+OR+flood+OR+wildfire+OR+hurricane)'
    f'+AND+India&language=en&sortBy=publishedAt&apiKey={api_key}'
)
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
database_name = 'news_db'
collection_name = 'disasters_news'

geolocator = Nominatim(user_agent="disaster_locator", timeout=10)

disaster_keywords = {
    'natural disaster': 'General',
    'earthquake': 'Earthquake',
    'tsunami': 'Tsunami',
    'landslide': 'Landslide',
    'flood': 'Flood',
    'wildfire': 'Wildfire',
    'hurricane': 'Hurricane',
    'cyclone': 'Cyclone',
    'storm': 'Storm',
    'drought': 'Drought',
    'volcano': 'Volcano'
}

# Preprocess text by converting to lowercase and removing special characters
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

# Extract possible locations using spaCy NER
def extract_location(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    return locations

# Geocode the location name to coordinates
def geocode_location(location_name):
    try:
        location = geolocator.geocode(location_name)
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
    except Exception as e:
        st.write(f"Error geocoding location {location_name}: {e}")
    return None

# Identify disaster type using keyword matching and context
def identify_disaster_type(title, description, content):
    for keyword, disaster_type in disaster_keywords.items():
        if keyword in title or keyword in description or keyword in content:
            return disaster_type
    return 'Unknown'

# Filter function to check if an article is related to natural disasters and find its type
def is_relevant_article(article):
    title = preprocess_text(article.get('title', ''))
    description = preprocess_text(article.get('description', ''))
    content = preprocess_text(article.get('content', ''))
    
    disaster_type = identify_disaster_type(title, description, content)
    if disaster_type != 'Unknown':
        article['disaster_type'] = disaster_type  # Add disaster type to the article
        return True
    return False

def fetch_and_store_news():
    client = None
    try:
        response = requests.get(news_url)
        response.raise_for_status()
        data = response.json()

        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        if data.get('status') == 'ok':
            articles = data.get('articles', [])

            relevant_articles = []
            for article in articles:
                if is_relevant_article(article):
                    content = article.get('content', '')
                    possible_locations = extract_location(content)

                    for loc in possible_locations:
                        coordinates = geocode_location(loc)
                        if coordinates:
                            # Enhance accuracy by verifying the location against disaster type
                            if loc.lower() in content.lower():
                                article['location'] = coordinates
                                relevant_articles.append(article)
                                break

            if relevant_articles:
                inserted_count = 0
                for article in relevant_articles:
                    if not collection.find_one({'url': article['url']}):
                        collection.insert_one(article)
                        inserted_count += 1
                        # Notify Streamlit app of new article insertion
                        st.experimental_rerun()  # Force a rerun to update the UI
                st.write(f'Inserted {inserted_count} new articles with locations into MongoDB.')
            else:
                st.write('No relevant articles found.')
        else:
            st.write('Failed to fetch news data:', data.get('message'))

    except requests.RequestException as e:
        st.write('Error fetching news data:', e)
    except Exception as e:
        st.write('Error connecting to MongoDB or inserting data:', e)
    finally:
        if client:
            client.close()

def fetch_data_from_mongo():
    client = None
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        articles = list(collection.find().sort("publishedAt", -1))
        return articles
    except Exception as e:
        st.write('Error fetching data from MongoDB:', e)
        return []
    finally:
        if client:
            client.close()
