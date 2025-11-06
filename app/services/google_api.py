from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (FORMAT, PERMISSION_ROLE, PERMISSION_TYPE,
                                RANGE, SHEET_COLUMNS, SHEET_ROWS, SHEET_TITLE,
                                SPREADSHEET_LOCALE, SPREADSHEET_TITLE_TEMPLATE,
                                TABLE_COLUMNS, TABLE_HEADER_MAIN,
                                TABLE_HEADER_TITLE)


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {
            'title': SPREADSHEET_TITLE_TEMPLATE.format(date=now_date_time),
            'locale': SPREADSHEET_LOCALE
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': SHEET_TITLE,
                'gridProperties': {
                    'rowCount': SHEET_ROWS,
                    'columnCount': SHEET_COLUMNS,
                }
            }
        }]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': PERMISSION_TYPE,
        'role': PERMISSION_ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def update_spreadsheets_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        [TABLE_HEADER_MAIN, now_date_time],
        TABLE_HEADER_TITLE,
        TABLE_COLUMNS,
    ]

    for project in charity_projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description),
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
