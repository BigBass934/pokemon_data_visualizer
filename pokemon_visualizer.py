import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QCheckBox, QGridLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

# Load the Pokémon dataset
pokemon_df = pd.read_csv('./dataset/pokemon_data.csv')

class PokemonVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokémon Data Visualizer")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Legendary checkbox above the search bar
        self.legendary_checkbox = QCheckBox("Legendary")
        main_layout.addWidget(self.legendary_checkbox)

        # Centered search box
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter a keyword...")
        self.search_bar.setFixedWidth(400)
        self.search_bar.setFixedHeight(30)
        search_layout.addStretch()
        search_layout.addWidget(self.search_bar)
        search_layout.addStretch()
        main_layout.addLayout(search_layout)

        # Filters layout
        filter_layout = QVBoxLayout()
        main_layout.addLayout(filter_layout)

        # Type 1 and Type 2 filters
        self.type1_checkboxes = self.create_type_filter_section("Type 1", filter_layout)
        self.type2_checkboxes = self.create_type_filter_section("Type 2", filter_layout)

        # Generation filter section
        self.create_generation_filter_section(filter_layout)

        # Stat filters
        self.stat_inputs = {}
        self.create_stat_filters(filter_layout)

        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_pokemon)
        main_layout.addWidget(search_button)

        # Results table
        self.results_table = QTableWidget()
        main_layout.addWidget(self.results_table)

    def create_type_filter_section(self, label, parent_layout):
        """Creates a section for type filters and adds it to the parent layout."""
        section_layout = QVBoxLayout()
        section_label = QLabel(label)
        section_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        section_layout.addWidget(section_label)

        type_checkboxes = {}
        type_grid = QGridLayout()
        for idx, pokemon_type in enumerate(["Normal", "Fire", "Fighting", "Water", "Flying",
                                             "Grass", "Poison", "Electric", "Ground", "Psychic",
                                             "Rock", "Ice", "Bug", "Dragon", "Ghost", "Dark",
                                             "Steel", "Fairy"]):
            checkbox = QCheckBox(pokemon_type)
            type_checkboxes[pokemon_type] = checkbox
            type_grid.addWidget(checkbox, idx // 9, idx % 9)
        section_layout.addLayout(type_grid)
        parent_layout.addLayout(section_layout)
        return type_checkboxes

    def create_generation_filter_section(self, parent_layout):
        """Creates the generation filter section with two horizontal columns."""
        section_layout = QVBoxLayout()
        section_label = QLabel("Generation")
        section_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        section_layout.addWidget(section_label)

        generation_layout = QGridLayout()
        self.generation_checkboxes = {}
        for idx, generation in enumerate(range(1, 9)):
            checkbox = QCheckBox(str(generation))
            self.generation_checkboxes[generation] = checkbox
            generation_layout.addWidget(checkbox, idx // 4, idx % 4)
        section_layout.addLayout(generation_layout)
        parent_layout.addLayout(section_layout)

    def create_stat_filters(self, parent_layout):
        """Creates the stat filters for hp, attack, defense, sp_attack, sp_defense, and speed."""
        stat_labels = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
        for stat in stat_labels:
            stat_layout = QHBoxLayout()

            # Label
            stat_label = QLabel(stat.capitalize())
            stat_layout.addWidget(stat_label)

            # Input field
            input_field = QLineEdit()
            self.stat_inputs[stat] = {"input": input_field}
            stat_layout.addWidget(input_field)

            # Greater and Less checkboxes
            greater_checkbox = QCheckBox("Greater Than")
            less_checkbox = QCheckBox("Less Than")
            greater_checkbox.toggled.connect(lambda checked, s=stat: self.toggle_stat_filter(s, "greater", checked))
            less_checkbox.toggled.connect(lambda checked, s=stat: self.toggle_stat_filter(s, "less", checked))
            self.stat_inputs[stat]["greater"] = greater_checkbox
            self.stat_inputs[stat]["less"] = less_checkbox

            stat_layout.addWidget(greater_checkbox)
            stat_layout.addWidget(less_checkbox)
            parent_layout.addLayout(stat_layout)

    def toggle_stat_filter(self, stat, mode, checked):
        """Ensures only one of 'greater' or 'less' checkboxes is selected."""
        other_mode = "greater" if mode == "less" else "less"
        if checked:
            self.stat_inputs[stat][other_mode].setChecked(False)



    def search_pokemon(self):
        """Filters Pokémon data based on search criteria."""
        filtered_df = pokemon_df.copy()

        # Keyword search
        keyword = self.search_bar.text().strip().lower()
        if keyword:
            filtered_df = filtered_df[filtered_df['name'].str.contains(keyword, case=False)]

        # Type 1 and Type 2 filters
        type1_selected = [ptype for ptype, checkbox in self.type1_checkboxes.items() if checkbox.isChecked()]
        if type1_selected:
            filtered_df = filtered_df[filtered_df['type 1'].fillna("").isin(type1_selected)]

        type2_selected = [ptype for ptype, checkbox in self.type2_checkboxes.items() if checkbox.isChecked()]
        if type2_selected:
            filtered_df = filtered_df[filtered_df['type 2'].fillna("").isin(type2_selected)]

        # Generation filter
        selected_generations = [gen for gen, checkbox in self.generation_checkboxes.items() if checkbox.isChecked()]
        if selected_generations:
            filtered_df = filtered_df[filtered_df['generation'].isin(selected_generations)]

        # Legendary filter
        if self.legendary_checkbox.isChecked():
            filtered_df = filtered_df[filtered_df['legendary'] == True]

        # Stat filters
        for stat, filters in self.stat_inputs.items():
            value = filters["input"].text().strip()
            if value.isdigit():
                value = int(value)
                if filters["greater"].isChecked():
                    filtered_df = filtered_df[filtered_df[stat] > value]
                elif filters["less"].isChecked():
                    filtered_df = filtered_df[filtered_df[stat] < value]
                else:
                    filtered_df = filtered_df[filtered_df[stat] == value]

        # Display results
        self.populate_table(filtered_df)

    def populate_table(self, df):
        """Populates the results table with filtered Pokémon data."""
        self.results_table.setRowCount(df.shape[0])
        self.results_table.setColumnCount(df.shape[1])
        self.results_table.setHorizontalHeaderLabels(df.columns.tolist())

        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PokemonVisualizer()
    window.show()
    sys.exit(app.exec())