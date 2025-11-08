import os
import subprocess
import sys
import py_compile
from pathlib import Path

PROJECT_ROOT = Path(".").resolve()
SOURCE_DIRS = ["people", "academia", "finance", "infrastructure", "documents", "exceptions"]
def run_tests():
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
    return result.returncode
def run_coverage():
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "--cov"])
    return result.returncode
def compile_all():
    error_count = 0

    for src_dir in SOURCE_DIRS:
        dir_path = PROJECT_ROOT / src_dir
        for py_file in dir_path.rglob("*.py"):
            try:
                py_compile.compile(str(py_file), doraise=True)
                print(f"✅ {py_file.relative_to(PROJECT_ROOT)}")
            except py_compile.PyCompileError as e:
                print(f"❌ Синтаксическая ошибка в {py_file.relative_to(PROJECT_ROOT)}:")
                print(f"   {e.msg}")
                error_count += 1
            except Exception as e:
                print(f"❌ Неизвестная ошибка в {py_file.relative_to(PROJECT_ROOT)}: {e}")
                error_count += 1

    if error_count == 0:
        print("\n✨ Все файлы синтаксически корректны!")
        return 0
    else:
        print(f"\n💥 Найдено ошибок: {error_count}")
        return 1
def main():
    if len(sys.argv) != 2:
        print("Использование: python commands.py [test|clean]")
        return
    command = sys.argv[1]
    if command == "test":
        sys.exit(run_tests())
    elif command == "coverage":
        sys.exit(run_coverage())
    elif command == "compile":
        sys.exit(compile_all())
    else:
        print("Неизвестная команда")


if __name__ == "__main__":
    main()