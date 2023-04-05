// FIXME: constants
const FIND_N_CASES = 10;
const MY_PY_CODE = "./my.py";
const ANSWER_PY_CODE = "./main.py";
const OUT_FILE_NAME = "output.txt";
const INPUT_PROPS = {
  T: 10,
  W: 5,
};

// FIXME: input generator
function makeInput(props: InputGeneratorProps): string {
  const { T, W } = props;
  let randomT = Math.floor(Math.random() * T + 1);
  let randomW = Math.floor(Math.random() * W + 1);
  let args: number[] = [];

  for (let i = 0; i < randomT; i++) {
    args[i] = Math.floor(Math.random() * 2 + 1);
  }

  return [`${randomT} ${randomW}`, ...args].join("\n");
}

/************************************/
//   Below are not to be modified   //
/************************************/
// @ts-ignore - no type definition
import { spawnSync, execSync, SpawnSyncReturns } from "child_process";
// @ts-ignore - no type definition
import fs from "fs";
// @ts-ignore - no type definition
import { Buffer } from "node";

const COMPILER = "python3";
const FILE_EXTENSION = /\.py$/;

type InputGeneratorProps = typeof INPUT_PROPS;

interface FindDifferentCasesInterface {
  myCode?: CodeProcessor;
  answerCode?: CodeProcessor;
  inputGen?: InputGenerator;
  findingCases?: number;
  outFile?: string;
}

class InputGenerator {
  private props: InputGeneratorProps;
  private generator: (props: InputGeneratorProps) => string;
  input = "";

  constructor(props: InputGeneratorProps, generator = makeInput) {
    this.props = props;
    this.generator = generator;

    this.make();
  }

  make() {
    this.input = this.generator(this.props);
  }
}

class CodeProcessor {
  private code: string;

  constructor(code: string) {
    this.code = code;
  }

  execute(input: string) {
    const result = spawnSync("python3", [this.code], {
      input,
    });
    return result.stdout.toString().trim();
  }
}

class FindDifferentCases {
  private myCode: CodeProcessor;
  private answerCode: CodeProcessor;
  private inputGen: InputGenerator;
  private findingCases: number;
  private outFile: string;
  private case = 0;

  constructor({
    myCode = new CodeProcessor("my.cpp"),
    answerCode = new CodeProcessor("main.cpp"),
    inputGen = new InputGenerator(INPUT_PROPS),
    findingCases = FIND_N_CASES,
    outFile = "output.txt",
  }: FindDifferentCasesInterface) {
    this.myCode = myCode;
    this.answerCode = answerCode;
    this.inputGen = inputGen;
    this.findingCases = findingCases;
    this.outFile = outFile;
  }

  run() {
    this.makeFile();

    while (this.case < this.findingCases) {
      this.setup();
      if (this.isOutputDifferent()) {
        this.logToConsole();
        this.logToFile();
        this.case++;
      }
    }
  }

  private setup() {
    this.inputGen.make();
    this.myCode.execute(this.inputGen.input);
    this.answerCode.execute(this.inputGen.input);
  }

  private isOutputDifferent() {
    return this.myResult !== this.answerResult;
  }

  private logToConsole() {
    console.log(this.prettyPrint);
  }

  private logToFile() {
    fs.appendFileSync(this.outFile, this.prettyPrint);
  }

  private makeFile() {
    fs.writeFileSync(this.outFile, "");
  }

  private get myResult() {
    return this.myCode.execute(this.inputGen.input);
  }
  private get answerResult() {
    return this.answerCode.execute(this.inputGen.input);
  }
  private get prettyPrint() {
    return `${this.inputGen.input}\nexpected: ${this.answerResult}\nreceived: ${this.myResult}\n\n`;
  }
}

const main = () => {
  const compare = new FindDifferentCases({
    myCode: new CodeProcessor(MY_PY_CODE),
    answerCode: new CodeProcessor(ANSWER_PY_CODE),
    outFile: OUT_FILE_NAME,
    findingCases: FIND_N_CASES,
    inputGen: new InputGenerator(INPUT_PROPS),
  });
  compare.run();
};

main();
