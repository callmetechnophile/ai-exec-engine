# WORKFLOWGUIDE.AI 🚀
**Idea → Execution.** An Autonomous Multi-Agent Engineering Engine.

Transform abstract hardware ideas (e.g., "I want to build an ESP32 remote control car") into fully optimized, production-ready engineering execution packages in under a minute.

## 🌟 Features

- **Autonomous Multi-Agent Orchestration**: Deploys an entire virtual engineering team (Retrieval, Extraction, Research, Optimization, Validation, Simulation, Planning, and Deployment agents) to work sequentially on your project.
- **Lexical RAG (Zero-RAM)**: Uses a custom pure-Python Jaccard Similarity retrieval architecture, completely bypassing heavy vector databases (ChromaDB) to survive strict cloud memory limits while retaining high-fidelity academic context injection.
- **Explainable Tradeoffs**: View a real-time architectural decision trace that shows exactly *why* the AI chose specific components or optimized certain pathways.
- **Hardware Code Generation**: Instantly generates starter code tailored to your specific microcontroller (Arduino, ESP32, STM32, Raspberry Pi) and the exact components selected by the AI.
- **Complete Export Packages**: Automatically compiles the finalized architecture into PDF Reports, Markdown (for Obsidian/GitHub), Notion-compatible CSV timelines, and raw JSON schemas.

## 🛠️ Tech Stack

### Frontend (Deployed on Vercel)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Shadcn UI (Glassmorphism aesthetics)
- **Timeline Visualization**: Frappe Gantt

### Backend (Deployed on Railway)
- **Framework**: FastAPI (Python)
- **LLM Engine**: Groq (for ultra-fast inference)
- **Image Generation**: Fal.ai (Hugging Face Inference routing)
- **Web Research**: Tavily API
- **Memory/Cache**: Lightweight JSON Disk Cache (Vectorless)

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/callmetechnophile/ai-exec-engine.git
cd ai-exec-engine
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `keys.env` file in the `backend` directory with your API keys:
```env
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
FAL_KEY=your_key_here
NVIDIA_API_KEY=your_key_here
```
Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```
Run the development server:
```bash
npm run dev
```

## 🧠 Architecture Highlights
- **Crash-Proof Design**: Engineered to survive free-tier cloud limits. Heavy ML libraries (Sentence-Transformers, Chroma) were aggressively ripped out and replaced with optimized math algorithms, reducing RAM overhead by 95%.
- **Event-Driven UI**: Frontend actively polls the orchestrator pipeline, providing real-time timeline updates as agents hand off tasks to one another.

---
Built with ❤️ for the Hackathon.
