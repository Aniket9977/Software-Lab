# Software-Lab

**Software-Lab** is an AI-powered agent system that transforms a natural language project brief into a full-stack web application codebase. It automates the initial phases of software development, from planning to code generation.

## ✨ Overview

This project leverages a multi-agent architecture to interpret user requirements, create a technical plan, and generate code for both the frontend and backend.

- **Input**: A simple text description of the desired web application (e.g., "a website to store and display names and emails").
- **Process**: AI agents collaborate to architect, plan, and code the application.
- **Output**: Ready-to-use source code for a React frontend and a Python FastAPI backend.

## 🚀 How It Works

The system follows a structured, multi-step process orchestrated by `main.py`:

1.  **Project Brief**: The user provides a high-level description of the application.

2.  **Coordinator Agent (`coordinator.py`)**: An AI agent acting as a "Senior Software Architect" receives the brief. It breaks down the requirements into a detailed technical plan, creating separate, structured task lists for the frontend and backend.

3.  **Task Extraction (`extract_utils.py`)**: The system parses the coordinator's plan to isolate the frontend and backend tasks.

4.  **Code Generation**:
    - **Frontend Agent (`frontend.py`)**: An AI "React Developer" takes the frontend tasks and generates React components using functional components, React Router, and Tailwind CSS.
    - **Backend Agent (`backend.py`)**: An AI "Backend Developer" takes the backend tasks and generates a complete Python backend using FastAPI, including SQLAlchemy models for the database schema and API routes.

5.  **File Creation**:
    - The generated backend code, which is structured in a markdown format, is parsed to create a complete directory structure with all the necessary Python files (e.g., `main.py`, `models.py`, routers, etc.) inside the `backend_generated/` directory.
    - The frontend code is saved to `frontend_output.js`.
    - A complete log of the process, including the plan and generated code, is saved to `output.json`.

## 🛠️ Tech Stack

- **AI**: OpenAI's GPT models (e.g., `gpt-4o`)
- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: React, React Router, Tailwind CSS
- **Orchestration**: Python

## 📋 Prerequisites

- Python 3.8+
- An OpenAI API key

## ⚙️ Setup & Usage

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd Software-Lab
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

4.  **Run the application:**
    Execute the main script and enter your project brief when prompted.
    ```bash
    python main.py
    ```

5.  **Check the output:**
    - The generated backend files will be in the `backend_generated/` directory.
    - The frontend code will be in `frontend_output.js`.
    - The full transaction log will be in `output.json`.