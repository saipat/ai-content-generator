import streamlit as st
from main import generate_response
from db import save_to_db, get_last_n_entries, get_total_count, get_guest_conversion_stats, init_all_databases
from auth import auth_tabs, logout_button, is_logged_in

# -- Page Config --
st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

# -- Initialize DBs --
init_all_databases()

# -- Session state init --
if "history" not in st.session_state:
    st.session_state.history = []
if "edited_text" not in st.session_state:
    st.session_state.edited_text = ""
if "rephrased_text" not in st.session_state:
    st.session_state.rephrased_text = ""

# -- Auth --
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

# -- Styles --
st.markdown("""
<style>
h1 { margin-bottom: 0.2rem; }
h3 { font-weight: 400; color: #555; margin-top: 0; }
hr { margin-top: 2rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# -- Hero --
st.markdown("# 🤖 AI Content Generator")
st.markdown("### Create high-quality content in seconds with AI precision.\nAutomate your writing workflow—faster, smarter, cleaner.")
st.markdown("---")

# -- Controls --
content_type = st.selectbox("📝 What do you want to generate?", [
    "📰 Blog Post", "🐦 Tweet", "🛍️ Product Description", "💼 LinkedIn Post"
])
tone = st.selectbox("🎨 Choose a tone/style:", [
    "😐 Neutral", "🏢 Professional", "😎 Casual", "😂 Funny", "🧲 Persuasive"
])
user_input = st.text_area("💡 Enter a topic, idea, or keywords:")

# -- Generate --
if st.button("⚡ Generate", type="primary"):
    with st.spinner("Thinking..."):
        tone_clean = tone.split(" ", 1)[1]
        content_clean = content_type.split(" ", 1)[1]
        prompt = f"Write a {tone_clean.lower()} {content_clean.lower()} about: {user_input}"
        result = generate_response(prompt)

        st.session_state.generated_output = result
        st.session_state.edited_text = result  # reset editor
        st.session_state.rephrased_text = ""

        st.session_state.history.append({
            "type": content_type,
            "input": user_input,
            "output": result
        })
        save_to_db(st.session_state.user, content_clean, tone_clean, user_input, result)
        st.success("Done!")

# -- Editing + Rephrase (only for signed-in users) --
if "generated_output" in st.session_state:
    # --- Show Generated ---
    st.text_area("🤖 Generated Content", 
                 value=st.session_state.generated_output, 
                 height=200)

    # --- Show Editable Content (for signed-in users) ---
    if st.session_state.user != "guest":
        if st.button("✏️ Edit"):
            st.text_area("Your Edited Version", 
                        key="edited_text", 
                        value=st.session_state.generated_output,
                        height=200)

        if st.button("🔁 Rephrase"):
            with st.spinner("Rephrasing..."):
                prompt = f"Please rephrase the following text in a clearer and more polished way:\n\n{st.session_state.generated_output}"
                rephrased = generate_response(prompt)
                st.session_state.rephrased_text = rephrased

        # --- Show Rephrased Output ---
        if st.session_state.rephrased_text:
            st.text_area("🔁 Rephrased Version", 
                        value=st.session_state.rephrased_text, 
                        height=200)
            st.success("🔁 Rephrased!")
    else:
        st.info("🔒 Editing and rephrasing are only available for signed-in users.")


# -- Download final content --
final_output = st.session_state.get("rephrased_text") or st.session_state.get("edited_text", "")
if final_output:
    st.download_button("⬇️ Download", final_output, file_name="content.txt", mime="text/plain")

# -- Sidebar History --
with st.sidebar:
    if st.session_state.user == "guest":
        st.sidebar.info("🔓 Guest mode. Your data may not be saved.")
        st.sidebar.warning("🔒 Sign up to save your content and unlock editing!")

    if st.session_state.user == "sailakshmi.pattabiraman@gmail.com":
        g, c = get_guest_conversion_stats()
        st.sidebar.markdown(f"📈 Guest Conversions: {c}/{g} ({(c/g)*100 if g else 0:.1f}%)")

    total_content = get_total_count(st.session_state.user)
    st.markdown(f"### 🤖 Generated contents: {total_content}", unsafe_allow_html=True)

    for i, (ctype, tone, input_text, output_text, created_at) in enumerate(get_last_n_entries(st.session_state.user, 10), 1):
        with st.expander(f"{i}. {ctype} ({tone}) — {input_text[:30].title()}"):
            st.markdown(f"**🕒 {created_at.split('T')[0]}**")
            st.markdown("##### ✍️ Output")
            st.write(output_text)

st.markdown("---")
st.markdown("Built with 💙 using Streamlit + OpenAI", unsafe_allow_html=True)
