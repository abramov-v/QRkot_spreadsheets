# Время жизни JWT-токена
JWT_LIFETIME_SECONDS = 3600

# Минимально допустимая длина пароля
MIN_PASSWORD_LENGTH = 3

# Минимальная вложенная сумма в проект (для валидации)
MIN_INVESTED_AMOUNT = 0

# Формат строкового представления времени
FORMAT = '%Y/%m/%d %H:%M:%S'

# Параметры создаваемой таблицы
SPREADSHEET_TITLE_TEMPLATE = 'Отчёт от {date}'
SPREADSHEET_LOCALE = 'ru_RU'
SHEET_TITLE = 'Закрытые проекты'
SHEET_ROWS = 100
SHEET_COLUMNS = 11
TABLE_HEADER_MAIN = ['Отчёт от']
TABLE_HEADER_TITLE = ['Топ проектов по скорости закрытия']
TABLE_COLUMNS = ['Название проекта', 'Время сбора', 'Описание']
PERMISSION_ROLE = 'writer'
PERMISSION_TYPE = 'user'
RANGE = 'A1'