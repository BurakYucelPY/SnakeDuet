import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np

st.set_page_config(page_title="SnakeDuet", layout="wide")
st.title("SnakeDuet - Kamera Testi")

class VideoIsleyici(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = cv2.flip(img, 1)
        
        h, w, _ = img.shape 
        orta_nokta = w // 2
        
        cv2.line(img, (orta_nokta, 0), (orta_nokta, h), (255, 255, 255), 2)
        
        cv2.putText(img, "SOL OYUNCU", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, "SAG OYUNCU", (w - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return img

st.write("Kamera erişimi başlatılıyor. Aşağıdaki 'START' butonuna bas.")

# WebRTC başlatıcı
webrtc_streamer(
    key="test",
    video_transformer_factory=VideoIsleyici
)