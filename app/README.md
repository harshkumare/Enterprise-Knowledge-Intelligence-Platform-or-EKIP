# 🧠 Enterprise Knowledge Intelligence Platform (EKIP)

An enterprise-grade Retrieval-Augmented Generation (RAG) platform that enables intelligent document search and question answering using Large Language Models (LLMs).

EKIP combines semantic search, keyword search, and modern LLMs to provide accurate, explainable, and context-aware responses from enterprise documents.

---

## ✨ Features

- 🔍 Hybrid Retrieval (FAISS + BM25)
- ⚖️ Reciprocal Rank Fusion (RRF)
- 🧠 HuggingFace Embeddings
- 🤖 Multiple LLM Providers (Groq & Gemini)
- 💬 Conversation Memory
- 📚 Source Citations
- ⚡ Streaming Responses
- 🏗️ Modular Enterprise Architecture
- ⚙️ Configurable via Environment Variables

---

## 🏛️ System Architecture

```text
                    User
                     │
                     ▼
               Streamlit UI
                     │
             Response Generator
                     │
        Hybrid Retriever (RRF)
         ┌──────────┴──────────┐
         │                     │
      BM25 Search         FAISS Search
         │                     │
         └──────────┬──────────┘
                    ▼
            Prompt Construction
                    │
              LLM Factory
        ┌───────────┴───────────┐
        │                       │
      Groq                  Gemini
                    │
             Streaming Response
                    │
             Source Citations
```

---

## 📂 Project Structure

```text
EKIP
│
├── app
│   ├── config
│   ├── embeddings
│   ├── generation
│   ├── ingestion
│   ├── retrieval
│   ├── ui
│   └── utils
│
├── data
├── logs
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | LangChain |
| UI | Streamlit |
| Vector Database | FAISS |
| Lexical Search | BM25 |
| Embeddings | HuggingFace BAAI/bge-small-en-v1.5 |
| LLM Providers | Groq, Gemini |
| Configuration | dotenv |
| Logging | Python Logging |

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/harshkumare/Enterprise-Knowledge-Intelligence-Platform-or-EKIP.git
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file:

```env
LLM_PROVIDER=groq

GROQ_API_KEY=YOUR_KEY
GEMINI_API_KEY=YOUR_KEY

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
TOP_K=5
```

### Run

```bash
streamlit run app/ui/main.py
```

---

## 🎯 Current Capabilities

- Hybrid Search
- Enterprise Modular Architecture
- Multi-LLM Support
- Streaming Responses
- Source Attribution
- Conversation Memory

---

## 🚧 Roadmap

- [ ] Query Rewriting
- [ ] Cross-Encoder Reranking
- [ ] PDF Upload UI
- [ ] Multi-Document Search
- [ ] Automatic LLM Fallback
- [ ] Docker Support
- [ ] GitHub Actions CI/CD
- [ ] Azure OpenAI Integration

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Harsh Kumare**

M.Sc. Mathematics, IIT Bombay

Interested in AI Engineering, Retrieval-Augmented Generation, LLM Systems, and Enterprise AI.
