import streamlit as st
from streamlit_webrtc import webrtc_streamer
from processor import VideoIsleyici

st.set_page_config(page_title="SnakeDuet", layout="wide")
st.title("SnakeDuet")

webrtc_streamer(
    key="hareket-fix",
    video_transformer_factory=VideoIsleyici
)