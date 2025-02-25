from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Make sure you have GOOGLE_API_KEY in your .env file
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please add it to your .env file.")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_gemini(dom_chunks, parse_description):
    # Initialize Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=GEMINI_API_KEY,
        temperature=0.1,  # Lower temperature for more factual responses
        top_p=0.95,
        max_output_tokens=4096  # Adjust based on your needs
    )
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        # Extract content from the response - Gemini returns a structured object
        response_content = response.content if hasattr(response, 'content') else str(response)
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response_content)

    return "\n".join(parsed_results)