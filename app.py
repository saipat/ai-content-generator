import streamlit as st
from main import generate_response
from db import save_to_db, get_last_n_entries, get_total_count, get_guest_conversion_stats, init_all_databases
import os
from auth import auth_tabs, logout_button, is_logged_in

# -- Page Config --
st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

# -- Initialize DBs --
init_all_databases()

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

if st.session_state.user == "guest":
    from db import delete_old_guest_entries
    delete_old_guest_entries(hours=1)

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
        save_to_db(st.session_state.user, content_clean, tone_clean, user_input, result)
        st.markdown("### ✅ Output")
        st.write(result)
        st.download_button("⬇️ Download", result, file_name="content.txt", mime="text/plain")


with st.sidebar:
    if st.session_state.user == "guest":
        st.sidebar.info("🔓 You are using Guest mode. Your data may not be saved permanently.")
        st.sidebar.warning("🔒 Sign up to save your content and access full features!")
    
    if st.session_state.user == "sailakshmi.pattabiraman@gmail.com":
        total_guests, converted_guests = get_guest_conversion_stats()
        st.sidebar.markdown(f"📈 Guest Conversions: {converted_guests}/{total_guests} ({(converted_guests/total_guests*100) if total_guests else 0:.1f}%)")


    total_content_count = get_total_count(st.session_state.user)
    st.markdown(f"### 🤖 Generated contents: {total_content_count}", unsafe_allow_html=True)

    rows = get_last_n_entries(st.session_state.user, 10)

    for i, (ctype, tone, input_text, output_text, created_at) in enumerate(rows, 1):
        preview = input_text[:30].title()
        with st.expander(f"{i}. {ctype} ({tone}) — {preview}"):
            st.markdown(f"**🕒 {created_at.split('T')[0]}**")
            st.markdown("##### ✍️ Output")
            st.write(output_text)

st.markdown("---")
st.markdown("Built with 💙 using Streamlit + OpenAI", unsafe_allow_html=True)