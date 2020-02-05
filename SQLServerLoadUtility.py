#This program will automatically load from a csv file into a database, prompting the user for the servername, a database name and a tablename. When you supply these, and select a file, it will do the rest.

import os
import sys
from sys import argv
import pyodbc
from  sqlalchemy import create_engine 
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog


class Frame1(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.greetinglabel = tk.Label(text = 'SQL Server Database Auto Loader', font = ("Arial Bold", 12))
        self.greetinglabel.pack(side = TOP, padx = 10, pady = 3)

        self.lbl1 = tk.Label(text = 'Server Name: ', font =("Arial", 12))
        self.lbl1.pack(side = TOP, padx = 10, pady = 3)

        self.entry1 = tk.Entry(root, width = 32)
        self.entry1.pack(side = TOP, padx = 10, pady = 3)

        self.lbl2 = tk.Label(text = 'Database Name: ', font =("Arial", 12))
        self.lbl2.pack(side = TOP, padx = 10, pady = 3)

        self.entry2 = tk.Entry(root, width = 32)
        self.entry2.pack(side = TOP, padx = 10, pady = 3)

        self.lbl3 = tk.Label(text = 'Table Name: ', font =("Arial", 12))
        self.lbl3.pack(side = TOP, padx = 10, pady = 3)

        self.entry3 = tk.Entry(root, width = 32)
        self.entry3.pack(side = TOP, padx = 10, pady = 3)
        
        self.button1 = tk.Button(root, text = 'Submit', font = ("Arial", 12), command = self.onok)
        self.button1.pack()

    def onok(self):
        servername = self.entry1.get()
        database = self.entry2.get()
        tablename = self.entry3.get()
        c = sqlserverconnection(servername)
        infile = fileselect()
        df1 = pd_fileprep(infile)
        createdatabase(df1, database, c)
        createtable(df1, database, tablename, c)
        eng = sqlalch(database)
        alchload(df1, tablename, eng)
        root.quit()

def fileselect():
    root = tk.Tk() 
    root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    infile = root.filename
    return infile
    
#Fills all missing data with a zero.
def pd_fileprep(infile):
    l1 = []
    with open(infile, 'r') as f:
        l1 = []
        for ele in f:
            line = ele.split('\n')
            l1.append(line)

        header = l1[0]
        del header[1:]
        header = [x.replace(" ","_")for x in header]
        header = str(header)
        headerstring = header.replace("[",'').replace("]",'').replace("'",'')
        l2 = headerstring.split(",")

        rest_of_rows = l1[1:]
        l3 = []
        for ele in rest_of_rows:
            ele = str(ele)
            elestring = ele.replace("[",'').replace("]",'').replace("'",'')
            elestring = elestring.split(",")
            l3.append(elestring)
        for ele in l3:
            del ele[-1]

        df1 = pd.DataFrame(l3, columns = l2, index = None)
        df1.fillna(0, inplace = True)

        return df1

def sqlserverconnection(servername):
    conn = pyodbc.connect(
	"Driver={SQL Server Native Client 11.0};"
	"Server=" + servername + ";"
	"Trusted_Connection=yes;"
	)
    conn.autocommit = True
    c = conn.cursor()
    return c

def createdatabase(df1, database, c):
    c.execute("create database " + database)

def createtable(df1, database, tablename, c):
    hlist = list(df1.columns.values)
    allpieces = []
    for elements in hlist:
        sqlpiece = str(elements) + " VARCHAR(50)"
        allpieces.append(sqlpiece)
    fullstring = ",".join(allpieces) 
    c.execute("USE " + database + ";")
    c.execute("CREATE TABLE " + tablename + " (" + fullstring + ");")

def sqlalch(database): #Enter your servername, and choose your driver below(default: Native Client 11.0)
    DB = {'servername': 'ENTER_YOUR_SERVERNAME_HERE','database': database,
    'driver': 'driver=SQL Server Native Client 11.0'}
    
    eng = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])
    return eng

def alchload(df1, tablename, eng):
    df1.to_sql(
        name = tablename,
        con = eng,
        index = False,
        if_exists = 'append'
    )

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SQL Server Database Auto Loader')
    root.geometry("400x250")
    win1 = Frame1(root).pack(fill="both", expand=True)
    root.mainloop()


