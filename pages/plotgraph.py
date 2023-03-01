import streamlit as st
import pandas as pd
import altair as alt
alt.themes.enable("streamlit")

df2 = pd.read_csv("data/user_1.csv")
df2['timestamp'] = pd.to_datetime(df2['timestamp'])
st.table(df2.head(5))
    # Convert 'timestamp' column to a pa
# Load dta from CSV file
# df2 = pd.read_csv('data.csv')

# Create a checkbox to toggle data points with true/false labels
show_true = st.checkbox('Show True Labels')

# Filter the data based on the checkbox value
if show_true:
    dta = df2
else:
    dta = df2[df2['bp_label'] == False]


# Create a selection for the tooltip
selection = alt.selection_single(fields=['timestamp'], nearest=True, on='mouseover', empty='none')

# Create the chart
chart1 = alt.Chart(dta).mark_circle(size=100).encode(
    x='timestamp:T',
    y='bp_label:N',
    color=alt.Color('bp_label:N', scale=alt.Scale(domain=['True', 'False'], range=['red', 'blue'])),
    tooltip=['tweet']
).add_selection(selection).interactive()

# Add a line that follows the selected timestamp
line1 = chart1.transform_filter(selection).mark_line(color='black')

# Add the chart and line to the Streamlit app
st.altair_chart(chart1+line1, use_container_width=True)
