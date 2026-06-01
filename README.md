# 🎯 Smart Attendance System

An AI-powered Smart Attendance System that automates attendance marking using real-time face recognition. The system leverages **Computer Vision** and **Deep Learning** techniques to identify individuals through a webcam and automatically record attendance in a MySQL database.

By using **MTCNN** for face detection and **FaceNet** for face recognition, the system provides an efficient, contactless, and accurate attendance management solution.

---

## 🚀 Features

- Real-time face detection and recognition
- Automated attendance marking
- Face embedding generation using FaceNet
- MySQL database integration
- Duplicate attendance prevention
- Attendance history tracking
- Email notifications via SMTP
- Interactive Streamlit interface
- Secure environment variable management
- Fast recognition using pre-generated embeddings

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- MySQL
- mysql.connector

### Computer Vision
- OpenCV
- MTCNN

### Deep Learning
- FaceNet

### Data Processing
- NumPy
- Pandas
- Pickle

### Notifications
- SMTP Email Service

### Configuration
- Python Dotenv

---

## 📂 Project Structure

```text
SMART-ATTENDANCE/
│
├── dataset/                 # Registered user images
│   ├── Person_1/
│   └── Person_2/
│
├── embeddings/
│   └── embeddings.pkl       # Stored FaceNet embeddings
│
├── working/                 # Temporary files
│
├── database.py              # MySQL operations
├── email_utils.py           # Email notifications
├── generate_embeddings.py   # Generate face embeddings
├── recognition_core.py      # Face recognition logic
├── main.py                  # Main Streamlit application
│
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 System Workflow

```text
Dataset Images
      ↓
Face Detection (MTCNN)
      ↓
Face Embedding Generation (FaceNet)
      ↓
Store Embeddings (.pkl)
      ↓
Real-Time Webcam Input
      ↓
Face Recognition
      ↓
Attendance Marked
      ↓
MySQL Database
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd SMART-ATTENDANCE
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📖 Usage

### Step 1: Create Dataset

Create a folder inside the `dataset` directory for each person and add multiple face images.

Example:

```text
dataset/
├── Kavya/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── img3.jpg
│
├── Manya/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── img3.jpg
```

> Use clear images with different angles and lighting conditions for better recognition accuracy.

### Step 2: Generate Face Embeddings

After adding new users, generate embeddings by running:

```bash
python generate_embeddings.py
```

This creates or updates:

```text
embeddings/embeddings.pkl
```

### Step 3: Configure Environment Variables

Create a `.env` file and add your database and email credentials.

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=attendance_db

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
```

### Step 4: Run the Application

```bash
streamlit run main.py
```

### Step 5: Mark Attendance

- Open the webcam interface.
- Face is detected using MTCNN.
- FaceNet generates embeddings.
- Stored embeddings are compared using cosine similarity.
- Attendance is automatically recorded in the MySQL database.

---

## 📌 Important Note

The `dataset/` folder and generated `embeddings.pkl` file are not included in the repository for privacy reasons.

After cloning the repository:

1. Create your own dataset.
2. Add face images for each user.
3. Run `generate_embeddings.py`.
4. Start the application.

---

## 📊 Core Technologies Used

- Face Detection using MTCNN
- Face Recognition using FaceNet Embeddings
- Cosine Similarity Matching
- Real-Time Computer Vision
- MySQL Database Management
- Streamlit Web Application Development

---

## 🔒 Security Features

- Environment variables stored in `.env`
- Database credentials protected
- Duplicate attendance prevention
- Precomputed embeddings for faster processing

---

## 📈 Future Enhancements

- Anti-spoofing detection
- Liveness detection
- Mobile application integration
- Cloud deployment
- Multi-camera support
- Advanced attendance analytics dashboard
