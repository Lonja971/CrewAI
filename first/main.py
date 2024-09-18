import streamlit as st
from crew_ai.crewai_main import process_user_blog

st.title("Improving the text of the blog.")

user_text = st.text_area("Enter your text:")

if st.button("Improve"):
    if user_text:
        with st.spinner("We are processing your text..."):
            result = process_user_blog(user_text)
            st.success("Answer received!")
            st.write(result.raw)
    else:
        st.error("Please enter a text.")