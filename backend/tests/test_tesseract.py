"""Quick verification script for Tesseract OCR integration.
Run: python tests/test_tesseract.py
"""
import os
import sys

try:
    import pytesseract
except ImportError:
    print("ERROR: pytesseract not installed. Install with: pip install pytesseract pillow")
    sys.exit(1)

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv not installed, using system env only")

# Allow override via env variable
custom_path = os.getenv("TESSERACT_PATH")
if custom_path:
    pytesseract.pytesseract.tesseract_cmd = custom_path
    print(f"Using TESSERACT_PATH from .env: {custom_path}")
elif os.name == "nt":
    # Fallback to common Windows install path
    default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.isfile(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path
        print(f"Using default Windows path: {default_path}")

# Show resolved path
print(f"Tesseract command: {pytesseract.pytesseract.tesseract_cmd}")

# Version check
try:
    version = pytesseract.get_tesseract_version()
    print(f"Tesseract version detected: {version}")
except Exception as e:
    print(f"Failed to get Tesseract version: {e}")
    print("If not installed, download Windows installer from: https://github.com/UB-Mannheim/tesseract/wiki")
    sys.exit(1)

# Optional sample OCR if sample image exists
sample_image = "sample_receipt.png"
if os.path.isfile(sample_image):
    try:
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(sample_image))
        print("--- OCR Output (first 300 chars) ---")
        print(text[:300])
    except Exception as e:
        print(f"OCR test failed: {e}")
else:
    print(f"No '{sample_image}' found. Place a receipt image as '{sample_image}' to test OCR.")

print("Tesseract OCR check completed.")
