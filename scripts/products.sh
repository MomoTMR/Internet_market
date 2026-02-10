#!/bin/bash

# Путь к файлу дампа (находится в папке scripts, которая в .gitignore)
BACKUP_FILE="scripts/products_data.json"

# Проверяем, как запускать: через docker exec или локально
if [ -f "docker-compose.yml" ] && [ "$(docker ps -q -f name=${WEB_CONTAINER_NAME:-hopbarley_web})" ]; then
    RUN_CMD="docker exec -it ${WEB_CONTAINER_NAME:-hopbarley_web} python manage.py"
else
    RUN_CMD="poetry run python manage.py"
fi

case "$1" in
    dump)
        echo "--- Экспорт категорий и товаров в $BACKUP_FILE ---"
        $RUN_CMD dumpdata products.Category products.Product --indent 2 --skip-checks > $BACKUP_FILE
        echo "Готово! Данные сохранены."
        ;;
    load)
        if [ ! -f "$BACKUP_FILE" ]; then
            echo "Ошибка: Файл $BACKUP_FILE не найден. Сначала запустите './scripts/products.sh dump'."
            exit 1
        fi
        echo "--- Импорт данных из $BACKUP_FILE ---"
        $RUN_CMD loaddata $BACKUP_FILE --skip-checks
        echo "Готово! Товары и категории восстановлены."
        ;;
    *)
        echo "Использование: $0 {dump|load}"
        echo "  dump - сохранить текущие товары и категории в файл"
        echo "  load - загрузить товары и категории из файла в базу"
        exit 1
        ;;
esac
