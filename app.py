import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="AI Headline & Summary Generator", layout="centered")

st.title("🏈 AI-Powered Headline & Summary Generator")
st.markdown("Paste a sports article below to get headline suggestions and a concise summary optimized for engagement and SEO.")

# Input text
article = st.text_area("✍️ Article Text", height=300)

# Load Gemini API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Generate button
if st.button("🚀 Generate"):
    if not article.strip():
        st.warning("Please paste an article to analyze.")
    else:
        with st.spinner("Generating with Gemini..."):
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"""
            Analyze the following sports article and generate:
            - 5 compelling, diverse headline suggestions (SEO-friendly, attention-grabbing).
            - A concise 2-3 sentence summary of the article.

            Article:
            {article}
            """
            try:
                response = model.generate_content(prompt)
                result = response.text
                st.subheader("📰 Suggestions")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
