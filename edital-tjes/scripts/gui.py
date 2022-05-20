"""
-> Módulo que possibilita criar todos os itens necessários para a interface.
"""


from .config import load_color_scheme, save_color_scheme
from main import PROGRAM_NAME


from tkinter import (
    BooleanVar, Tk, Text, StringVar, PhotoImage, END
)

from tkinter.ttk import (
    Frame, Label, Entry, Combobox, Button, Checkbutton
)

color_scheme = {
    True: 'dark',
    False: 'light'
}


class Interface(Tk):
    def __init__(self, title: str, xsize: int, ysize: int, layer: int) -> None:
        super().__init__()

        self.entries = {}
        self.description = None

        self.padx = (50, 25)
        self.col = 0
        self.row = 0

        self.color = load_color_scheme()
        self.default_var = BooleanVar(value=self.color)

        self.load_style(title, xsize, ysize)

        if layer != 0:
            self.protocol('WM_DELETE_WINDOW', \
                lambda: show_message('Você realmente deseja sair do programa?', options=2, forms=self))

        self.iconphoto(False, PhotoImage(file='./edital-tjes/assets/icon_small.png', master=self))

    ######

    def load_style(self, title: str, xsize: int, ysize: int) -> None:
        self.tk.call('source', './edital-tjes/assets/Azure Theme 2.1.0/azure.tcl')
        self.tk.call('set_theme', color_scheme[self.color])

        self.resizable(False, False)
        self.title(title)

        xpos = (self.winfo_screenwidth() / 2) - (xsize / 2)
        ypos = (self.winfo_screenheight() / 2) - (ysize / 2)

        self.geometry(F'{xsize}x{ysize}+{int(xpos)}+{int(ypos)}')

    ############

    def label_with_input(self, style: str, name: str, key: str, info: str = '', values: tuple or str = ()) -> bool:
        Label(
            self,
            text=name,
            padding=(5, 0, 0, 0)
        ).grid(column=self.col, row=self.row, padx=self.padx, pady=(20 if self.row else 40, 0), sticky='W')

        match style:
            case 'Entry':
                self.entries[key] = self.create_entry(values, info, self.col, self.row)

            case 'Combobox':
                self.entries[key] = self.create_combobox(values, self.col, self.row, self.padx)
            
            case 'Textbox':
                self.entries[key] = self.create_textbox(self.col, self.row)

            case _:
                return False

        if self.col == 0 and self.row == 0:
            self.focus_force()
            self.entries[key].focus()

        self.position(2)
        return True

    ######

    def create_entry(self, value: str, info: str, col: int, row: int) -> Entry:
        entry = Entry(
            self, width=34,
            justify='center',
        )

        entry.grid(column=col, row=row+1, padx=self.padx, ipady=4)
        entry.insert(0, value)

        entry.bind('<FocusIn>', lambda bind, phrase=info: self.show_field_description(phrase))
        return entry

    ######

    def create_combobox(self, values: tuple, col: int, row: int, padx: tuple, **kwargs) -> Combobox:
        combobox = Combobox(
            self, width=34,
            state='readonly',
            justify='center',
            values=values
        )

        combobox.grid(column=col, row=row+1, padx=padx, ipady=4, **kwargs)
        combobox.set(values[0])
        return combobox

    ######

    def create_textbox(self, col: int, row: int) -> Text:
        frame = Frame(
            self,
            style='Card.TFrame',
            padding=(5, 5, 5, 5),
        )
        frame.grid(column=col, row=row+1, padx=self.padx, pady=(0, 0))

        textbox = Text(
            frame, width=40, height=10,
            font=('Segoe UI', 9),
            relief='flat',
        )
        textbox.grid(column=col, row=row+1, padx=(0, 0), pady=(0, 0))
        return textbox

    ######

    def create_button(self, name: str, cmd, pady=(40, 00), **kwargs) -> None:
        button = Button(
            self,
            text=name,
            command=cmd
        )

        button.grid(column=self.col, row=self.row, pady=pady, ipadx=10, ipady=10, **kwargs)
        self.position(1)

    ######

    def create_switch(self, padx: tuple, pady: tuple) -> None:
        switch = Checkbutton(self, text='Modo Escuro', variable=self.default_var, style='Switch.TCheckbutton', command=self.change_color)
        switch.grid(column=self.col, row=self.row, padx=padx, pady=pady)

        self.position(1)

    ######

    def position(self, rows):
        self.col = not self.col

        if not self.col:
            self.row += rows

        self.padx = (50, 25) if self.col == 0 else (25, 50)

    ######

    def get_entries(self) -> dict:
        entries = dict.fromkeys(self.entries.keys(), '')

        for key in self.entries:
            if isinstance(self.entries[key], Text):
                entries[key] = self.entries[key].get('1.0', END).replace('\n', '')
                continue
            
            entries[key] = self.entries[key].get()

        return entries

    ######

    def change_color(self):
        self.color = not self.color
        self.tk.call('set_theme', color_scheme[self.color])

        save_color_scheme(str(self.color))

    ######

    def show_field_description(self, phrase):        
        if self.description is None:
            self.description = StringVar()

            label = Label(self, text=phrase, textvariable=self.description)
            label.grid(column=0, pady=(15, 0), columnspan=2)
            return
            
        self.description.set(phrase)


pop_up = None

def show_message(message: str, options: int = 1, forms=None) -> None:
    global pop_up
    delete_message()

    pop_up = Interface(PROGRAM_NAME, 320, 140 + (20 if len(message) > 44 else 0), 2)

    Label(
        pop_up,
        text=message,
        justify='center',
        wraplength=280,
    ).pack(expand=False, pady=(25, 0))

    ######

    if options <= 1:
        Button(
            pop_up,
            text='Fechar',
            command=delete_message
        ).pack(expand=False, pady=(25, 0), ipady=4)

    else:

        Button(
            pop_up,
            text='Sim',
            command=lambda: delete_message(forms)
        ).pack(expand=False, padx=(50, 15), ipady=2, side='left')

        Button(
            pop_up,
            text='Não',
            command=delete_message
        ).pack(expand=False, padx=(15, 50), ipady=2, side='left')

    pop_up.protocol('WM_DELETE', delete_message)
    pop_up.bell()

    pop_up.focus_force()
    pop_up.mainloop()

######

def delete_message(window=None):
    global pop_up

    if pop_up is not None:
        pop_up.destroy()
        pop_up = None

    if window is not None:
        window.destroy()
