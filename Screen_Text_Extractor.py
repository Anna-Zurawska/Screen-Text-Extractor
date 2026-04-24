import mss
import cv2
import numpy as np
import easyocr
import time
import re
import difflib
from autocorrect import Speller

OUTPUT_FILE = "napisy_z_wideo.txt"

# Inicjalizacja modeli: OCR dla PL i autokorekta, gpu wyłączone bo na laptopie nie ma sensu
reader = easyocr.Reader(['pl'], gpu=False)
spell = Speller(lang='pl')

# Obszar skanowania (z kalibracji): top, left, width, height
crop_area = {"top": 1224, "left": 2207, "width": 1336, "height": 280}

def get_similarity(s1, s2):
    """Liczy podobieństwo tekstów, żeby unikać duplikatów"""
    return difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def run_scanner():
    captured_text = []
    
    print("Skaner gotowy. Naciśnij 'q' w oknie podglądu, by zakończyć.")

    with mss.mss() as sct:
        while True:
            # Zrzut wybranego fragmentu ekranu
            img = np.array(sct.grab(crop_area))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Odczyt tekstu - paragraph=True łączy linie w bloki
            results = reader.readtext(frame, detail=0, paragraph=True)
            text = " ".join(results).strip()

            if len(text) > 3:
                # Czyszczenie znaków specjalnych i poprawianie literówek
                clean = re.sub(r'[^a-zA-ZąęćłńóśźżĄĘĆŁŃÓŚŹŻ\s.,!?-]', '', text)
                final = " ".join([spell(w) for w in clean.split()])

                # Zapisujemy tylko, jeśli tekst różni się od poprzedniego (>80%)
                is_new = True
                if captured_text and get_similarity(final, captured_text[-1]) > 0.8:
                    is_new = False

                if is_new:
                    captured_text.append(final)
                    print(f"Dodano: {final}")

            # Mini podgląd dla kontroli obszaru
            cv2.imshow("Preview", cv2.resize(frame, (400, 100)))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(0.5) # Przerwa dla oszczędności CPU

    cv2.destroyAllWindows()

    # Zapis do TXT
    if captured_text:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(captured_text))
        print(f"Zapisano {len(captured_text)} linii do {OUTPUT_FILE}")

if __name__ == "__main__":
    run_scanner()