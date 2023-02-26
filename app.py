import streamlit as st
import pandas as pd
import altair as alt
from textblob import TextBlob

alt.themes.enable("streamlit")
# Define a function to get sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity




st.set_page_config(
    page_title="Bipolar Disorder Analytical Diagnosis", page_icon=":brain:", layout="wide"
)

data = pd.read_csv('user_1.csv')
sentiments = []
for text in data['tweet']:
    sentiment = get_sentiment(str(text))
    sentiments.append(sentiment)
# Add a new column 'sentiment' to the DataFrame with the calculated sentiment scores
data['sentiment'] = sentiments




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
            x="timestamp",
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


st.title("Bipolar Disorder Analytical Diagnostics")

# 

# Original time series chart. Omitted `get_chart` for clarity
source = data


# Create a chart with annotations
annotations_df = pd.DataFrame(source, columns=["timestamp", "sentiment","tweet","bp_label"])
annotations_df.timestamp = pd.to_datetime(annotations_df.timestamp)
annotations_df["y"] = 0
# annotation_layer = (
#     alt.Chart(annotations_df)
#     .mark_text(size=15, text=ticker, dx=ticker_dx, dy=ticker_dy, align="center")
#    .encode(
#         x="timestamp",
#         y="tweet",
#         tooltip=["tweet"],
#     )
#     .interactive()
# )
slider = alt.binding_range(min=-1, max=1, step=0.01, name='SentimentFilter:')
selector = alt.selection_single(name="SelectorName", fields=['cutoff'],
                                bind=slider, init={'cutoff': 0.5})

input_dropdown = alt.binding_select(options=['True', 'False'], name='bp_label')
selection = alt.selection_single(fields=['False'], bind=input_dropdown, init={'bp_label': 'True'})
colaor = alt.condition(
 alt.datum.bp_label == 'False',
        alt.value('gray'),
        alt.value('green')
                    )



c = alt.Chart(annotations_df).mark_point().encode(
    x='timestamp', y='sentiment',
     tooltip=['tweet','bp_label'] ,color=alt.condition(
        alt.datum.sentiment < selector.cutoff,
        alt.value('red'), alt.value('blue'))).add_selection(
    selector
)

# Display both charts together
st.altair_chart((c).interactive(), theme="streamlit",use_container_width=True)

st.subheader("Bipolar Labeled")


bp = alt.Chart(annotations_df).mark_circle().encode(
    x='timestamp', y='sentiment',
     tooltip=['tweet','bp_label:N'] ,color=colaor)

# Display both charts together
st.altair_chart((bp).interactive(), theme="streamlit",use_container_width=True)


st.subheader("Dataset")

st.dataframe(data, width=800, height=500)
