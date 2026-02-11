from core.workflow import run_test
import csv
from datetime import datetime
import os
import json

def load_test_cases_from_csv(csv_filename="test_cases.csv"):
    """Load test cases from CSV file"""
    test_cases = []
    
    try:
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Parse expected_actions (comma-separated string to list)
                expected_actions = row['expected_actions'].split(',') if row['expected_actions'] else []
                expected_actions = [action.strip() for action in expected_actions]
                
                test_case = {
                    "number": row.get('test_case_number', 'N/A'),
                    "name": row.get('test_case_name', 'Unnamed Test'),
                    "priority": row.get('priority', 'Medium'),
                    "category": row.get('category', 'General'),
                    "input": row.get('input', ''),
                    "expected_actions": expected_actions
                }
                
                test_cases.append(test_case)
        
        print(f"✅ Loaded {len(test_cases)} test cases from {csv_filename}")
        return test_cases
        
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_filename}' not found!")
        print(f"   Please generate it first by running: python generate_sample_test_cases.py")
        return []
    except Exception as e:
        print(f"❌ Error loading test cases: {e}")
        return []

def format_data_preview(data, max_length=100):
    """Format data for CSV display"""
    if not data:
        return ""
    
    if isinstance(data, list):
        preview = json.dumps(data[:3], ensure_ascii=False)
        if len(data) > 3:
            preview += f" ... ({len(data)} total items)"
        return preview[:max_length]
    
    data_str = str(data)
    return data_str[:max_length] + ("..." if len(data_str) > max_length else "")

def run_all_tests(input_csv="test_cases.csv"):
    print("=" * 80)
    print("🧪 Running AI UI Tester Test Suite")
    print("=" * 80)
    
    # Load test cases from CSV
    test_cases = load_test_cases_from_csv(input_csv)
    
    if not test_cases:
        print("⚠️  No test cases to run. Exiting.")
        return None
    
    # Prepare output CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"test_results_{timestamp}.csv"
    
    # Enhanced CSV headers for results
    csv_headers = [
        "Test_ID",
        "Test_Case_Name",
        "Test_Category",
        "Test_Priority",
        "Test_Input",
        "Expected_Actions",
        "Step_Number",
        "Step_Action",
        "Step_Target",
        "Step_Value",
        "Step_Status",
        "Step_Result",
        "Execution_Time_Sec",
        "Extracted_Data_Preview",
        "Extracted_Data_Count",
        "Error_Message",
        "Error_Type",
        "Screenshot_Path",
        "Overall_Test_Status",
        "Test_Summary",
        "Total_Steps",
        "Passed_Steps",
        "Failed_Steps",
        "Test_Start_Time",
        "Test_End_Time",
        "Miscellaneous_Notes"
    ]
    
    csv_rows = []
    passed = 0
    failed = 0
    skipped = 0
    test_suite_start = datetime.now()
    
    for i, test in enumerate(test_cases, 1):
        test_id = test['number']
        print(f"\n📋 Test {i}/{len(test_cases)}: {test_id} - {test['name']}")
        print(f"   Category: {test['category']} | Priority: {test['priority']}")
        print(f"   Input: {test['input']}")
        print(f"   Expected Actions: {', '.join(test['expected_actions'])}")
        print("-" * 80)
        
        if not test['input']:
            print(f"⊘ SKIPPED: No input provided for test case")
            skipped += 1
            continue
        
        test_start_time = datetime.now()
        
        try:
            report = run_test(test['input'])
            test_end_time = datetime.now()
            
            # Calculate statistics
            total_steps = len(report.steps)
            passed_steps = sum(1 for s in report.steps if s.status == "success")
            failed_steps = sum(1 for s in report.steps if s.status == "failed")
            
            # Extract report data
            test_status = report.status
            test_summary = report.summary
            
            # Process each step
            for step_num, step_result in enumerate(report.steps, 1):
                step_data = step_result.step
                
                # Calculate step execution time (approximate)
                step_time = (test_end_time - test_start_time).total_seconds() / total_steps
                
                # Extract and format data
                extracted_count = 0
                extracted_preview = ""
                if step_result.data:
                    if isinstance(step_result.data, list):
                        extracted_count = len(step_result.data)
                        extracted_preview = format_data_preview(step_result.data)
                    else:
                        extracted_preview = format_data_preview(step_result.data)
                
                # Determine error type
                error_type = ""
                if step_result.error:
                    if "timeout" in step_result.error.lower():
                        error_type = "Timeout"
                    elif "not found" in step_result.error.lower():
                        error_type = "Element Not Found"
                    elif "network" in step_result.error.lower():
                        error_type = "Network Error"
                    else:
                        error_type = "General Error"
                
                # Miscellaneous notes
                misc_notes = []
                if step_num == 1:
                    misc_notes.append(f"Expected: {', '.join(test['expected_actions'])}")
                if step_result.status == "skipped":
                    misc_notes.append("Step was skipped")
                if extracted_count > 100:
                    misc_notes.append(f"Large dataset extracted ({extracted_count} items)")
                
                # Validate if action matches expected
                step_action = step_data.get('action', 'N/A')
                if step_action in test['expected_actions']:
                    misc_notes.append(f"✓ Action matched expected")
                
                # Create row for this step
                row = {
                    "Test_ID": test_id,
                    "Test_Case_Name": test['name'],
                    "Test_Category": test['category'],
                    "Test_Priority": test['priority'],
                    "Test_Input": test['input'],
                    "Expected_Actions": ', '.join(test['expected_actions']),
                    "Step_Number": step_num,
                    "Step_Action": step_action,
                    "Step_Target": step_data.get('target', 'N/A'),
                    "Step_Value": step_data.get('value', 'N/A'),
                    "Step_Status": step_result.status,
                    "Step_Result": "✅ PASS" if step_result.status == "success" else "❌ FAIL" if step_result.status == "failed" else "⊘ SKIP",
                    "Execution_Time_Sec": f"{step_time:.2f}",
                    "Extracted_Data_Preview": extracted_preview,
                    "Extracted_Data_Count": extracted_count if extracted_count else "",
                    "Error_Message": step_result.error if step_result.error else "",
                    "Error_Type": error_type,
                    "Screenshot_Path": step_result.screenshot if step_result.screenshot else "",
                    "Overall_Test_Status": test_status.upper(),
                    "Test_Summary": test_summary if step_num == 1 else "",
                    "Total_Steps": total_steps if step_num == 1 else "",
                    "Passed_Steps": passed_steps if step_num == 1 else "",
                    "Failed_Steps": failed_steps if step_num == 1 else "",
                    "Test_Start_Time": test_start_time.strftime("%Y-%m-%d %H:%M:%S") if step_num == 1 else "",
                    "Test_End_Time": test_end_time.strftime("%Y-%m-%d %H:%M:%S") if step_num == 1 else "",
                    "Miscellaneous_Notes": " | ".join(misc_notes)
                }
                
                csv_rows.append(row)
            
            # Check if test passed
            if report.status in ['success', 'partial']:
                print(f"✅ Test PASSED: {test['name']}")
                print(f"   Status: {report.status} | Steps: {passed_steps}/{total_steps} passed")
                passed += 1
            else:
                print(f"❌ Test FAILED: {test['name']}")
                print(f"   Status: {report.status} | Steps: {passed_steps}/{total_steps} passed")
                failed += 1
            
        except Exception as e:
            test_end_time = datetime.now()
            print(f"❌ Test FAILED: {test['name']}")
            print(f"   Error: {str(e)}")
            
            # Add error row to CSV
            row = {
                "Test_ID": test_id,
                "Test_Case_Name": test['name'],
                "Test_Category": test['category'],
                "Test_Priority": test['priority'],
                "Test_Input": test['input'],
                "Expected_Actions": ', '.join(test['expected_actions']),
                "Step_Number": 0,
                "Step_Action": "ERROR",
                "Step_Target": "N/A",
                "Step_Value": "N/A",
                "Step_Status": "failed",
                "Step_Result": "❌ FAIL",
                "Execution_Time_Sec": f"{(test_end_time - test_start_time).total_seconds():.2f}",
                "Extracted_Data_Preview": "",
                "Extracted_Data_Count": "",
                "Error_Message": str(e),
                "Error_Type": "Test Execution Error",
                "Screenshot_Path": "",
                "Overall_Test_Status": "FAILED",
                "Test_Summary": f"Test execution failed: {str(e)}",
                "Total_Steps": 0,
                "Passed_Steps": 0,
                "Failed_Steps": 0,
                "Test_Start_Time": test_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Test_End_Time": test_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Miscellaneous_Notes": f"Exception: {type(e).__name__}"
            }
            csv_rows.append(row)
            
            failed += 1
            
            import traceback
            traceback.print_exc()
        
        print("-" * 80)
    
    test_suite_end = datetime.now()
    
    # Write to CSV
    if csv_rows:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(csv_rows)
        
        file_size = os.path.getsize(output_csv) / 1024  # KB
        
        print(f"\n📄 Test results exported to CSV:")
        print(f"   File: {output_csv}")
        print(f"   Location: {os.path.abspath(output_csv)}")
        print(f"   Total rows: {len(csv_rows)} (excluding header)")
        print(f"   File size: {file_size:.2f} KB")
    
    # Print summary
    total_time = (test_suite_end - test_suite_start).total_seconds()
    total_tests = len(test_cases)
    
    print("\n" + "=" * 80)
    print(f"📊 Test Suite Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed} ({(passed/total_tests*100):.1f}%)")
    print(f"   Failed: {failed} ({(failed/total_tests*100):.1f}%)")
    print(f"   Skipped: {skipped} ({(skipped/total_tests*100):.1f}%)" if skipped > 0 else "")
    print(f"   Success Rate: {(passed/total_tests*100):.1f}%")
    print(f"   Total Execution Time: {total_time:.2f} seconds")
    print(f"   Average Time per Test: {(total_time/total_tests):.2f} seconds")
    print("=" * 80)
    
    return output_csv

if __name__ == "__main__":
    import sys
    
    # Check if custom input CSV is provided
    input_csv = sys.argv[1] if len(sys.argv) > 1 else "test_cases.csv"
    
    print(f"📂 Using input CSV: {input_csv}\n")
    
    result_file = run_all_tests(input_csv)
    
    if result_file:
        print(f"\n✅ All tests completed!")
        print(f"📊 Detailed results available in: {result_file}")
        print(f"\n💡 Tip: Open the CSV file in Excel or Google Sheets for better visualization")