import streamlit as st
from main import generate_response

if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

st.title("🤖 AI Content Generator")
st.subheader("Write high-quality content in seconds")

# Content type selector
content_type = st.selectbox("What do you want to generate?", [
    "Blog Post",
    "Tweet",
    "Product Description",
    "LinkedIn Post"
])

# Input prompt
user_input = st.text_area("Enter a topic, idea, or keywords:")

if st.button("⚡ Generate"):
    with st.spinner("Thinking..."):
        # Prefix the content_type to the prompt for context
        full_prompt = f"Write a {content_type.lower()} about: {user_input}"
        result = generate_response(full_prompt)
        st.session_state.history.append({
            "type": content_type,
            "input": user_input,
            "output": result
        })
        st.success("Done!")
        st.markdown("### ✍️ Output")
        st.write(result)

        st.download_button("⬇️ Download", result, file_name="content.txt", mime="text/plain")

        with st.expander("📜 View History"):
            for i, entry in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"**{i}. {entry['type']} on _{entry['input']}_**")
                st.code(entry["output"])