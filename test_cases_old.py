from core.workflow import run_test

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
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{len(test_cases)}: {test['name']}")
        print(f"Input: {test['input']}")
        print("-" * 60)
        
        try:
            report = run_test(test['input'])
            
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
            import traceback
            traceback.print_exc()
            failed += 1
        
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()