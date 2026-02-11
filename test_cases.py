from core.workflow import run_test
import csv
from datetime import datetime
import os

test_cases = [
    {
        "name": "Simple Navigation",
        "input": "open google.com",
        "expected_actions": ["navigate"]
    },
    {
        "name": "Navigation with Extract",
        "input": "open github.com and list repositories",
        "expected_actions": ["navigate", "extract"]
    },
    {
        "name": "Search Flow",
        "input": "navigate to amazon.com search for books",
        "expected_actions": ["navigate", "type"]
    },
    {
        "name": "Complex Multi-step",
        "input": "open wikipedia.org extract links and click random article",
        "expected_actions": ["navigate", "extract", "click"]
    }
]

def run_all_tests():
    print("=" * 60)
    print("🧪 Running AI UI Tester Test Suite")
    print("=" * 60)
    
    # Prepare CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"test_results_{timestamp}.csv"
    
    # CSV headers
    csv_headers = [
        "Test Case Number",
        "Test Case Name",
        "Test Input",
        "Step Number",
        "Step Action",
        "Step Target",
        "Step Value",
        "Step Status",
        "Step Result",
        "Extracted Data",
        "Error Message",
        "Screenshot Path",
        "Overall Test Status",
        "Test Summary",
        "Test Timestamp",
        "Miscellaneous"
    ]
    
    csv_rows = []
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{len(test_cases)}: {test['name']}")
        print(f"Input: {test['input']}")
        print("-" * 60)
        
        try:
            report = run_test(test['input'])
            
            # Extract report data
            test_status = report.status
            test_summary = report.summary
            test_timestamp = report.timestamp
            
            # Process each step
            for step_num, step_result in enumerate(report.steps, 1):
                step_data = step_result.step
                
                # Extract data as string (handle lists/dicts)
                extracted_data = ""
                if step_result.data:
                    if isinstance(step_result.data, list):
                        extracted_data = f"{len(step_result.data)} items: " + str(step_result.data[:3])  # First 3 items
                    else:
                        extracted_data = str(step_result.data)
                
                # Create row for this step
                row = {
                    "Test Case Number": i,
                    "Test Case Name": test['name'],
                    "Test Input": test['input'],
                    "Step Number": step_num,
                    "Step Action": step_data.get('action', 'N/A'),
                    "Step Target": step_data.get('target', 'N/A'),
                    "Step Value": step_data.get('value', 'N/A'),
                    "Step Status": step_result.status,
                    "Step Result": "PASS" if step_result.status == "success" else "FAIL" if step_result.status == "failed" else "SKIP",
                    "Extracted Data": extracted_data,
                    "Error Message": step_result.error if step_result.error else "",
                    "Screenshot Path": step_result.screenshot if step_result.screenshot else "",
                    "Overall Test Status": test_status,
                    "Test Summary": test_summary if step_num == 1 else "",  # Only show on first row
                    "Test Timestamp": test_timestamp if step_num == 1 else "",  # Only show on first row
                    "Miscellaneous": f"Expected: {', '.join(test['expected_actions'])}" if step_num == 1 else ""
                }
                
                csv_rows.append(row)
            
            # Check if test passed
            if report.status in ['success', 'partial']:
                print(f"✅ Test PASSED: {test['name']}")
                print(f"   Status: {report.status}")
                print(f"   Summary: {report.summary}")
                passed += 1
            else:
                print(f"⚠️  Test COMPLETED with status: {report.status}")
                print(f"   Summary: {report.summary}")
                passed += 1
            
        except Exception as e:
            print(f"❌ Test FAILED: {test['name']}")
            print(f"   Error: {str(e)}")
            
            # Add error row to CSV
            row = {
                "Test Case Number": i,
                "Test Case Name": test['name'],
                "Test Input": test['input'],
                "Step Number": 0,
                "Step Action": "ERROR",
                "Step Target": "N/A",
                "Step Value": "N/A",
                "Step Status": "failed",
                "Step Result": "FAIL",
                "Extracted Data": "",
                "Error Message": str(e),
                "Screenshot Path": "",
                "Overall Test Status": "failed",
                "Test Summary": f"Test execution failed: {str(e)}",
                "Test Timestamp": datetime.now().isoformat(),
                "Miscellaneous": f"Exception occurred during test execution"
            }
            csv_rows.append(row)
            
            failed += 1
            
            import traceback
            traceback.print_exc()
        
        print("-" * 60)
    
    # Write to CSV
    if csv_rows:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(csv_rows)
        
        print(f"\n📄 Test results saved to: {csv_filename}")
        print(f"   Total rows: {len(csv_rows)}")
        print(f"   Location: {os.path.abspath(csv_filename)}")
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 60)
    
    return csv_filename

if __name__ == "__main__":
    result_file = run_all_tests()
    print(f"\n✅ All tests completed! Results saved to: {result_file}")