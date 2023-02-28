import streamlit as st
import pandas as pd
# import altair as alt


# alt.themes.enable("streamlit")
# # Define a function to get sentiment analysis
# def get_sentiment(text):
#     return TextBlob(text).sentiment.polarity


# def get_keyword(text):
#     return TextBlob(text).noun_phrases

# global source
# annotations_df = pd.DataFrame(source, columns=["timestamp", "sentiment","tweet","bp_label"])
# annotations_df.timestamp = pd.to_datetime(annotations_df.timestamp)
# annotations_df["y"] = 0

# slider = alt.binding_range(min=-1, max=1, step=0.01, name='SentimentFilter:')
# selector = alt.selection_single(name="SelectorName", fields=['cutoff'],
#                                 bind=slider, init={'cutoff': 0.5})

# c = alt.Chart(annotations_df).mark_point().encode(
#     x='timestamp', y='sentiment',
#     tooltip=['tweet','bp_label'] ,color=alt.condition(
#         alt.datum.sentiment < selector.cutoff,
#         alt.value('red'), alt.value('blue'))).add_selection( selector )
# st.altair_chart((c).interactive(), theme="streamlit",use_container_width=True)



# def get_chart(data):
#     hover = alt.selection_single(
#         fields=["timestamp"],
#         nearest=True,
#         on="mouseover",
#         empty="none",
#     )

#     lines = (
#         alt.Chart(data, height=500, title="Tweet Analysis of User")
#         .mark_line()
#         .encode(
#             x=alt.X("timestamp", title="Date"),
#             y=alt.Y("sentiment", title="Price"),
#             color="symbol",
#         )
#     )

#     # Draw points on the line, and highlight based on selection
#     points = lines.transform_filter(hover).mark_circle(size=65)

#     # Draw a rule at the location of the selection
#     tooltips = (
#         alt.Chart(data)
#         .mark_rule()
#         .encode(
#             x="timestamp",
#             y="sentiment",
#             opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
#             tooltip=[
#                 alt.Tooltip("timestamp", title="Date"),
#                 alt.Tooltip("sentiment", title="Price (USD)"),
#             ],
#         )
#         .add_selection(hover)
#     )

#     return (lines + points + tooltips).interactive()

