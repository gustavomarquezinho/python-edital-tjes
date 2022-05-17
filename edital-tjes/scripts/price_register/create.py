"""
-> Realiza as devidas alterações no documento utilizando as entradas informadas.
"""


from .checks import Checks
from .outputs import *
from scripts.docs import Docs


def create_price_record(entries: dict) -> bool:
    checks = Checks(entries)

    if not checks.status:
        return False

    outputs = Outputs(
        checks.entries,
        checks.exclusives
    )

    docx = Docs(F'./edital-tjes/data/registro-de-preços/Registro de Preços ({outputs.get_docs_type()}).docx')

    if not docx.load_file():
        return False

    replace_a = {
        '#PROCESSO':
            entries['Processo'],

        '#ITEM':
            entries['Objeto'],

        '#VALOR':
            outputs.get_full_value(),

        '#LICITAÇÃO':
            entries['Licitação'].upper(),

        '#REQUISITOS':
            outputs.get_requirements(),

        '#OBSERVAÇÃO':
            outputs.get_observation()
    }
    replace_b = {
        '#ATO_NORMATIVO':
            get_normative(),

        '#EXCLUSIVO_A':
            outputs.get_exclusive_a(),

        '#EXCLUSIVO_B':
            outputs.get_exclusive_b(),
    }
    replace_c = {
        '#JULGAMENTO_A':
            outputs.get_judgment_a(),

        '#JULGAMENTO_B':
            outputs.get_judgment_b(),

        '#JULGAMENTO_C':
            outputs.get_judgment_c(),

        '#JULGAMENTO_D':
            outputs.get_judgment_d(),

        '#JULGAMENTO_E':
            outputs.get_judgment_e(),

        '#JULGAMENTO_F':
            outputs.get_judgment_f(),

        '#JULGAMENTO_G':
            outputs.get_judgment_g(),
    }
    replace_d = {
        '#INTERESSADOS_A':
            outputs.get_interested_a(),

        '#INTERESSADOS_B':
            outputs.get_interested_b(),
    }
    
    if outputs.get_docs_type() == 'Misto':
        replace_b.update({
            '#EXCLUSIVO_C': outputs.get_exclusive_c(),
            '#EXCLUSIVO_D': outputs.get_exclusive_d(),
        })

    docx.loop_docs({**replace_a, **replace_b, **replace_c, **replace_d})
    
    status_save = docx.save_file(
        F'Registro de Preços de {entries["Objeto"].title()} ({entries["Processo"]})'
    )
    return status_save
