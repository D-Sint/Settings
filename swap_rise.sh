# Вимкнути існуючий своп
<<<<<<< HEAD
sudo swapoff /swapfile

# Розширити файл свопу до 8 гігабайт
sudo dd if=/dev/zero of=/swapfile bs=1G count=6 seek=2

# Відформатувати розширений файл як своп
sudo mkswap /swapfile

# Увімкнути новий своп
sudo swapon /swapfile

# Перевірити, що своп успішно збільшено
free -h
=======
sudo swapoff /mnt/swapfile

# Розширити файл свопу до 8 гігабайт
sudo dd if=/dev/zero of=/mnt/swapfile bs=1G count=6 seek=2

# Відформатувати розширений файл як своп
sudo mkswap /mnt/swapfile

# Увімкнути новий своп
sudo swapon /mnt/swapfile

# Перевірити, що своп успішно збільшено
free -h
>>>>>>> 0f002ca480f2a3c0e4b5eb262997cf65472a4a89
