"""
CS200L Data Structures and Algorithms (Pr) - Lab 4, Part 2
CRUD application using PyQt5 + CSV file (data persists after restart)

Name: Shamaim
Registration No: 2025-GA-112

Run:
    pip install pyqt5
    python crud_app.py

NOTE: Apne Project 1 ke hisaab se sirf neeche wali FIELDS list badalni hai.
      Baaki poora code (form, table, CSV) automatically adjust ho jata hai.
"""

import csv
import os
import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QAbstractItemView, QHeaderView,
)

# ------------------------------------------------------------------
# CONFIG: apne Project 1 ke fields yahan likho
# ------------------------------------------------------------------
APP_TITLE = "Student Records - CRUD"
CSV_FILE = "data.csv"
FIELDS = ["ID", "Name", "Department", "Semester", "CGPA"]   # first field = unique key
# ------------------------------------------------------------------


class CrudApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(850, 520)

        self.records = []          # list of lists (har record ek row hai)
        self.inputs = {}           # field name -> QLineEdit

        self.build_ui()
        self.load_csv()            # app start hote hi purana data load
        self.refresh_table()

    # ---------------------------- UI ----------------------------
    def build_ui(self):
        main_layout = QVBoxLayout(self)

        title = QLabel(APP_TITLE)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # ---- form (inputs) ----
        form = QFormLayout()
        for field in FIELDS:
            edit = QLineEdit()
            edit.setPlaceholderText(f"Enter {field}")
            self.inputs[field] = edit
            form.addRow(f"{field}:", edit)
        main_layout.addLayout(form)

        # ---- buttons ----
        btn_row = QHBoxLayout()
        self.btn_add = QPushButton("Add (Create)")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_clear = QPushButton("Clear Form")
        for b in (self.btn_add, self.btn_update, self.btn_delete, self.btn_clear):
            btn_row.addWidget(b)
        main_layout.addLayout(btn_row)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_update.clicked.connect(self.update_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_clear.clicked.connect(self.clear_form)

        # ---- search ----
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search (kisi bhi field mein)...")
        self.search_box.textChanged.connect(self.refresh_table)
        main_layout.addWidget(self.search_box)

        # ---- table (Read) ----
        self.table = QTableWidget(0, len(FIELDS))
        self.table.setHorizontalHeaderLabels(FIELDS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellClicked.connect(self.fill_form_from_row)
        main_layout.addWidget(self.table)

    # ------------------------- helpers --------------------------
    def get_form_values(self):
        return [self.inputs[f].text().strip() for f in FIELDS]

    def clear_form(self):
        for edit in self.inputs.values():
            edit.clear()
        self.inputs[FIELDS[0]].setReadOnly(False)
        self.table.clearSelection()

    def find_index_by_key(self, key):
        for i, rec in enumerate(self.records):
            if rec[0] == key:
                return i
        return -1

    def warn(self, msg):
        QMessageBox.warning(self, "Warning", msg)

    # --------------------------- CSV ----------------------------
    def load_csv(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)          # pehli row header hai
            if header is None:
                return
            for row in reader:
                if len(row) == len(FIELDS):
                    self.records.append(row)

    def save_csv(self):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)
            writer.writerows(self.records)

    # ---------------------------- CRUD --------------------------
    def add_record(self):                        # CREATE
        values = self.get_form_values()
        if any(v == "" for v in values):
            self.warn("Please fill all the fields.")
            return
        if self.find_index_by_key(values[0]) != -1:
            self.warn(f"{FIELDS[0]} '{values[0]}' already exists.")
            return
        self.records.append(values)
        self.save_csv()
        self.refresh_table()
        self.clear_form()

    def refresh_table(self):                     # READ
        query = self.search_box.text().strip().lower()
        shown = [r for r in self.records
                 if not query or any(query in cell.lower() for cell in r)]
        self.table.setRowCount(len(shown))
        for row, rec in enumerate(shown):
            for col, value in enumerate(rec):
                self.table.setItem(row, col, QTableWidgetItem(value))

    def fill_form_from_row(self, row, _col):
        for col, field in enumerate(FIELDS):
            self.inputs[field].setText(self.table.item(row, col).text())
        self.inputs[FIELDS[0]].setReadOnly(True)  # key ko edit nahi karna

    def update_record(self):                     # UPDATE
        values = self.get_form_values()
        idx = self.find_index_by_key(values[0])
        if idx == -1:
            self.warn("Select a record from the table first.")
            return
        if any(v == "" for v in values):
            self.warn("Please fill all the fields.")
            return
        self.records[idx] = values
        self.save_csv()
        self.refresh_table()
        self.clear_form()

    def delete_record(self):                     # DELETE
        key = self.inputs[FIELDS[0]].text().strip()
        idx = self.find_index_by_key(key)
        if idx == -1:
            self.warn("Select a record from the table first.")
            return
        answer = QMessageBox.question(
            self, "Confirm", f"Delete record '{key}'?",
            QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            del self.records[idx]
            self.save_csv()
            self.refresh_table()
            self.clear_form()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CrudApp()
    window.show()
    sys.exit(app.exec_())
