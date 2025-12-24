import asyncio
import shlex
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging

def _setup_logger(active: bool = True) -> logging.Logger:
    """Setup logger for the shell executor service."""
    if active:
        logger = logging.getLogger("shell_executor")
        logger.setLevel(logging.INFO)  
        return logger
    return None

def log(message: str, type: str = "info"):
    """Log a message if logging is enabled."""
    logger = _setup_logger()

    if logger:
        if type == "error":
            logger.error(message)
        elif type == "warning":
            logger.warning(message)
        else:
            logger.info(message)



app = FastAPI(
    title="Shell Command Executor",
    description="Async shell command execution API",
    version="1.0.0"
)


async def execute_command(cmd_list: List[str], timeout: int = 300) -> Dict[str, Any]:
    """
    Execute a command asynchronously and return the result.
    
    Args:
        cmd_list: List of command arguments
        timeout: Maximum time to wait for command completion (seconds)
    
    Returns:
        Dictionary containing stdout, stderr, and returncode
    """
    try:
        # Create the subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the process to complete with timeout
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )
        
        # Decode output
        stdout_text = stdout.decode('utf-8', errors='replace')
        stderr_text = stderr.decode('utf-8', errors='replace')
        
        return {
            "stdout": stdout_text,
            "stderr": stderr_text,
            "returncode": process.returncode
        }
        
    except asyncio.TimeoutError:
        # Kill the process if it times out
        try:
            process.kill()
            await process.wait()
        except Exception:
            pass
        
        raise HTTPException(
            status_code=408,
            detail=f"Command execution timed out after {timeout} seconds"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Command not found: '{cmd_list[0]}'"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing command: {str(e)}"
        )


@app.post("/exec")
async def exec_command(request: Request):
    """
    Execute a shell command asynchronously.
    
    Accepts either:
    - A string command (e.g., "nmap -p 80 target.com")
    - A list of command arguments (e.g., ["nmap", "-p", "80", "target.com"])
    
    Returns:
        JSON response with stdout, stderr, and returncode
    """
    try:
        # Parse JSON body
        body = await request.json()
        cmd_input = body.get("cmd")
        timeout = body.get("timeout", 300)
        
        if not cmd_input:
            log( "Missing 'cmd' in request body", type="error")
            raise HTTPException(
                status_code=400,
                detail="Missing 'cmd' in request body"
            )
        
        log(f"Received command: {cmd_input} with timeout {timeout} seconds")
        # Parse command into a list
        if isinstance(cmd_input, str):
            try:
                # shlex.split safely handles quoted arguments and prevents shell injection
                cmd_list = shlex.split(cmd_input)
            except ValueError as e:
                log(f"Invalid command string: {e}", type="error")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid command string: {e}"
                )
        elif isinstance(cmd_input, list):
            # Already a list, assume arguments are separated correctly
            cmd_list = cmd_input
        else:
            log("*cmd* must be a string or a list of strings", type="error")
            raise HTTPException(
                status_code=400,
                detail="'cmd' must be a string or a list of strings"
            )
        
        # Execute command asynchronously
        result = await execute_command(cmd_list, timeout=timeout)
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        log(f"Server error: {str(e)}", type="error")
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "shell-executor"}


if __name__ == "__main__":
    # Run the server with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9756,
        loop="uvloop",
        log_level="info"
    )

    log("Shell command executor server started.", type="info")
    
