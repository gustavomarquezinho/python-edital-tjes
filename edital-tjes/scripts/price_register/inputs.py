"""
-> Exibe para o usuário todos os campos necessários para a criação do Registro de Preços.
"""


from scripts.gui import Interface

from main import (
    create_docs, load_main_screen
)


infos = {
    'Número do Processo':
        'Insira o número do processo presente na ...',

    'Exclusivos (Opcional)':
        'Insira os itens ou lotes exclusivos caso haja, separando-os por vírgula.',
}


def load_price_record(title):
    from .outputs import judgments

    gui = Interface(title, 664, 620, 1)

    ############

    gui.label_with_input(
        style='Entry',
        name='Número do Processo',
        key='Processo',
        values='0000000-00.0000.0.00.0000'
    )

    gui.label_with_input(
        style='Entry',
        name='Objeto da Licitação',
        key='Objeto',
        values=''
    )

    ######

    gui.label_with_input(
        style='Entry',
        name='Valor Total Estimado',
        key='Valor',
        values='R$000.000,00'
    )

    ######

    gui.label_with_input(
        style='Combobox',
        name='Licitação e Julgamento',
        key='Licitação e Julgamento',
        values=judgments
    )

    gui.label_with_input(
        style='Entry',
        name='Quantidade de Itens ou Lotes',
        key='Quantidade',
        values=''
    )
    gui.label_with_input(
        style='Entry',
        name='Exclusivos (Opcional)',
        key='Exclusivos',
        info=infos['Exclusivos (Opcional)'],
        values=''
    )

    ######

    gui.label_with_input(
        style='Textbox',
        name='Requisitos (Opcional)',
        key='Requisitos'
    )
    gui.label_with_input(
        style='Textbox',
        name='Observação (Opcional)',
        key='Observação'
    )

    ######

    gui.create_button(
        name='Gerar',
        cmd=lambda: create_docs('Registro de Preços', gui.get_entries())
    )

    gui.create_button(
        name='Voltar',
        cmd=lambda: load_main_screen(gui)
    )

    ############

    gui.mainloop()
