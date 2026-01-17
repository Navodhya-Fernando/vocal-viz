# VocalViz – Live Spectrogram & Audio Analytics 🎙️📊

*Modern Streamlit app for real‑time audio visualization, comparison, and feature extraction directly in the browser.*

[![Platform](https://img.shields.io/badge/Platform-Streamlit-FF4B4B)](#)
[![Audio](https://img.shields.io/badge/Audio-WebAudio%20API-00c2ff)](#)
[![Language](https://img.shields.io/badge/Language-Python-3776AB)](#)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](#)
[![License](https://img.shields.io/badge/License-MIT-black)](#)

---

## 🔗 Live App

**Streamlit App:**

```text
https://vocal-viz.streamlit.app
```

---

## ✨ Overview

VocalViz is a lightweight but powerful **real‑time audio analysis dashboard** built with Streamlit and Web Audio API.  
It allows you to:

* Visualize audio as a scrolling spectrogram  
* Compare two audio sources (A vs B)  
* Monitor live microphone input  
* Extract core audio features in real time  
* Apply a noise gate to stabilize measurements

The interface is designed for **speech analysis, podcast testing, voice research, and creative audio exploration**.

---

## 🧠 Core Features

* 🎤 Live microphone capture with permission handling  
* 📁 Upload and analyze audio files (WAV/MP3/etc.)  
* 🆚 Compare Mode with A vs B sparklines  
* 🚧 Noise Gate slider to ignore low‑level mic noise  
* 📈 Real‑time metrics:
  - Spectral Centroid (brightness)  
  - RMS Power (loudness)  
  - Clarity Ratio (harmonic proxy)
* 📸 Snapshot download of active spectrogram  
* 🖥 Fullscreen canvas mode  
* 🔁 Swap A/B sources instantly  
* 🧼 One‑click reset

---

## 📁 Project Structure

```bash
vocal-viz/
│
├── app.py                # Streamlit + UI + WebAudio pipeline
├── requirements.txt      # Dependencies
├── README.md             # Project overview
├── LICENSE               # MIT license
└── .gitignore
```

---

## ⚙️ Setup Guide

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install streamlit
```

---

### 2️⃣ Run locally

```bash
streamlit run app.py
```

Open in browser:

```text
http://localhost:8501
```

> You must allow **microphone permissions** in the browser to use live input.

---

## 🔧 How It Works

* Audio is processed using the **Web Audio API** inside a Streamlit HTML component  
* FFT size: 2048  
* Metrics are extracted from frequency bins in real time  
* Compare mode maintains short histories for A and B  
* Noise gate ignores RMS below selected threshold for mic input

---

## 🧱 Roadmap

* [ ] Pitch / F0 tracking overlay  
* [ ] MFCC feature extraction  
* [ ] Export metrics as CSV  
* [ ] Record & download mic sessions  
* [ ] ML voice embeddings preview  
* [ ] Theme toggle (dark / true black)

---

## 🪪 License

This project is licensed under the **MIT License**.  
See [`LICENSE`](./LICENSE) for full details.