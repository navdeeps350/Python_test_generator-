import plotly.graph_objects as go
import numpy as np

# Provided data
o_1_list = ['34.8', '34.8', '17.4', '17.4', '34.8', '17.4', '17.4', '21.7', '39.1', '34.8']
o_2_list = ['47.8', '52.2', '34.8', '43.5', '47.8', '56.5', '47.8', '60.9', '34.8', '47.8']

# Convert strings to float
o_1_values = [float(value) for value in o_1_list]
o_2_values = [float(value) for value in o_2_list]

# Create box plots
fig = go.Figure()

fig.add_trace(go.Box(y=o_1_values, name='Fuzzer'))
fig.add_trace(go.Box(y=o_2_values, name='GA'))

# Update layout for better visualization
fig.update_layout(
    title='Fuzzer vs. GA',
    xaxis=dict(title='Categories'),
    yaxis=dict(title='Values'),
    boxgap = "group"  # 'group' places the boxes next to each other
)

# Show the plot
fig.show()
