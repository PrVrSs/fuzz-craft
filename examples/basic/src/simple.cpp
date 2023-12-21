#include <stdio.h>
#include <cstdint>
#include <cstring>
#include <string>


void printSimple(int n) {
  char* simple = nullptr;

  simple = (char*)malloc((n*3<4096) ? n*3 : 4096);

  std::string onesimple{"simple"};
  for (size_t i = 0; i < n; i++) {
    memcpy(simple, onesimple.data(), onesimple.size());
  }

  printf("%s", simple);

  free(simple);
}


bool VulnerableFunction(const uint8_t* data, size_t size) {
  bool result = false;
  if (size >= 3) {
    result = data[0] == 'F' &&
             data[1] == 'U' &&
             data[2] == 'Z' &&
             data[3] == 'Z';
  }

  return result;
}