# Real-Time Screen OCR & Text Extractor

### Overview
This project is a high-performance Python tool designed to automate text extraction from video streams in real-time. It monitors a specific area of the screen, performs Optical Character Recognition (OCR), cleans the output, and saves unique sentences to a text file.

### Key Engineering Features
* **Efficient Screen Capture:** Utilizes the `mss` library for low-latency frame grabbing, focusing only on a calibrated sub-region to minimize CPU load.
* **Neural OCR Engine:** Powered by `EasyOCR` (Convolutional Neural Network based) to ensure high accuracy in character recognition for the Polish language.
* **Intelligent Deduplication:** Implements a similarity-check algorithm using `difflib.SequenceMatcher`. This prevents redundant data logging by comparing new captures with previous entries based on a defined threshold (80% similarity).
* **Text Refinement Pipeline:** * **Noise Reduction:** Uses Regular Expressions (RegEx) to filter out non-textual artifacts.
    * **Automated Correction:** Integrated `autocorrect` library to fix recognition errors in real-time.

### Tech Stack
* **Core:** Python 3.x
* **Computer Vision:** OpenCV, EasyOCR
* **Data Processing:** NumPy, RegEx, Difflib
* **Performance:** mss (low-level screen capture)

### Relevance to Research Engineering (R&D)
This script demonstrates an end-to-end **Computer Vision Pipeline** similar to those used in biometric systems (e.g., Rococo's AUTH system):
1. **Signal Extraction:** Converting raw visual signals into structured data.
2. **Robustness:** Handling "noise" and environmental variables through software-level filtering and validation.
3. **Efficiency:** Managing computational resources (sampling intervals and localized cropping) to ensure stable performance.
