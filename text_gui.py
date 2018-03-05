<<<<<<< HEAD
from tkinter import *
import tkinter.filedialog
import os
import tkinter.messagebox as messagebox

file_name=None
PROGRAM_NAME="PyEditor"

window=Tk()
window.title("PyEditor")
window.iconbitmap('icons/pypad.ico')
w, h = window.winfo_screenwidth(),window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))

def quit():
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        window.destroy()

def new_file(event=None):
    window.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0,END)

def open_file(event=None):
    input_file_name=tkinter.filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if input_file_name:
        global file_name
        file_name=input_file_name
        window.title('{} - {}'.format(os.path.basename(file_name),PROGRAM_NAME))
        content_text.delete(1.0,END)
        with open(file_name) as f:
            content_text.insert(1.0,f.read())

def save_file(event=None):
    global file_name
    if not file_name:
        save_as_file()
    else:
        write_to_file(file_name)
    return "break"

def save_as_file(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name),PROGRAM_NAME))
    return "break"

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass

def cut():
    content_text.event_generate("<<Cut>>")

def copy():
    content_text.event_generate("<<Copy>>")

def paste():
    content_text.event_generate("<<Paste>>")

def undo():
    content_text.event_generate("<<Undo>>")

def redo(event=None):
    content_text.event_generate("<<Redo>>")
    return 'break'

def find(event=None):
    search_top_level=Toplevel(window)
    search_top_level.title("Find Text")
    search_top_level.transient(window)
    Label(search_top_level,text="Find All:").grid(row=0,column=0,sticky='e')
    search_entry_widget=Entry(search_top_level,width=25)
    search_entry_widget.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value=IntVar()
    Checkbutton(search_top_level, text='Ignore Case',variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_top_level,text="Find All",underline=0,command=lambda:search_output(search_entry_widget.get(),ignore_case_value.get(),content_text,search_top_level,search_entry_widget)).grid(row=2,column=2,sticky='e'+'w',padx=2,pady=2)
    def close_search_window():
        content_text.tag_remove('match','1.0',END)
        search_top_level.destroy()
        search_top_level.protocol('WM_DELETE_WINDOW',close_search_window)
        return 'break'

def search_output(needle,if_ignore_case,content_text,search_top_level,search_box):
    content_text.tag_remove('match','1.0',END)
    matches_found=0
    if needle:
        start_pos='1.0'
        while True:
            start_pos=content_text.search(needle,start_pos,nocase=if_ignore_case,stopindex=END)
            if not start_pos:
                break
            end_pos='{}+{}c'.format(start_pos,len(needle))
            content_text.tag_add('match',start_pos,end_pos)
            matches_found+=1
            start_pos=end_pos
            content_text.tag_config('match',foreground='red',background='yellow')
            search_box.focus_set()
            search_top_level.title('{} matches found'.format(matches_found))

def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return "break"

def about():
    tkinter.messagebox.showinfo("About", "{}{}".format(PROGRAM_NAME, "\nThis is a Chess Game developed in Python by barasingha(Sanjeev)"))
def help():
    tkinter.messagebox.showinfo("Help", "For help email to sanjeevkumarchintakindi@gmail.com", icon='question')

def show_info_bar():
    val = showinbar.get()
    if val:
        line_number_bar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    elif not val:
        line_number_bar.pack_forget()

def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add("active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)

def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event=None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()

def theme():
        global bgc,fgc
        val = themechoice.get()
        clrs = clrschms.get(val)
        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc
        content_text.config(bg=bgc, fg=fgc)

def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()

def show_cursor_info_bar():
    show_cursor_info_checked = showinbar.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right',anchor='se')
    else:
        cursor_info_bar.pack_forget()

def get_line_numbers():
    output = ''
    if showinbar.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i)+ '\n'
    return output

def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col)+1)
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file='icons/open_file.gif')
saveicon = PhotoImage(file='icons/Save.gif')
cuticon = PhotoImage(file='icons/Cut.gif')
copyicon = PhotoImage(file='icons/Copy.gif')
pasteicon = PhotoImage(file='icons/Paste.gif')
undoicon = PhotoImage(file='icons/Undo.gif')
redoicon = PhotoImage(file='icons/Redo.gif')
abouticon=PhotoImage(file='icons/about.gif')

shortcutbar = Frame(window, height=25)
icons = {'new_file':'new_file','open_file':'open_file','save_file':'save','cut':'Cut','copy':'Copy','paste':'Paste',"undo":'Undo','redo':'Redo',"find":'on_find',"about":'about'}
for f,icon in icons.items():
    tbicon = PhotoImage(file='icons/'+icons[f]+'.gif')
    cmd = eval(f)
    toolbar = Button(shortcutbar, image=tbicon,  command=cmd)
    toolbar.image = tbicon
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)


menubar = Menu(window)

content_text = Text(window, wrap='word',undo=1)
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-f>', find)
content_text.bind('<Control-F>', find)
content_text.bind('<Control-f>', find)
content_text.bind('<Control-F>', find)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-s>', save_file)
content_text.bind('<Control-S>', save_file)
content_text.bind('<Shift-Control-S>', save_as_file)
content_text.bind('<Shift-Control-s>', save_as_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-N>', new_file)
content_text.bind('<KeyPress-F1>', help)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.bind('<Button-3>', show_popup_menu)

file_menu = Menu(menubar,tearoff=0)
file_menu.add_command(label="New",accelerator='Ctrl+N',compound='left',image=newicon,underline=0,command=new_file)
file_menu.add_command(label="Open",accelerator='Ctrl+O',compound='left',image=openicon,underline=0,command=open_file)
file_menu.add_command(label="Save",accelerator='Ctrl+S',compound='left',image=saveicon,underline=0,command=save_file)
file_menu.add_command(label="Save As",accelerator='Shift+Ctrl+S',compound='left',image=saveicon,underline=0,command=save_as_file)
file_menu.add_command(label="Exit",accelerator='Alt+F4',compound='left',underline=0,command=quit)
menubar.add_cascade(label='File',menu=file_menu)

edit_menu=Menu(menubar,tearoff=0)
edit_menu.add_command(label="Cut",accelerator="Ctrl+X",compound='left',image=cuticon,underline=0,command=cut)
edit_menu.add_command(label="Copy",accelerator="Ctrl+C",compound='left',image=copyicon,underline=0,command=copy)
edit_menu.add_command(label="Paste",accelerator="Ctrl+V",compound='left',image=pasteicon,underline=0,command=paste)
edit_menu.add_command(label="Undo",accelerator="Ctrl+Z",compound='left',image=undoicon,underline=0,command=undo)
edit_menu.add_command(label="Redo",accelerator="Ctrl+Y",compound='left',image=redoicon,underline=0,command=redo)
edit_menu.add_command(label="Find",accelerator="Ctrl+F",compound='left',underline=0,command=find)
edit_menu.add_command(label="Select All",accelerator="Ctrl+A",compound='left',underline=7,command=select_all)
menubar.add_cascade(label="Edit",menu=edit_menu)

view_menu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="View", menu=view_menu)
showln = IntVar()
showln.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=showln)
showinbar = IntVar()
showinbar.set(1)
view_menu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
view_menu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=toggle_highlight)
themes_menu = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Themes", menu=themes_menu)
clrschms = {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey':'83406A.D1D4D1',
'3. Lovely Lavender':'202B4B.E1E1FF' ,
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Cobalt Blue':'ffffBB.3333aa',
'7. Olive Green': 'D1E7E0.5B8340',
}
themechoice= StringVar()
themechoice.set('1. Default White')
for k in sorted(clrschms):
    themes_menu.add_radiobutton(label=k, variable=themechoice, command=theme)

about_menu=Menu(menubar,tearoff=0)
about_menu.add_command(label="About",compound='left',underline=0,command=about,image=abouticon)
about_menu.add_command(label="Help",compound='left',underline=0,command=help)
menubar.add_cascade(label="About",menu=about_menu)

cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT,anchor='se')

shortcut_bar = Frame(window, height=25, background='light sea green')
shortcut_bar.pack(expand='no', fill='x')

line_number_bar = Text(window, width=4, padx=3, takefocus=0,border=0,background='khaki', state='disabled', wrap='none')
line_number_bar.pack(side='left', fill='y')

view_menu.add_checkbutton(label='Show Cursor Location at Bottom',variable=showinbar, command=show_cursor_info_bar)

popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
    popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7,command=select_all)

scroll_bary = Scrollbar(content_text)
scroll_bary.config(command=content_text.yview)
scroll_bary.pack(side='right', fill='y')

content_text.pack(expand='yes', fill='both')
content_text.configure(yscrollcommand=scroll_bary.set)

window.protocol('WM_DELETE_WINDOW',quit)
window.config(menu=menubar)
window.mainloop()
=======
from tkinter import *
import tkinter.filedialog
import os
import tkinter.messagebox as messagebox

file_name=None
PROGRAM_NAME="PyEditor"

window=Tk()
window.title("PyEditor")
window.iconbitmap('icons/pypad.ico')
w, h = window.winfo_screenwidth(),window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))

def quit():
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        window.destroy()

def new_file(event=None):
    window.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0,END)

def open_file(event=None):
    input_file_name=tkinter.filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if input_file_name:
        global file_name
        file_name=input_file_name
        window.title('{} - {}'.format(os.path.basename(file_name),PROGRAM_NAME))
        content_text.delete(1.0,END)
        with open(file_name) as f:
            content_text.insert(1.0,f.read())

def save_file(event=None):
    global file_name
    if not file_name:
        save_as_file()
    else:
        write_to_file(file_name)
    return "break"

def save_as_file(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name),PROGRAM_NAME))
    return "break"

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass

def cut():
    content_text.event_generate("<<Cut>>")

def copy():
    content_text.event_generate("<<Copy>>")

def paste():
    content_text.event_generate("<<Paste>>")

def undo():
    content_text.event_generate("<<Undo>>")

def redo(event=None):
    content_text.event_generate("<<Redo>>")
    return 'break'

def find(event=None):
    search_top_level=Toplevel(window)
    search_top_level.title("Find Text")
    search_top_level.transient(window)
    Label(search_top_level,text="Find All:").grid(row=0,column=0,sticky='e')
    search_entry_widget=Entry(search_top_level,width=25)
    search_entry_widget.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value=IntVar()
    Checkbutton(search_top_level, text='Ignore Case',variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_top_level,text="Find All",underline=0,command=lambda:search_output(search_entry_widget.get(),ignore_case_value.get(),content_text,search_top_level,search_entry_widget)).grid(row=2,column=2,sticky='e'+'w',padx=2,pady=2)
    def close_search_window():
        content_text.tag_remove('match','1.0',END)
        search_top_level.destroy()
        search_top_level.protocol('WM_DELETE_WINDOW',close_search_window)
        return 'break'

def search_output(needle,if_ignore_case,content_text,search_top_level,search_box):
    content_text.tag_remove('match','1.0',END)
    matches_found=0
    if needle:
        start_pos='1.0'
        while True:
            start_pos=content_text.search(needle,start_pos,nocase=if_ignore_case,stopindex=END)
            if not start_pos:
                break
            end_pos='{}+{}c'.format(start_pos,len(needle))
            content_text.tag_add('match',start_pos,end_pos)
            matches_found+=1
            start_pos=end_pos
            content_text.tag_config('match',foreground='red',background='yellow')
            search_box.focus_set()
            search_top_level.title('{} matches found'.format(matches_found))

def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return "break"

def about():
    tkinter.messagebox.showinfo("About", "{}{}".format(PROGRAM_NAME, "\nThis is a Text Editor developed in Python by barasingha"))

def help():
    tkinter.messagebox.showinfo("Help", "For help email to sanjeevkumarchintakindi@gmail.com", icon='question')

def show_info_bar():
    val = showinbar.get()
    if val:
        line_number_bar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    elif not val:
        line_number_bar.pack_forget()

def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add("active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)

def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event=None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()

def theme():
        global bgc,fgc
        val = themechoice.get()
        clrs = clrschms.get(val)
        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc
        content_text.config(bg=bgc, fg=fgc)

def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()

def show_cursor_info_bar():
    show_cursor_info_checked = showinbar.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right',anchor='se')
    else:
        cursor_info_bar.pack_forget()

def get_line_numbers():
    output = ''
    if showinbar.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i)+ '\n'
    return output

def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col)+1)
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file='icons/open_file.gif')
saveicon = PhotoImage(file='icons/Save.gif')
cuticon = PhotoImage(file='icons/Cut.gif')
copyicon = PhotoImage(file='icons/Copy.gif')
pasteicon = PhotoImage(file='icons/Paste.gif')
undoicon = PhotoImage(file='icons/Undo.gif')
redoicon = PhotoImage(file='icons/Redo.gif')
abouticon=PhotoImage(file='icons/about.gif')

shortcutbar = Frame(window, height=25)
icons = {'new_file':'new_file','open_file':'open_file','save_file':'save','cut':'Cut','copy':'Copy','paste':'Paste',"undo":'Undo','redo':'Redo',"find":'on_find',"about":'about'}
for f,icon in icons.items():
    tbicon = PhotoImage(file='icons/'+icons[f]+'.gif')
    cmd = eval(f)
    toolbar = Button(shortcutbar, image=tbicon,  command=cmd)
    toolbar.image = tbicon
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)


menubar = Menu(window)

content_text = Text(window, wrap='word',undo=1)
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-f>', find)
content_text.bind('<Control-F>', find)
content_text.bind('<Control-f>', find)
content_text.bind('<Control-F>', find)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-s>', save_file)
content_text.bind('<Control-S>', save_file)
content_text.bind('<Shift-Control-S>', save_as_file)
content_text.bind('<Shift-Control-s>', save_as_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-N>', new_file)
content_text.bind('<KeyPress-F1>', help)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.bind('<Button-3>', show_popup_menu)

file_menu = Menu(menubar,tearoff=0)
file_menu.add_command(label="New",accelerator='Ctrl+N',compound='left',image=newicon,underline=0,command=new_file)
file_menu.add_command(label="Open",accelerator='Ctrl+O',compound='left',image=openicon,underline=0,command=open_file)
file_menu.add_command(label="Save",accelerator='Ctrl+S',compound='left',image=saveicon,underline=0,command=save_file)
file_menu.add_command(label="Save As",accelerator='Shift+Ctrl+S',compound='left',image=saveicon,underline=0,command=save_as_file)
file_menu.add_command(label="Exit",accelerator='Alt+F4',compound='left',underline=0,command=quit)
menubar.add_cascade(label='File',menu=file_menu)

edit_menu=Menu(menubar,tearoff=0)
edit_menu.add_command(label="Cut",accelerator="Ctrl+X",compound='left',image=cuticon,underline=0,command=cut)
edit_menu.add_command(label="Copy",accelerator="Ctrl+C",compound='left',image=copyicon,underline=0,command=copy)
edit_menu.add_command(label="Paste",accelerator="Ctrl+V",compound='left',image=pasteicon,underline=0,command=paste)
edit_menu.add_command(label="Undo",accelerator="Ctrl+Z",compound='left',image=undoicon,underline=0,command=undo)
edit_menu.add_command(label="Redo",accelerator="Ctrl+Y",compound='left',image=redoicon,underline=0,command=redo)
edit_menu.add_command(label="Find",accelerator="Ctrl+F",compound='left',underline=0,command=find)
edit_menu.add_command(label="Select All",accelerator="Ctrl+A",compound='left',underline=7,command=select_all)
menubar.add_cascade(label="Edit",menu=edit_menu)

view_menu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="View", menu=view_menu)
showln = IntVar()
showln.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=showln)
showinbar = IntVar()
showinbar.set(1)
view_menu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
view_menu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=toggle_highlight)
themes_menu = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Themes", menu=themes_menu)
clrschms = {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey':'83406A.D1D4D1',
'3. Lovely Lavender':'202B4B.E1E1FF' ,
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Cobalt Blue':'ffffBB.3333aa',
'7. Olive Green': 'D1E7E0.5B8340',
}
themechoice= StringVar()
themechoice.set('1. Default White')
for k in sorted(clrschms):
    themes_menu.add_radiobutton(label=k, variable=themechoice, command=theme)

about_menu=Menu(menubar,tearoff=0)
about_menu.add_command(label="About",compound='left',underline=0,command=about,image=abouticon)
about_menu.add_command(label="Help",compound='left',underline=0,command=help)
menubar.add_cascade(label="About",menu=about_menu)

cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT,anchor='se')

shortcut_bar = Frame(window, height=25, background='light sea green')
shortcut_bar.pack(expand='no', fill='x')

line_number_bar = Text(window, width=4, padx=3, takefocus=0,border=0,background='khaki', state='disabled', wrap='none')
line_number_bar.pack(side='left', fill='y')

view_menu.add_checkbutton(label='Show Cursor Location at Bottom',variable=showinbar, command=show_cursor_info_bar)

popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
    popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7,command=select_all)

scroll_bary = Scrollbar(content_text)
scroll_bary.config(command=content_text.yview)
scroll_bary.pack(side='right', fill='y')

content_text.pack(expand='yes', fill='both')
content_text.configure(yscrollcommand=scroll_bary.set)

window.protocol('WM_DELETE_WINDOW',quit)
window.config(menu=menubar)
window.mainloop()
>>>>>>> ae3ff231d9368fc63948b02f936367b639644b10
