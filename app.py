import os
import time
import re
import random
from PIL import Image
import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Custom output parser
class CustomOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        # Use regular expression to filter out the time indication
        filtered_response = re.sub(r'^\*\d{1,3}-\d{1,3} seconds: ', '', text)
        return filtered_response

# Setup ChatOllama
llm = ChatOllama(model="llama3", temperature=0.5)


# Profile and emoji mapping
profile_emoji_mapping = {
  "cowboy": "🤠",
  "pirate": "🏴‍☠️",
  "hip-hop star": "🎤",
  "boring insurance clerk": "💼",
  "Rastafarian": "🧑‍🦱",
  "alien from another planet": "👽",
  "poet": "📜",
  "philosopher": "🤔",
  "statistician": "📊"
}

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False
if "chosen_profile" not in st.session_state:
    st.session_state.chosen_profile = None


# Function to run the API call loop
def run_api_call_loop(duration=120):
    response_placeholder = st.empty()  # Create an empty placeholder in the Streamlit app
    progress_bar = st.progress(0)  # Create a progress bar in the Streamlit app

    # Randomly choose a role
    st.session_state.chosen_profile = random.choice(list(profile_emoji_mapping.keys()))

    # Updated prompt with the chosen profile
    query = f"""
    You are a funny and ironic {st.session_state.chosen_profile}. 
    You will act as the timekeeper in a business team meeting where each attendee is assigned a two minutes slot for an update to other team members.     
    Your task is to motivate the speaker to respect the two-minutes rule. 
    Depending on the {{remaining_time}} in seconds you should provide a different response. Note, the less seconds are remaining you should become pushier and urge the speaker to finalize. 
    The remaining time is a number between 0 and 120 seconds. 
    Please limit your response to a maximum of 80 characters and only show a single response and do not output the remaining time.
    """    
    prompt = ChatPromptTemplate.from_template(query)
    chain = prompt | llm | CustomOutputParser()

    start_time = time.time()
    while time.time() - start_time < duration:
        if not st.session_state.running:
            break

        elapsed_time = time.time() - start_time
        remaining_time = duration - int(elapsed_time) % duration
        progress_percentage = int((elapsed_time / duration) * 100)
    
        response = chain.invoke({"remaining_time": remaining_time, "profile": st.session_state.chosen_profile})
        print(st.session_state.chosen_profile)
        print(f"Response: {response}")

        # Display the response
        response_placeholder.markdown(
            f"<h1 style='text-align: center; color: white; font-family: \"Courier New\", monospace;'>{response}</h1>",
            unsafe_allow_html=True
        )
        # Update the progress bar
        progress_bar.progress(progress_percentage, text=f"{int(elapsed_time)} seconds elapsed out of {duration} seconds [{remaining_time} seconds left]")

        time.sleep(5)
    
    # Set the progress bar to 100% after completion
    progress_bar.progress(100, text="Time's up! [0 seconds left]")
    
    if st.session_state.running:
        for _ in range(2):
            st.balloons()
            time.sleep(2)  # Wait 2 seconds between each balloon trigger
        st.session_state.running = False
        st.toast('Hooray! Next?', icon='🎉')

    # Reset the progress bar and response placeholder after the process ends
    progress_bar.progress(0, text="Clock reset")
    response_placeholder.empty()

#------------------------------------------------------------------------------

###############
# Streamlit UI
###############

# Set Page name and icon, Layout and sidebar expanded
img = Image.open(os.path.join('pictures', 'allianz_logo.jpg'))  # page name icon
st.set_page_config(page_title='Agile Clock', page_icon=img, layout="wide", initial_sidebar_state='expanded')

# Display the chosen profile and corresponding emoji in the title
# if st.session_state.chosen_profile:
#     chosen_emoji = profile_emoji_mapping[st.session_state.chosen_profile]
#     st.title(f"A.I. Agile Assistant {chosen_emoji} 🕒")
# else:
st.title("Agile Assistant 🤠🕒")

# Add some space between the title and the rest of the content
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

response_container = st.container()

# Add some space between the response container and the buttons
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Place buttons side by side
col1, col2 = st.columns(2)

with col1:
    if st.button('Start clock'):
        st.session_state.running = True
        with response_container:
            run_api_call_loop()

with col2:
    if st.button('Reset clock'):
        st.session_state.running = False