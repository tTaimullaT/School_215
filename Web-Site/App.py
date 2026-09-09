# App.py — Teacher Assistant v2 🚀
import streamlit as st
from openai import OpenAI

# --- 0. Auto-pick the provider: Groq key if you have one, DeepSeek otherwise ---
if "GROQ_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    model = "llama-3.3-70b-versatile"
else:
    client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    model = "deepseek-chat"

# --- 1. Collect inputs from the teacher ---
st.title("🎓 Teacher Assistant")
st.header("Lesson Plan Generator")

topic = st.text_input("Lesson topic", placeholder="e.g. Photosynthesis")
grade = st.selectbox(
    "Grade level", ["5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"])
minutes = st.slider("Lesson length (minutes)", 30, 90, 45)
extra = st.text_area("Extra notes (optional)",
                     placeholder="e.g. focus on vocabulary")

# --- 2. Generate on click ---
if st.button("⚡ Generate Lesson Plan"):
    if not topic:
        st.warning("Type a topic first 🙂")
    else:
        with st.spinner("Writing your lesson plan..."):
            # --- 3. Build the prompt ---
            prompt = f"""You are a veteran teacher with 20 years of classroom experience.
Create a practical lesson plan:
- Topic: {topic}
- Grade: {grade}
- Length: {minutes} minutes
- Teacher's notes: {extra or "none"}

Answer in markdown with sections:
1. Lesson objectives (2-3 bullets)
2. Timed breakdown — split the {minutes} minutes into blocks (warm-up, main activity, practice, wrap-up)
3. Materials needed
4. Homework (one short task)"""

            # --- 4. Send it ---
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a veteran teacher. Output clear, practical lesson plans in markdown."},
                    {"role": "user", "content": prompt},
                ],
            )
            answer = response.choices[0].message.content

            # --- 5. Show + download ---
            st.markdown("---")
            st.markdown(answer)
            st.download_button("⬇️ Download this plan", answer,
                               file_name=f"lesson_plan_{topic}.md")
