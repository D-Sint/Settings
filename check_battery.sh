#!/bin/bash

# Дізнаємось назву батареї (зазвичай BAT0 або BAT1)
BATTERY_PATH="/sys/class/power_supply/BAT1/"


# Читаємо статус живлення
STATUS=$(cat "$BATTERY_PATH/status")

# Виводимо тільки якщо живлення йде від батареї
if [ "$STATUS" = "Discharging" ]; then
    CAPACITY=$(cat "$BATTERY_PATH/capacity")
    echo "Заряд батареї: $CAPACITY%"
fi
