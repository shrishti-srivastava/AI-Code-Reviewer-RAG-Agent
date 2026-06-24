# ✨ AI Code Reviewer — Powered by Gemini AI

A smart, beginner-friendly AI code reviewer built with **Gemini 1.5 Flash (Google)** and a **FAISS RAG system**.  
Paste your code, get an instant quality score, mistake breakdown, suggestions, and improved code.

---

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI framework |
| Gemini 1.5 Flash (Google) | AI code review engine |
| FAISS | Vector search for RAG |
| Sentence Transformers | Code embeddings |
| streamlit-ace | Cursor-enabled code editor |
| python-dotenv | Secure API key loading |

---

## 📁 Folder Structure

```
ai_code_reviewer_rag/
│
├── app.py                        ← Main Streamlit application
├── requirements.txt              ← Python dependencies
├── .env                          ← Your Gemini API key (keep secret!)
├── .gitignore                    ← Prevents .env from being committed
├── README.md                     ← This file
└── knowledge_base/
    └── coding_rules.txt          ← RAG knowledge base (coding rules)
```

---

## ⚙️ Setup & Run

### 1. Navigate to project folder
```bash
cd ai_code_reviewer_rag
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Add your Gemini API key

Open `.env` and replace the placeholder:
```env
GEMINI_API_KEY=AIzaSy-your-actual-api-key-here
```

> Get your free API key at 👉 https://aistudio.google.com/app/apikey

### 6. Run the app
```bash
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

---

## ✨ Features

- 🖱️ **Cursor-enabled code editor** — full IDE experience (streamlit-ace)
- 🔢 **Line numbers** and syntax highlighting
- 🌐 **10 languages** — Python, JS, Java, C++, Go, Rust, SQL, HTML, etc.
- 🎨 **8+ editor themes** — Monokai, Dracula, Nord Dark, GitHub Dark, etc.
- 📊 **Quality Score** — rated out of 10
- ❌ **Mistakes Found** — clearly listed
- 💡 **Suggestions** — actionable improvements
- 🚀 **Improved Code** — rewritten and optimized
- 📖 **Simple Explanation** — beginner-friendly language
- 📥 **Export** — download review as `.md` or `.txt`
- 🕓 **Review History** — last 6 reviews tracked in sidebar

---

## 🔄 How RAG Works

1. Coding rules are stored in `knowledge_base/coding_rules.txt`
2. Rules are converted into vector embeddings using Sentence Transformers
3. FAISS searches for the most relevant rules for the submitted code
4. Gemini 1.5 Flash receives: user code + related rules → generates review

---

## 🎓 Viva Questions & Answers

**Q1. What is this project?**  
An AI-based code reviewer that checks code and gives improvement suggestions using Gemini AI.

**Q2. What is RAG?**  
RAG (Retrieval-Augmented Generation) first retrieves relevant rules from stored documents, then uses AI to generate a response.

**Q3. Why FAISS?**  
FAISS performs fast vector similarity search to find the most relevant coding rules.

**Q4. Why Gemini AI?**  
Gemini 1.5 Flash by Google is a fast, powerful LLM used to generate the code review response.

**Q5. What is the knowledge base?**  
A text file storing Python coding rules and clean code tips used by the RAG system.

**Q6. Does this use a database?**  
No — only a simple text file and an in-memory FAISS index.

**Q7. What is streamlit-ace?**  
A Streamlit component that embeds the Ace code editor, providing cursor support, line numbers, and syntax highlighting.

**Q8. Can this project be improved?**  
Yes — possible additions: file upload, multi-file review, login system, GitHub integration, Docker deployment.
