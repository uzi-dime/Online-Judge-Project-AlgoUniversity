import subprocess
import os
import tempfile
import resource
import signal
import time
from .base import BaseCompiler, Verdict, CompilerResult

class PythonCompiler(BaseCompiler):
    def __init__(self):
        super().__init__()
        self.version = "3"  # Python version
        self.time_limit = 2  # seconds
        self.memory_limit = 256  # MB
        self.output_limit = 64 * 1024  # 64KB output limit

    def compile(self, source_code):
        """
        Python doesn't need compilation, but we check for syntax errors
        """
        try:
            compile(source_code, '<string>', 'exec')
            return CompilerResult(Verdict.PENDING)
        except Exception as e:
            return CompilerResult(Verdict.COMPILATION_ERROR, error_message=str(e))

    def run(self, source_code, test_input):
        # Create temporary files for code and input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as code_file:
            code_file.write(source_code)
            code_path = code_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as input_file:
            input_file.write(test_input)
            input_path = input_file.name

        try:
            start_time = time.time()
            
            # Run the Python script with resource limits
            process = subprocess.Popen(
                ['python3', code_path],
                stdin=open(input_path, 'r'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=lambda: (
                    resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout)),
                    resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit * 1024 * 1024, -1))
                )
            )

            try:
                output, error = process.communicate(timeout=self.timeout)
                execution_time = (time.time() - start_time) * 1000  # Convert to ms
                
                # Get memory usage (in MB)
                memory_used = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024
                
                # Check memory limit
                if memory_used > self.memory_limit:
                    return CompilerResult(
                        Verdict.MEMORY_LIMIT_EXCEEDED,
                        execution_time=execution_time,
                        memory_used=memory_used,
                        error_message=f"Memory limit exceeded: {memory_used:.2f}MB used of {self.memory_limit}MB allowed"
                    )
                
                # Check output size
                if len(output) > self.output_limit:
                    return CompilerResult(
                        Verdict.OUTPUT_LIMIT_EXCEEDED,
                        execution_time=execution_time,
                        memory_used=memory_used,
                        error_message=f"Output limit exceeded: {len(output)} bytes of {self.output_limit} bytes allowed"
                    )
                
                if process.returncode != 0:
                    return CompilerResult(
                        Verdict.RUNTIME_ERROR,
                        execution_time=execution_time,
                        memory_used=memory_used,
                        error_message=error.decode()
                    )

                return CompilerResult(
                    Verdict.ACCEPTED,
                    execution_time=execution_time,
                    memory_used=memory_used,
                    output=output.decode()
                )

            except subprocess.TimeoutExpired:
                process.kill()
                return CompilerResult(
                    Verdict.TIME_LIMIT_EXCEEDED,
                    execution_time=self.timeout * 1000,
                    error_message="Time limit exceeded"
                )

        except Exception as e:
            return CompilerResult(
                Verdict.RUNTIME_ERROR,
                error_message=str(e)
            )
        finally:
            # Cleanup
            self.cleanup(code_path, input_path)

    def cleanup(self, *files):
        """Remove temporary files"""
        for file_path in files:
            try:
                os.remove(file_path)
            except:
                pass
