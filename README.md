Setup and Installation

This project uses Python packages and a native Tesseract OCR engine. Follow the steps below on Windows (PowerShell) to create an isolated environment and install everything needed.

1) Create a virtual environment (no activation required for these commands):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
```

2) Install CPU-only PyTorch (recommended for most Windows users without a CUDA GPU):

```powershell
.venv\Scripts\python -m pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio
```

3) Install the remaining Python dependencies from `requirements.txt`:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
```

4) Install Tesseract OCR (native binary) for Windows:
- Preferred: download and run the installer from the UB Mannheim builds: https://github.com/UB-Mannheim/tesseract/wiki
- Or try `winget install --id UB.Mannheim.Tesseract` if you have `winget`.

After installing, ensure Tesseract is on your PATH (e.g., `C:\Program Files\Tesseract-OCR`). Verify:

```powershell
tesseract --version
```

If `tesseract` isn't recognized, add its folder to your PATH or set `pytesseract.pytesseract.tesseract_cmd` in `ocr_utils.py` (not recommended if PATH is configured).

5) Run the Flask app:

```powershell
# use the venv python to run
.venv\Scripts\python app.py
# then open http://127.0.0.1:5000/ in your browser
```

Notes & Tips
- The summarizer loads `facebook/bart-large-cnn` by default; the first run will download the model (~1.5GB). If you want a smaller/faster model, edit `summarizer.py` and change the model string (e.g., `sshleifer/distilbart-cnn-12-6`).
- If you have a GPU and want CUDA-enabled PyTorch, follow instructions at https://pytorch.org/get-started/locally/ and install the appropriate `torch` wheel instead of the CPU wheel above.
- To avoid PowerShell execution policy issues, the commands above invoke the venv python directly and do not require activating the venv shell.

Troubleshooting
- If `pymupdf` fails to install, ensure you have a recent `pip` and a supported Python version (3.8+ recommended).
- If `pytesseract` returns empty text, confirm `tesseract --version` works and the PATH is correct.
