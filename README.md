## Графическое представление данных с телескопа БСА-3

Используется Python2
### Запуск проекта:
1. Создание виртуального окружения (не обязательно, но крайне рекомендуется):
```bash
python -m virtualenv project_env
```
```bash
source project_env/bin/activate
```
2. Установка необходимых пакетов (в директории src):
```bash
python -m pip install -r requirements
```
Если возикли проблемы с недостающими пакетами:<br>
```python -m pip install <pack_name>```<br>
записать в файл requirements название недостающего пакета

3. В директории ```src/data/pnt_files/``` должны находится pnt файлы
4. Файл настройки должен находится в директории ```src/data/eqv/```
5. ```python main.py```
6. enjoy!
