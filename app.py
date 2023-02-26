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
    ax.plot(df.index, df['sentiment'])
    ax.set_title('Sentiment Analysis over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    st.pyplot(fig)

# Load the data
data = pd.read_csv('user_1.csv', index_col=0)
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Calculate sentiment score for each row
data['bp_label'] = data['tweet'].apply(get_sentiment)

# Group the data by date and calculate the mean sentiment score
sentiment_by_date = data.groupby('date')['sentiment'].mean()

# Plot the timeseries graph
plot_timeseries(sentiment_by_date)
