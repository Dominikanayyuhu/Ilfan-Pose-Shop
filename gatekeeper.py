from datetime import datetime

def check_access():
    """
    Проверяет, можно ли сейчас пользоваться ботом.
    Возвращает текст ошибки, если доступ закрыт, иначе None.
    """
    now = datetime.now()
    # Период отпуска: с 30 декабря 2025 по 6 января 2026 включительно
    vacation_start = datetime(2025, 12, 30, 0, 0)
    vacation_end = datetime(2026, 1, 7, 0, 0) # Откроется 7 января

    if vacation_start <= now < vacation_end:
        return "Извините, но сайт закрыт с 30 декабря по 6 января, приносим свои извинение"
    return None
