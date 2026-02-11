from agents.parser import parse_test
from agents.planner import create_plan
from agents.executor import execute_plan
from agents.validator import validate_results
import json
import re

def run_test(prompt: str):
    print(f"\n🔍 Parsing test instruction: {prompt}")
    
    # Parse the test
    parsed = parse_test(prompt)
    
    # Try to extract JSON/list from the response
    try:
        # Remove markdown code blocks if present
        cleaned = re.sub(r'```(?:python|json)?\n?', '', parsed)
        cleaned = cleaned.strip()
        
        # Try to find a list in the response
        if '[' in cleaned and ']' in cleaned:
            start = cleaned.index('[')
            end = cleaned.rindex(']') + 1
            cleaned = cleaned[start:end]
        
        steps = eval(cleaned)
    except Exception as e:
        print(f"⚠️  Parsing error: {e}")
        print(f"Raw response: {parsed}")
        # Fallback to simple parsing
        steps = [{"action": "error", "message": "Could not parse test steps"}]
    
    print(f"✅ Parsed steps: {steps}\n")
    
    # Create execution plan
    print("📋 Creating execution plan...")
    plan = create_plan(steps)
    print(f"Plan: {plan}\n")
    
    # Execute the plan
    print("🚀 Executing test plan...")
    results = execute_plan(plan)
    print(f"Results: {results}\n")
    
    # Validate results
    print("✔️  Validating results...")
    report = validate_results(results)
    
    # Convert report to dict for display
    report_dict = report.model_dump()
    print(f"\n📊 Final Report:")
    print(f"   Status: {report_dict['status']}")
    print(f"   Summary: {report_dict['summary']}")
    print(f"   Timestamp: {report_dict['timestamp']}")
    
    return report