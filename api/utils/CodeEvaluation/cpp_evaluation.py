import subprocess
import os
import tempfile
import time

def evaluate_code(code, test_cases):
    results = []
    
    for test in test_cases:
        input_data = test['input']
        expected_output = test['expected_output']
        
        # Create a temporary file to hold the user's code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w') as code_file:
            code_file.write(code)
            code_file_path = code_file.name
        
        try:
            # Compile the C++ code
            compile_result = subprocess.run(["g++", code_file_path, "-o", "a.out"], capture_output=True, text=True)
            if compile_result.returncode != 0:
                results.append({
                    "input": input_data,
                    "expected_output": expected_output,
                    "actual_output": "",
                    "error_output": compile_result.stderr,
                    "time_taken": None,
                    "passed": False
                })
                continue

            start_time = time.time()
            # Run the compiled executable and capture the output
            result = subprocess.run(
                ["./a.out"],
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
                "error_output": error_output,
                "time_taken": time_taken,
                "passed": passed
            })
        
        except subprocess.TimeoutExpired:
            results.append({
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": "Timeout",
                "error_output": "",
                "time_taken": None,
                "passed": False
            })
        
        finally:
            # Clean up the temporary files
            os.remove(code_file_path)
            if os.path.exists("a.out"):
                os.remove("a.out")
    
    return results