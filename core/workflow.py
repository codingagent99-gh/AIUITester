from agents.parser import parse_test
from agents.executor import Executor
from agents.validator import validate
from schemas.result_schema import StepResult, TestReport

def run_test(prompt):

    steps = eval(parse_test(prompt))

    executor = Executor()
    results = []

    for step in steps:
        status, error = executor.run_step(step)

        if status == "Passed":
            valid = validate(step, executor.browser)
            if not valid:
                status = "Failed"
                error = "Validation failed"

        results.append(
            StepResult(step=step, status=status, error=error)
        )

    final = "Passed" if all(r.status=="Passed" for r in results) else "Failed"

    return TestReport(
        test_name=prompt[:40],
        steps=results,
        final_status=final
    )
