# **Disaster Information Aggregation**

This project is a real-time disaster information aggregation system that collects and displays news about various natural disasters occurring in India. The application provides users with insights on disaster types, locations, and safety precautions, making it easier to stay informed and prepared.

## **Features**
- **Fetch Real-Time Disaster News**: The application uses the News API to fetch the latest articles on natural disasters such as earthquakes, tsunamis, floods, wildfires, and more.
- **Location Mapping**: Visualizes disaster data on a map using PyDeck, helping users understand the geographic spread of ongoing disasters.
- **Data Storage**: The news data is stored in a MongoDB database, ensuring efficient retrieval and management of large datasets.
- **Disaster Precautions**: Provides safety tips and precautionary measures for various disaster types.
- **Interactive Visualizations**: Uses Plotly for enhanced data visualization and filtering, allowing users to analyze disaster trends over time.

## **Tech Stack**
- **Frontend**: Streamlit for the web interface.
- **Backend**: Python, MongoDB, PyDeck, and Plotly.
- **APIs**: News API for fetching real-time disaster information.
- **Geolocation**: GeoPy for extracting location details from news articles.
- **NLP**: spaCy for processing and categorizing disaster-related news.

## **File Overview**

### `app.py`
This is the main application file responsible for:
- Rendering the Streamlit user interface.
- Fetching data from the MongoDB database using the `fetch_news.py` script.
- Displaying a map with disaster locations using PyDeck.
- Presenting disaster information, precautions, and Plotly-based visualizations to the user.

### `fetch_news.py`
This script handles:
- Fetching the latest disaster news articles from the News API.
- Extracting relevant location information using spaCy and GeoPy.
- Storing the processed news data in a MongoDB collection.

## **How to Run the Project**

1. Clone the repository:
   ```bash
   git clone https://github.com/imohammedsaad/Disaster-Information-Aggregation.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure to set up the necessary environment variables for the News API and MongoDB connection:
   - `NEWS_API_KEY`: Your News API key.
   - `MONGO_URI`: Your MongoDB connection URI.

4. Run the application using Streamlit:
   ```bash
   streamlit run app.py
   ```

## **Configuration**
- The application expects `NEWS_API_KEY` and `MONGO_URI` environment variables to be set.
- The `app.py` and `fetch_news.py` files are designed to work together, with `app.py` handling the frontend and `fetch_news.py` handling the data fetching and processing.
