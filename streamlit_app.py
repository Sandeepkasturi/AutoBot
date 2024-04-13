import streamlit as st
import requests
import webbrowser
from google.generativeai import configure, GenerativeModel
from IPython.display import Markdown
import textwrap
import os
import base64


# Function to convert plain text to Markdown format
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Function to download HTML code
def download_html_code(html_content, filename='extracted_html.html'):
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="{filename}">Download HTML</a>'
    st.markdown(href, unsafe_allow_html=True)


# Function to download generated code
def download_generated_code(content, filename='generated_code.txt'):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Code</a>'
    st.markdown(href, unsafe_allow_html=True)


# Main Streamlit application
def main():
    st.title("Auto BOT")
    st.image("auto_bot_1.png")
    st.markdown("""
    SKAV TECH presents Auto Bot AI:""")
    st.markdown("""Functionalities:
     1. Extracts HTML code from a URL.
     2. Generates responses using SKAV AI Chatbot.
     3. Available for Downloading code files.

     Auto BOT is for educational purposes only.
     We are not responsible for any illegal and unethical activities done by You.
    """)
    st.markdown("Get API key from Google AI Studio")

    # Prompt user for API key
    api_key = st.text_input("Enter your Generative AI API key:")

    # Check if API key is provided
    if api_key:
        # Set up the Generative AI configuration with the provided API key
        configure(api_key=api_key)

        # Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
        model = GenerativeModel('gemini-pro')

        
        # AI Chatbot section
        st.header("Auto Bot Chatbot")
        question = st.text_input("Ask the model a question:")
        if st.button("Ask AI"):
            # Call your AI model and get the response
            response = model.generate_content(question)
            st.text("Auto Bot Response:")
            st.write(response.text)

            # Check if the response contains a URL
            if "http" in response.text:
                st.write("The response contains a URL.")

            # Check if the question is related to generating code
            code_keywords = ["code", "write code", "develop code", "generate code"]
            if any(keyword in question.lower() for keyword in code_keywords):
                download_generated_code(response.text)
                
        # HTML Extraction section
        st.header("Extract HTML Code")
        url = st.text_input("Enter URL:")
        if st.button("Extract HTML Code"):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    download_html_code(response.text)
                else:
                    st.error(f"Failed to retrieve HTML content. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Additional buttons
    st.markdown('---')
    st.markdown("&copy; 2024 - All rights reserved SKAV TECH.")
    st.subheader('Our recent projects')
    button_col3, button_col4, button_col5 = st.columns(3)

    if button_col3.button('DataVerse AI'):
        webbrowser.open("https://dataverse-ai.vercel.app/")

    if button_col4.button('Ulink'):
        webbrowser.open("https://ulink-io.vercel.app")
    if button_col5.button('SKAV TECH'):
        webbrowser.open("https://skavtech.mydurable.com")


if __name__ == "__main__":
    main()
