# Example

Go to the directory
```shell
cd examples/basic
```

Download CodeQL
```shell
wget https://github.com/github/codeql-cli-binaries/releases/download/v2.15.5/codeql-linux64.zip
```

```shell
unzip codeql-linux64.zip
```

Download the dependencies and install
```shell
codeql/codeql pack install ../../fuzz_craft/ql/c-cpp/
```

Create CodeQL codebase

```shell
python -m fuzz_craft create_database -l cpp -ql codeql/codeql -s src/
```

Create harnesses

```shell
python -m fuzz_craft create_harness -l cpp -ql codeql/codeql -s src/ -t libfuzzer -k YOUR_OPENAI_KEY
```

After that, two files will be generated

**src/.fuzz_craft/harnesses/printSimple.cc**
```cpp
#include <stdint.h>
#include <stdlib.h>
#include <string>
#include "simple.cpp"
// any other imports go here


extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  // fuzzed code goes here
  int arg_0 = 0;
  if (size >= sizeof(int)) {
    arg_0 = *reinterpret_cast<const int*>(data);
  }
  printSimple(arg_0);
  return 0;
}
```

**src/.fuzz_craft/harnesses/vulnerableFunction.cc**

```cpp
#include <stdint.h>
#include <stdlib.h>
#include <string>
#include "simple.cpp"
// any other imports go here


extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  // fuzzed code goes here
  std::string input(reinterpret_cast<const char*>(data), size);
  vulnerableFunction(reinterpret_cast<const uint8_t*>(input.c_str()), input.size());
  return 0;
}
```

Compile the fuzzer in the following way:

```shell
clang++ -g src/.fuzz_craft/harness/printSimple.cc -O2 -fno-omit-frame-pointer -fsanitize=address,fuzzer -fsanitize-coverage=trace-cmp,trace-gep,trace-div -Isrc src/libsimple.a -o print_simple_fuzzer
```

Run the fuzzer
```shell
./print_simple_fuzzer
```
