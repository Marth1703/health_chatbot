# Mental Health Assistant 💙

A Streamlit-based mental health chatbot powered by Azure OpenAI that provides different response formats based on experimental conditions.

## Features

- 🤖 AI-powered mental health assistance
- 🔄 Multiple response formats (A1-A4 conditions)
- 💭 Expandable reasoning sections
- 📚 Collapsible source citations
- 🚫 Input blocking during response streaming (toggleable)

## Local Development

### Prerequisites

- Python 3.7+
- Azure OpenAI API access

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd health_chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   copy .env.example .env  # Windows
   # or
   cp .env.example .env    # macOS/Linux
   ```

4. Edit `.env` and add your Azure OpenAI API key:
   ```
   OPEN_AI_KEY=your_actual_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run llm_app.py
   ```

6. Access the app at `http://localhost:8501`

### URL Parameters

You can test different conditions by adding URL parameters:
- `http://localhost:8501/?cond=A1` - Reasoning + Citations
- `http://localhost:8501/?cond=A2` - Reasoning only
- `http://localhost:8501/?cond=A3` - Citations only
- `http://localhost:8501/?cond=A4` - Basic response

## Deployment

### Streamlit Cloud

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)

3. Connect your GitHub repository

4. In the app settings, add your secrets:
   - Go to "Advanced settings" → "Secrets"
   - Add: `OPEN_AI_KEY = "your_actual_api_key_here"`

5. Deploy the app

### GitHub Secrets (for GitHub Actions)

If you're using GitHub Actions for deployment:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `OPEN_AI_KEY`
5. Value: Your actual API key

## Configuration

### Input Blocking

You can toggle input blocking during streaming by changing this variable in `llm_app.py`:

```python
BLOCK_INPUT_DURING_STREAMING = True  # Set to False to allow input during streaming
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPEN_AI_KEY` | Azure OpenAI API key | Yes |

## Troubleshooting

### API Key Issues

If you see "❌ API key not found":

1. **Local development**: Make sure your `.env` file exists and contains `OPEN_AI_KEY=your_key`
2. **Production**: Ensure the secret is properly set in your deployment platform
3. **GitHub Actions**: Check that the secret is added to repository secrets

### Local Testing

To test locally while having secrets in GitHub:

1. Keep your `.env` file locally (it won't be committed due to `.gitignore`)
2. The app will automatically use the local `.env` file when running `streamlit run llm_app.py`
3. In production, it will use the platform's secret management system