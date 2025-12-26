import subprocess
import shlex # Used to safely parse a string into a list of arguments
from flask import Flask, request, jsonify

app = Flask(__name__)

# The client/agent MUST now send a list of strings, e.g., ["nmap", "-p", "80", "target.com"]
# Or, if you need to support a single string command:
@app.post("/exec")
def exec():
    # Expect the command as a list of arguments
    cmd_input = request.json.get("cmd")
    timeout = request.json.get("timeout", 300)

    if not cmd_input:
        return jsonify({"error": "Missing 'cmd' in request body"}), 400

    # If the input is a single string (for convenience), safely parse it into a list
    if isinstance(cmd_input, str):
        try:
            # shlex.split safely handles quoted arguments and prevents shell injection
            cmd_list = shlex.split(cmd_input)
        except ValueError as e:
            return jsonify({"error": f"Invalid command string: {e}"}), 400
    elif isinstance(cmd_input, list):
        # Already a list, assume arguments are separated correctly
        cmd_list = cmd_input
    else:
        return jsonify({"error": "'cmd' must be a string or a list of strings"}), 400

    # --- SECURITY FIX: shell=False (default) is used by passing a list ---
    # The list 'cmd_list' is executed directly without shell processing.
    try:
        result = subprocess.run(
            cmd_list, # <--- Pass the command as a list of arguments
            shell=False, # <--- EXPLICITLY set to False for security
            text=True,
            capture_output=True,
            timeout=timeout,
            # It's also good practice to ensure the command is executed from a safe directory
            # cwd='/tmp' 
        )

        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    except FileNotFoundError:
        # This catches cases where the command itself (e.g., 'nmap') is not found
        return jsonify({"error": f"Command not found: '{cmd_list[0]}'"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host="0.0.0.0", port=9756)
