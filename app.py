import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp

# --- KRİTİK DÜZELTME ---
# mp.solutions yerine direkt dosyadan çekiyoruz.
# Python 3.10'da bu yöntem %100 çalışır.
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_draw

st.set_page_config(page_title="SnakeDuet", layout="wide")
st.title("SnakeDuet - Hareket Testi (Final Fix)")

class VideoIsleyici(VideoTransformerBase):
    def __init__(self):
        # self.hands'i direkt yukarıda çağırdığımız modülden üretiyoruz
        self.hands = mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Ayna Efekti
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        orta_nokta = w // 2
        
        # Çizgi
        cv2.line(img, (orta_nokta, 0), (orta_nokta, h), (255, 255, 255), 2)

        # El Tespiti
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        sonuc = self.hands.process(img_rgb)

        if sonuc.multi_hand_landmarks:
            for el_noktalari in sonuc.multi_hand_landmarks:
                # Çizim
                mp_draw.draw_landmarks(img, el_noktalari, mp_hands.HAND_CONNECTIONS)

                # Koordinatlar
                bilek = el_noktalari.landmark[0]
                parmak_uc = el_noktalari.landmark[8]

                bilek_x, bilek_y = int(bilek.x * w), int(bilek.y * h)
                uc_x, uc_y = int(parmak_uc.x * w), int(parmak_uc.y * h)

                fark_x = uc_x - bilek_x
                fark_y = bilek_y - uc_y 

                yon = "DURUYOR"
                hassasiyet = 40 

                if abs(fark_x) > abs(fark_y):
                    if fark_x > hassasiyet: yon = "SAG"
                    elif fark_x < -hassasiyet: yon = "SOL"
                else:
                    if fark_y > hassasiyet: yon = "YUKARI"
                    elif fark_y < -hassasiyet: yon = "ASAGI"

                if bilek_x < orta_nokta:
                    cv2.putText(img, f"SOL: {yon}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    cv2.putText(img, f"SAG: {yon}", (w - 350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        return img

st.write("Lütfen START butonuna bas.")

webrtc_streamer(
    key="hareket-fix",
    video_transformer_factory=VideoIsleyici
)