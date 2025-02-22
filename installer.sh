#!/bin/bash

echo "+ Start installation? [y/n]"
read -r start
[[ "$start" != "y" ]] && exit 0

echo "+ Install dependencies? (Linux only) [y/n]"
read -r deps
if [[ "$deps" == "y" ]]; then
    echo "+ Select distribution:"
    echo "1. Arch/Manjaro"
    echo "2. Debian/Ubuntu"
    read -p "Enter number: " distro_choice

    if [[ "$distro_choice" == "1" ]]; then
        echo "=DEBUG= Installing for Arch/Manjaro..."
        sudo pacman -S --noconfirm python python-pip python-requests python-tqdm
    elif [[ "$distro_choice" == "2" ]]; then
        echo "=DEBUG= Installing for Debian/Ubuntu..."
        sudo apt update && sudo apt install -y python3 python3-pip python3-requests python3-tqdm
    else
        echo "=DEBUG= Invalid choice. Exiting."
        exit 1
    fi
fi

echo "+ Create virtual environment? [y/n]"
read -r venv
if [[ "$venv" == "y" ]]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip requests tqdm
    echo "=DEBUG= Virtual environment ready."
fi

echo "+ Run script? [y/n]"
read -r run
[[ "$run" == "y" ]] && python3 dpturl.py -h
