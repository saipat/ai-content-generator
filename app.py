import streamlit as st
from auth_setup import *  # Handles auth + init
from main import generate_response
from db import get_guest_conversion_stats, save_to_db, get_last_n_entries, get_total_count

st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

# -- Session State Init --
for state_key in ["user", "history", "edited_text", "rephrased_text"]:
    if state_key not in st.session_state:
        st.session_state[state_key] = [] if state_key == "history" else ""


# Styles
st.markdown("""
<style>
h1 { margin-bottom: 0.2rem; }
h3 { font-weight: 400; color: #555; margin-top: 0; }
hr { margin-top: 2rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# UI: Inputs
st.markdown("---")
content_type = st.selectbox("📝 What do you want to generate?", [
    "📰 Blog Post", "🐦 Tweet", "🛍️ Product Description", "💼 LinkedIn Post"
])
tone = st.selectbox("🎨 Choose a tone/style:", [
    "😐 Neutral", "🏢 Professional", "😎 Casual", "😂 Funny", "🧲 Persuasive"
])
user_input = st.text_area("💡 Enter a topic, idea, or keywords:")

# Generate
if st.button("⚡ Generate", type="primary"):
    with st.spinner("Thinking..."):
        prompt = f"Write a {tone.split(' ')[1].lower()} {content_type.split(' ')[1].lower()} about: {user_input}"
        result = generate_response(prompt)

        st.session_state.generated_output = result
        st.session_state.edited_text = result
        st.session_state.rephrased_text = ""
        st.session_state.history.append({
            "type": content_type, "input": user_input, "output": result
        })
        save_to_db(st.session_state.user, content_type, tone, user_input, result)
        st.success("Done!")

# Output
if "generated_output" in st.session_state:
    st.text_area("🤖 Generated Content", value=st.session_state.generated_output, height=200)
    if st.session_state.user != "guest":
        if st.button("✏️ Edit"):
            st.text_area("Your Edited Version", key="edited_text", value=st.session_state.generated_output, height=200)
        if st.button("🔁 Rephrase"):
            with st.spinner("Rephrasing..."):
                rephrased = generate_response(f"Please rephrase clearly: {st.session_state.generated_output}")
                st.session_state.rephrased_text = rephrased
        if st.session_state.rephrased_text:
            st.text_area("🔁 Rephrased Version", value=st.session_state.rephrased_text, height=200)
    else:
        st.info("🔒 Editing/rephrasing only available for signed-in users.")

# Download
final_output = st.session_state.get("rephrased_text") or st.session_state.get("edited_text")
if final_output:
    st.download_button("⬇️ Download", final_output, file_name="content.txt", mime="text/plain")

# Sidebar History & Stats 
with st.sidebar:
    user = st.session_state.get("user")
    auth_status = st.session_state.get("authentication_status")
    print(f"{auth_status}")

    if auth_status:
        st.write(f"👤 Logged in as: {user}")
        authenticator.logout("Logout", "sidebar")

    elif user == "guest":
        st.info("🔓 Guest mode. Your data may not be saved.")
        st.warning("🔒 Sign up to save your content and unlock editing!")

    # Optional: fallback message if neither guest nor logged in
    elif user is None:
        st.info("🔐 Please log in to see your content history.")

    # Show guest conversion stats only for Sai
    if user == "sailakshmi.pattabiraman@gmail.com":
        g, c = get_guest_conversion_stats()
        st.markdown(f"📈 Guest Conversions: {c}/{g} ({(c/g)*100 if g else 0:.1f}%)")

    total_content = get_total_count(user)
    st.markdown(f"### 🤖 Generated contents: {total_content}", unsafe_allow_html=True)

    for i, (ctype, tone, input_text, output_text, created_at) in enumerate(get_last_n_entries(user, 10), 1):
        with st.expander(f"{i}. {ctype} ({tone}) — {input_text[:30].title()}"):
            st.markdown(f"**🕒 {created_at.split('T')[0]}**")
            st.markdown("##### ✍️ Output")
            st.write(output_text)



st.markdown("---")
st.markdown("Built with 💙 using Streamlit + OpenAI")