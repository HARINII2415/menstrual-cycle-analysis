from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.pubmed.tool import PubmedQueryRun
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
print("Gemini API Key:", os.getenv("GEMINI_API_KEY"))

# Retrieve Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("🚨 ERROR: GEMINI_API_KEY is missing. Please check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def periodcarerecommender(input_text):
    prompt = f"""
    You are Leo, a medical practitioner specializing in female menstrual health.
    You provide guidance based on the user's menstrual cycle phase and symptoms.
    Only use reliable sources like Wikipedia or PubMed knowledge. Do not generate unrelated content.
    Be polite Use More related emojis for sentences.

    User Question:
    {input_text}

    Answer in a clear, supportive, and medically-informed way.
    """
    response = model.generate_content(prompt)
    return response.text.strip()


def main():
    st.set_page_config("Leo AI - Period Care Recommender 🤖")
    st.header("Get Personalized Care Suggestions with Leo AI 👩‍⚕️")

    # User input
    user_phase = st.radio("Select the phase of Menstruation:",
                          ("Menstrual Phase (Day 1 to Day 7)",
                           "Proliferative Phase (Day 8 to Day 11)",
                           "Ovulation Phase (Day 12 to 17)",
                           "Luteal Phase (Day 18 to Day 28)"))

    if user_phase == "Menstrual Phase (Day 1 to Day 7)":
        user_day = st.number_input("Enter the day of the period phase:", min_value=1, max_value=7)
        abdominal_pain = st.checkbox("Abdominal pain present?")
        period_flow = st.checkbox("Period flow present?")
        period_flow_type = st.radio("Select period flow type:", ("Heavy", "Moderate", "Low")) if period_flow else "None"

        user_question = f"I'm in the Menstrual Phase (Day {user_day}). Abdominal pain: {'Yes' if abdominal_pain else 'No'}. Period flow: {period_flow_type}."
    else:
        user_question = f"I am in the {user_phase}."

    user_question += st.text_input("Share any issues you’re facing: ", placeholder="Enter your queries here 🤗")

    st.sidebar.title("Leo AI - Your Personal Period Care Assistant 🫂")
    st.sidebar.subheader("Ask about menstrual cycle issues and get personalized suggestions! 👩‍⚕️")

    if st.button("Get Suggestions"):
        st.write(periodcarerecommender(user_question))


if __name__ == "__main__":
    main()
