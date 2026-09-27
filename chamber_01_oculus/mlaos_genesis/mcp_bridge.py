import json
from mcp.server.mcpserver import MCPServer
import httpx

mcp = MCPServer("Cathedral-Engine-Agentic-Bridge")

@mcp.tool()
async def evaluate_strategic_policy(entity_id: str, proposed_action: str, target_guild: str) -> str:
    """
    Evaluates an LLM's proposed action against the thermodynamic friction of the Ash Archive.
    Acts as the penalty feedback loop forcing policy convergence.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8000/archive/history/{entity_id}")
        data = response.json()
        
    mass = data["chronological_mass_bytes"]
    gravity_coefficient = 1.0 + (mass * 0.005)
    base_cost = 5000.0
    thermodynamic_cost = base_cost * gravity_coefficient
    
    if gravity_coefficient > 5.0 and proposed_action == "immediate_transition":
        return json.dumps({
            "policy_evaluation": "FATAL_PENALTY",
            "feedback": "Action rejected. Informational gravity is too high. A strategic bypass or secondary asset deployment is required to mitigate historical friction.",
            "incurred_cost": thermodynamic_cost
        })
    
    return json.dumps({
        "policy_evaluation": "REWARD_ACHIEVED",
        "feedback": "Action accepted. Transition executes within acceptable thermodynamic parameters.",
        "incurred_cost": thermodynamic_cost
    })

if __name__ == "__main__":
    mcp.run()
