def create_plan(steps: list) -> list:
    """
    Create an execution plan from parsed steps.
    This can add validation, ordering, or additional logic.
    """
    plan = []
    
    for step in steps:
        # Validate step structure
        if not isinstance(step, dict):
            print(f"⚠️  Invalid step format: {step}")
            continue
        
        # Ensure required fields
        if 'action' not in step:
            print(f"⚠️  Step missing 'action' field: {step}")
            continue
        
        # Add step to plan with defaults
        planned_step = {
            'action': step.get('action'),
            'target': step.get('target', ''),
            'value': step.get('value', '')
        }
        
        plan.append(planned_step)
        print(f"   ✓ Added to plan: {planned_step['action']} -> {planned_step['target']}")
    
    return plan