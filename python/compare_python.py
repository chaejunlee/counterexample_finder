from typing import List
import subprocess
import random

# FIXME: constants
FIND_N_CASES = 10
MY_PY_CODE = "./my.py"
ANSWER_PY_CODE = "./main.py"
OUT_FILE_NAME = "output.txt"
INPUT_PROPS = {
    'T': 10,
    'W': 5,
}

# FIXME: input generator
def make_input(props: dict) -> str:
    T, W = props['T'], props['W']
    random_T = random.randint(1, T)
    random_W = random.randint(1, W)
    args: List[int] = []

    for i in range(random_T):
        args.append(random.randint(1, 2))

    return f"{random_T} {random_W}\n" + "\n".join(str(arg) for arg in args)

################################################################################
################################################################################
################################################################################

class InputGenerator:
    def __init__(self, props: dict, generator=make_input):
        self.props = props
        self.generator = generator
        self.input = ""
        self.make()

    def make(self):
        self.input = self.generator(self.props)

class CodeProcessor:
    def __init__(self, code: str):
        self.code = code

    def execute(self, input_str: str) -> str:
        result = subprocess.run(['python3', self.code], input=input_str.encode(), stdout=subprocess.PIPE)
        return result.stdout.decode().strip()

class FindDifferentCases:
    def __init__(self, my_code: CodeProcessor, answer_code: CodeProcessor, input_gen: InputGenerator, finding_cases=FIND_N_CASES, out_file=OUT_FILE_NAME):
        self.my_code = my_code
        self.answer_code = answer_code
        self.input_gen = input_gen
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
        self.my_code.execute(self.input_gen.input)
        self.answer_code.execute(self.input_gen.input)

    def is_output_different(self) -> bool:
        return self.my_result != self.answer_result

    def log_to_console(self):
        print(self.pretty_print)

    def log_to_file(self):
        with open(self.out_file, 'a') as f:
            f.write(self.pretty_print)

    def make_file(self):
        with open(self.out_file, 'w'):
            pass

    @property
    def my_result(self) -> str:
        return self.my_code.execute(self.input_gen.input)

    @property
    def answer_result(self) -> str:
        return self.answer_code.execute(self.input_gen.input)

    @property
    def pretty_print(self) -> str:
        return f"{self.input_gen.input}\nexpected: {self.answer_result}\nreceived: {self.my_result}\n\n"

def main():
    compare = FindDifferentCases(
        my_code=CodeProcessor(MY_PY_CODE),
        answer_code=CodeProcessor(ANSWER_PY_CODE),
        out_file=OUT_FILE_NAME,
        finding_cases=FIND_N_CASES,
        input_gen=InputGenerator(INPUT_PROPS)
    )
    compare.run()

if __name__ == '__main__':
    main()
