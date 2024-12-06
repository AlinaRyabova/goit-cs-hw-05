import argparse
import asyncio
import os
from pathlib import Path
import shutil
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Асинхронна функція для рекурсивного читання папок
async def read_folder(source_folder: Path, output_folder: Path):
    """Рекурсивно читає файли у вихідній папці та передає їх для копіювання."""
    tasks = []  # Список задач для виконання
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file = Path(root) / file
            tasks.append(copy_file(source_file, output_folder))
    
    await asyncio.gather(*tasks)  # Асинхронне виконання задач

# Асинхронна функція для копіювання файлів
async def copy_file(source_file: Path, output_folder: Path):
    """Копіює файл у відповідну підпапку на основі розширення."""
    try:
        extension = source_file.suffix.lstrip(".").lower() or "others"
        destination_folder = output_folder / extension
        destination_folder.mkdir(parents=True, exist_ok=True)  # Створення папки, якщо її немає
        destination_file = destination_folder / source_file.name

        # Копіювання файлу
        await asyncio.to_thread(shutil.copy2, source_file, destination_file)

        logging.info(f"Скопійовано: {source_file} -> {destination_file}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {source_file}: {e}")

# Основна функція
def main():
    # Обробка аргументів командного рядка
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument(
        "source", type=str, help="Вихідна папка, де розміщені файли для сортування."
    )
    parser.add_argument(
        "output", type=str, help="Цільова папка для збереження відсортованих файлів."
    )
    args = parser.parse_args()

    source_folder = Path(args.source).resolve()
    output_folder = Path(args.output).resolve()

    if not source_folder.exists():
        logging.error(f"Вихідна папка {source_folder} не існує.")
        return

    # Запуск асинхронного процесу
    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
