
# Практическое задание №2

В корневой директории и в директории 'exe_version' хранится файл generated.dat, который представляет собой построенную псевдо случайную последовательность с помощью prng.py.

Для запуска основной программы rnc.py:

```bash
python rnc.py --help
```

> Все результаты программы сохраняются в директорию 'result'. (Об этом не было сказано в задании, но показалось, что так будет удобнее)

Для запуска тестов самой python программы:
```bash
./rnc_python_run.bat
```

Сам файл 'rnc_python_run' выглядит следующим образом:
```bash
python rnc.py /d st /p1 134 /p2 123124;
python rnc.py /d tr /p1 289 /p2 1323;
python rnc.py /d ex /p1 289 /p2 1323;
python rnc.py /d nr /p1 234 /p2 12300;
python rnc.py /d gm /p1 289 /p2 1323 /p3 2;
python rnc.py /d ln /p1 289 /p2 132;
python rnc.py /d ls /p1 289 /p2 132;
python rnc.py /d bi /p1 234 /p2 5;
```

---

Также имеется скомпилированная (с помощью pyinstaller) версия. Находится она в папке '**exe_version**'.
Для запуска, нужно прописать следующую команду:
```bash
cd /exe_version/dist/rnc; 
./rnc --help
```

Также в папке 'exe_version' предоставлены переписанные тесты:
```bash
/dist/rnc/rnc /d st /p1 134 /p2 123124;
/dist/rnc/rnc /d tr /p1 289 /p2 1323;
/dist/rnc/rnc /d ex /p1 289 /p2 1323;
/dist/rnc/rnc /d nr /p1 234 /p2 12300;
/dist/rnc/rnc /d gm /p1 289 /p2 1323 /p3 2;
/dist/rnc/rnc /d ln /p1 289 /p2 132;
/dist/rnc/rnc /d ls /p1 289 /p2 132;
/dist/rnc/rnc /d bi /p1 234 /p2 5;
```