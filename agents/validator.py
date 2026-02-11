from schemas.result_schema import TestReport, StepResult
from datetime import datetime

def validate_results(results: dict) -> TestReport:
    """Validate test execution results and generate report"""
    
    # Extract step results
    step_results = []
    for step_data in results.get('steps', []):
        step_result = StepResult(
            step=step_data.get('step', {}),
            status=step_data.get('status', 'unknown'),
            error=step_data.get('error'),
            screenshot=step_data.get('screenshot'),
            data=step_data.get('data')
        )
        step_results.append(step_result)
    
    # Determine overall status
    statuses = [sr.status for sr in step_results]
    if 'failed' in statuses:
        overall_status = 'failed'
    elif 'skipped' in statuses:
        overall_status = 'partial'
    else:
        overall_status = 'success'
    
    # Generate summary
    total = len(step_results)
    passed = statuses.count('success')
    failed = statuses.count('failed')
    skipped = statuses.count('skipped')
    
    summary = f"Total steps: {total}, Passed: {passed}, Failed: {failed}, Skipped: {skipped}"
    
    # Create report
    report = TestReport(
        test_name=results.get('test_name', 'UI Test'),
        status=overall_status,
        steps=step_results,
        summary=summary,
        timestamp=datetime.now().isoformat()
    )
    
    return report