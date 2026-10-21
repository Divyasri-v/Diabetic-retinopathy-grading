# Diabetic Retinopathy Grading Using Deep Learning

## 📌 Project Overview

This project uses deep learning to classify retinal fundus images into five stages of diabetic retinopathy. A pretrained MobileNetV2 model with transfer learning is used to predict the severity level from Grade 0 to Grade 4.

## 🎯 Objective

To develop a deep-learning-based prototype that can analyze a retinal image and predict the severity of diabetic retinopathy.

## 🩺 Retinopathy Grades

| Grade   | Severity                           |
| ------- | ---------------------------------- |
| Grade 0 | No Diabetic Retinopathy            |
| Grade 1 | Mild                               |
| Grade 2 | Moderate                           |
| Grade 3 | Severe                             |
| Grade 4 | Proliferative Diabetic Retinopathy |

## 🛠️ Technologies Used

* Python
* TensorFlow / Keras
* MobileNetV2
* Transfer Learning
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Google Colab

## 📊 Dataset

The project uses a colored retinal fundus image dataset containing five diabetic retinopathy severity classes.

A balanced subset of **3,500 images** was used for model development, with **700 images per class**.

## 🧠 Model

A pretrained **MobileNetV2** architecture was used as the base model.

The model was trained in two stages:

1. Transfer learning with the pretrained MobileNetV2 layers frozen.
2. Fine-tuning of the final 30 layers using a low learning rate.

## 📈 Results

The final selected model achieved:

* **Validation Accuracy: 43.43%**
* Five-class diabetic retinopathy classification
* Confusion matrix evaluation
* Confidence-based individual image prediction

The model can take a new retinal image as input and return the predicted diabetic retinopathy grade along with the prediction confidence.

## 🔍 Project Workflow

```text
Retinal Image
      ↓
Image Preprocessing
      ↓
MobileNetV2 Transfer Learning
      ↓
Feature Extraction
      ↓
Classification
      ↓
Grade 0 – Grade 4
      ↓
Prediction + Confidence
```

## 📁 Project Files

* `Diabetic_Retinopathy_Grading.ipynb` — Complete project notebook
* `diabetic_retinopathy_model.keras` — Trained deep learning model

## ⚠️ Disclaimer

This project is an academic deep-learning prototype intended for educational and demonstration purposes. It is **not a medical diagnostic system** and should not be used as a substitute for professional medical evaluation.

## 👩‍💻 Author

Divyasri V
B.Tech Artificial Intelligence and Data Science
Rajalakshmi Engineering College
# Diabetic Retinopathy Grading Using Deep Learning

A Streamlit website that grades retinal fundus photographs into five diabetic retinopathy (DR) stages using the project's **own trained EfficientNetB0 model** (`models/diabetic_retinopathy_model.keras`). Nothing is retrained and no other model is used.

**Project members**

| Name | Roll Number |
|---|---|
| Divyasri.V | 241801063 |
| Divyadarshini.S | 241801059 |

> **Educational project only.** Not a medical device. It must not be used to diagnose or treat any condition.

---

## What is in this folder

```
diabetic-retinopathy-website/
├── app.py                  <- the file you run (website entry point)
├── requirements.txt        <- Python packages to install
├── README.md               <- this file
├── .gitignore
├── .streamlit/config.toml  <- theme and server settings
├── models/
│   └── diabetic_retinopathy_model.keras   <- YOUR trained model (already included)
├── utils/
│   ├── config.py           <- settings (paths, class names, preprocessing options)
│   ├── preprocessing.py    <- image validation + resizing
│   ├── prediction.py       <- loads the model once and predicts
│   ├── evaluation.py       <- reads real evaluation results (if you create them)
│   └── ui.py               <- website styling
├── views/                  <- one file per page (Home, Predict, Dataset, Performance, About)
├── scripts/evaluate_model.py   <- optional: measure the model on your test images
├── evaluation/             <- optional results folder (empty until you run the script)
└── assets/retina.svg       <- illustration on the home page
```

You do **not** need the APTOS dataset to run the website. Predictions only need the model file.

---

## Step-by-step setup on Windows (VS Code)

### 0. Install the two programs you need (one time only)

1. **Python 3.11 or 3.12 (64-bit)** from <https://www.python.org/downloads/windows/>.
   During installation, **tick "Add python.exe to PATH"** at the bottom of the first screen.
   Do **not** use Python 3.14: TensorFlow does not support it yet.
2. **Visual Studio Code** from <https://code.visualstudio.com/>.

### 1. Download and extract the ZIP

1. Download `diabetic-retinopathy-website.zip`.
2. Right-click it, choose **Extract All…**, and pick a **short** location such as `C:\Projects`.
   (Short paths avoid a Windows "path too long" problem when installing TensorFlow.)
3. You should now have `C:\Projects\diabetic-retinopathy-website`.

### 2. Open the folder in VS Code

1. Start VS Code.
2. Choose **File → Open Folder…** and select the `diabetic-retinopathy-website` folder (the one that contains `app.py`).
3. If VS Code asks *"Do you trust the authors?"*, click **Yes, I trust the authors**.

### 3. Open the terminal

In VS Code choose **Terminal → New Terminal**. A panel opens at the bottom, already inside the project folder.

If the line starts with `PS C:\...>` you are in PowerShell. That is fine.

### 4. Create a virtual environment

```
python -m venv venv
```

Wait until it finishes (a few seconds, no message means success).
If `python` is not recognised, try `py -m venv venv` instead.

### 5. Activate the environment

```
venv\Scripts\activate
```

Your prompt should now begin with `(venv)`.

> **If PowerShell says "running scripts is disabled on this system"**, run this once and then repeat the activate command:
> ```
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```
> Or switch the terminal to **Command Prompt** (click the small `v` next to the `+` in the terminal panel → *Command Prompt*) and run `venv\Scripts\activate.bat`.

### 6. Install the packages

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This downloads TensorFlow and Streamlit (about 1 GB). It can take 5–15 minutes. Wait for it to finish.

### 7. Check the model file is in place

The file must be here:

```
diabetic-retinopathy-website\models\diabetic_retinopathy_model.keras
```

It is already included in the ZIP. If you ever delete or replace it, copy your `.keras` file back into the `models` folder and make sure the name is exactly `diabetic_retinopathy_model.keras`.

### 8. Run the website

```
streamlit run app.py
```

### 9. Open it in your browser

Streamlit normally opens your browser automatically. If not, open <http://localhost:8501>.
To stop the website, click in the terminal and press **Ctrl + C**.

### 10. Make a prediction

1. Click **Predict** in the left sidebar. The first visit takes 10–30 seconds while the model loads. It is loaded **once** and reused for every later image.
2. Upload a retinal fundus photograph (JPG, JPEG or PNG).
3. Click **Predict DR grade**.
4. You will see the predicted grade, the model output score, and the scores for all five grades.
5. Click **Upload another image** to start again.

Next time you only need steps 2, 3, 5, 8 (open folder, open terminal, activate, run).

---

## How predictions work (and one thing to double-check)

* The saved model is **EfficientNetB0 → global average pooling → dropout (0.3) → Dense(5, softmax)**, input `224 × 224 × 3`.
* Its first layers are `Rescaling(1/255)` and `Normalization`, so the model **normalises pixels itself and expects raw 0–255 values**. The website therefore only does: convert to RGB → resize to 224 × 224 → send to the model. It does **not** divide by 255.
* The percentage shown is the model's **output score** (softmax value), not a medically confirmed probability.

**Preprocessing uncertainty.** I could confirm the pixel scaling from the model file, but I could not see your training notebook, so I could not confirm *how images were resized* during training (Pillow vs TensorFlow resizing). On a test image, the two methods changed the scores noticeably. If you want to check this:

* On the Predict page open **Advanced: preprocessing options** and try **Resize method → TensorFlow bilinear**.
* To change the default, edit `RESIZE_BACKEND` (and, if ever needed, `PIXEL_SCALING`) in `utils/config.py`.
* Best check: run `scripts/evaluate_model.py` (below) once with each setting on your test images and keep the setting with the higher accuracy. The right setting should reproduce your recorded ~74.55%.

---

## Optional: generate the confusion matrix and classification report

The Model performance page shows your recorded results (accuracy 74.55%, loss ≈ 0.649). It only shows a confusion matrix / classification report when real results exist, because none were supplied with the project. To create them you need your **test images** and a CSV with columns `id_code,diagnosis` (the APTOS `train.csv` format, restricted to your 550 test images):

```
python scripts/evaluate_model.py --csv C:\data\test.csv --images C:\data\test_images
```

This writes `evaluation/confusion_matrix.csv`, `classification_report.txt` and `metrics.json`. Refresh the Model performance page and they appear. Use the *same* 550 test images from your project, otherwise the numbers will differ from the recorded ones.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| **"Model file missing" / red error on Predict page** | Put `diabetic_retinopathy_model.keras` in the `models` folder (exact name). Refresh the page. |
| **"The model file exists but could not be loaded"** | Your TensorFlow/Keras is too old for this model (it was saved with Keras 3.13). Run `pip install --upgrade -r requirements.txt` and restart. |
| **`python` / `pip` / `streamlit` is not recognised** | The environment isn't active. Run `venv\Scripts\activate` (prompt must show `(venv)`). If `python` itself is missing, reinstall Python and tick *Add to PATH*. |
| **PowerShell blocks `activate`** | See step 5 (`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`). |
| **`No matching distribution found for tensorflow`** | You have an unsupported Python (often 3.14 or 32-bit). Install 64-bit Python 3.11 or 3.12, delete the `venv` folder and redo steps 4–6. |
| **`OSError: [WinError 206]` or "path too long" during install** | Move the project to a short path like `C:\Projects\` or enable Windows long paths. Delete `venv` and redo steps 4–6. |
| **TensorFlow DLL load failed** | Install the *Microsoft Visual C++ Redistributable 2015–2022 (x64)* from Microsoft, then reinstall TensorFlow. |
| **Streamlit asks for an email** | Press **Enter** to skip. (This project's settings normally prevent the prompt.) |
| **Port 8501 already in use** | Run `streamlit run app.py --server.port 8502` and open <http://localhost:8502>. |
| **Upload shows "This image can't be used"** | The file is empty, corrupt, smaller than 64 px, larger than 15 MB, or not a real JPG/PNG (for example a renamed file). Re-export the photo as JPG or PNG. |
| **Only JPG, JPEG, PNG are accepted** | Convert other formats (e.g. TIFF, BMP, DICOM) to JPG or PNG first. |
| **Slow first prediction** | Normal. TensorFlow starts and loads the model once; later predictions take about a second. |
| **Fonts look plain** | The page loads fonts from Google Fonts and needs internet; it falls back to system fonts offline. Nothing else needs internet after installation. |

---

## What was tested (and what was not)

Tested in a Linux environment with Python 3.12, TensorFlow 2.21, Keras 3.15.1 and Streamlit 1.66, using the **exact model file included in this ZIP**:

* The model loads from `models/` and runs; its input is `(None, 224, 224, 3)` and its output is five softmax scores.
* The website's predictions are identical to calling `model.predict` directly on the same preprocessed image.
* All five pages render with no errors; navigation, upload, prediction, "Upload another image" and the invalid-upload messages (empty, corrupt, truncated, GIF, too small, too large) work, including in a real headless browser.
* Missing-model and corrupt-model errors show a clear message instead of crashing.
* `scripts/evaluate_model.py` and the confusion-matrix page run correctly, checked with scikit-learn on synthetic data.

**Not tested:**

* Running on Windows itself (I could not). The commands above are standard Windows commands, but I could not run them.
* Predictions on **real retinal photographs with known labels**. No labelled data was provided, so I have **not** reproduced the 74.55% accuracy, and the final choice of resize method is unconfirmed (see above). The recorded results (74.55% accuracy, loss ≈ 0.649, dataset split sizes) are your project's previously measured values; this website did not recompute them.
* Per-grade counts on the Dataset page (1,805 / 370 / 999 / 193 / 295) come from the public APTOS 2019 dataset description, not from your files. Verify them against Kaggle if you cite them.

---

## Recorded project information

| Item | Value |
|---|---|
| Dataset | APTOS 2019 Blindness Detection |
| Total / train / validation / test images | 3,662 / 2,563 / 549 / 550 |
| Input size | 224 × 224 pixels |
| Batch size / epochs | 16 / 10 |
| Test accuracy / test loss | 74.55% / ≈ 0.649 |
