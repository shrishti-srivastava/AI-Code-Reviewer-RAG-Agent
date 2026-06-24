import streamlit as st
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

st.set_page_config(
    page_title="AI Code Reviewer | Gemini",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

if not st.session_state.user_api_key:

    st.title("🔑 Enter Your Gemini API Key")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your Gemini API key here..."
    )

    if st.button("Continue"):
        if api_key.strip():
            st.session_state.user_api_key = api_key
            st.rerun()
        else:
            st.warning("Please enter a valid API key.")

    st.stop()

    GEMINI_API_KEY = st.session_state.user_api_key

    # Ask user for API key
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

if not st.session_state.user_api_key:

    st.title("🔑 Enter Your Gemini API Key")

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    if st.button("Continue"):
        if api_key.strip():
            st.session_state.user_api_key = api_key
            st.rerun()

    st.stop()

# Create GEMINI_API_KEY variable
GEMINI_API_KEY = st.session_state.user_api_key

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=genai.types.GenerationConfig(
        temperature=0.3
    )
)

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=genai.types.GenerationConfig(
        temperature=0.3
    )
)

try:
    from streamlit_ace import st_ace
    ACE_AVAILABLE = True
except ImportError:
    ACE_AVAILABLE = False

def load_rules():
    file_path = "knowledge_base/coding_rules.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    rules = text.split("\n\n")
    rules = [rule.strip() for rule in rules if rule.strip()]
    return rules

def create_faiss_index(rules):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(rules)
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return model, index, rules

def search_related_rules(user_code, model, index, rules, top_k=3):
    query_embedding = model.encode([user_code])
    query_embedding = np.array(query_embedding).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    selected_rules = [rules[i] for i in indices[0]]
    return "\n\n".join(selected_rules)

def review_code_with_gemini(user_code, related_rules, language="Python"):
    prompt = f"""You are a smart AI Code Reviewer for {language} developers.

Review the {language} code using the coding rules given below.

Coding Rules:
{related_rules}

User Code:
{user_code}

Give the answer in this EXACT format (use markdown):

### 🏆 Code Quality Score: X/10

### ❌ Mistakes Found:
- List each mistake clearly

### 💡 Suggestions:
- List each suggestion

### 🚀 Improved Code:
```{language.lower()}
# Paste improved code here
```

### 📖 Simple Explanation:
Explain the changes in beginner-friendly language.

Keep language simple, clear, and beginner-friendly.
"""

    response = gemini_model.generate_content(prompt)
    return response.text

st.set_page_config(
    page_title="AI Code Reviewer | Gemini",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "user_code" not in st.session_state:
    st.session_state.user_code = ""
if "review_result" not in st.session_state:
    st.session_state.review_result = None
if "show_rules_info" not in st.session_state:
    st.session_state.show_rules_info = False
if "review_history" not in st.session_state:
    st.session_state.review_history = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "editor"
if "editor_theme" not in st.session_state:
    st.session_state.editor_theme = "monokai"
if "editor_lang" not in st.session_state:
    st.session_state.editor_lang = "python"

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

.stApp {
    background: linear-gradient(135deg, #060812 0%, #0a0d1a 50%, #06081a 100%) !important;
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}

.block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem !important;
    max-width: 1500px !important;
}

/* ── Animated gradient background ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 10% 20%, rgba(99,102,241,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(6,182,212,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(139,92,246,0.04) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── HERO BANNER ── */
.hero {
    background: linear-gradient(135deg, rgba(26,31,62,0.95) 0%, rgba(15,23,42,0.98) 50%, rgba(30,16,64,0.95) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 28px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 25px 80px rgba(99,102,241,0.15),
        0 0 0 1px rgba(255,255,255,0.05) inset;
    backdrop-filter: blur(20px);
}

.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    border-radius: 50%;
    animation: pulse-orb 4s ease-in-out infinite;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -50px; left: -50px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
    border-radius: 50%;
    animation: pulse-orb 4s ease-in-out infinite reverse;
}

@keyframes pulse-orb {
    0%, 100% { transform: scale(1); opacity: 0.7; }
    50% { transform: scale(1.1); opacity: 1; }
}

.hero-top {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 10px;
}

.hero-logo {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 8px 24px rgba(79,70,229,0.45);
    flex-shrink: 0;
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(90deg, #a5b4fc 0%, #38bdf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    position: relative;
    z-index: 1;
}

.hero-sub {
    color: #94a3b8;
    font-size: 15.5px;
    font-weight: 400;
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
}

.hero-badges {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.badge {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: 0.3px;
    transition: all 0.2s ease;
}

.badge:hover {
    background: rgba(99,102,241,0.25);
    border-color: rgba(99,102,241,0.6);
    transform: translateY(-1px);
}

.badge.green {
    background: rgba(16,185,129,0.12);
    border-color: rgba(16,185,129,0.3);
    color: #34d399;
}

.badge.cyan {
    background: rgba(6,182,212,0.12);
    border-color: rgba(6,182,212,0.3);
    color: #38bdf8;
}

/* ── API STATUS PILL ── */
.api-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    position: relative;
    z-index: 1;
    float: right;
    margin-top: -60px;
}

.api-status.connected {
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.4);
    color: #34d399;
}

.api-status.disconnected {
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.4);
    color: #f87171;
}

.api-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    animation: blink 1.5s ease infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── TOOLBAR ── */
.toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(19,24,43,0.9);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 12px 18px;
    margin-bottom: 14px;
    backdrop-filter: blur(10px);
}

.toolbar-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    white-space: nowrap;
}

/* ── Section Labels ── */
.section-label {
    color: #e2e8f0;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: 0.2px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #0891b2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
    width: 100% !important;
    letter-spacing: 0.2px !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    transition: left 0.5s ease;
}

.stButton > button:hover::before { left: 100%; }

.stButton > button:hover {
    background: linear-gradient(135deg, #3730a3 0%, #0e7490 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(79,70,229,0.45) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Review CTA button ── */
[data-testid="stButton"]:last-of-type > button {
    font-size: 16px !important;
    padding: 15px 24px !important;
    background: linear-gradient(135deg, #6d28d9 0%, #0891b2 100%) !important;
    box-shadow: 0 4px 24px rgba(109,40,217,0.35) !important;
    letter-spacing: 0.5px !important;
}

/* ── Textarea fallback ── */
div[data-testid="stTextArea"] textarea {
    background-color: #111827 !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13.5px !important;
    border-radius: 16px !important;
    border: 1.5px solid rgba(99,102,241,0.35) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.03) inset !important;
    line-height: 1.75 !important;
    transition: border-color 0.2s !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(99,102,241,0.7) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15), 0 4px 24px rgba(0,0,0,0.35) !important;
}

div[data-testid="stTextArea"] label { color: #64748b !important; font-size: 13px !important; }

/* ── ACE Editor container ── */
.ace-editor-wrapper {
    border-radius: 16px;
    overflow: hidden;
    border: 1.5px solid rgba(99,102,241,0.35);
    box-shadow: 0 4px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.03) inset;
    transition: border-color 0.25s;
}

.ace-editor-wrapper:focus-within {
    border-color: rgba(99,102,241,0.65);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12), 0 4px 24px rgba(0,0,0,0.35);
}

/* ── Status Bar (cursor info) ── */
.status-bar {
    background: rgba(10,13,26,0.95);
    border: 1px solid rgba(99,102,241,0.2);
    border-top: none;
    border-radius: 0 0 14px 14px;
    padding: 7px 16px;
    display: flex;
    align-items: center;
    gap: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
}

.status-item {
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 5px;
}

.status-item span.val {
    color: #a5b4fc;
    font-weight: 600;
}

.status-sep {
    width: 1px;
    height: 12px;
    background: rgba(99,102,241,0.2);
}

/* ── Tip box ── */
.tip-box {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 11px 16px;
    color: #a5b4fc;
    font-size: 13px;
    margin-top: 10px;
    line-height: 1.6;
}

/* ── Result Card ── */
.result-card {
    background: linear-gradient(135deg, rgba(17,24,39,0.97) 0%, rgba(19,24,43,0.97) 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 22px;
    padding: 30px;
    margin-top: 24px;
    box-shadow: 0 12px 50px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.04) inset;
    animation: fadeInUp 0.45s cubic-bezier(0.4,0,0.2,1);
    backdrop-filter: blur(12px);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-title {
    font-size: 18px;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(99,102,241,0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Feature Cards ── */
.feat-card {
    background: linear-gradient(135deg, rgba(26,31,62,0.8), rgba(15,23,42,0.9));
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 14px;
    padding: 13px 16px;
    margin-bottom: 10px;
    color: #c7d2fe;
    font-size: 13.5px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.25s ease;
    cursor: default;
    backdrop-filter: blur(8px);
}

.feat-card:hover {
    border-color: rgba(99,102,241,0.45);
    background: linear-gradient(135deg, rgba(26,31,72,0.9), rgba(15,23,52,0.95));
    transform: translateX(3px);
    box-shadow: 0 4px 16px rgba(99,102,241,0.15);
}

.feat-icon {
    width: 34px; height: 34px;
    background: rgba(99,102,241,0.15);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

/* ── How-it-works ── */
.how-box {
    background: rgba(19,24,43,0.85);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 16px;
    padding: 18px 20px;
    color: #94a3b8;
    font-size: 13px;
    line-height: 2.1;
    margin-top: 8px;
    backdrop-filter: blur(8px);
}

.how-box strong { color: #38bdf8; }

/* ── History ── */
.history-item {
    background: rgba(26,31,62,0.7);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px;
    padding: 12px 15px;
    margin-bottom: 8px;
    color: #94a3b8;
    font-size: 12.5px;
    transition: border-color 0.2s;
}

.history-item:hover { border-color: rgba(99,102,241,0.35); }

/* ── Selectbox styling ── */
div[data-testid="stSelectbox"] > div {
    background: rgba(19,24,43,0.9) !important;
    border-color: rgba(99,102,241,0.3) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-color: #6366f1 !important; }
.stSpinner > div > div { border-top-color: #38bdf8 !important; }

/* ── Alerts ── */
.stAlert { border-radius: 14px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: #060812; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #334155; }

/* ── HR ── */
hr {
    border-color: rgba(99,102,241,0.15) !important;
    margin: 20px 0 !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #059669, #0891b2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(19,24,43,0.8) !important;
    border-color: rgba(99,102,241,0.2) !important;
    border-radius: 14px !important;
}

/* ── Code blocks in review ── */
.stMarkdown pre {
    background: #0d1117 !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Column gap fix ── */
[data-testid="stHorizontalBlock"] {
    gap: 16px !important;
}

/* ── Stats strip ── */
.stats-strip {
    display: flex;
    gap: 14px;
    margin-top: 14px;
    flex-wrap: wrap;
}

.stat-chip {
    background: rgba(19,24,43,0.9);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.stat-chip .label {
    color: #64748b;
    font-size: 11.5px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-chip .val {
    color: #a5b4fc;
    font-size: 14px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Cursor info box ── */
.cursor-info {
    background: rgba(10,13,26,0.9);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 10px;
    padding: 8px 16px;
    display: inline-flex;
    align-items: center;
    gap: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    margin-top: 8px;
}

.cursor-info .ci-item {
    color: #64748b;
}

.cursor-info .ci-item strong {
    color: #c084fc;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

api_status_html = (
    '<div class="api-status connected"><div class="api-dot"></div>Gemini Connected</div>'
    if GEMINI_API_KEY else
    '<div class="api-status disconnected"><div class="api-dot"></div>API Key Missing</div>'
)

st.markdown(f"""
<div class="hero">
    {api_status_html}
    <div class="hero-top">
        <div class="hero-logo">✨</div>
        <div class="hero-title">AI Code Reviewer</div>
    </div>
    <div class="hero-sub">
        Powered by <strong style="color:#38bdf8">Gemini 1.5 Flash</strong> (Google) &nbsp;·&nbsp;
        Smart code analysis with <strong style="color:#a5b4fc">FAISS RAG</strong> &nbsp;·&nbsp;
        Professional editor with <strong style="color:#c084fc">cursor support</strong>
    </div>
    <div class="hero-badges">
        <span class="badge">🤖 Gemini 1.5 Flash</span>
        <span class="badge cyan">🔍 FAISS RAG</span>
        <span class="badge">🐍 Python</span>
        <span class="badge green">✅ Cursor Editor</span>
        <span class="badge">🎓 Beginner Friendly</span>
        <span class="badge cyan">📥 Export Reports</span>
    </div>
</div>
""", unsafe_allow_html=True)


col_main, col_sidebar = st.columns([3, 1], gap="large")

with col_main:

    st.markdown('<div class="section-label">📝 Code Editor</div>', unsafe_allow_html=True)

    tc1, tc2, tc3, tc4 = st.columns([2, 2, 1, 1])
    with tc1:
        lang_options = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Rust", "SQL", "HTML"]
        ace_lang_map = {
            "Python": "python", "JavaScript": "javascript", "TypeScript": "typescript",
            "Java": "java", "C++": "c_cpp", "C": "c_cpp", "Go": "golang",
            "Rust": "rust", "SQL": "sql", "HTML": "html"
        }
        selected_lang = st.selectbox("🌐 Language", lang_options, index=0, key="lang_select")
        ace_lang = ace_lang_map.get(selected_lang, "python")

    with tc2:
        theme_options = ["monokai", "dracula", "github_dark", "solarized_dark", "tomorrow_night", "nord_dark", "one_dark"]
        selected_theme = st.selectbox("🎨 Theme", theme_options, index=0, key="theme_select")

    with tc3:
        font_size = st.selectbox("🔤 Font", [12, 13, 14, 15, 16], index=2, key="font_select")

    with tc4:
        tab_size = st.selectbox("⇥ Tab", [2, 4, 8], index=1, key="tab_select")

    # ── Quick Action Buttons ──
    st.markdown("<div style='margin-top:4px'></div>", unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("🧪 Sample Code", key="load_sample"):
            st.session_state.user_code = '''def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    avg = total / len(numbers)
    return avg

data = [10, 20, 30, 40, 50]
print("Average:", calculate_average(data))
'''
            st.rerun()

    with b2:
        if st.button("🐛 Bug Example", key="load_bug"):
            st.session_state.user_code = '''def divide(a,b):
    result = a/b
    return result

x=divide(10,0)
print(x)

def greet(name):
    print("Hello " + name)
greet(123)
'''
            st.rerun()

    with b3:
        if st.button("🧹 Clear All", key="clear_code"):
            st.session_state.user_code = ""
            st.session_state.review_result = None
            st.rerun()

    with b4:
        if st.button("📚 View Rules", key="view_rules"):
            st.session_state.show_rules_info = not st.session_state.show_rules_info

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    if ACE_AVAILABLE:
        st.markdown('<div class="ace-editor-wrapper">', unsafe_allow_html=True)
        edited_code = st_ace(
            value=st.session_state.user_code,
            language=ace_lang,
            theme=selected_theme,
            font_size=font_size,
            tab_size=tab_size,
            show_gutter=True,
            show_print_margin=True,
            wrap=False,
            auto_update=True,
            height=380,
            key="ace_editor",
            placeholder=(
                f"# Write or paste your {selected_lang} code here...\n"
                "# ✨ Full editor with cursor, line numbers & syntax highlighting\n"
                "# 🔢 Line:Col shown below | Tab = indent | Ctrl+Z = undo\n"
            ),
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Sync back to session state
        if edited_code is not None:
            st.session_state.user_code = edited_code
        user_code = st.session_state.user_code

        # ── Status Bar with cursor info ──
        line_count = len(user_code.splitlines()) if user_code else 0
        char_count = len(user_code) if user_code else 0
        word_count = len(user_code.split()) if user_code else 0

        st.markdown(f"""
        <div class="status-bar">
            <div class="status-item">📄 <span class="val">{line_count}</span>&nbsp;Lines</div>
            <div class="status-sep"></div>
            <div class="status-item">🔤 <span class="val">{char_count}</span>&nbsp;Chars</div>
            <div class="status-sep"></div>
            <div class="status-item">📝 <span class="val">{word_count}</span>&nbsp;Words</div>
            <div class="status-sep"></div>
            <div class="status-item">🌐 <span class="val">{selected_lang}</span></div>
            <div class="status-sep"></div>
            <div class="status-item">🎨 <span class="val">{selected_theme}</span></div>
            <div class="status-sep"></div>
            <div class="status-item">✅ Cursor &amp; Line Numbers Active</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        
        user_code = st.text_area(
            "Paste your code here:",
            value=st.session_state.user_code,
            height=380,
            key="user_code",
            placeholder=f"# Write or paste your {selected_lang} code here...",
        )
        line_count = len(user_code.splitlines()) if user_code else 0
        char_count = len(user_code) if user_code else 0
        st.markdown(
            f'<div class="tip-box">💡 <b>Tip:</b> Install <code>streamlit-ace</code> for a full code editor with cursor &amp; line numbers. '
            f'Run: <code>pip install streamlit-ace</code> &nbsp;|&nbsp; Current: {line_count} lines · {char_count} chars</div>',
            unsafe_allow_html=True,
        )

    if st.session_state.show_rules_info:
        try:
            rules_preview = load_rules()
            with st.expander(f"📚 Knowledge Base — {len(rules_preview)} Coding Rules", expanded=True):
                for i, rule in enumerate(rules_preview, 1):
                    st.markdown(f"**{i}.** {rule}")
        except Exception as e:
            st.error(f"❌ Could not load rules: {e}")

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    if st.button(f"✨ Review My {selected_lang} Code with Gemini AI", key="review_btn"):


        if not st.session_state.user_api_key:
            st.error("⚠️ Please enter your Gemini API key.")
    
        elif not gemini_model:
            st.error("⚠️ Could not initialize Gemini client. Check your API key.")
        elif not user_code or user_code.strip() == "":
            st.warning("⚠️ Please write or paste some code first!")
        else:
            with st.spinner(f"✨ Gemini AI is analyzing your {selected_lang} code..."):
                try:
                    rules = load_rules()
                    embedding_model, faiss_index, stored_rules = create_faiss_index(rules)
                    related_rules = search_related_rules(user_code, embedding_model, faiss_index, stored_rules)
                    review = review_code_with_gemini(user_code, related_rules, selected_lang)
                    st.session_state.review_result = review
                    # Add to history
                    snippet = user_code.strip()[:60].replace("\n", " ")
                    st.session_state.review_history.append({
                        "snippet": snippet + ("..." if len(user_code) > 60 else ""),
                        "result": review,
                        "language": selected_lang,
                        "lines": line_count,
                    })
                    st.success("✅ Review complete!")
                except Exception as e:
                    st.error(f"❌ Error during review: {e}")

    if st.session_state.review_result:
        st.markdown("""
        <div class="result-card">
            <div class="result-title">📊 Code Review Result</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.review_result)

        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="📥 Download Review (.md)",
                data=st.session_state.review_result,
                file_name="code_review.md",
                mime="text/markdown",
                key="dl_md",
            )
        with dl2:
            st.download_button(
                label="📄 Download as Text (.txt)",
                data=st.session_state.review_result,
                file_name="code_review.txt",
                mime="text/plain",
                key="dl_txt",
            )

with col_sidebar:

    # Features
    st.markdown('<div class="section-label" style="font-size:14px">✨ Features</div>', unsafe_allow_html=True)
    for icon, label in [
        ("✨", "Gemini 1.5 Flash AI"),
        ("🔍", "FAISS RAG Search"),
        ("🖱️", "Cursor Editor"),
        ("🔢", "Line Numbers"),
        ("🎨", "8+ Themes"),
        ("🌐", "10 Languages"),
        ("📊", "Quality Scoring"),
        ("💡", "Smart Suggestions"),
        ("🚀", "Improved Code"),
        ("🎓", "Beginner Friendly"),
        ("📥", "Export Reports"),
    ]:
        st.markdown(
            f'<div class="feat-card"><div class="feat-icon">{icon}</div>{label}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("""
    <div class="how-box">
        <strong>How it works</strong><br>
        1️⃣ &nbsp;Choose language &amp; theme<br>
        2️⃣ &nbsp;Write / paste your code<br>
        3️⃣ &nbsp;FAISS finds related rules<br>
        4️⃣ &nbsp;Grok AI reviews code<br>
        5️⃣ &nbsp;Get score + improvements<br>
        6️⃣ &nbsp;Download your report
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.review_history:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-label" style="color:#94a3b8;font-size:13px">🕓 Review History</div>', unsafe_allow_html=True)
        for i, item in enumerate(reversed(st.session_state.review_history[-6:])):
            idx = len(st.session_state.review_history) - i
            lang_badge = item.get("language", "Python")
            lines_info = item.get("lines", "?")
            st.markdown(
                f'<div class="history-item">'
                f'<span style="color:#6366f1;font-weight:700">#{idx}</span> '
                f'<span style="color:#38bdf8;font-size:11px">[{lang_badge}]</span> '
                f'<span style="color:#64748b;font-size:11px">{lines_info}L</span><br>'
                f'<code style="color:#a5b4fc;font-size:11.5px">{item["snippet"]}</code>'
                f'</div>',
                unsafe_allow_html=True,
            )
