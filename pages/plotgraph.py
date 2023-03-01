import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components

# Load the data
data = pd.read_csv("data/streamlitdatabase.csv", parse_dates=['timestamp'])

# Sidebar filters
x_axis = st.sidebar.selectbox('Select X-axis', ['timestamp', 'bp_label', 'hour', 'weekday', 'patient_index'])
y_axis = st.sidebar.selectbox('Select Y-axis', ['timestamp', 'bp_label', 'hour', 'weekday', 'patient_index'])
patient_filter = st.sidebar.slider('Patient Index', 1, 25, 1)

# Filter the data based on the selected patient index
filtered_data = data[data['patient_index'] == patient_filter]

# Create the scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(filtered_data[x_axis], filtered_data[y_axis], alpha=0.5)

# Add tooltip with tweet text
tooltip = plugins.PointHTMLTooltip(scatter, labels=list(filtered_data['tweet']))
plugins.connect(fig, tooltip)

# Format the plot
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.title(f'Scatter Plot of {x_axis} vs {y_axis} for Patient {patient_filter}')
plt.ylim(-0.5, 1.5)
plt.xlim(-0.5, 1.5)

# Convert the plot to an interactive HTML
html_graph = mpld3.fig_to_html(fig)

# Display the interactive HTML graph
components.html(html_graph)
