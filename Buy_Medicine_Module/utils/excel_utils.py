import openpyxl


def read_excel_data(file_path, sheet_name):

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook[sheet_name]

    data = []

    headers = []

    for cell in sheet[1]:
        headers.append(cell.value)

    for row in sheet.iter_rows(min_row=2, values_only=True):

        row_data = {}

        for key, value in zip(headers, row):
            row_data[key] = value

        data.append(row_data)

    return data