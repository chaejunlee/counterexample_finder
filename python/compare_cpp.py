import subprocess
import random

# FIXME: constants
FIND_N_CASES = 10
MY_CPP_CODE = "./my.cpp"
ANSWER_CPP_CODE = "./main.cpp"
OUT_FILE_NAME = "output.txt"
INPUT_PROPS = {
  "N": 10
}

# FIXME: input generator
def make_input(props):
    N = props["N"]
    args = [random.randint(0, N - 1) for _ in range(N)]
    return f"{N} {' '.join(map(str, args))}"

class InputGenerator:
    def __init__(self, props, generator=make_input):
        self.props = props
        self.generator = generator
        self.make()
        
    def make(self):
        self.input = self.generator(self.props)

class CodeProcessor:
    COMPILER = "g++"
    COMPILER_OPTION = "c++11"
    FILE_EXTENSION = ".cpp"

    def __init__(self, code):
        self.code = code
        self.compiled = code.replace(self.FILE_EXTENSION, "")

        self.compile()

    def compile(self):
        subprocess.check_output([
            self.COMPILER, f"-std={self.COMPILER_OPTION}", self.code, "-o", self.compiled
        ])

    def execute(self, input_):
        self.executable = subprocess.run([self.compiled], input=input_, capture_output=True)

class FindDifferentCases:
    def __init__(self, my_code=None, answer_code=None, input_gen=None, finding_cases=FIND_N_CASES, out_file=OUT_FILE_NAME):
        self.my_code = my_code or CodeProcessor(MY_CPP_CODE)
        self.answer_code = answer_code or CodeProcessor(ANSWER_CPP_CODE)
        self.input_gen = input_gen or InputGenerator(INPUT_PROPS)
        self.finding_cases = finding_cases
        self.out_file = out_file
        self.case = 0

    def run(self):
        self.make_file()

        while self.case < self.finding_cases:
            self.setup()
            if self.is_output_different():
                self.log_to_console()
                self.log_to_file()
                self.case += 1

    def setup(self):
        self.input_gen.make()
        self.my_code.execute(self.input_gen.input.encode())
        self.answer_code.execute(self.input_gen.input.encode())

    def is_output_different(self):
        return self.my_result != self.answer_result

    def log_to_console(self):
        print(self.pretty_print)

    def log_to_file(self):
        with open(self.out_file, "a") as f:
            f.write(self.pretty_print)

    def make_file(self):
        with open(self.out_file, "w"):
            pass

    @property
    def my_result(self):
        return self.my_code.executable.stdout.decode().strip()

    @property
    def answer_result(self):
        return self.answer_code.executable.stdout.decode().strip()

    @property
    def pretty_print(self):
        return f"{self.input_gen.input}\nexpected: {self.answer_result}\nreceived: {self.my_result}\n\n"

def main():
    compare = FindDifferentCases(
        my_code=CodeProcessor(MY_CPP_CODE),
        answer_code=CodeProcessor(ANSWER_CPP_CODE),
        out_file=OUT_FILE_NAME,
        finding_cases=FIND_N_CASES,
        input_gen=InputGenerator(INPUT_PROPS),
    )
    compare.run()

if __name__ == "__main__":
    main()
