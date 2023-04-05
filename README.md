# counterexample_finder

작성한 코드가 분명 맞는데 틀렸을 때!

반례가 분명 있을텐데 절대 못 찾겠을 때!

`반례 탐색기`를 사용하세요.

인터넷에서 찾은 정답 코드와 내 코드를 비교해 반례를 찾아보세요.

## 지원 언어

### 탐색기 실행 언어

1. typescript
2. python

### 실행 가능한 코드 포맷

1. cpp
2. python
  - chatGPT한테 ts에서 python으로의  번역을 부탁한 것이라 오류가 있을 수 있습니다.

## 사용법

### 공통

1. 원하시는 실행 가능한 코드 포맷과 탐색기 실행 언어를 선택하세요.

2. 탐색기 파일에서 다음을 원하는 대로 수정하세요.

```typescript
const FIND_N_CASES = 10; // 찾고 싶은 반례 개수
const MY_CPP_CODE = "./my.cpp"; // 내가 작성한 코드 파일명
const ANSWER_CPP_CODE = "./main.cpp"; // 내가 찾은 정답 코드 파일명
const OUT_FILE_NAME = "output.txt" // 반례들이 담길 텍스트 파일명
const INPUT_PROPS = {
  N: 10 // 예: N의 최대 값
  // 입력의 조건들
}
```

3. "내 코드"와 "정답 코드"를 탐색기 스크립트와 같은 디렉토리에 위치시켜두세요.

4. 입력 값을 생성할 make_input()를 완성하세요.
  - 입력 값 생성 함수는 경우의 수가 너무 많아서 제작하지 못했습니다.
  - 여러분들의 기여를 기다리고 있습니다.
  - (입력에 대한 조건이 주어지면 그에 맞는 입력 값이 자동으로 생성되는 함수)

5. 탐색기 스크립트를 실행하세요.

### typescript

```bash
$ ts-node compare_cpp.ts

or

$ ts-node compare_py.ts
```

### python

```bash
$ python3 compare_cpp.py

or

$ python3 compare_py.py
```

6. 출력 양식은 다음과 같습니다.

```

1 2 3 4 5 6 7 8   // 내 코드와 정답 코드 간에 출력이 다른 입력 값
expected: 12      // 정답 코드가 뱉은 출력
received: 10      // 내 코드가 뱉은 출력

```

## 부족한 점: 입력 값 생성 함수

입력 값 생성 함수도 쉽게 생성할 수 있도록 발전시키고 싶습니다.

저도 열심히 노력 중입니다.

혹시 괜찮은 방법이 있으시다면 고민하지 말고 기여해주세요!
