import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# Define a function to get sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Define a function to plot the timeseries graph
def plot_timeseries(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df['bp_label'])
    ax.set_title('Sentiment Analysis over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    st.pyplot(fig)

# Load the data
data = pd.read_csv('user_1.csv', index_col=1)
# data['date'] = pd.to_datetime(data['timestamp'])

sentiments = []
for text in data['tweet']:
    sentiment = get_sentiment(str(text))
    sentiments.append(sentiment)

# Add a new column 'sentiment' to the DataFrame with the calculated sentiment scores
data['sentiment'] = sentiments

st.dataframe(data, width=800, height=500)
# data['sentiment'] = data['tweet'].apply(get_sentiment)

# Group the data by date and calculate the mean sentiment score
sentiment_by_date = data.groupby('timestamp')['sentiment'].mean()

# Plot the timeseries graph
#plot_timeseries(data)
