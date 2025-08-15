import sys
import platform

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt
from datetime import date

from models.repair_history import RepairHistory
from models.vehicle import Vehicle