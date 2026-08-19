from app.agents import support_agent, sales_agent, hr_agent, orchestrator_agent

AGENTS = {
    "support": support_agent.handle_message,
    "sales": sales_agent.handle_message,
    "hr": hr_agent.handle_message,
    "orchestrator": orchestrator_agent.handle_message,
}

def get_agent_handler(agent_name: str):
    return AGENTS.get(agent_name, AGENTS["support"])
