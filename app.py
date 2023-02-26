import streamlit as st
import pandas as pd
import altair as alt
from textblob import TextBlob

# Define a function to get sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity




st.set_page_config(
    page_title="Time series annotations", page_icon="⬇", layout="centered"
)


@st.experimental_memo
def get_data():
    # Load the data
    data = pd.read_csv('user_1.csv')
    sentiments = []
    for text in data['tweet']:
        sentiment = get_sentiment(str(text))
        sentiments.append(sentiment)
    # Add a new column 'sentiment' to the DataFrame with the calculated sentiment scores
    data['sentiment'] = sentiments
    st.dataframe(data, width=800, height=500)



@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["timestamp"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, height=500, title="Tweet Analysis of User")
        .mark_line()
        .encode(
            x=alt.X("timestamp", title="Date"),
            y=alt.Y("sentiment", title="Price"),
            color="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(timestamp)",
            y="sentiment",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("timestamp", title="Date"),
                alt.Tooltip("sentiment", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


st.title("⬇ Time series annotations")

st.write("Give more context to your time series using annotations!")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Choose a ticker (⬇💬👇ℹ️ ...)", value="⬇")
with col2:
    ticker_dx = st.slider(
        "Horizontal offset", min_value=-30, max_value=30, step=1, value=0
    )
with col3:
    ticker_dy = st.slider(
        "Vertical offset", min_value=-30, max_value=30, step=1, value=-10
    )

# Original time series chart. Omitted `get_chart` for clarity
source = get_data()
chart = get_chart(source)

# # Input annotations
# ANNOTATIONS = [
#     ("Mar 01, 2008", "Pretty good day for GOOG"),
#     ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
#     ("Nov 01, 2008", "Market starts again thanks to..."),
#     ("Dec 01, 2009", "Small crash for GOOG after..."),
# ]

# Create a chart with annotations
annotations_df = pd.DataFrame(source, columns=["timestamp", "tweet"])
annotations_df.timestamp = pd.to_datetime(annotations_df.timestamp)
annotations_df["y"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=15, text=ticker, dx=ticker_dx, dy=ticker_dy, align="center")
    .encode(
        x="timestamp",
        y="tweet",
        tooltip=["tweet"],
    )
    .interactive()
)

# Display both charts together
st.altair_chart((chart).interactive(), use_container_width=True)
