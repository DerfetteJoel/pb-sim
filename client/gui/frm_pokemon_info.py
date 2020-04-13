import os
import ssl
from urllib import request
from urllib.error import HTTPError
from operator import itemgetter

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from api import pokemon
from api.move import Move
from api.util import io_utils, utils

pk_path = os.path.join(io_utils.root_dir, 'data', 'sprites', '0.png')


def launch():
    app = QApplication([])
    QFontDatabase.addApplicationFont(os.path.join(io_utils.root_dir, 'data', 'assets', 'fonts', 'Roboto-Regular.ttf'))
    QFontDatabase.addApplicationFont(os.path.join(io_utils.root_dir, 'data', 'assets', 'fonts', 'Roboto-Bold.ttf'))
    app.setStyle('Fusion')
    app.setFont(QFont('Roboto', 14))
    frm = FrmPokemonInfo()
    app.exec()


class FrmPokemonInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.pokemon_data = pokemon.pokemon_data

        self.is_image_shiny = False

        # COMPONENT LIST
        self.window = QWidget()
        self.grid = QGridLayout()
        self.lb_cb_desc = QLabel('Select a Pokemon: ')
        self.lb_bt_desc = QLabel('or')
        self.lb_move_desc = QLabel('Learnable moves: ')
        self.bt_add_pokemon = QPushButton('Create a new Pokemon')
        self.cb_pokemon = QComboBox()
        self.lb_pokemon_name = QLabel()
        self.lb_image = QLabel()
        self.pokemon_view = QVBoxLayout()
        self.bt_shiny = QPushButton('Toggle Shiny')
        self.stat_info_group = QVBoxLayout()
        self.stat_info_rows = []
        self.lb_stat_names = []
        self.stat_bars = []
        self.lb_stat_values = []
        self.type_group = QHBoxLayout()
        self.type_1 = QLabel()
        self.type_2 = QLabel()
        self.table_moves = QTableWidget()
        # END OF COMPONENT LIST

        self.init_ui()
        self.window.show()

    def init_ui(self):
        self.window.setLayout(self.grid)

        self.grid.setVerticalSpacing(20)

        self.lb_move_desc.setAlignment(Qt.AlignBottom |Qt.AlignLeft)

        self.bt_add_pokemon.setEnabled(False)

        self.cb_pokemon.addItem('')
        for key in self.pokemon_data:
            self.cb_pokemon.addItem(self.pokemon_data[key]['name'])
        self.cb_pokemon.setEditable(True)

        self.lb_pokemon_name.setText(self.cb_pokemon.currentText().split('-')[0].title())
        self.lb_pokemon_name.setStyleSheet('font-size: 24pt; font: bold;')
        self.lb_pokemon_name.setAlignment(Qt.AlignCenter)
        self.lb_pokemon_name.setMinimumWidth(150)

        pixmap = QPixmap(pk_path)
        self.lb_image.setPixmap(pixmap)
        self.lb_image.setAlignment(Qt.AlignCenter)
        self.lb_image.setStyleSheet('border: 1px solid gray;'
                                    'border-radius: 5px;'
                                    'margin: 10px;'
                                    'background: #fafafa')

        stat_names = ['HP', 'Atk', 'Def', 'SpAtk', 'SpDef', 'Spe']
        for i in range(0, 6):
            self.stat_info_rows.append(QHBoxLayout())
            self.lb_stat_names.append(QLabel())
            self.lb_stat_names[i].setText(stat_names[i])
            self.lb_stat_names[i].setFixedWidth(70)
            self.lb_stat_names[i].setAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.lb_stat_names[i].setStyleSheet('margin: 5px;')

            self.stat_bars.append(QProgressBar())
            self.stat_bars[i].setRange(0, 255)
            self.stat_bars[i].setMinimumSize(255, 30)
            self.stat_bars[i].setTextVisible(False)
            self.stat_bars[i].setValue(0)

            self.lb_stat_values.append(QLabel(''))
            self.lb_stat_values[i].setFixedWidth(40)
            self.lb_stat_values[i].setAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.lb_stat_values[i].setUpdatesEnabled(True)

            self.stat_info_rows[i].addWidget(self.lb_stat_names[i])
            self.stat_info_rows[i].addWidget(self.stat_bars[i])
            self.stat_info_rows[i].addWidget(self.lb_stat_values[i])
            self.stat_info_group.addLayout(self.stat_info_rows[i])

        self.type_1.setFixedSize(70, 20)
        self.type_2.setFixedSize(70, 20)
        self.type_1.setAlignment(Qt.AlignCenter)
        self.type_2.setAlignment(Qt.AlignCenter)
        self.type_group.addWidget(self.type_1)
        self.type_group.addWidget(self.type_2)

        self.pokemon_view.addWidget(self.lb_image)
        self.pokemon_view.addWidget(self.bt_shiny)

        self.table_moves.setAlternatingRowColors(True)
        self.table_moves.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_moves.setCornerButtonEnabled(False)
        self.table_moves.setShowGrid(False)
        self.table_moves.horizontalHeader().hide()
        self.table_moves.verticalHeader().hide()
        self.table_moves.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_moves.setFixedWidth(340)

        self.cb_pokemon.currentIndexChanged.connect(lambda: self.on_pokemon_selected())
        self.bt_shiny.pressed.connect(lambda: self.on_shiny_toggle_pressed())

        self.grid.addWidget(self.lb_cb_desc, 0, 0)
        self.grid.addWidget(self.cb_pokemon, 0, 2)
        self.grid.addWidget(self.lb_bt_desc, 0, 3)
        self.grid.addWidget(self.bt_add_pokemon, 0, 4)
        self.grid.addWidget(self.lb_pokemon_name, 1, 2)
        self.grid.addLayout(self.type_group, 1, 0)
        self.grid.addWidget(self.lb_move_desc, 1, 4)
        self.grid.addLayout(self.pokemon_view, 2, 0)
        self.grid.addLayout(self.stat_info_group, 2, 2)
        self.grid.addWidget(self.table_moves, 2, 4)

    def on_pokemon_selected(self):
        try:
            raw_data = self.pokemon_data[self.cb_pokemon.currentText()]
        except KeyError:
            return
        self.is_image_shiny = not self.is_image_shiny
        self.on_shiny_toggle_pressed()
        self.lb_pokemon_name.setText(self.cb_pokemon.currentText().split('-')[0].title())
        self.type_1.setText(raw_data['types']['type_1'].capitalize())
        self.type_1.setStyleSheet(f'color: white;'
                                  f'background-color: {utils.TYPE_COLORS.get(self.type_1.text().lower())};'
                                  f'border-radius: 10px')
        type_2_data = raw_data['types']['type_2']
        if type_2_data != 'none':
            self.type_2.setText(type_2_data.capitalize())
        else:
            self.type_2.setText('')
        self.type_2.setStyleSheet(f'color: white;'
                                  f'background-color: {utils.TYPE_COLORS.get(self.type_2.text().lower())};'
                                  f'border-radius: 10px')
        for i in range(0, 6):
            self.stat_bars[i].setValue(raw_data['base_stats'][i])
            self.lb_stat_values[i].setText(str(raw_data['base_stats'][i]))
        self.table_moves.clear()
        self.table_moves.setRowCount(len(raw_data['moves']))
        self.table_moves.setColumnCount(3)
        self.table_moves.setColumnWidth(0, 70)
        self.table_moves.setColumnWidth(1, 160)
        self.table_moves.setColumnWidth(2, 90)

        move_data = raw_data['moves']
        move_data.sort(key=itemgetter('level_learned_at'))
        move_data.sort(key=itemgetter('learn_method'))
        for i in range(0, len(raw_data['moves'])):
            move = Move(move_data[i]['name'])
            lb_name = QLabel(move.name)
            lb_name.setStyleSheet('margin: 2px')
            lb_type = QLabel(move.type.name.capitalize())
            lb_type.setStyleSheet(f'color: white;'
                                  f'background-color: {utils.TYPE_COLORS.get(move.type.name.lower())};'
                                  f'border-radius: 10px;'
                                  f'margin: 2px;')
            lb_type.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)
            learn_method = raw_data['moves'][i]['learn_method'].capitalize()
            if learn_method == 'Level-up':
                learn_method = 'Level ' + str(raw_data['moves'][i]['level_learned_at'])
            lb_learn_method = QLabel(learn_method)
            self.table_moves.setRowHeight(i, 24)
            self.table_moves.setCellWidget(i, 0, lb_type)
            self.table_moves.setCellWidget(i, 1, lb_name)
            self.table_moves.setCellWidget(i, 2, lb_learn_method)

    def on_shiny_toggle_pressed(self):
        try:
            raw_data = self.pokemon_data[self.cb_pokemon.currentText()]
        except KeyError:
            return
        if not self.is_image_shiny:
            url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/' + \
                   str(raw_data['id']) + '.png'
        else:
            url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' + \
                  str(raw_data['id']) + '.png'
        self.is_image_shiny = not self.is_image_shiny
        ssl._create_default_https_context = ssl._create_unverified_context
        pixmap = QPixmap()
        try:
            img_data = request.urlopen(url).read()
            pixmap.loadFromData(img_data)
            self.lb_image.setPixmap(pixmap.scaledToWidth(96))
        except HTTPError:
            pixmap = QPixmap(pk_path)
            self.lb_image.setPixmap(pixmap.scaledToWidth(96))
