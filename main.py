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
    
def select_notes(available_notes: list[pathlib.Path]):
    """
    Реализует функцию выбора заметок из списка.

    Args:
        available_notes: Спосок объектов Path из доступных заметок

    Returns:
        Список объектов Path, представляющих выбранные пользователем заметки 
    """
    if not available_notes:
        print("Нет доступных заметок")
        return None
    while True:
        try:
            selected_indexes_str = input(
                "Введите номера заметок через запятую (например: 1,2,3,4,5) или 'все':"
            ).lower()
            if selected_indexes_str == 'все':
                # Выбраны все заметки
                selected_indexes = list(range(len(available_notes)))
            else:
                # Обработка введенных номеров заметок
                selected_indexes = [
                    int(index.strip()) - 1 for index in selected_indexes_str.split(",")
                ]

            # Проверка наличия выбранных заметок
            for index in selected_indexes:
                if not 0 <= index < len(available_notes):
                    raise ValueError(
                        f"Недопустимый номерзаметки: {index+1}. Введите номер от 1 до {len(available_notes)}"
                    )
            select_notes = [available_notes[index] for index in selected_indexes]
            return select_notes
        except ValueError as e:
            logging.error(f"Input error: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}. Попробуй еще раз.")
            logging.error(f"Unexpected error: {e}", exc_info=True)

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
            select_notes = select_notes(found_notes)
            if select_notes:
                print("\nВыбранные заметки:")
                for note in select_notes:
                    print(f"- {note.name}")
            else:
                print("Заметки не выбранны")

        else:
            # Список пуст
            print("В директории нет Markdown файлов")
    else:
        # Функция вернула None
        print("При выполнении программы произошла ошибка")