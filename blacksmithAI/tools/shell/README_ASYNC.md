# Async Shell Command Executor API

A production-ready, asynchronous shell command execution API built with FastAPI and Uvicorn. This is an async version of the original Flask-based shell executor, offering better performance and scalability.

## Features

- **Asynchronous Execution**: Uses `asyncio` for non-blocking command execution
- **Security**: Commands are executed without shell (`shell=False`) to prevent injection attacks
- **Flexible Input**: Accepts both string commands and list of arguments
- **Timeout Handling**: Built-in timeout protection (default 5 hours)
- **Multiple Workers**: Production-ready with 4 worker processes
- **Health Check Endpoint**: Monitor service availability
- **Automatic Documentation**: OpenAPI/Swagger UI at `/docs`

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_async.txt
```

Or install manually:
```bash
pip install fastapi uvicorn uvloop
```

## Usage

### Running the Server

**Development mode:**
```bash
python server_async.py
```

**Production mode (recommended):**
```bash
uvicorn server_async:app --host 0.0.0.0 --port 9756 --workers 4 --loop uvloop
```

**Alternative: Using gunicorn with uvicorn workers:**
```bash
gunicorn server_async:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:9756
```

### API Endpoints

#### Execute Command
- **URL**: `POST /exec`
- **Content-Type**: `application/json`

**Request Body (String format):**
```json
{
  "cmd": "nmap -p 80,443 target.com"
}
```

**Request Body (List format):**
```json
{
  "cmd": ["nmap", "-p", "80,443", "target.com"]
}
```

**Response:**
```json
{
  "stdout": "output...",
  "stderr": "",
  "returncode": 0
}
```

**Error Responses:**
- `400` - Missing or invalid command
- `404` - Command not found
- `408` - Command timeout
- `500` - Server error

#### Health Check
- **URL**: `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "shell-executor"
}
```

### API Documentation

- **Swagger UI**: http://localhost:9756/docs
- **ReDoc**: http://localhost:9756/redoc
- **OpenAPI Schema**: http://localhost:9756/openapi.json

## Example Usage with curl

```bash
# Execute a simple command
curl -X POST http://localhost:9756/exec \
  -H "Content-Type: application/json" \
  -d '{"cmd": "ls -la"}'

# Execute a complex command
curl -X POST http://localhost:9756/exec \
  -H "Content-Type: application/json" \
  -d '{"cmd": ["nmap", "-sV", "-p", "80,443", "scanme.nmap.org"]}'

# Health check
curl http://localhost:9756/health
```

## Example Usage with Python

```python
import requests

# Execute command
response = requests.post(
    "http://localhost:9756/exec",
    json={"cmd": "nmap -p 80 target.com"}
)

result = response.json()
print(f"Return code: {result['returncode']}")
print(f"Output: {result['stdout']}")
print(f"Errors: {result['stderr']}")
```

## Security Considerations

- **No Shell Execution**: Commands are executed directly without shell interpretation
- **Input Sanitization**: Uses `shlex.split()` to safely parse string commands
- **Timeout Protection**: Commands are terminated if they exceed the timeout
- **Error Handling**: All errors are caught and returned with appropriate HTTP status codes

## Performance Tuning

The server is configured with:
- **4 Workers**: Handles concurrent requests efficiently
- **uvloop**: Faster event loop for better I/O performance
- **Timeout**: 18000 seconds (5 hours) default timeout

Adjust these parameters in `server_async.py` based on your needs:

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=9756,
    workers=4,  # Adjust based on CPU cores
    loop="uvloop",  # Remove if uvloop is not installed
    log_level="info"
)
```

## Docker Deployment

Example Dockerfile for production deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_async.txt .
RUN pip install --no-cache-dir -r requirements_async.txt

COPY server_async.py .

EXPOSE 9756

CMD ["uvicorn", "server_async:app", "--host", "0.0.0.0", "--port", "9756", "--workers", "4"]
```

Build and run:
```bash
docker build -t shell-executor .
docker run -p 9756:9756 --rm shell-executor
```

## Differences from Flask Version

| Feature | Flask (server.py) | FastAPI (server_async.py) |
|---------|------------------|---------------------------|
| Execution Model | Synchronous | Asynchronous |
| Performance | Single-threaded | Multi-worker with async I/O |
| Documentation | Manual | Auto-generated (OpenAPI) |
| Type Hints | None | Full type hints |
| Validation | Manual | Pydantic models |
| Health Check | None | Built-in endpoint |

## Troubleshooting

**Import Error: No module named 'uvloop'**
- Remove `uvloop` from requirements_async.txt
- Or install it: `pip install uvloop`

**Port already in use**
- Change the port in the script or use: `uvicorn server_async:app --port 9757`

**Command not found error**
- Ensure the command is available in the system PATH
- Use absolute paths if necessary

## License

Same as the parent project.
