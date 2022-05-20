from tkinter import Label
from scripts.gui import *
from scripts.config import *


program_info = {
    'name': 'Criador de Edital',
    'version': '1205.22'
}

PROGRAM_NAME = F'{program_info["name"]} ({program_info["version"]})'


types = (
    'Registro de Preços',
    'Simples Aquisição',
    'Engenharia',
    'Tecnologia da Informação',
    'Dedicação de Mão de Obra',
    'Concorrência'
)


############


def create_docs(types: str, entries: dict) -> bool:
    entries['Tipo'] = types

    match types:
        case 'Registro de Preços':
            from scripts.price_register.create import create_price_record
            create_price_record(entries)

        case _:
            return False
    return True

######

def load_main_screen(delete=None):
    if delete is not None:
        delete.destroy()

    from scripts.gui import Interface
    main = Interface(PROGRAM_NAME, 424, 264, 0)

    Label(main, text='Tipo').grid(pady=(20, 0), padx=(85, 0))
    docs_type = main.create_combobox(
        values=types,
        col=0, row=1,
        padx=(85, 0),
        pady=(5, 5)
    )

    main.row = 3
    main.create_switch(
        padx=(85, 0), pady=(15, 10)
    )

    main.row, main.col = 4, 0
    main.create_button(
        name='Confirmar',
        cmd=lambda: load_second_screen(docs_type.get(), main),
        padx=(85, 0), pady=(25, 0)
    )

    main.mainloop()

######


def load_second_screen(types: str, delete=None):
    match types:
        case 'Registro de Preços':
            from scripts.price_register.inputs import load_price_record

            if delete is not None:
                delete.destroy()

            load_price_record(PROGRAM_NAME)

        case _:
            show_message('(Erro) Não existe nenhuma configuração disponível para esse tipo!')
            return False


############


if __name__ == '__main__':
    load_main_screen()
        