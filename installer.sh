#!/usr/bin/env bash

set -x

# Конфигурация
INSTALL_DIR="/home/thm/.dpturl"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="dpturl.py"
BIN_PATH="/usr/local/bin/dpturl"

# Функция для установки зависимостей
install_dependencies() {
    echo "+ Установка зависимостей..."
    echo "1. Arch/Manjaro"
    echo "2. Debian/Ubuntu"
    read -rp "Выберите дистрибутив (1 или 2): " distro_choice

    if [[ "$distro_choice" == "1" ]]; then
        echo "=DEBUG= Установка для Arch/Manjaro..."
        sudo pacman -S --noconfirm python python-pip python-requests python-tqdm
    elif [[ "$distro_choice" == "2" ]]; then
        echo "=DEBUG= Установка для Debian/Ubuntu..."
        sudo apt update && sudo apt install -y python3 python3-pip python3-requests python3-tqdm
    else
        echo "=DEBUG= Неверный выбор. Выход."
        exit 1
    fi
}

# Основной процесс установки
echo "Этот скрипт установит dpturl в $INSTALL_DIR и создаст виртуальное окружение."
read -rp "Продолжить? [Y/n] " confirm

if [[ -z "$confirm" || "$confirm" =~ ^[Yy]$ ]]; then
    # Создание директории для установки
    mkdir -p "$INSTALL_DIR"

    # Установка зависимостей
    read -rp "Установить зависимости? [Y/n] " install_deps
    if [[ -z "$install_deps" || "$install_deps" =~ ^[Yy]$ ]]; then
        install_dependencies
    fi

    # Создание виртуального окружения
    echo "+ Создание виртуального окружения..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip requests tqdm
    deactivate

    # Копирование скрипта в директорию установки
    echo "+ Копирование скрипта..."
    cp "$SCRIPT_NAME" "$INSTALL_DIR/$SCRIPT_NAME"

    # Создание исполняемого файла в /usr/local/bin
    echo "+ Создание символьной ссылки в /usr/local/bin..."
    echo '#!/usr/bin/env bash
VENV_PATH="'$VENV_DIR'"
SCRIPT_PATH="'$INSTALL_DIR'/'$SCRIPT_NAME'"

source "$VENV_PATH/bin/activate"
python3 "$SCRIPT_PATH" "$@"
deactivate' | sudo tee "$BIN_PATH" > /dev/null

    sudo chmod +x "$BIN_PATH"

    echo "Установка завершена. Используйте команду 'dpturl'."
else
    echo "Установка отменена."
fi
