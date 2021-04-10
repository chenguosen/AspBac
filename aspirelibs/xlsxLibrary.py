import xlrd3 as xlrd

def get_xlsx_data(file_path):
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    data = []
    for i in range(1, sheet.nrows):
        data.append(sheet.row_values(i))
    book.release_resources()
    return data
    
def get_xlsx_data_by_index(file_path, indx=0):
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(indx)
    data = []
    for i in range(1, sheet.nrows):
        data.append(sheet.row_values(i))
    book.release_resources()
    return data

def get_xlsx_data_by_name(file_path, sname='Sheet1'):
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_name(sname)
    data = []
    for i in range(1, sheet.nrows):
        data.append(sheet.row_values(i))
    book.release_resources()
    return data