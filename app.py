import streamlit as st
from main import generate_response
from db import init_db, save_to_db, get_last_n_entries, get_total_count
import os
from auth import auth_tabs, logout_button, is_logged_in, init_user_db
init_user_db()


# -- Page Config --
st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

# -- Initialize DBs --
init_db()
init_user_db()

# -- Session state for history --
if "history" not in st.session_state:
    st.session_state.history = []

# -- Auth & Entry --
if not is_logged_in():
    st.markdown("# 🤖 AI Content Generator")
    st.markdown("### Create high-quality content in seconds with AI precision.")
    st.markdown("Automate your writing workflow—faster, smarter, cleaner.")
    auth_tabs()
    st.stop()
else:
    logout_button()


# -- Inject custom styles --
st.markdown("""
<style>
h1 {
    margin-bottom: 0.2rem;
}
h3 {
    font-weight: 400;
    color: #555;
    margin-top: 0;
}
hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -- Main Hero Section --
st.markdown("""
# 🤖 AI Content Generator  
### Create high-quality content in seconds with AI precision.  
Automate your writing workflow—faster, smarter, cleaner.
""")

st.markdown("---")

# -- Content Generation Section --
# st.subheader("✍️ Write high-quality content")

content_type = st.selectbox("📝 What do you want to generate?", [
    "📰 Blog Post",
    "🐦 Tweet",
    "🛍️ Product Description",
    "💼 LinkedIn Post"
])

tone = st.selectbox("🎨 Choose a tone/style:", [
        "😐 Neutral",
        "🏢 Professional",
        "😎 Casual",
        "😂 Funny",
        "🧲 Persuasive"
    ])

user_input = st.text_area("💡 Enter a topic, idea, or keywords:")

if st.button("⚡ Generate", type="primary"):
    with st.spinner("Thinking..."):
        tone_clean = tone.split(" ", 1)[1]  # Remove emoji
        content_clean = content_type.split(" ", 1)[1]  # Remove emoji
        full_prompt = f"Write a {tone_clean.lower()} {content_type.lower()} about: {user_input}"
        result = generate_response(full_prompt)

        st.session_state.history.append({
            "type": content_type,
            "input": user_input,
            "output": result
        })

        st.success("Done!")
        save_to_db(content_clean, tone_clean, user_input, result)
        st.markdown("### ✅ Output")
        st.write(result)
        st.download_button("⬇️ Download", result, file_name="content.txt", mime="text/plain")


with st.sidebar:

    total_content_count = get_total_count()
    st.markdown(f"### 🤖 Generated contents: {total_content_count}", unsafe_allow_html=True)

    rows = get_last_n_entries(10)

    for i, (ctype, tone, input_text, output_text, created_at) in enumerate(rows, 1):
        preview = input_text[:30].title()
        with st.expander(f"{i}. {ctype} ({tone}) — {preview}"):
            st.markdown(f"**🕒 {created_at.split('T')[0]}**")
            st.markdown("##### ✍️ Output")
            st.write(output_text)
    
    

   

st.markdown("---")
st.markdown("Built with 💙 using Streamlit + OpenAI", unsafe_allow_html=True)