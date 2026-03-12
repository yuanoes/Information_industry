# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
Single-file C++ console application (信息产业发展统计系统 — Information Industry Statistics System). No external services, databases, or package managers needed.

### Building
```
g++ -I./stubs -o info_industry "究极无敌最终版.cpp" -std=c++11
```

### Linux compatibility notes
- The source targets Windows (`#include <windows.h>`, `system("cls")`, `system("color b4")`, hardcoded `d:\inf.dat` path).
- `stubs/windows.h` provides an empty stub so the include resolves on Linux.
- `Information_industry.h` is a required empty header (referenced at line 491 but not shipped in the original repo).
- `system("cls")` and `system("color b4")` produce harmless "not found" warnings on Linux — they do not affect application functionality.
- File save/read (menu options 5 & 6) uses the Windows path `d:\inf.dat` and will print "open binary file error" on Linux. All other features work normally.

### Running
The application is interactive (stdin menu). To run: `./info_industry`. To pipe automated input: `printf '1\n1\n北京\n2025\n...\n7\n' | ./info_industry`.

### Testing
No automated test framework. Verify by compiling (exit code 0, only expected warning about `JudgePlace`) and running the program interactively.
