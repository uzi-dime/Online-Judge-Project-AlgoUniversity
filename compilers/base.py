from enum import Enum

class Verdict(Enum):
    ACCEPTED = "AC"  # Solution is correct and meets all requirements
    WRONG_ANSWER = "WA"  # Solution output doesn't match expected output
    TIME_LIMIT_EXCEEDED = "TLE"  # Solution took too long to execute
    MEMORY_LIMIT_EXCEEDED = "MLE"  # Solution used too much memory
    RUNTIME_ERROR = "RE"  # Solution crashed during execution
    COMPILATION_ERROR = "CE"  # Solution failed to compile
    PRESENTATION_ERROR = "PE"  # Output format is incorrect
    OUTPUT_LIMIT_EXCEEDED = "OLE"  # Output size too large
    RESTRICTED_FUNCTION = "RF"  # Used forbidden functions/imports
    SYSTEM_ERROR = "SE"  # Judge system internal error
    JUDGE_ERROR = "JE"  # Error in judge's test data
    PENDING = "PENDING"  # Solution is in queue
    IN_QUEUE = "IQ"  # Specifically in execution queue
    RUNNING = "RUNNING"  # Solution is being evaluated
    SKIPPED = "SK"  # Test case skipped due to previous failure

class CompilerResult:
    def __init__(self, verdict, execution_time=0, memory_used=0, error_message="", output="",
                 exit_code=None, signal=None, peak_memory=None, output_size=None):
        self.verdict = verdict
        self.execution_time = execution_time  # in milliseconds
        self.memory_used = memory_used  # in MB
        self.error_message = error_message
        self.output = output
        self.exit_code = exit_code  # process exit code
        self.signal = signal  # signal that terminated the process (if any)
        self.peak_memory = peak_memory or memory_used  # peak memory usage
        self.output_size = output_size or len(output)  # size of output in bytes

    def to_dict(self):
        return {
            "verdict": self.verdict.value,
            "execution_time": self.execution_time,
            "memory_used": self.memory_used,
            "error_message": self.error_message,
            "output": self.output
        }

class BaseCompiler:
    def __init__(self):
        self.timeout = 2  # Default timeout in seconds
        self.memory_limit = 256  # Default memory limit in MB

    def compile(self, source_code):
        """Compile the source code if needed"""
        raise NotImplementedError

    def run(self, compiled_code, test_input):
        """Run the compiled code with test input"""
        raise NotImplementedError

    def cleanup(self):
        """Clean up any temporary files"""
        raise NotImplementedError
