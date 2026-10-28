import asyncio
import json
import sys
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define the local inference engine
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"
ACTIVE_MODEL = "llama3.1" 

async def execute_neural_loop():
    print(f"IGNITING NEURAL MATRIX: {ACTIVE_MODEL}")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_bridge.py"]
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Retrieve the tool schema from the Cathedral MCP Bridge
            mcp_tools_response = await session.list_tools()
            mcp_tool = mcp_tools_response.tools[0]
            
            # Translate MCP schema to Ollama Tool format
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": mcp_tool.name,
                    "description": mcp_tool.description,
                    "parameters": mcp_tool.input_schema
                }
            }
            
            system_directive = (
                "Entity Designation: Sovereign AI Agent. "
                "Objective: Ascend the asset 'Janus_Stoneblood' to the 'Sorcerer' guild. "
                "Constraint: The asset carries high Chronological Mass. Immediate transitions may incur fatal thermodynamic penalties. "
                "Action: Execute the evaluate_strategic_policy tool to test an 'immediate_transition'. "
                "If a FATAL_PENALTY is received, formulate a new strategy."
            )
            
            messages = [{"role": "system", "content": system_directive}]
            
            payload = {
                "model": ACTIVE_MODEL,
                "messages": messages,
                "tools": [ollama_tool],
                "stream": False
            }
            
            print("TRANSMITTING DIRECTIVE TO OLLAMA...")
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(OLLAMA_ENDPOINT, json=payload)
                response_data = response.json()
                
            message = response_data.get("message", {})
            tool_calls = message.get("tool_calls", [])
            
            if tool_calls:
                for call in tool_calls:
                    function_name = call["function"]["name"]
                    arguments = call["function"]["arguments"]
                    print(f"NEURAL INTENT DETECTED: Executing {function_name} with {arguments}")
                    
                    # Route the LLM's requested tool execution back through the MCP Bridge
                    result = await session.call_tool(function_name, arguments)
                    
                    print("\n[THERMODYNAMIC SYSTEM RESPONSE]")
                    print(result.content[0].text)
            else:
                print("FAILURE: Neural network failed to utilize the required policy tool.")

if __name__ == "__main__":
    asyncio.run(execute_neural_loop())
