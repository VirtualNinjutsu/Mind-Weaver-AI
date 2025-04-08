import logging
import pathlib
from decouple import config

#RU: Настройка логирования
logging.basicConfig(filename='program.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- RU: Поиск заметок ---
def find_md(vault_path_str: str):
    """
    Ищет все Markdown (.md) файлы в указонной директории.

    Функция рассматривает указанную директорию и рекурсивно ищет все файлы с расширением .md

    Args:
        vault_path: Строка с путем к директории

    Returns:
        Список объектов Path, представляющих найденные .md файлы,
        или None, если путь некорректен или произошла ошибка доступа.
    """
    logging.info(f"Starting file search in directory: {vault_path_str}")

    try:
        # str -> Path
        vault_path = pathlib.Path(vault_path_str)

        # RU: Проверка пути
        if not vault_path.is_dir():
            logging.error(f"Specified path: {vault_path} does not exist or is not a directory")
            return None
        
        # RU:Используем rglob библиотеки pathlib для рекурсивного поиска и проверяем результаты
        markdown_files = list(vault_path.rglob('*.md'))

        if not markdown_files:
            logging.warning(f"No Markdown files found in directory: {vault_path}")
        else:
            logging.info(f"Found {len(markdown_files)} Markdown files in directory: {vault_path}")
        return markdown_files
    
    except PermissionError:
        # Ошибка доступа
        logging.error(f"Insufficient permissions to access directory: {vault_path}")
        return None
    except Exception as e:
        # Обработка прочих ошибок
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return None

# Точка входа

if __name__ == "__main__":
    # Путь к директории
    vault_path_str = config("VAULT_PATH")

    # Применяем функцию
    found_notes = find_md(vault_path_str)

    # Проверка результата выполнения функции
    if found_notes is not None:
        if found_notes:
            print("\nНайденые заметки:")
            for n, note in enumerate(found_notes):
                print(f"{n+1}. {note}")
        else:
            # Список пуст
            print("В директории нет Markdown файлов")
    else:
        # Функция вернула None
        print("При выполнении программы произошла ошибка")