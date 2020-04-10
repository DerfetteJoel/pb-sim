import os
import ssl
from urllib import request
from urllib.error import HTTPError

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from api.util import io_utils, utils

pk_path = os.path.join(io_utils.root_dir, 'data', 'sprites', '0.png')


def launch():
    app = QApplication([])
    app.setStyle('Fusion')
    frm = FrmPokemonInfo()
    app.exec()


class FrmPokemonInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.data = io_utils.load_all_pokemon()

        # COMPONENT LIST
        self.window = QWidget()
        self.grid = QGridLayout()
        self.lb_cb_desc = QLabel('Select a Pokemon: ')
        self.lb_bt_desc = QLabel('or')
        self.lb_move_desc = QLabel('Learnable moves:')
        self.bt_add_pokemon = QPushButton('Create a new Pokemon')
        self.cb_pokemon = QComboBox()
        self.lb_pokemon_name = QLabel()
        self.lb_image = QLabel()
        self.is_image_shiny = False
        self.stat_info_group = QVBoxLayout()
        self.stat_info_rows = []
        self.lb_stat_names = []
        self.stat_bars = []
        self.lb_stat_values = []
        self.type_group = QHBoxLayout()
        self.type_1 = QLabel()
        self.type_2 = QLabel()
        self.list_moves = QListWidget()
        # END OF COMPONENT LIST

        self.init_ui()
        self.window.show()

    def init_ui(self):
        self.window.setLayout(self.grid)

        self.bt_add_pokemon.setEnabled(False)

        self.cb_pokemon.addItem('')
        for key in self.data:
            self.cb_pokemon.addItem(self.data[key]['name'])
        self.cb_pokemon.setEditable(True)

        self.lb_pokemon_name.setText(self.cb_pokemon.currentText().split('-')[0].title())
        self.lb_pokemon_name.setStyleSheet('font-size: 24pt; font: bold;')
        self.lb_pokemon_name.setAlignment(Qt.AlignCenter)
        self.lb_pokemon_name.setMinimumWidth(150)

        pixmap = QPixmap(pk_path)
        self.lb_image.setPixmap(pixmap)
        self.lb_image.setMaximumSize(96, 96)

        stat_names = ['HP', 'Atk', 'Def', 'SpAtk', 'SpDef', 'Spe']
        for i in range(0, 6):
            self.stat_info_rows.append(QHBoxLayout())
            self.lb_stat_names.append(QLabel())
            self.lb_stat_names[i].setText(stat_names[i])
            self.lb_stat_names[i].setMinimumWidth(40)
            self.lb_stat_names[i].setMaximumWidth(40)

            self.stat_bars.append(QProgressBar())
            self.stat_bars[i].setRange(0, 255)
            self.stat_bars[i].setMinimumSize(255, 30)
            self.stat_bars[i].setTextVisible(False)
            self.stat_bars[i].setValue(0)

            self.lb_stat_values.append(QLabel(''))
            self.lb_stat_values[i].setMinimumWidth(30)
            self.lb_stat_values[i].setMaximumWidth(30)
            self.lb_stat_values[i].setUpdatesEnabled(True)

            self.stat_info_rows[i].addWidget(self.lb_stat_names[i])
            self.stat_info_rows[i].addWidget(self.stat_bars[i])
            self.stat_info_rows[i].addWidget(self.lb_stat_values[i])
            self.stat_info_group.addLayout(self.stat_info_rows[i])

        self.type_1.setMaximumSize(70, 20)
        self.type_1.setMinimumSize(70, 20)
        self.type_2.setMaximumSize(70, 20)
        self.type_2.setMinimumSize(70, 20)
        self.type_1.setAlignment(Qt.AlignCenter)
        self.type_2.setAlignment(Qt.AlignCenter)
        self.type_group.addWidget(self.type_1)
        self.type_group.addWidget(self.type_2)

        self.list_moves.setStyleSheet('font-size: 14pt;')
        self.list_moves.setAlternatingRowColors(True)
        self.list_moves.setMinimumWidth(255)

        self.cb_pokemon.currentIndexChanged.connect(lambda: self.on_pokemon_selected())

        self.grid.addWidget(self.lb_cb_desc, 0, 0)
        self.grid.addWidget(self.cb_pokemon, 0, 2)
        self.grid.addWidget(self.lb_bt_desc, 0, 3)
        self.grid.addWidget(self.bt_add_pokemon, 0, 4)
        self.grid.addWidget(self.lb_pokemon_name, 1, 2)
        self.grid.addLayout(self.type_group, 1, 0)
        self.grid.addWidget(self.lb_move_desc, 1, 4)
        self.grid.addWidget(self.lb_image, 2, 0)
        self.grid.addLayout(self.stat_info_group, 2, 2)
        self.grid.addWidget(self.list_moves, 2, 4)

    def on_pokemon_selected(self):
        try:
            raw_data = self.data[self.cb_pokemon.currentText()]
        except KeyError:
            return
        url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' + \
              str(raw_data['id']) + '.png'
        ssl._create_default_https_context = ssl._create_unverified_context
        pixmap = QPixmap()
        try:
            img_data = request.urlopen(url).read()
            pixmap.loadFromData(img_data)
            self.lb_image.setPixmap(pixmap)
        except HTTPError:
            pixmap.load(pk_path)
            self.lb_image.setPixmap(pixmap.scaledToWidth(96))
        self.lb_pokemon_name.setText(self.cb_pokemon.currentText().split('-')[0].title())
        self.type_1.setText(raw_data['types']['type_1'].upper())
        self.type_1.setStyleSheet(f'color: white;'
                                  f'background-color: {utils.TYPE_COLORS.get(self.type_1.text().lower())};'
                                  f'border-radius: 10px')
        type_2_data = raw_data['types']['type_2']
        if type_2_data != 'none':
            self.type_2.setText(type_2_data.upper())
        else:
            self.type_2.setText('')
        self.type_2.setStyleSheet(f'color: white;'
                                  f'background-color: {utils.TYPE_COLORS.get(self.type_2.text().lower())};'
                                  f'border-radius: 10px')
        for i in range(0, 6):
            self.stat_bars[i].setValue(raw_data['base_stats'][i])
            self.lb_stat_values[i].setText(str(raw_data['base_stats'][i]))
        self.list_moves.clear()
        for i in range(0, len(raw_data['moves'])):
            self.list_moves.addItem(raw_data['moves'][i]['name'].replace('-', ' ').title())
