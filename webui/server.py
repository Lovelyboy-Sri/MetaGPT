from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import yaml
import json
from typing import Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class ChatRequest(BaseModel):
    prompt: str
    model: str
    system_prompt: Optional[str] = None

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config2.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/models")
async def list_models():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://03ef5b24c906.ngrok-free.app/v1/models")
            if response.status_code == 200:
                data = response.json()
                return {"models": [model["id"] for model in data["data"]]}
    except:
        # Fallback to config
        config = load_config()
        if "model" in config:
            return {"models": [config["model"]]}
        return {"models": ["gemma3:1b"]}  # Default fallback from config

@app.post("/stream_chat")
async def stream_chat(request: ChatRequest):
    async def generate():
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "model": request.model,
                    "prompt": request.prompt,
                    "stream": True
                }
                if request.system_prompt:
                    data["system"] = request.system_prompt

                async with client.stream(
                    "POST",
                    "https://03ef5b24c906.ngrok-free.app/v1/chat/completions",
                    json={
                        "model": request.model,
                        "messages": [
                            {"role": "user", "content": request.prompt}
                        ] if not request.system_prompt else [
                            {"role": "system", "content": request.system_prompt},
                            {"role": "user", "content": request.prompt}
                        ],
                        "stream": True
                    },
                    timeout=60.0
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line.lstrip("data: "))
                                if chunk.get("choices") and chunk["choices"][0].get("delta", {}).get("content"):
                                    content = chunk["choices"][0]["delta"]["content"]
                                    yield f"data: {json.dumps({'response': content})}\n\n"
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            yield f"data: {{'error': '{str(e)}'}}\n\n"
            return

    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)