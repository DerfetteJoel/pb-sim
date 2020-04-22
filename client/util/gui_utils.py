TYPE_COLORS = {
    'normal': '#a8a87e',
    'fighting': '#b23c31',
    'flying': '#a493ea',
    'poison': '#95499c',
    'ground': '#dcc075',
    'rock': '#b5a04b',
    'bug': '#acb642',
    'ghost': '#6c5b94',
    'steel': '#b8b9ce',
    'fire': '#e25844',
    'water': '#6f92e9',
    'grass': '#8bc561',
    'electric': '#f2d054',
    'psychic': '#e66488',
    'ice': '#a6d7d7',
    'dragon': '#6745ef',
    'dark': '#6d594a',
    'fairy': '#e29dac',
    '???': '#759f91'
}

DAMAGE_CATEGORY_COLORS = {
    'physical': '#b93423',
    'special': '#51586e',
    'status': '#8c888c'
}


def get_stat_color(stat: int):
    if stat < 30:
        return "#e30000"
    elif 30 <= stat < 50:
        return "#e34400"
    elif 50 <= stat < 70:
        return "#e38100"
    elif 70 <= stat < 90:
        return "#ffd119"
    elif 90 <= stat < 110:
        return "#d3f000"
    elif 110 <= stat < 130:
        return "#b1ff1f"
    elif 130 <= stat < 150:
        return "#5eff19"
    elif 150 <= stat < 170:
        return "#19ff88"
    elif 170 <= stat < 190:
        return "#19ffc9"
    else:
        return "#19fffb"
