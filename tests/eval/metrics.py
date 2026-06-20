def evaluate_task_success(instance):
    """
    Evaluates the deterministic state-machine output of the HR Onboarding Agent.
    """
    turns = (instance.get("agent_data") or {}).get("turns", [])
    
    if not turns:
        return {"score": 1, "explanation": "No turns found in trace."}
    
    last_turn = turns[-1]
    called_tools = []
    
    for event in last_turn.get("events", []):
        if event.get("author") != "user":
            for part in event.get("content", {}).get("parts", []):
                if "function_call" in part and part["function_call"]["name"] != "set_model_response":
                    called_tools.append(part["function_call"]["name"])
    
    case_id = instance.get("eval_case_id", "")
    score = 5
    reasoning = "Tools called correctly."
    
    if case_id == "start_onboarding":
        if "send_welcome_packet" not in called_tools:
            score, reasoning = 1, f"Missing send_welcome_packet. Called: {called_tools}"
    
    elif case_id == "documents_signed_transition":
        if "provision_software_accounts" not in called_tools or "order_hardware" not in called_tools:
            score, reasoning = 1, f"Missing provision or hardware. Called: {called_tools}"

    elif case_id == "docusign_timeout_transition":
        if len(called_tools) > 0:
            score, reasoning = 1, f"Should not call tools immediately on timeout. Called: {called_tools}"
    
    return {"score": score, "explanation": reasoning}
