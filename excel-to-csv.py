# -*- coding: UTF-8 -*-

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import Radiobutton
from tkinter import messagebox

def selectFile():
    filePath = tk.filedialog.askopenfilename(filetypes=[('xlsx', '*.xlsx'), ('xls', '*.xls')])
    if filePath == '':
        return

    operate = tk.messagebox.askquestion('提示', '转换时间取决于文档大小。\n转换过程请耐心等待，不要退出程序。\n确定立即转换？')

    if operate == 'no':
        return

    entry.config(state='normal')
    entry.insert(0, filePath)
    entry.config(state='readonly')

    # 解剖文件路径
    path, fileFullName = os.path.split(filePath)
    fileName, extension = os.path.splitext(fileFullName)

    # 获取单选选项
    sheetType = radioEle.get()

    # 加载整个excel
    excel = pd.ExcelFile(filePath)
    sheets = excel.sheet_names
    if sheetType == 1:
        dataExcel = pd.read_excel(excel, sheet_name=None, index_col=0)
        for i in dataExcel:
            transfterPath = os.path.join(path + '/', fileName + ' - ' + i + '.csv')
            try:
                dataExcel[i].to_csv(transfterPath, encoding='utf-8')
            except Exception as e:
                tk.messagebox.showerror('错误', e)
    tk.messagebox.showinfo('提示', '已转换完成，路径：' + path)

def readSheets(filePath):
    # 方法一
    excel = pd.ExcelFile(filePath)

    return excel.sheet_names

    # 方法二
    # df = pd.read_excel(filePath, None)
    # return df.keys()

    # 方法三
    # wb = openpyxl.load_workbook(filePath)
    # return wb.sheetnames

window = tk.Tk()
window.title('excel转换csv工具')

frame = tk.Frame(window)
frame.grid(padx=20, pady=20)


entry = tk.Entry(frame, width=40, state='readonly')
entry.grid(row=1, column=0, columnspan=2)

choiceBtn = tk.Button(frame, text='选择文件', command=selectFile)
choiceBtn.grid(row=1, column=2)
choiceTip = tk.Label(frame, text='支持xlsx/xls文件')
choiceTip.grid(row=2, column=0, sticky=tk.NW)


radioEle = tk.IntVar()
radioEle.set(1)

transfterLabel = tk.Label(frame, text='sheet操作：')
transfterLabel.grid(row=0, column=0, sticky=tk.NW)
radioBtn1 = Radiobutton(frame, text='全部转换', variable=radioEle, value=1)
radioBtn1.grid(row=0, column=1, sticky=tk.NW)

window.mainloop()