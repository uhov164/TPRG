
# Лабораторная работа

В корневой директории и в директории 'exe_version' имеется папка 'generators_result', которая в себе содержит результаты генерации псевдо случайных последовательностей из первого задания. (По сути, это просто скопированная папка result из task_1 после выполнения скрипта 'prng_python_run' [смотреть README из task_1])

Для запуска основной программы lab.py:

```bash
python lab.py --help
```

> Все результаты программы сохраняются в директорию 'result'. (Об этом не было сказано в задании, но показалось, что так будет удобнее)

Для запуска тестов самой python программы:
```bash
./lab_python_run.bat
```

Сам файл 'lab_python_run' выглядит следующим образом:
```bash
python lab.py /file ./generators_result/lc_rnd.dat;   printf "\n"
python lab.py /file ./generators_result/add_rnd.dat;  printf "\n"
python lab.py /file ./generators_result/5p_rnd.dat;   printf "\n"
python lab.py /file ./generators_result/lfsr_rnd.dat; printf "\n"
python lab.py /file ./generators_result/mt_rnd.dat;   printf "\n"
python lab.py /file ./generators_result/nfsr_rnd.dat; printf "\n"
python lab.py /file ./generators_result/rc4_rnd.dat;  printf "\n"
python lab.py /file ./generators_result/rsa_rnd.dat;  printf "\n"
python lab.py /file ./generators_result/bbs_rnd.dat;  printf "\n"
```

---

Также имеется скомпилированная (с помощью pyinstaller) версия. Находится она в папке '**exe_version**'.
Для запуска, нужно прописать следующую команду:
```bash
cd /exe_version/dist/lab; 
./lab --help
```

Также в папке 'exe_version' предоставлены переписанные тесты:
```bash
./dist/lab/lab /file ./generators_result/lc_rnd.dat;   printf "\n"
./dist/lab/lab /file ./generators_result/add_rnd.dat;  printf "\n"
./dist/lab/lab /file ./generators_result/5p_rnd.dat;   printf "\n"
./dist/lab/lab /file ./generators_result/lfsr_rnd.dat; printf "\n"
./dist/lab/lab /file ./generators_result/mt_rnd.dat;   printf "\n"
./dist/lab/lab /file ./generators_result/nfsr_rnd.dat; printf "\n"
./dist/lab/lab /file ./generators_result/rc4_rnd.dat;  printf "\n"
./dist/lab/lab /file ./generators_result/rsa_rnd.dat;  printf "\n"
./dist/lab/lab /file ./generators_result/bbs_rnd.dat;  printf "\n"
```