import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_gemini  # Changed from parse_with_ollama to parse_with_gemini
import os

# Check for environment variables on startup
if not os.getenv("SBR_WEBDRIVER"):
    st.error("SBR_WEBDRIVER environment variable is not set. Please check your .env file.")
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY environment variable is not set. Please check your .env file.")

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        try:
            st.write("Scraping the website...")

            # Scrape the website
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable text box
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        except Exception as e:
            st.error(f"Error occurred during scraping: {str(e)}")


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            try:
                st.write("Parsing the content...")

                # Parse the content with Gemini
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_gemini(dom_chunks, parse_description)
                st.write(parsed_result)
            except Exception as e:
                st.error(f"Error occurred during parsing: {str(e)}")