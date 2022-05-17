"""
-> Realiza as devidas verificações em dados informados pelo usuário.
"""


from .outputs import get_monetary_value, get_only_numbers
from scripts.gui import show_message


class Checks:
    def __init__(self, entries) -> None:
        self.entries = entries
        self.exclusives = []

        self.status = self.is_valid_entries()

    ######

    def is_valid_entries(self) -> bool:
        if not self.is_valid_process():
            return False

        if not self.is_valid_item():
            return False

        if not self.is_valid_value():
            return False

        if not self.is_valid_licitation():
            return False

        if not self.is_valid_quantity():
            return False

        if not self.is_valid_exclusive():
            return False

        if not self.is_valid_requirements():
            return False
    
        if not self.is_valid_observation():
            return False
        return True

    ############

    def is_valid_process(self) -> bool:
        if (process := self.entries.get('Processo')) is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Processo'!")
            return False

        if len(process) == 0:
            show_message('(Aviso) Você deve inserir um processo válido!')
            return False
        return True

    ######

    def is_valid_item(self) -> bool:
        if (item := self.entries.get('Objeto')) is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Objeto'!")
            return False

        if len(item) == 0:
            show_message('(Aviso) Você deve inserir um objeto válido!')
            return False
        return True

    ######

    def is_valid_value(self) -> bool:
        if (value := self.entries.get('Valor')) is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Valor'!")
            return False

        cedules, cents = get_monetary_value(value)

        if len(value) == 0 or (cedules == 0 and cents == 0):
            show_message('(Aviso) Você deve inserir um valor estimado válido!')
            return False
        return True

    ######

    def is_valid_licitation(self) -> bool:
        if (values := self.entries.get('Licitação e Julgamento')) is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Licitação e Julgamento'!")
            return False

        self.entries['Licitação'] = 'Item' if values.title().find('Item') else 'Lote'
        self.entries['Julgamento'] = values
        return True

    ######

    def is_valid_quantity(self) -> bool:
        if (quantity := self.entries.get('Quantidade')) is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Quantidade'!")
            return False

        if not quantity.isdigit() or int(quantity) <= 0:
            show_message('(Aviso) Você deve inserir uma quantidade válida de itens ou lotes!')
            return False
        return True

    ######

    def is_valid_exclusive(self) -> bool:
        if (exclusives := self.entries.get('Exclusivos')) is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Exclusivos'!")
            return False

        if len(exclusives) >= 1:
            self.exclusives = get_only_numbers(exclusives)

        if (length_exclusive := len(self.exclusives)) == 0 and len(exclusives) >= 1:
            show_message('(Aviso) Nenhum valor numérico foi encontrado em Exclusivos!')
            return False

        if length_exclusive == 0:
            return True

        if 0 in self.exclusives:
            show_message('(Aviso) Número zero não é permitido no campo de exclusivos!')
            return False

        if length_exclusive != len(set(self.exclusives)):
            show_message('(Aviso) Valores repetidos não são permitidos no campo de exclusivos!')
            return False

        if length_exclusive > int(self.entries['Quantidade']):
            show_message('(Aviso) Quantidade de exclusivos não pode exceder a quantidade total!')
            return False

        if max(self.exclusives) > int(self.entries['Quantidade']):
            show_message('(Aviso) Nenhum valor exclusivo pode exceder a quantidade total!')
            return False
        return True

    ######

    def is_valid_requirements(self) -> bool:
        if self.entries.get('Requisitos') is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Requisitos'!")
            return False
        return True

    ######

    def is_valid_observation(self) -> bool:
        if self.entries.get('Observação') is None:
            show_message("(Erro) Falha ao obter o valor da chave 'Observação'!")
            return False
        return True
