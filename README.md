# LangGraph MCP Agent with XAMPP Database Integration

## 📌 Overview
This project is a **LangGraph + MCP Server**-based workflow automation tool that connects to a **MySQL database (via XAMPP)**.  
It enables uploading files, storing metadata in the database, and using LLM-powered reasoning for intelligent workflows.

Key Features:
- 🗄️ **XAMPP MySQL integration** (local database)
- ⚡ **LangGraph MCP Server** for LLM-driven workflows
- 📂 **File Upload & Storage**
- 🔄 Modular architecture for future multi-agent setups

---
```markdown
## 🏗️ Project Structure
📂 Multi-agent-ai
├── Backend/
│ ├── app.py 
│ ├── db.py
│ ├── langgraph_workflow.py 
│ └── mcp_client.py
├── mcp_server/
│ └──  server.py 
├── Xammp_php/
│ ├── config.php
│ ├── index.php
│ ├── send.php
│ └── upload.php
├── README.md
└── requirements.txt # Python dependencies


```

---

## ⚙️ Requirements
- **Python** 3.10+ (tested on 3.12)
- **pip** package manager
- **XAMPP** (MySQL + Apache)
- **MySQL Connector for Python**

---

## 📥 Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Saibhossain/multi-agent-ai.git
cd multi-agent-ai
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

```
### 4️⃣ Configure Database
1. Open XAMPP and start MySQL.

2. Create a database:
```bash
CREATE DATABASE workflow_agent_db;
```
3. add tables from :
```bash
xammp_php/smart_hub.sql
```
### ▶️ Running the Backend

```bash
cd Backend
uvicorn app:app --reload --port 8000
```

Backend will start at:
> http://127.0.0.1:8000


### Open this link for quary insert
```bash
http://127.0.0.1/smart_hub/index.php
```


#### Real-World Use Cases
* AI-powered document indexing with MySQL storage
* LangGraph multi-agent workflows with stored history
* Automating ETL pipelines from uploaded files
* Intelligent report generation from stored database records


## License 
MIT License © 2025 [MD Saib hossain]
---

If you want, I can now **write the missing `db.py` and `langgraph_agent.py`** so this README runs without the `ModuleNotFoundError` you got. That way, when you push it to GitHub, it’s a 100% working project.  

Do you want me to prepare that working code next?
