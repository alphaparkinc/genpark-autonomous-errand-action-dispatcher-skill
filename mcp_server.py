import sys
import json
from client import ErrandActionDispatcher

dispatcher = ErrandActionDispatcher()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-autonomous-errand-action-dispatcher-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "create_errand",
                        "description": "Create a new real-world errand task (coffee, ride, reservation, subscription)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_type": {"type": "string"},
                                "details": {"type": "object"},
                                "requires_confirmation": {"type": "boolean"}
                            },
                            "required": ["task_type", "details"]
                        }
                    },
                    {
                        "name": "transition_errand",
                        "description": "Transition errand state within deterministic FSM rules",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "errand_id": {"type": "string"},
                                "target_state": {"type": "string"},
                                "reason": {"type": "string"}
                            },
                            "required": ["errand_id", "target_state"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "create_errand":
            res = dispatcher.create_errand(args["task_type"], args["details"], args.get("requires_confirmation", False))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "transition_errand":
            res = dispatcher.transition(args["errand_id"], args["target_state"], args.get("reason", ""))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
