# 🧠 Neo4j Graph AI Assistant

A mini AI assistant that translates natural language questions into Neo4j Cypher queries, executes them, and provides human-friendly responses. Built with LangChain, Groq LLM, and Streamlit.

## 📋 Overview

This project demonstrates an end-to-end AI system that:
- Accepts user questions in natural language
- Automatically generates valid Cypher queries for Neo4j
- Validates queries for safety and correctness
- Executes queries against a Neo4j graph database
- Converts results back into clear, human-friendly responses

## ✨ Features

- **Natural Language Processing**: Ask questions in plain English
- **Automatic Cypher Generation**: LLM-powered query translation
- **Query Validation**: Built-in safety checks to prevent dangerous operations
- **Neo4j Integration**: Direct connection to Neo4j database
- **Interactive UI**: Streamlit-based chat interface
- **Error Handling**: Graceful error messages when queries are invalid or unsafe

## 🔐 Safety Features

The system prevents execution of dangerous operations by blocking:
- `DELETE` / `DETACH DELETE`
- `CREATE` / `MERGE`
- `DROP`
- `SET` / `REMOVE`
- `LOAD CSV`

Only read-only queries (`MATCH`, `WHERE`, filtering, etc.) are allowed.

## 🛠️ Tech Stack

- **LLM**: Groq (llama-3.1-8b-instant)
- **Framework**: LangChain with Neo4j integration
- **Database**: Neo4j Graph Database
- **Frontend**: Streamlit
- **Validation**: Pydantic
- **Environment**: Python 3.x with dotenv

## 📦 Installation

### Prerequisites
- Python 3.8+
- Neo4j database instance
- Groq API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/JohnnyWorku/mini_ai_assistant.git
cd mini_ai_assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file in the root directory:
```env
# Groq LLM Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Neo4j Configuration
LOCAL_NEO4J_URI=bolt://localhost:7687
LOCAL_NEO4J_USERNAME=neo4j
LOCAL_NEO4J_PASSWORD=your_password
LOCAL_NEO4J_DB=neo4j
```

4. **Run the application**
```bash
streamlit run frontend.py
```

The app will be available at `http://localhost:8501`

## 📁 Project Structure

```
mini_ai_assistant/
├── frontend.py              # Streamlit UI and chat interface
├── backend.py               # Core AI logic and Neo4j integration
├── query_validator.py       # Pydantic model for query validation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
├── task.txt                # Project requirements
└── README.md               # This file
```

## 🔧 Components

### `frontend.py`
Streamlit-based chat interface that:
- Displays conversation history
- Accepts user input
- Shows assistant responses
- Handles errors gracefully

### `backend.py`
Core business logic including:
- **`get_schema()`**: Retrieves Neo4j database schema
- **`generate_cypher()`**: Uses LLM to convert natural language to Cypher
- **`validate_with_neo4j()`**: Validates query syntax using Neo4j EXPLAIN
- **`run_query()`**: Executes Cypher query against the database
- **`format_results()`**: Converts query results to readable format
- **`generate_humanized_answer()`**: Uses LLM to create natural language response
- **`ask_the_graph()`**: Orchestrates the entire pipeline

### `query_validator.py`
Pydantic validation model that:
- Enforces strict field structure
- Strips markdown from generated queries
- Blocks dangerous operations
- Ensures query safety before execution

## 🚀 Usage

1. Start the application:
```bash
streamlit run frontend.py
```

2. Ask questions about your graph data:
```
"Show me all users created in the last month"
"Find the connection between Alice and Bob"
"What are the top 5 most connected nodes?"
```

3. The AI assistant will:
   - Generate an appropriate Cypher query
   - Validate it for safety
   - Execute it against Neo4j
   - Return results in natural language

## 💡 Example Workflow

```
User: "Find all users named John"
↓
LLM generates: MATCH (n:User {name: 'John'}) RETURN n
↓
Validator checks: ✓ Safe query (read-only)
↓
Neo4j executes query
↓
Results formatted and humanized
↓
Assistant: "I found 3 users named John: John Smith (ID: 1), John Doe (ID: 2), John Johnson (ID: 3)"
```

## 📋 Requirements

See `requirements.txt` for all dependencies:
- `python-dotenv` - Environment variable management
- `langchain` - LLM framework
- `langchain-groq` - Groq LLM integration
- `langchain-neo4j` - Neo4j integration
- `neo4j` - Neo4j driver
- `streamlit` - Web UI framework
- `pydantic` - Data validation

## ⚙️ Configuration

### Groq Model Selection
The default model is `llama-3.1-8b-instant`. You can change it in `.env`:
```env
GROQ_MODEL=llama-3.1-70b-versatile
```

### Neo4j Connection
Update `.env` with your Neo4j instance details:
```env
LOCAL_NEO4J_URI=bolt://your-host:7687
LOCAL_NEO4J_USERNAME=neo4j
LOCAL_NEO4J_PASSWORD=your_secure_password
LOCAL_NEO4J_DB=neo4j
```

## 🐛 Troubleshooting

**Connection Error to Neo4j**
- Verify Neo4j is running
- Check URI, username, and password in `.env`
- Ensure firewall allows connections on port 7687

**Invalid Cypher Query Generated**
- Check that your Neo4j schema matches the LLM's understanding
- Try rewording your question
- Provide more specific context

**API Key Issues**
- Verify `GROQ_API_KEY` is set in `.env`
- Check that your API key has sufficient credits
- Ensure the key is valid and active

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

[JohnnyWorku](https://github.com/JohnnyWorku)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📞 Support

For issues or questions, please open a GitHub issue in this repository.

---

**Note**: This is a demonstration project. For production use, consider implementing additional security measures, caching, and performance optimizations.
