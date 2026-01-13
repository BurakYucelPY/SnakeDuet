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
        self.KARE_BOYUTU = 20  # Grid kare boyutu
        self.yilan_sol = Yilan(100, 240, (0, 255, 0))
        self.yilan_sag = Yilan(self.OYUN_GENISLIK - 100, 240, (0, 0, 255))
        self.yem = Yem(self.OYUN_GENISLIK, self.OYUN_YUKSEKLIK)

        # Oyun Durumu
        self.oyun_basladi = False
        self.baslangic_sayaci = 0
        self.oyun_bitti = False
        self.kazanan = None  # "yesil", "kirmizi" veya "berabere"
        self.tekrar_sayaci = 0  # Tekrar oynamak için geri sayım

    def ciz_neon_grid(self, img):
        """Mavi neon kareli zemin çizer"""
        h, w = img.shape[:2]

        img[:] = (10, 10, 20)

        neon_mavi = (255, 150, 0)  
        koyu_mavi = (80, 40, 0)    

        for x in range(0, w, self.KARE_BOYUTU):
            cv2.line(img, (x, 0), (x, h), koyu_mavi, 1)

        for y in range(0, h, self.KARE_BOYUTU):
            cv2.line(img, (0, y), (w, y), koyu_mavi, 1)

        cv2.rectangle(img, (2, 2), (w-3, h-3), neon_mavi, 2)
        
        return img

    def ciz_oyun_bitti_ekrani(self, img, eller_gorunuyor=False):
        """Oyun bitti ekranını çizer"""
        h, w = img.shape[:2]
        
        # Yarı saydam koyu overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Panel çerçevesi
        panel_x1, panel_y1 = w // 6, h // 5
        panel_x2, panel_y2 = w - w // 6, h - h // 6
        cv2.rectangle(img, (panel_x1, panel_y1), (panel_x2, panel_y2), (255, 255, 255), 3)
        cv2.rectangle(img, (panel_x1 + 5, panel_y1 + 5), (panel_x2 - 5, panel_y2 - 5), (30, 30, 30), -1)
        
        # Oyun Bitti yazısı
        cv2.putText(img, "OYUN BITTI!", (w // 2 - 120, panel_y1 + 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        
        # Kazanan bilgisi
        if self.kazanan == "yesil":
            cv2.putText(img, "YESIL YILAN KAZANDI!", (w // 2 - 170, h // 2 - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        elif self.kazanan == "kirmizi":
            cv2.putText(img, "KIRMIZI YILAN KAZANDI!", (w // 2 - 180, h // 2 - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            cv2.putText(img, "BERABERE!", (w // 2 - 80, h // 2 - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
        
        # Skorlar
        skor_text = f"YESIL: {self.yilan_sol.skor}  -  KIRMIZI: {self.yilan_sag.skor}"
        cv2.putText(img, skor_text, (w // 2 - 140, h // 2 + 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        # Tekrar oyna talimatı ve geri sayım
        if eller_gorunuyor and self.tekrar_sayaci > 0:
            # Geri sayım göster
            kalan = 3 - (self.tekrar_sayaci // 10)
            if kalan > 0:
                cv2.putText(img, f"BASLIYOR: {kalan}", (w // 2 - 100, h // 2 + 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        else:
            cv2.putText(img, "Tekrar oynamak icin", (w // 2 - 130, h // 2 + 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(img, "ELLERINI GOSTER", (w // 2 - 120, h // 2 + 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(img, "veya asagidaki butona tikla", (w // 2 - 160, h // 2 + 110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 2)
        
        return img

    def oyunu_sifirla(self):
        """Oyunu sıfırlar ve yeniden başlatır"""
        self.yilan_sol.reset(100, 240)
        self.yilan_sag.reset(self.OYUN_GENISLIK - 100, 240)
        self.yem.spawn()
        self.oyun_bitti = False
        self.kazanan = None
        self.tekrar_sayaci = 0
        self.oyun_basladi = True

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        img = cv2.resize(img, (640, self.OYUN_YUKSEKLIK))
        h, w, _ = img.shape
        
        kamera_orta = w // 2
        sol_kamera = img[:, :kamera_orta]
        sag_kamera = img[:, kamera_orta:]

        oyun_tahtasi = np.zeros((self.OYUN_YUKSEKLIK, self.OYUN_GENISLIK, 3), dtype=np.uint8)
        self.ciz_neon_grid(oyun_tahtasi)
        
        self.yem.ekran_w = self.OYUN_GENISLIK
        self.yem.ekran_h = self.OYUN_YUKSEKLIK

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

        if not self.oyun_basladi:
            # Giriş Ekranı
            cv2.putText(oyun_tahtasi, "SNAKE DUET", (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
            
            if sonuc.multi_hand_landmarks:
                self.baslangic_sayaci += 1
                kalan_sure = 30 - self.baslangic_sayaci
                if kalan_sure > 0:
                    cv2.putText(oyun_tahtasi, f"BASLIYOR: {kalan_sure // 10 + 1}", (220, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    self.oyun_basladi = True
                    self.baslangic_sayaci = 0
            else:
                self.baslangic_sayaci = 0
                cv2.putText(oyun_tahtasi, "ELLERINI GOSTER", (180, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        elif self.oyun_bitti:
            # Oyun Bitti Ekranı
            self.yilan_sol.ciz(oyun_tahtasi, cv2)
            self.yilan_sag.ciz(oyun_tahtasi, cv2)
            
            eller_gorunuyor = sonuc.multi_hand_landmarks is not None
            
            if eller_gorunuyor:
                self.tekrar_sayaci += 1
                if self.tekrar_sayaci >= 30:  # 3 saniyelik geri sayım
                    self.oyunu_sifirla()
            else:
                self.tekrar_sayaci = 0
            
            self.ciz_oyun_bitti_ekrani(oyun_tahtasi, eller_gorunuyor)
        
        else:
            # Oyun Mantığı
            self.yem.ciz(oyun_tahtasi, cv2)
            
            # Yılanları hareket ettir
            self.yilan_sol.hareket_et(sol_komut, self.OYUN_GENISLIK, self.OYUN_YUKSEKLIK)
            self.yilan_sag.hareket_et(sag_komut, self.OYUN_GENISLIK, self.OYUN_YUKSEKLIK)
            
            # Yem yeme kontrolü
            if self.yilan_sol.yedi_mi(self.yem):
                self.yem.spawn()
            if self.yilan_sag.yedi_mi(self.yem):
                self.yem.spawn()
            
            # Çarpışma kontrolleri
            sol_carpti = self.yilan_sol.carpti_mi(self.yilan_sag) or self.yilan_sol.kendine_carpti_mi()
            sag_carpti = self.yilan_sag.carpti_mi(self.yilan_sol) or self.yilan_sag.kendine_carpti_mi()
            
            # Oyun bitti mi kontrol et
            if sol_carpti or sag_carpti:
                self.oyun_bitti = True
                if sol_carpti and sag_carpti:
                    self.kazanan = "berabere"
                elif sol_carpti:
                    self.kazanan = "kirmizi"
                else:
                    self.kazanan = "yesil"
            
            # Yılanları çiz
            self.yilan_sol.ciz(oyun_tahtasi, cv2)
            self.yilan_sag.ciz(oyun_tahtasi, cv2)

            # Skorları göster
            cv2.putText(oyun_tahtasi, str(self.yilan_sol.skor), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.putText(oyun_tahtasi, str(self.yilan_sag.skor), (self.OYUN_GENISLIK - 60, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        sol_kamera_guncel = img[:, :kamera_orta]
        sag_kamera_guncel = img[:, kamera_orta:]
        final_goruntu = np.concatenate((sol_kamera_guncel, oyun_tahtasi, sag_kamera_guncel), axis=1)
        return final_goruntu