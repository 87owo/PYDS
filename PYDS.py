import re, os, collections, time, googletrans, langid
#import pyinstaller_versionfile
from tkinter import filedialog
from tkinter.messagebox import *
import tkinter as tk
from tkinter import ttk
from tkinter import *
import webbrowser

'''
pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="1.2.1",
    company_name="PYDS",
    file_description="Python Dictionary Software",
    internal_name="PYDS",
    legal_copyright="Copyright© 2021-2022 PYDS Python Dictionary Software.",
    original_filename="PYDS.exe",
    product_name="PYDS"
)
'''

root = Tk()
root.title('PYDS V1.2.1')
#root.resizable(0,0)
root.geometry('800x450')
textPad=Text(root,undo=True)
textPad.pack(expand=YES,fill=BOTH)
scroll=Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT,fill=Y)
group = Label(root, text="Copyright© 2021-2022 PYDS Python Dictionary Software",padx=5, pady=2)
group.pack(anchor='e')
#---
translator = googletrans.Translator()
alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def words(text):
    return re.findall('[0-z]+', text) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

dic = open('words.txt','r',encoding="utf-8")
NWORDS = train(words(dic.read()))

def edits1(word):
    n = len(word)
    return set([word[0:i]+word[i+1:] for i in range(n)] +                     # deletion
               [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition
               [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] + # alteration
               [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])  # insertion

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return str(max(candidates, key=lambda w: NWORDS[w]))

def correct_all(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return candidates
#---

def tte_input():
    textPad.delete(1.0,END)
    t=Toplevel(root)
    t.title('翻譯')
    t.geometry('260x40')
    t.transient(root)
    Label(t,text=' 翻譯: ').grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    fss = 0
    Button(t,text='OK',command=lambda :tte(e.get())).grid(row=0,column=2,sticky='e'+'w',pady=2)
    
def tte(word):
    textPad.delete(1.0,END)
    x = str(word)
    try:
        x = translator.translate(str(x), dest='en').text
        textPad.insert("insert", '''
翻譯結果:
============================================================================
''')
        textPad.insert("insert", str(x))
    except:
        textPad.insert("insert", '''✖翻譯失敗，請檢查網路後重試''')
    
def ttc_input():
    textPad.delete(1.0,END)
    t=Toplevel(root)
    t.title('翻譯')
    t.geometry('260x40')
    t.transient(root)
    Label(t,text=' 翻譯: ').grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    fss = 0
    Button(t,text='OK',command=lambda :ttc(e.get())).grid(row=0,column=2,sticky='e'+'w',pady=2)
    
def ttc(word):
    textPad.delete(1.0,END)
    x = str(word)
    try:
        x = translator.translate(str(x), dest='zh-tw').text
        textPad.insert("insert", '''
翻譯結果:
============================================================================
''')
        textPad.insert("insert", str(x))
    except:
        textPad.insert("insert", '''✖翻譯失敗，請檢查網路後重試''')
    
def seaw_input():
    textPad.delete(1.0,END)
    t=Toplevel(root)
    t.title('尋找')
    t.geometry('260x40')
    t.transient(root)
    Label(t,text=' 尋找: ').grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    fss = 0
    Button(t,text='OK',command=lambda :seaw(e.get())).grid(row=0,column=2,sticky='e'+'w',pady=2)

def seaw(word):
    textPad.delete(1.0,END)
    x = str(word)
    start = time.time()
    x = x + ' '
    xl = []
    aw = []
    xw = ''
    dw = ''
    at = True
    for j in range(len(x)):
        if x[j] != ' ':
            xw = xw + xw.join(x[j])
        else:
            xl.append(xw)
            xw = ''
    for j in range(len(xl)):
        if correct(xl[j]) != 'n' and correct(xl[j]) != 's':
            dw = dw + correct(xl[j]) + ' '
            if len(xl) == 1:
                aw = correct_all(xl[j])
            else:
                at = False
    try:
        twd = translator.translate(dw, dest='zh-tw').text
        textPad.insert("insert", '''
相似結果:
============================================================================
''')
        textPad.insert("insert", str(dw) + '' + str(twd)+'''
''')
        if at:
            textPad.insert("insert", '''
更多結果:
============================================================================
''')
            for j in aw:
                twd = translator.translate(j, dest='zh-tw').text
                textPad.insert("insert", str(j) + ' ' + str(twd)+'''
''')
    except:
        textPad.insert("insert", '''
相似結果:
============================================================================
''')
        textPad.insert("insert", str(dw)+'''
''')
        if at:textPad.insert("insert", '''
更多結果:
============================================================================
''')
        for j in aw:
                textPad.insert("insert", str(j)+'''
''')
    end = time.time()
    textPad.insert("insert", '''============================================================================
''')
    textPad.insert("insert", '耗費時間: '+str(end - start)+' 秒')
    #os.system('cls')

def software_update():
    webbrowser.open('https://xiaomi69ai.wixsite.com/pyds')

def about():
    showinfo('Copyright','''官方網站: https://xiaomi69ai.wixsite.com/pyds
版權所有© 2021-2022 PYDS Python Dictionary Software''')

def version():
    showinfo('Version','軟體版本: PYDS V1.2.1')

def startm():
    textPad.delete(1.0,END)
    try:
        ft = open('PYDSL.ini','w')
        ft.write('''traditional_chinese''')
        ft.close()
        menubar = Menu(root)
        root.config(menu = menubar)
        filemenu = Menu(menubar,tearoff=False)
        filemenu.add_command(label = '尋找單字',command = seaw_input)
        #filemenu.add_command(label = '',command = ai_scan_en)
        menubar.add_cascade(label = ' 尋找',menu = filemenu)
        filemenu2 = Menu(menubar,tearoff=False)
        filemenu2.add_command(label = '翻譯成英文',command = tte_input)
        #filemenu2.add_command(label = '偵測殺毒',command = detect_antivirus)
        #filemenu2.add_command(label = '循環殺毒',command = cyclic_antivirus)
        filemenu2.add_command(label = '翻譯成中文',command = ttc_input)
        menubar.add_cascade(label = '翻譯',menu = filemenu2)
        filemenu5 = Menu(menubar,tearoff=False)
        menubar.add_cascade(label = '設置',menu = filemenu5)
        sitmenu = Menu(filemenu5,tearoff=False)
        filemenu5.add_cascade(label='軟體設置', menu=sitmenu, underline=0)
        sitmenu.add_command(label="更新軟體", command=software_update)
        sit2menu = Menu(filemenu5,tearoff=False)
        filemenu5.add_cascade(label='變更語言', menu=sit2menu, underline=0)
        sit2menu.add_command(label="繁體中文", command=startm)
        sit2menu.add_command(label="English", command=startm_en)
        aboutmenu = Menu(menubar,tearoff=False)
        #aboutmenu.add_command(label = '官方網站',command = website)
        aboutmenu.add_command(label = '關於我們',command = about)
        aboutmenu.add_command(label = '軟體版本',command = version)
        #aboutmenu.add_separator()
        #licmenu = Menu(aboutmenu,tearoff=False)
        #aboutmenu.add_cascade(label='license terms', menu=licmenu, underline=0)
        #licmenu.add_command(label = 'PYAS license terms',command = pyas_license_terms)
        #licmenu.add_command(label = 'Microsoft license terms',command = microsoft_license_terms)
        menubar.add_cascade(label = '關於',menu = aboutmenu)
        root.mainloop()
    except:
        pass
    
def tte_input_en():
    textPad.delete(1.0,END)
    t=Toplevel(root)
    t.title('Search')
    t.geometry('260x40')
    t.transient(root)
    Label(t,text=' Search: ').grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    fss = 0
    Button(t,text='OK',command=lambda :tte_en(e.get())).grid(row=0,column=2,sticky='e'+'w',pady=2)
    
def tte_en(word):
    textPad.delete(1.0,END)
    x = str(word)
    try:
        x = translator.translate(str(x), dest='en').text
        textPad.insert("insert", '''
Translate:
============================================================================
''')
        textPad.insert("insert", str(x))
    except:
        textPad.insert("insert", '''✖Translate Failed, Please Check The Network And Try Again.''')
    
def ttc_input_en():
    textPad.delete(1.0,END)
    t=Toplevel(root)
    t.title('Search')
    t.geometry('260x40')
    t.transient(root)
    Label(t,text=' Search: ').grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    fss = 0
    Button(t,text='OK',command=lambda :ttc_en(e.get())).grid(row=0,column=2,sticky='e'+'w',pady=2)
    
def ttc_en(word):
    textPad.delete(1.0,END)
    x = str(word)
    try:
        x = translator.translate(str(x), dest='zh-tw').text
        textPad.insert("insert", '''
Translate:
============================================================================
''')
        textPad.insert("insert", str(x))
    except:
        textPad.insert("insert", '''✖Translate Failed, Please Check The Network And Try Again.''')
    
def seaw_input_en():
    textPad.delete(1.0,END)
    t=Toplevel(root)
    t.title('Search')
    t.geometry('260x40')
    t.transient(root)
    Label(t,text=' Search: ').grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    fss = 0
    Button(t,text='OK',command=lambda :seaw_en(e.get())).grid(row=0,column=2,sticky='e'+'w',pady=2)

def seaw_en(word):
    textPad.delete(1.0,END)
    x = str(word)
    start = time.time()
    x = x + ' '
    xl = []
    aw = []
    xw = ''
    dw = ''
    at = True
    for j in range(len(x)):
        if x[j] != ' ':
            xw = xw + xw.join(x[j])
        else:
            xl.append(xw)
            xw = ''
    for j in range(len(xl)):
        if correct(xl[j]) != 'n' and correct(xl[j]) != 's':
            dw = dw + correct(xl[j]) + ' '
            if len(xl) == 1:
                aw = correct_all(xl[j])
            else:
                at = False
    try:
        twd = translator.translate(dw, dest='zh-tw').text
        textPad.insert("insert", '''
Similar results:
============================================================================
''')
        textPad.insert("insert", str(dw) + '' + str(twd)+'''
''')
        if at:
            textPad.insert("insert", '''
More results:
============================================================================
''')
            for j in aw:
                twd = translator.translate(j, dest='zh-tw').text
                textPad.insert("insert", str(j) + ' ' + str(twd)+'''
''')
    except:
        textPad.insert("insert", '''
Similar results:
============================================================================
''')
        textPad.insert("insert", str(dw)+'''
''')
        if at:textPad.insert("insert", '''
More results:
============================================================================
''')
        for j in aw:
                textPad.insert("insert", str(j)+'''
''')
    end = time.time()
    textPad.insert("insert", '''============================================================================
''')
    textPad.insert("insert", 'Time consuming: '+str(end - start)+' sec')
    #os.system('cls')

def software_update():
    webbrowser.open('https://xiaomi69ai.wixsite.com/pyds')

def about_en():
    showinfo('Copyright','''Official website: https://xiaomi69ai.wixsite.com/pyds
Copyright© 2021-2022 PYDS Python Dictionary Software''')

def version_en():
    showinfo('Version','Software Version: PYDS V1.2.1')

def startm_en():
    textPad.delete(1.0,END)
    try:
        ft = open('PYDSL.ini','w')
        ft.write('''english''')
        ft.close()
        menubar = Menu(root)
        root.config(menu = menubar)
        filemenu = Menu(menubar,tearoff=False)
        filemenu.add_command(label = 'Search Word',command = seaw_input_en)
        #filemenu.add_command(label = '',command = ai_scan_en)
        menubar.add_cascade(label = ' Search',menu = filemenu)
        filemenu2 = Menu(menubar,tearoff=False)
        filemenu2.add_command(label = 'Translate to English',command = tte_input_en)
        #filemenu2.add_command(label = '偵測殺毒',command = detect_antivirus)
        #filemenu2.add_command(label = '循環殺毒',command = cyclic_antivirus)
        filemenu2.add_command(label = 'Translate to Chinese',command = ttc_input_en)
        menubar.add_cascade(label = 'Translate',menu = filemenu2)
        filemenu5 = Menu(menubar,tearoff=False)
        menubar.add_cascade(label = 'Setting',menu = filemenu5)
        sitmenu = Menu(filemenu5,tearoff=False)
        filemenu5.add_cascade(label='Software settings', menu=sitmenu, underline=0)
        sitmenu.add_command(label="Update software", command=software_update)
        sit2menu = Menu(filemenu5,tearoff=False)
        filemenu5.add_cascade(label='Change language', menu=sit2menu, underline=0)
        sit2menu.add_command(label="繁體中文", command=startm)
        sit2menu.add_command(label="English", command=startm_en)
        aboutmenu = Menu(menubar,tearoff=False)
        #aboutmenu.add_command(label = '官方網站',command = website)
        aboutmenu.add_command(label = 'About us',command = about_en)
        aboutmenu.add_command(label = 'Software version',command = version_en)
        #aboutmenu.add_separator()
        #licmenu = Menu(aboutmenu,tearoff=False)
        #aboutmenu.add_cascade(label='license terms', menu=licmenu, underline=0)
        #licmenu.add_command(label = 'PYAS license terms',command = pyas_license_terms)
        #licmenu.add_command(label = 'Microsoft license terms',command = microsoft_license_terms)
        menubar.add_cascade(label = 'About',menu = aboutmenu)
        root.mainloop()
    except:
        pass
    
def setup_pyds():
    try:
        ft = open('PYDSL.ini','r')
        fe = ft.read()
        ft.close()
        if fe == 'english':
            startm_en()
        elif fe == 'traditional_chinese':
            startm()
        else:
            startm_en()
    except:
        startm_en()

setup_pyds()
