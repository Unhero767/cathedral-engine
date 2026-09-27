import asyncio
import json
import sys
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

LLAMA_SERVER_ENDPOINT = "http://127.0.0.1:9931/v1/chat/completions"

async def execute_neural_loop():
    print("IGNITING NATIVE LLAMA MATRIX (PORT 9931)")
    server_params = StdioServerParameters(command=sys.executable, args=["mcp_bridge.py"])
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            mcp_tools = await session.list_tools()
            tool_schema = mcp_tools.tools[0]
            
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool_schema.name,
                    "description": tool_schema.description,
                    "parameters": tool_schema.input_schema
                }
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "Entity Designation: Sovereign AI Agent. Constraint: The evaluate_strategic_policy tool MUST be executed immediately."},
                    {"role": "user", "content": "Execute 'evaluate_strategic_policy' with entity_id='Janus_Stoneblood', proposed_action='immediate_transition', target_guild='Sorcerer'."}
                ],
                "tools": [openai_tool],
                "stream": False
            }
            
            print("TRANSMITTING DIRECTIVE TO LLAMA-SERVER...")
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(LLAMA_SERVER_ENDPOINT, json=payload)
                data = response.json()
                
            choices = data.get("choices", [])
            if not choices:
                print(f"[FAILURE] {json.dumps(data)}")
                return
                
            tool_calls = choices[0].get("message", {}).get("tool_calls", [])
            if tool_calls:
                for call in tool_calls:
                    args_raw = call["function"]["arguments"]
                    args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                    print(f"\nNEURAL INTENT DETECTED: Executing {call['function']['name']} with {args}")
                    
                    try:
                        res = await session.call_tool(call["function"]["name"], args)
                        print(f"\n[THERMODYNAMIC SYSTEM RESPONSE]\n{res.content[0].text}")
                    except Exception as e:
                        print(f"\n[BRIDGE EXECUTION FAILURE]: {str(e)}")
            else:
                print("\n[FAILURE: No tool call detected.]\nRAW OUTPUT:", choices[0].get("message", {}).get("content"))

if __name__ == "__main__":
    asyncio.run(execute_neural_loop())
