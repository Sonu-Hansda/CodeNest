import subprocess
import os
import tempfile
import time 

def evaluate_code(code, test_cases):
    results = []
    
    for test in test_cases:
        input_data = test['input']
        expected_output = test['expected_output']
        
        # Creating a temporary file to hold the user's code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as code_file:
            code_file.write(code)
            code_file_path = code_file.name
        
        try:
            start_time = time.time()
            # Running the code using subprocess and capturing the output
            result = subprocess.run(
                ["python", code_file_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5
            )
            end_time = time.time()

            actual_output = result.stdout
            error_output = result.stderr
            passed = actual_output.strip() == expected_output.strip()
            time_taken = end_time - start_time
            results.append({
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "error_output":error_output,
                "time_taken":time_taken,
                "passed": passed
            })
        
        except subprocess.TimeoutExpired:
            results.append({
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": "Timeout",
                "error_output":"",
                "time taken":None,
                "passed": False
            })
        
        finally:
            # Cleaning up the temporary file
            os.remove(code_file_path)
    
    return results