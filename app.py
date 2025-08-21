import streamlit as st
import os

st.set_page_config(page_title="Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 Snake Game")
st.write("Welcome to your Snake Game project!")

st.info("⚠️ Note: Snake Game uses Pygame window, "
        "which does not run in the browser on Render. "
        "This button will only work locally, not online.")

if st.button("▶️ Play Snake Game (Local Only)"):
    os.system("python snakegame.py")
