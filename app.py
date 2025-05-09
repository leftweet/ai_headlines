import streamlit as st
import google.generativeai as genai
import re

# Page config
st.set_page_config(page_title="AI Headline & Summary Generator", layout="centered")

st.title("🧠 AI-Powered Headline & Meta Description Generator")
st.markdown("Paste a sports article below to get headline suggestions, a concise meta description, and a clean URL slug optimized for SEO.")

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
            model = genai.GenerativeModel("gemini-2.0-flash")
            prompt = f"""
You are an expert editorial assistant with a deep understanding of digital media, SEO best practices, and audience engagement.

Analyze the following sports article and return the following outputs clearly and separately, each marked with a bold section title:

1. **Headlines**:
   - Generate 5 unique, compelling headline suggestions.
   - Each headline should be under 70 characters.
   - Use active voice and powerful action words.
   - Optimize for search intent and shareability.
   - Avoid clickbait and ambiguity.

2. **Meta Description**:
   - Write a concise meta description under 160 characters.
   - Clearly summarize the article’s main point.
   - Include keywords relevant to the article’s content.
   - Make it engaging and encourage click-throughs.

3. **URL Slug**:
   - Generate a clean, SEO-friendly URL slug.
   - Use lowercase letters, hyphens to separate words, and no special characters.
   - Keep it concise (ideally 4–8 words).
   - Reflect the article’s core topic or headline.

Here is the article:

\"\"\"{article}\"\"\"
"""

            try:
                response = model.generate_content(prompt)
                result = response.text

                # Extract sections using regex
                headlines = re.search(r"\*\*Headlines\*\*\s*([\s\S]*?)\*\*", result)
                meta_desc = re.search(r"\*\*Meta Description\*\*\s*([\s\S]*?)\*\*", result)
                url_slug = re.search(r"\*\*URL Slug\*\*\s*([\s\S]*)", result)

                if not (headlines and meta_desc and url_slug):
                    st.warning("Unexpected response format. Displaying raw output:")
                    st.markdown(result)
                    st.stop()

                # Clean and display each section
                st.subheader("📰 Headline Suggestions")
                headline_lines = headlines.group(1).strip().split("\n")
                for h in headline_lines:
                    clean_h = h.strip("-•1234567890. ").strip()
                    if clean_h:
                        st.markdown(f"- {clean_h}")
                        st.code(clean_h, language="")

                st.subheader("📄 Meta Description")
                meta = meta_desc.group(1).strip()
                st.markdown(meta)
                st.code(meta, language="")

                st.subheader("🔗 URL Slug")
                slug = url_slug.group(1).strip()
                st.markdown(f"`{slug}`")
                st.code(slug, language="")

            except Exception as e:
                st.error(f"An error occurred: {e}")
