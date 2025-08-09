import subprocess
import os
import tempfile
import resource
import time
from .base import BaseCompiler, Verdict, CompilerResult


class PythonCompiler(BaseCompiler):
    def __init__(self):
        super().__init__()
        self.version = "3"          # Python version
        self.time_limit = 2         # seconds (CPU time)
        self.memory_limit = 256     # MB
        self.output_limit = 64 * 1024  # 64KB output limit

    def compile(self, source_code):
        """
        Python doesn't need compilation, but check syntax errors.
        """
        try:
            compile(source_code, '<string>', 'exec')
            return CompilerResult(Verdict.PENDING)
        except Exception as e:
            return CompilerResult(Verdict.COMPILATION_ERROR, error_message=str(e))

    def run(self, source_code, test_input):
        # Write source code and input to temporary files
        code_path = None
        input_path = None
        stdin_file = None

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', encoding='utf-8', delete=False) as code_file:
                code_file.write(source_code)
                code_path = code_file.name

            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False) as input_file:
                # test_input may be list; convert if needed
                if isinstance(test_input, list):
                    test_input = '\n'.join(test_input)
                input_file.write(test_input)
                input_path = input_file.name
            print(test_input)
            stdin_file = open(input_path, 'r', encoding='utf-8')

            start_time = time.time()
            process = subprocess.Popen(
                ['python3', code_path],
                stdin=stdin_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
                preexec_fn=lambda: (
                    resource.setrlimit(resource.RLIMIT_CPU, (self.time_limit, self.time_limit)),
                    resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit * 1024 * 1024, self.memory_limit * 1024 * 1024))
                )
            )

            try:
                output, error = process.communicate(timeout=self.time_limit)
                execution_time = (time.time() - start_time) * 1000  # milliseconds
                print(output, error)
                # Memory usage in MB from child process
                memory_used = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024

                # Check resource limits
                if memory_used > self.memory_limit:
                    return CompilerResult(
                        Verdict.MEMORY_LIMIT_EXCEEDED,
                        execution_time=execution_time,
                        memory_used=memory_used,
                        error_message=f"Memory limit exceeded: {memory_used:.2f}MB used of {self.memory_limit}MB allowed"
                    )

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
                        error_message=error.decode('utf-8', errors='replace')
                    )

                return CompilerResult(
                    Verdict.ACCEPTED,
                    execution_time=execution_time,
                    memory_used=memory_used,
                    output=output.decode('utf-8', errors='replace')
                )

            except subprocess.TimeoutExpired:
                process.kill()
                return CompilerResult(
                    Verdict.TIME_LIMIT_EXCEEDED,
                    execution_time=self.time_limit * 1000,
                    error_message="Time limit exceeded"
                )

        except Exception as e:
            return CompilerResult(
                Verdict.RUNTIME_ERROR,
                error_message=str(e)
            )

        finally:
            # Close stdin file if open
            if stdin_file and not stdin_file.closed:
                stdin_file.close()

            # Clean up temp files
            self.cleanup(code_path, input_path)

    def cleanup(self, *files):
        """Remove temporary files"""
        for file_path in files:
            if file_path:
                try:
                    os.remove(file_path)
                except Exception:
                    pass
