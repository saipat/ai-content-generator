import streamlit as st
from main import generate_response

# -- Session state for history --
if "history" not in st.session_state:
    st.session_state.history = []

# -- Page Config --
st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

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
st.subheader("✍️ Write high-quality content")

content_type = st.selectbox("What do you want to generate?", [
    "Blog Post",
    "Tweet",
    "Product Description",
    "LinkedIn Post"
])

user_input = st.text_area("Enter a topic, idea, or keywords:")

if st.button("⚡ Generate"):
    with st.spinner("Thinking..."):
        full_prompt = f"Write a {content_type.lower()} about: {user_input}"
        result = generate_response(full_prompt)

        st.session_state.history.append({
            "type": content_type,
            "input": user_input,
            "output": result
        })

        st.success("Done!")
        st.markdown("### ✅ Output")
        st.write(result)
        st.download_button("⬇️ Download", result, file_name="content.txt", mime="text/plain")


with st.sidebar:
    st.markdown(f"### 🤖 Generated contents: {len(st.session_state.history)}")
    
    for i, entry in enumerate(reversed(st.session_state.history[-50:]), 1):
        input_preview = entry.get("input", "")[:30].title()

        with st.expander(f"{i}. {entry['type']}: {input_preview}"):
            st.markdown("##### ✍️ Output")
            st.write(entry.get("output", "_No content available_"))
