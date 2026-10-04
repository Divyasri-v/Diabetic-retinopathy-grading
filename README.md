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
