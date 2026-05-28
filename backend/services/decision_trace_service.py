def generate_decision_trace(state: dict) -> list:
    trace = []
    opts = state.get("optimization_recommendations", [])
    
    for opt in opts:
        original = opt.get("original", "Component")
        alt = opt.get("alternative", "Alternative")
        reason = opt.get("reason", "Optimization requirement")
        
        trace.append({
            "decision": f"Replaced {original} with {alt}",
            "rationale": reason,
            "agent": "Optimization Agent"
        })
        
    warnings = state.get("validation_warnings", [])
    for warn in warnings:
        trace.append({
            "decision": "Flagged architecture risk",
            "rationale": warn,
            "agent": "Validation Agent"
        })
        
    return trace
