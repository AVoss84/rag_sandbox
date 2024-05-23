import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from time import sleep
import time

###############
# Streamlit UI
###############

# Set Page name and icon, Layout and sidebar expanded
img = Image.open(os.path.join('pictures', 'allianz_logo.jpg'))  # page name icon
st.set_page_config(page_title='Agile Clock', page_icon=img, layout="wide", initial_sidebar_state='expanded')

# Display the chosen profile and corresponding emoji in the title
st.title("Agile Circle 🕒")
#st.subheader(f"Role: {st.session_state.chosen_profile}")

# Add some space between the title and the rest of the content
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Draw random variates from within a unit circle:
#-------------------------------------------------
# prepare "circle data"
radius = 2
center_x = 0
center_y = 0

N_sample = 50000
r = radius * np.sqrt(np.random.uniform(size=N_sample))    # random radii
theta = np.random.uniform(size=N_sample) * 2 * np.pi     # random angles

# convert from polar to Cartesian coordinates
x = center_x + r * np.cos(theta)        # cartesian coordinates : a + m * u_x
y = center_y + r * np.sin(theta)        

fig, ax = plt.subplots(figsize=(6, 3))
scat = ax.scatter([], [], color="orange", s=5)

# Draw the circle
# cartesian coordinates
theta = np.linspace(0, 2 * np.pi, 200) # angles for drawing points around the circle
ax.plot(radius * np.cos(theta) + center_x, radius * np.sin(theta) + center_y)

# Remove the axes
ax.axis('off')

# Create a placeholder for the plot
plot_placeholder = st.empty()

# Set the total duration in seconds
duration = 2 * 60

# Get the start time
start_time = time.time()

for i in range(N_sample):
    scat.set_offsets(np.c_[x[:i], y[:i]])
    plot_placeholder.pyplot(fig)

    elapsed_time = time.time() - start_time
    if elapsed_time > duration:
        break  # Stop the loop if the elapsed time exceeds the duration

    remaining_time = duration - elapsed_time  # Calculate the remaining time

    # Print the remaining time
    print(f'Remaining time: {int(remaining_time)} seconds')

    sleep(2*60/N_sample)  # sleep for a while to create a delay for animation

st.balloons()
time.sleep(4)  
st.toast('Hooray! Next?', icon='🎉')