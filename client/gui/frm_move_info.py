from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from api.move import Move
from api.util import utils


class FrmMoveInfo(QWidget):
    def __init__(self, move_name: str):
        super().__init__()
        self.move = Move(move_name)

        # COMPONENT LIST
        self.grid = QGridLayout()
        self.top_bar = QHBoxLayout()
        self.lb_move_name = QLabel(self.move.name)
        self.lb_type = QLabel(self.move.type.name.capitalize())
        self.lb_info = QLabel(f'Power: {self.move.power}  |  '
                              f'Accuracy: {self.move.accuracy}  |  '
                              f'PP: {self.move.pp}  |  '
                              f'Priority: {self.move.priority}')
        self.te_description = QTextEdit(self.move.description)
        # END OF COMPONENT LIST

        self.init_ui()

    def init_ui(self):
        self.setLayout(self.grid)
        self.grid.setVerticalSpacing(20)

        self.lb_move_name.setStyleSheet('font-size: 24pt; font: bold;')
        self.lb_move_name.setFixedWidth(300)

        self.lb_type.setStyleSheet(f'color: white;'
                                   f'background-color: {utils.TYPE_COLORS.get(self.move.type.name.lower())};'
                                   f'border-radius: 10px;')
        self.lb_type.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)
        self.lb_type.setFixedSize(70, 20)

        self.top_bar.addWidget(self.lb_move_name)
        self.top_bar.addWidget(self.lb_type)

        self.te_description.setReadOnly(True)
        self.te_description.setFixedHeight(120)

        self.grid.addLayout(self.top_bar, 0, 0)
        self.grid.addWidget(self.lb_info, 1, 0)
        self.grid.addWidget(self.te_description, 2, 0)