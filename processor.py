import cv2
import numpy as np
from streamlit_webrtc import VideoTransformerBase
from game import Yilan, Yem

from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_draw

class VideoIsleyici(VideoTransformerBase):
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.OYUN_GENISLIK = 600 
        self.OYUN_YUKSEKLIK = 480
        
        self.yilan_sol = Yilan(100, 240, (0, 255, 0)) 
        self.yilan_sag = Yilan(self.OYUN_GENISLIK - 100, 240, (0, 0, 255))

        self.yem = Yem(self.OYUN_GENISLIK, self.OYUN_YUKSEKLIK)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        kamera_orta = w // 2
        sol_kamera = img[:, :kamera_orta]
        sag_kamera = img[:, kamera_orta:]

        oyun_tahtasi = np.zeros((h, self.OYUN_GENISLIK, 3), dtype=np.uint8)
        
        self.yem.ekran_w = self.OYUN_GENISLIK
        self.yem.ekran_h = h

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        sonuc = self.hands.process(img_rgb)

        sol_komut = "DURUYOR"
        sag_komut = "DURUYOR"

        if sonuc.multi_hand_landmarks:
            for el_noktalari in sonuc.multi_hand_landmarks:

                bilek = el_noktalari.landmark[0]
                parmak_uc = el_noktalari.landmark[8]

                bilek_x_global = int(bilek.x * w)

                bilek_x = int(bilek.x * w)
                bilek_y = int(bilek.y * h)
                uc_x = int(parmak_uc.x * w)
                uc_y = int(parmak_uc.y * h)

                fark_x = uc_x - bilek_x
                fark_y = bilek_y - uc_y 
                yon = "DURUYOR"
                hassasiyet = 30 

                if abs(fark_x) > abs(fark_y):
                    if fark_x > hassasiyet: yon = "SAG"
                    elif fark_x < -hassasiyet: yon = "SOL"
                else:
                    if fark_y > hassasiyet: yon = "YUKARI"
                    elif fark_y < -hassasiyet: yon = "ASAGI"

                if bilek_x_global < kamera_orta:
                    sol_komut = yon
                    mp_draw.draw_landmarks(img, el_noktalari, mp_hands.HAND_CONNECTIONS)
                    cv2.putText(sol_kamera, f"YON: {yon}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    sag_komut = yon
                    mp_draw.draw_landmarks(img, el_noktalari, mp_hands.HAND_CONNECTIONS)
                    cv2.putText(sag_kamera, f"YON: {yon}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        self.yem.ciz(oyun_tahtasi, cv2)

        self.yilan_sol.hareket_et(sol_komut, self.OYUN_GENISLIK, h)
        if self.yilan_sol.yedi_mi(self.yem):
            self.yem.spawn()
        self.yilan_sol.ciz(oyun_tahtasi, cv2)

        self.yilan_sag.hareket_et(sag_komut, self.OYUN_GENISLIK, h)
        if self.yilan_sag.yedi_mi(self.yem):
            self.yem.spawn()
        self.yilan_sag.ciz(oyun_tahtasi, cv2)

        cv2.putText(oyun_tahtasi, str(self.yilan_sol.skor), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(oyun_tahtasi, str(self.yilan_sag.skor), (self.OYUN_GENISLIK - 60, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        cv2.line(oyun_tahtasi, (self.OYUN_GENISLIK//2, 0), (self.OYUN_GENISLIK//2, h), (50, 50, 50), 1)

        sol_kamera_guncel = img[:, :kamera_orta]
        sag_kamera_guncel = img[:, kamera_orta:]
        
        final_goruntu = np.concatenate((sol_kamera_guncel, oyun_tahtasi, sag_kamera_guncel), axis=1)

        return final_goruntu