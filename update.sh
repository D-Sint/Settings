#!/usr/bin/bash

# Оновлення пакунків
sudo apt update && sudo apt upgrade -yy

# Автоматичне видалення зайвих пакунків
sudo apt autoremove -yy

# Перевірка наявності аргументів командного рядка
if [ $# -ge 1 ]; then
    # Цикл для обробки всіх переданих аргументів
    for arg in "$@"; do
        # Додавання аргумента до встановлення пакунків
        sudo apt install "$arg" -yy
    done
else
    echo "Необхідно вказати принаймні один аргумент!"
fi

