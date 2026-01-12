import cv2
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

        self.yilan_sol = Yilan(150, 150, (0, 255, 0)) # Yeşil
        self.yilan_sag = Yilan(450, 150, (0, 0, 255)) # Kırmızı

        self.yem = Yem(640, 480)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        orta_nokta = w // 2
        
        self.yem.ekran_w = w
        self.yem.ekran_h = h
        
        cv2.line(img, (orta_nokta, 0), (orta_nokta, h), (255, 255, 255), 2)

        # El Tespiti
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        sonuc = self.hands.process(img_rgb)

        sol_komut = "DURUYOR"
        sag_komut = "DURUYOR"

        if sonuc.multi_hand_landmarks:
            for el_noktalari in sonuc.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, el_noktalari, mp_hands.HAND_CONNECTIONS)

                bilek = el_noktalari.landmark[0]
                parmak_uc = el_noktalari.landmark[8]

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

                if bilek_x < orta_nokta:
                    sol_komut = yon
                else:
                    sag_komut = yon

        self.yem.ciz(img, cv2)

        self.yilan_sol.hareket_et(sol_komut, w, h)
        if self.yilan_sol.yedi_mi(self.yem):
            self.yem.spawn()
        self.yilan_sol.ciz(img, cv2)

        self.yilan_sag.hareket_et(sag_komut, w, h)
        if self.yilan_sag.yedi_mi(self.yem):
            self.yem.spawn()
        self.yilan_sag.ciz(img, cv2)

        cv2.putText(img, f"Skor: {self.yilan_sol.skor}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Skor: {self.yilan_sag.skor}", (w - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return img