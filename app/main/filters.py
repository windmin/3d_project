def peixian_danyuan(s):
    if isinstance(s, int):
        s = str(s)
    PEIXIAN_DANYUAN = {
        '1': '12',
        '2': '11',
        '3': '10',
        '4': '9',
        '5': '8',
        '6': '7',
        '7': '6',
        '8': '5',
        '9': '4',
        '10': '3',
        '11': '2',
        '12': '1'
    }
    return PEIXIAN_DANYUAN[s]