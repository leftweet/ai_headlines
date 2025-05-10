import streamlit as st
import google.generativeai as genai
import re

def strip_markdown(text):
    """Remove common Markdown formatting like bold and italics."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # italics with *
    text = re.sub(r"_(.*?)_", r"\1", text)        # italics with _
    return text.strip()

# Page config
st.set_page_config(page_title="AI SEO Tag Generator", layout="centered")

st.title("AI SEO Tag Generator")
st.markdown("Paste a sports article below to get headline suggestions, a concise meta description, and a clean URL slug optimized for SEO.")

# Input text
article = st.text_area("Article Text", height=300)

# Load Gemini API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Generate button
if st.button("Generate SEO Tags"):
    if not article.strip():
        st.warning("Please paste an article to analyze.")
    else:
        with st.spinner("Generating with Gemini..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            prompt = f"""
You are an expert editorial assistant with a deep understanding of digital media, SEO best practices, and audience engagement.

Analyze the following sports article and return the following outputs using **bolded numbered section titles**:

**1. Headlines**
- List 5 unique, compelling headline suggestions (under 70 characters each).
- Use active voice and action-oriented phrasing.
- Optimize for search intent and engagement.

**2. Meta Description**
- Provide a concise meta description under 160 characters.
- Summarize the article clearly using keywords and inviting tone.

**3. URL Slug**
- Create an SEO-friendly URL slug (lowercase, hyphenated, no special characters).
- Keep it short and descriptive (4–8 words).

Here is the article:

\"\"\"{article}\"\"\"
"""

            try:
                response = model.generate_content(prompt)
                result = response.text

                # Use bolded section titles in regex
                headlines_match = re.search(r"\*\*1\. Headlines\*\*\s*(.*?)\s*\*\*2\.", result, re.DOTALL)
                meta_match = re.search(r"\*\*2\. Meta Description\*\*\s*(.*?)\s*\*\*3\.", result, re.DOTALL)
                slug_match = re.search(r"\*\*3\. URL Slug\*\*\s*(.*)", result, re.DOTALL)

                if not (headlines_match and meta_match and slug_match):
                    st.warning("Unexpected response format. Displaying raw output:")
                    st.markdown(result)
                    st.stop()

                # Extracted sections
                headlines = headlines_match.group(1).strip()
                meta_description = meta_match.group(1).strip()
                url_slug = slug_match.group(1).strip()

                # Display Headlines
                st.subheader("Headline Suggestions")
                for h in re.findall(r"\d+\.\s+(.*)", headlines):
                    clean_h = strip_markdown(h.strip())
                    if clean_h:
                        st.code(clean_h, language="")

                # Display Meta Description
                st.subheader("Meta Description")
                st.markdown(meta_description)
                st.text_area("", meta_description, height=100, label_visibility="collapsed")

                # Display URL Slug
                st.subheader("URL Slug")
                st.markdown(f"`{url_slug}`")
                st.code(url_slug, language="")

            except Exception as e:
                st.error(f"An error occurred: {e}")
