import xlrd
from models import *


class ReadDiploma():
    def __init__(self,file_name):
        self.diploma = xlrd.open_workbook(file_name)
        self.sheet = self.diploma.sheet_by_index(0)
        self.colnum = self.sheet.ncols
        self.rowsnum = self.sheet.nrows

    def read(self):
        for index in range(1,self.rowsnum):
            num,project_name,compete_name,level,rank,members,teachers,time_date = self.sheet.row_values(index)
            compete_name_list = members.split(' ')
            teachers_list = teachers.split(' ')
            if str(time_date).find('年'):
                date_time = str(time_date).split('年')[0]+'-01-01'
            else:
                date_time = str(time_date).replace('.','-')+'-01'
            d = Diploma(project_name=project_name,compete_name=compete_name,diploma_time=date_time,level=level,rank=rank).add()
            d.add_members(compete_name_list)
            d.add_teachers(teachers_list)

