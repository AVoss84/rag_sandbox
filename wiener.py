import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import time
from scipy.stats import norm

# Display the chosen profile and corresponding emoji in the title
st.title("Agile Wiener 🕒")
#st.subheader(f"Role: {st.session_state.chosen_profile}")

# Add some space between the title and the rest of the content
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Parameters for the simulation
time_steps = 1000  # Number of time steps
T = 1.0  # Total time
duration = 120  # Duration of the simulation in seconds
dt = T / time_steps  # Time step size
num_paths = 200  # Number of paths to simulate

# Generate Wiener process paths
t = np.linspace(0, T, time_steps + 1)
W = np.zeros((num_paths, time_steps + 1))

for i in range(num_paths):
    dW = np.sqrt(dt) * np.random.randn(time_steps)
    W[i, 1:] = np.cumsum(dW)

# Create columns for the plots
col1, col2 = st.columns(2)

# Create placeholders for the plots
plot_placeholder = col1.empty()
hist_placeholder = col2.empty()

start_time = time.time()  # Get the start time

for tp_index in range(time_steps + 1):
    # Plot Wiener process paths
    fig, ax = plt.subplots(figsize=(18, 16))
    for i in range(num_paths):
        ax.plot(t[:tp_index + 1], W[i, :tp_index + 1], lw=1.5)
    ax.set_title('Wiener trajectories')
    ax.set_xlabel('Time')
    ax.set_ylabel('W(t)')
    ax.grid(True)
    plot_placeholder.pyplot(fig)
    plt.close(fig)  # Close the figure

    # Plot the marginal distribution of W(t) at time tp
    fig_hist, ax_hist = plt.subplots(figsize=(18, 16))
    ax_hist.hist(W[:, tp_index], bins=30, density=True, alpha=0.5, label=f't = {t[tp_index]}')

    # Theoretical normal distribution for comparison
    x = np.linspace(-3, 3, 100)
    ax_hist.plot(x, norm.pdf(x, scale=np.sqrt(t[tp_index])), lw=2, label=f'N(0, {t[tp_index]})')

    ax_hist.set_title('Marginal Distribution of W(t)')
    ax_hist.set_xlabel('Value')
    ax_hist.set_ylabel('Density')
    ax_hist.legend()
    ax_hist.grid(True)
    hist_placeholder.pyplot(fig_hist)
    plt.close(fig_hist)  # Close the figure

    elapsed_time = time.time() - start_time
    if elapsed_time > duration:
        break  # Stop the loop if the elapsed time exceeds the duration

    remaining_time = duration - elapsed_time  # Calculate the remaining time

    # Print the remaining time
    print(f'Remaining time: {remaining_time} seconds')

    sleep(2*60/(time_steps + 1))  # sleep for a while to create a delay for animation

st.balloons()