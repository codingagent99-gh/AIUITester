from browser.playwright_tools import PlaywrightBrowser
import asyncio

async def execute_plan_async(plan: list) -> dict:
    """Execute the test plan using Playwright (async)"""
    
    browser = PlaywrightBrowser(headless=False)
    await browser.start()
    
    results = {
        "test_name": "UI Test",
        "steps": []
    }
    
    try:
        for step in plan:
            print(f"\n▶️  Executing: {step}")
            
            action = step.get('action')
            target = step.get('target')
            value = step.get('value')
            
            step_result = {
                "step": step,
                "status": "success",
                "error": None,
                "data": None
            }
            
            try:
                if action == 'navigate':
                    result = await browser.navigate(target)
                    step_result['status'] = result['status']
                    if result['status'] == 'failed':
                        step_result['error'] = result.get('error')
                
                elif action == 'click':
                    result = await browser.click(target)
                    step_result['status'] = result['status']
                    if result['status'] == 'failed':
                        step_result['error'] = result.get('error')
                
                elif action == 'type':
                    result = await browser.type_text(target, value or '')
                    step_result['status'] = result['status']
                    if result['status'] == 'failed':
                        step_result['error'] = result.get('error')
                
                elif action == 'extract':
                    if target in ['links', 'link']:
                        result = await browser.extract_links()
                    else:
                        result = await browser.extract_text()
                    
                    step_result['status'] = result['status']
                    step_result['data'] = result.get('data', [])
                    
                    if result['status'] == 'failed':
                        step_result['error'] = result.get('error')
                    else:
                        print(f"   📊 Extracted {len(step_result['data'])} items")
                        if step_result['data']:
                            print(f"   Preview: {step_result['data'][:3]}")
                
                elif action == 'wait':
                    wait_time = int(target) if target else 2
                    await asyncio.sleep(wait_time)
                    print(f"   ⏳ Waited {wait_time} seconds")
                
                else:
                    step_result['status'] = 'skipped'
                    step_result['error'] = f"Unknown action: {action}"
                    print(f"   ⚠️  {step_result['error']}")
            
            except Exception as e:
                step_result['status'] = 'failed'
                step_result['error'] = str(e)
                print(f"   ❌ Error: {e}")
            
            results['steps'].append(step_result)
    
    finally:
        await browser.close()
    
    return results

def execute_plan(plan: list) -> dict:
    """Sync wrapper for execute_plan_async"""
    return asyncio.run(execute_plan_async(plan))