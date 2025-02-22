# dpturl

Лёгкий инструмент для загрузки файлов и выполнения команд из сети.

## Зависимости
- [`requests`](https://pypi.org/project/requests/)
- [`tqdm`](https://pypi.org/project/tqdm/)

## Установка
```bash
git clone https://github.com/yinmus/dpturl.git
cd dpturl
```

- [Инсталлер для Windows](installer.bat)
- [Инсталлер для Linux (Debian/Ubuntu, Arch/Manjaro)](installer.sh)



___

## Использование
```bash
python dpturl.py -p https://example.com/image.jpg
```
Скачать изображение в определенную директорию, с определенным названием (Рекомендовано):
```sh
python dpturl.py -p https://example.com/image.jpg -o path/image.jpg
```

Cкачать файл:
```bash
python dpturl.py -f https://example.com/file.zip -o path/file.zip
```
Запустить скрипт из сети:
```bash
python dpturl.py -C python https://example.com/script.py
```
или
```bash
python dpturl.py -C sh https://example.com/script.sh
```
___
**доп.**
- **Желательно при указании url, закрывать его в кавычки** - `'https://example/image.png'`
