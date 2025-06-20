# 🧠 MCP‑Streamlit

Interactive Streamlit app for chatting with LLMs via **Model Context Protocol (MCP)**.


### Install

```bash
git clone https://github.com/talrejanikhil/mcp-streamlit.git
cd mcp-streamlit

python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Or with Poetry:

```bash
poetry install
```

### Run

**Locally**:

```bash
streamlit run app/streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ⚙️ MCP Server Setup

Use your own MCP server or try the included examples:
For the GitHub example you need a personal access token with `repo` scope.
add it to your environment variables as `GITHUB_PERSONAL_ACCESS_TOKEN`.

---

## 🧩 Configuration

Check `.env.example` for the environment variables you can set to configure the app.

## 🧭 License

MIT License

## References

 - https://github.com/Nikunj2003/LLaMa-MCP-Streamlit
 - https://modelcontextprotocol.io/introduction
