# MetaGPT Web UI

A simple web interface for interacting with MetaGPT using Ollama as the backend.

## Features

- Modern, responsive chat interface
- Real-time streaming responses
- Model selection dropdown
- Easy setup and configuration

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running and accessible at http://localhost:11434

3. Run the server:
```bash
python server.py
```

4. Open your browser and navigate to http://localhost:8000

## Configuration

The web UI will automatically use the model specified in your MetaGPT config file (`config/config2.yaml`). If Ollama is available, it will fetch the list of available models from the Ollama API.

## Usage

1. Select a model from the dropdown menu
2. Type your message in the input field
3. Press Enter or click Send to start the conversation
4. The response will stream in real-time

## Development

The project structure is organized as follows:

```
webui/
├── static/
│   └── index.html    # Frontend UI
├── server.py         # FastAPI backend server
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

To modify the frontend, edit the `static/index.html` file. The backend API endpoints are defined in `server.py`.