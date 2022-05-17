"""
-> Obtêm as devidas saídas à serem escritas no documento.
"""


from scripts.gui import show_message

from num2words import (
    num2words as num_to_words
)


judgments = (
    'Menor valor unitário do item',
    'Menor valor total do item',
    'Menor valor total do lote',
    'Menor valor total dos itens do lote'
)


class Outputs:
    def __init__(self, entries, exclusives):
        self.entries = entries

        self.exclusives = exclusives
        self.judgments = judgments

        self.judgments_index = self.judgments.index(self.entries['Julgamento'])
     
    ######

    def get_docs_type(self) -> str:
        if len(self.exclusives) == 0:
            return 'Não Exclusivo'
        
        if len(self.exclusives) >= int(self.entries['Quantidade']):
            return 'Exclusivo'
        return 'Misto'

    ############

    def get_exclusive_a(self) -> str:
        match self.get_docs_type():
            case 'Exclusivo':
                return 'SIM'
    
            case 'Não Exclusivo':
                return 'NÃO'

            case _:
                return F'SIM, para o {self.entries["Licitação"].upper()} {str(self.exclusives)[1:-1]}'

    def get_exclusive_b(self) -> str:
        if self.get_docs_type() == 'Não Exclusivo':
            return ''

        exclusive = str(self.exclusives)[1:-1]
        return F'MICROEMPRESAS E EMPRESAS DE PEQUENO PORTE PARA O(S) {self.entries["Licitação"].upper()}(S) {exclusive}'

    def get_exclusive_c(self) -> str:
        return F'{self.entries["Licitação"].upper()}(S) {str(self.exclusives)[1:-1]}'

    def get_exclusive_d(self) -> str:
        if int(self.entries['Quantidade']) - len(self.exclusives) > 1:
            return 'PARA OS DEMAIS'

        not_exclusives = \
            [(i + 1) for i in range(int(self.entries['Quantidade']))]

        return F'PARA O {self.entries["Licitação"].upper()} {str(set(not_exclusives) ^ set(self.exclusives))[1:-1]}'

    ######

    def get_observation(self) -> str:
        if len(self.entries['Observação']) == 0:
            return '1) Não há.'
        
        return self.entries['Observação']

    def get_requirements(self) -> str:
        if len(self.entries['Requisitos']) == 0:
            return '1) Não há.'
        
        return self.entries['Requisitos']

    ######

    def get_interested_a(self) -> str:
        if self.get_exclusive_a() == 'SIM':
            return 'microempresas e empresas de pequeno porte'
        return 'empresas'

    def get_interested_b(self) -> str:
        if self.get_exclusive_a() == 'SIM':
            return 'microempresas e empresas de pequeno porte'
        return 'interessados'

    ######

    def get_judgment_a(self) -> str:
        return self.entries['Julgamento']

    def get_judgment_b(self) -> str:
        return self.entries['Julgamento'].upper()

    def get_judgment_c(self) -> str:
        values = (
            'Por cada item',
            'Pelo total do item',
            'Pelo lote',
            'Itens de cada lote',
        )
        return values[self.judgments_index].lower()

    def get_judgment_d(self) -> str:
        values = (
            'Valor unitário do item',
            'Valor total do item',
            'Valor total do lote',
            'Valor total dos itens do(s) lote(s)'
        )
        return values[self.judgments_index].lower()

    def get_judgment_e(self) -> str:
        values = (
            'Item',
            'Pelo total do item',
            'Lote',
            'Item do lote'
        )
        return values[self.judgments_index].upper()

    def get_judgment_f(self) -> str:
        values = (
            'Com valor unitário e total do item/itens',
            'Com valor unitário e total do item/itens',
            'Com valor unitário, total do item/itens e total do lote',
            'Com valor unitário, total dos itens e total do(s) lote(s)'
        )
        return values[self.judgments_index].lower()

    def get_judgment_g(self) -> str:
        values = (
            'Menor valor unitário do item',
            'Menor valor total do item',
            'Menor valor total do lote',
            'Menor valor total do lote'
        )
        return values[self.judgments_index].lower()

    ######

    def get_full_value(self):
        cedules, cents = get_monetary_value(string := self.entries['Valor'])

        if cents <= 0:
            return F'{string} ({num_to_words(cedules, lang="pt")} reais)'

        return F'{string} ({num_to_words(cedules, lang="pt")} reais e {num_to_words(cents, lang="pt")} centavos)'


############


def get_monetary_value(string: str):
    cedules, cents, found_cents = '0', '0', False

    for char in string:
        if char == ',':
            found_cents = True

        if char.isdigit():
            if found_cents:
                cents += char
                continue

            cedules += char

    cedules, cents = int(cedules), int(cents)
    return cedules, cents

######

def get_only_numbers(values):
    numbers, index = [], 0

    while index < len(values):
        if values[index].isdigit():
            begin = index

            while (index + 1) < len(values) and values[index + 1].isdigit():
                index += 1

            numbers.append(int(values[begin:index + 1]))

        index += 1

    numbers.sort()
    return numbers

######

def get_normative():
    try:
        with open('./edital-tjes/data/ato-normativo.log', 'r') as file:
            normative = file.readline()

            if len(normative) == 0:
                raise FileNotFoundError

    except (FileNotFoundError, PermissionError):
        show_message('Arquivo do Ato Normativo não encontrado (Mensagem padrão 041/2022 inserida).')

        normative = 'Ato Normativo de designação dos Pregoeiros e Equipes de Apoio nº 041/2022, ' \
                    'disponibilizado no Diário da Justiça eletrônico no dia de 26/04/2022'
    return normative
