from core.workflow import run_test
import json

prompt = input("Enter Test Instruction:\n")

report = run_test(prompt)

print(report.json(indent=2))

with open("report.json","w") as f:
    f.write(report.json(indent=2))
