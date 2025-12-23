# 🌱 AI Crop Disease Detection & Smart Treatment Advisor

An end-to-end **AI-powered plant disease detection system** that identifies crop diseases from leaf images using **Convolutional Neural Networks (CNN)** and provides **weather-aware treatment recommendations** (organic + chemical group-based) through an interactive **Streamlit dashboard**.

This project focuses on solving a **real-world agricultural problem** by combining **Deep Learning, Weather Intelligence, and Generative AI**.

---

## 🚀 Key Features

- 📷 **CNN-based Disease Detection** from leaf images  
- 🌦 **Real-time Weather Analysis** using Open-Meteo API  
- ⚠️ **Disease Spread Risk Assessment** (Low / Moderate / High)  
- 💊 **Treatment Recommendations**
  - Chemical (group-based, no brand names)
  - Organic / biological alternatives  
- 🌍 **Automatic Location Detection** (IP-based) with manual fallback  
- 🌐 **English + Hindi support** for farmer-friendly output  
- 🔄 **Offline fallback system** when Gemini API is unavailable  
- 🖥 **Interactive Streamlit Dashboard**

---

## 🧠 Tech Stack

- **Python**
- **TensorFlow / Keras**
- **Convolutional Neural Network (CNN)**
- **Streamlit**
- **Open-Meteo Weather API**
- **Google Gemini API**
- **NumPy, Pandas**

---

## 📂 Project Structure

# 🌱 AI Crop Disease Detection & Smart Treatment Advisor

An end-to-end **AI-powered plant disease detection system** that identifies crop diseases from leaf images using **Convolutional Neural Networks (CNN)** and provides **weather-aware treatment recommendations** (organic + chemical group-based) through an interactive **Streamlit dashboard**.

This project focuses on solving a **real-world agricultural problem** by combining **Deep Learning, Weather Intelligence, and Generative AI**.

---

## 🚀 Key Features

- 📷 **CNN-based Disease Detection** from leaf images  
- 🌦 **Real-time Weather Analysis** using Open-Meteo API  
- ⚠️ **Disease Spread Risk Assessment** (Low / Moderate / High)  
- 💊 **Treatment Recommendations**
  - Chemical (group-based, no brand names)
  - Organic / biological alternatives  
- 🌍 **Automatic Location Detection** (IP-based) with manual fallback  
- 🌐 **English + Hindi support** for farmer-friendly output  
- 🔄 **Offline fallback system** when Gemini API is unavailable  
- 🖥 **Interactive Streamlit Dashboard**

---

## 🧠 Tech Stack

- **Python**
- **TensorFlow / Keras**
- **Convolutional Neural Network (CNN)**
- **Streamlit**
- **Open-Meteo Weather API**
- **Google Gemini API**
- **NumPy, Pandas**

---

## 📂 Project Structure

PLANTDISEASEFINAL/
│
├── app/
│ ├── streamlit_app.py
│ ├── predict.py
│ ├── knowledge_base/
│
├── dataset/ # Not uploaded (large size)
│ ├── train/
│ ├── valid/
│ └── test/
│
├── models/ # Not uploaded
│
├── train_model.py
├── continue_training.py
├── requirements.txt
├── class_indices.json
├── README.md
└── .gitignore

## 📊 Dataset Used

**New Plant Diseases Dataset (Augmented)**  
📌 Kaggle Link:  
https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

> ⚠️ Dataset is **not uploaded to GitHub** due to large size.  
> Please download manually and place it inside the `dataset/` folder with `train`, `valid`, and `test` subfolders.

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/HimanshuKumar83/Plant-Disease-Prediction-and-Management-System
cd PLANTDISEASEFINAL

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Train the CNN Model (Optional)
python train_model.py


Pre-trained models are excluded from GitHub.

5️⃣ Run the Streamlit App
cd app
streamlit run streamlit_app.py

##  🧩 Project Workflow

User uploads leaf image

Image preprocessing (resize, normalization)

CNN extracts visual features

Softmax layer predicts disease probabilities

Location auto-detected → weather fetched

Disease risk calculated from humidity & rainfall

Gemini API generates smart treatment plan

Offline knowledge base used if API fails

##👤 About Me

I am an aspiring Machine Learning Engineer with strong interest in:

Artificial Intelligence & Deep Learning

Computer Vision

Data Science

Real-world problem solving using AI

I enjoy building practical, end-to-end projects that go beyond academic submissions and focus on real impact, clean design, and explainability.

📌 Open to internships, projects, and collaborations in:

Machine Learning

Data Science

AI Engineering

##⭐ Future Improvements

Mobile-friendly farmer app

Multi-language regional support

Disease severity prediction

Cloud deployment (AWS / GCP)

Time-series disease forecasting