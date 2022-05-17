from tika import parser


info_raw = parser.from_file('./data/Planilha.pdf')
splitted = info_raw['content'].strip().splitlines()


def get_fields():
    process = ''

    for word in splitted:
        if search_process(word):
            process = word

    return process


def search_process(word: str) -> bool:
    filters = 0
    
    if 20 < len(word) < 30:
        filters += 1

    if word.count('.') == 4:
        filters += 1

    return filters >= 2


print(get_fields())
