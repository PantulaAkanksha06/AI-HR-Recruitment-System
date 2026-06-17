# 🤖 AI HR Recruitment System

## 📌 Overview

AI HR Recruitment System is an intelligent resume screening and candidate evaluation platform built using Generative AI, Semantic Search, Vector Databases, and LLM Observability.

The system automatically parses resumes, performs semantic matching against job descriptions, evaluates candidates using AI, generates professional HR emails, and provides a recruitment dashboard for decision-making.

---

## 🚀 Features

* Resume Parsing (PDF, DOCX, TXT)
* Candidate Information Extraction
* Semantic Job Matching
* AI-Powered Resume Analysis
* Candidate Ranking
* Professional Email Generation
* Recruitment Dashboard
* Qdrant Vector Database Integration
* Langfuse Observability & Tracing
* Automated Candidate Evaluation

---

## 🏗️ System Architecture

Resume Upload

↓
Resume Parsing

↓
Candidate Name & Email Extraction

↓
Experience Estimation

↓
Resume Embedding Generation

↓
Qdrant Vector Storage

↓
Semantic Matching

↓
AI Resume Analysis

↓
Professional Email Generation

↓
SQLite Storage

↓
Langfuse Monitoring & Tracing

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### AI Model

* Groq (Llama 3.3 70B Versatile)

### Embedding Model

* all-MiniLM-L6-v2

### Vector Database

* Qdrant Cloud

### Relational Database

* SQLite

### Observability

* Langfuse

### Email Service

* SMTP

### Environment

* Python Virtual Environment (venv)

---

## 📊 Key Functionalities

### Resume Screening

* Extracts candidate details
* Calculates semantic similarity score
* Evaluates candidate strengths and weaknesses
* Generates hiring recommendations

### Candidate Ranking

* Scores candidates based on job description relevance
* Stores embeddings for future semantic search

### Email Automation

* Generates professional HR emails
* Sends shortlisted/rejection notifications automatically

### Observability

* Tracks prompts and responses using Langfuse
* Monitors LLM execution traces
* Helps debug and optimize AI workflows

---

## 📷 Screenshots

### Resume Screening Page

(Add Screenshot Here)

### Recruitment Dashboard

(Add Screenshot Here)

### Langfuse Monitoring Dashboard

(Add Screenshot Here)

---

## ⚙️ Installation

### Clone Repository

git clone https://github.com/PantulaAkanksha06/AI-HR-Recruitment-System.git

cd AI-HR-Recruitment-System

### Create Virtual Environment

python -m venv venv

source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Configure Environment Variables

Create a `.env` file using `.env.example`

### Run Application

streamlit run app.py

---

## 🔮 Future Enhancements

* Interview Scheduling Agent
* Multi-Agent Recruitment Workflow
* PostgreSQL Integration
* Advanced Candidate Analytics
* Resume Recommendation System
* RAG-based Candidate Search

---

## 👩‍💻 Author

**Akanksha Pantula**

Computer Science Engineering Student

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* Agentic AI
* Data Analytics

---

## ⭐ Project Highlights

* Semantic Resume Matching using Vector Search
* LLM-Powered Candidate Evaluation
* Langfuse Observability Integration
* Qdrant Cloud Vector Database
* End-to-End AI Recruitment Workflow

## 📷 Screenshots

### Resume Screening Page

Upload resumes and compare them against a job description using AI-powered semantic matching.

![Resume Screening](https://github.com/user-attachments/assets/f97c3e3c-e7fe-429d-ba00-61270b7ac298)

---

### Recruitment Dashboard

View candidate rankings, scores, experience, AI summaries, and email status.

![Dashboard](https://github.com/user-attachments/assets/6504d88e-c564-4adc-b588-5c1ebce59094)

---

### Langfuse Monitoring Dashboard

Monitor prompts, responses, traces, and LLM observability for debugging and optimization.

![Langfuse Dashboard](https://github.com/user-attachments/assets/cfe4988f-8db3-40ea-b166-ea9aec213a18)
