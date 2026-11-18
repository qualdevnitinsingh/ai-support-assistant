# AI Customer Support Assistant

A Python-based AI Customer Support Assistant using Google's Gemini API.

---

## 1. About the Project

This project is a prototype customer support assistant designed for an online jewellery store. It uses Google's Gemini API to analyze incoming customer inquiries, assess their intent and tone, categorize urgency, and produce structured, actionable responses following strict business rules without hallucinating private system data.

The project demonstrates production-focused Python practices, including modular design, virtual environments, dependency management, environment-based secret configuration, and schema validation.

---

## 2. Features

### Currently Implemented
- **Customer Message Analysis**: Accepts customer inquiries and analyzes them via LLM.
- **Triage & Classification**: Automatically identifies issue categories, priority levels, and customer sentiment.
- **Structured Output**: Generates strictly validated JSON responses backed by Pydantic models.
- **Support Action Generation**: Provides concise issue summaries, recommended internal actions, and draft replies ready for the customer.
- **Multi-Turn Conversation Context**: Retains conversational history across follow-up messages within a session.
- **Error Handling & Validation**: Gracefully handles API connectivity issues, model errors, and schema validation failures.
- **Pre-Request Token Estimation**: Counts input tokens before dispatching calls to the API.
- **Token & Cost Monitoring**: Tracks per-request and cumulative token usage (input, output, thinking, cached) and estimates paid-tier API costs.
- **Modular Codebase & Configuration**: Uses separated components for schemas, analysis, and CLI orchestration, with environment variable loading via `.env`.

### Pending / Planned Features
- FastAPI and building AI-powered backend APIs.
- Database integration and conversation persistence.
- RAG implementation using company documents and knowledge bases.
- Function calling and integration with external business systems.
- Caching, token optimisation, and cost management.
- AI application security, deployment, and monitoring.
- Working with different AI providers and models.

---

## 3. Example Output

Below is an actual example run from the CLI interface:

```text
==================================================
AI CUSTOMER SUPPORT ASSISTANT
==================================================

Enter a customer message to analyze.
Type '/new' to start a fresh conversation.
Type 'exit' or 'quit' to close the application.

Customer Message: I want to buy a ring

Analyzing customer message...

PRE-REQUEST TOKEN COUNT
System instructions + customer message: 167

--------------------------------------------------
AI CUSTOMER SUPPORT ANALYSIS
--------------------------------------------------
Category: product
Priority: low
Sentiment: neutral

Summary:
Customer expresses interest in purchasing a ring.

Required Action:
Assist the customer by asking for preferences to help them find a suitable ring.

Suggested Customer Reply:
That's wonderful! We have a beautiful selection of rings. To help you find the perfect one, could you tell me a little more about what you're looking for? For example, are you interested in a particular style, metal type, gemstone, or price range?
--------------------------------------------------

--------------------------------------------------
TOKEN USAGE - THIS REQUEST
--------------------------------------------------
Input tokens: 158
Output tokens: 106
Thinking tokens: 78
Cached input tokens: 0
Tool-use tokens: 0
Total tokens: 342
Estimated paid-tier cost: $0.00080850 USD

==================================================
CUMULATIVE SESSION USAGE
==================================================
Input tokens: 158
Output tokens: 106
Thinking tokens: 78
Cached tokens: 0
Total tokens: 342
Estimated paid-tier cost: $0.00080850 USD
```

---

## 4. Requirements

- **Python**: Python 3.10 or higher
- **Google Gemini API Key**: An active key from [Google AI Studio](https://aistudio.google.com/)
- **Core Dependencies**:
  - `google-genai`: Official Google GenAI SDK
  - `pydantic`: Schema definition and validation
  - `python-dotenv`: Environment variable loader

---

## 5. Local Setup Guide

Follow these steps to set up the project on your local machine:

1. **Navigate to the project directory**:
   ```bash
   cd ai-support-assistant
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

---

## 6. How to Run the Application

To start the interactive assistant, ensure your virtual environment is active and run `main.py`:

```bash
source venv/bin/activate
python main.py
```

### CLI Commands
- Enter any customer message to analyze it.
- Enter `/new` to clear the current conversation history and start a fresh session.
- Enter `exit` or `quit` to terminate the program.

---

## 7. Project Structure

```text
ai-support-assistant/
├── analyzer.py        # Gemini client initialization, token counting, and analysis logic
├── schemas.py         # Pydantic data schemas for structured analysis output
├── main.py            # CLI entry point, session loop, error handling, and usage tracking
├── requirements.txt   # Project dependencies
├── .env               # Local environment configuration (contains API key)
└── README.md          # Project documentation
```
# ai-support-assistant
