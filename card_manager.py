import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QListWidget, QLabel, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CardManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card Collection Manager")
        self.setGeometry(100, 100, 800, 600)
        
        
        self.all_cards = []
        self.user_cards = []
        self.current_profile = "Untitled Profile"
        
       
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        
        
        self.left_panel = QVBoxLayout()
        self.all_cards_label = QLabel("Available Cards")
        self.all_cards_list = QListWidget()
        self.all_cards_list.itemClicked.connect(self.preview_card)
        self.left_panel.addWidget(self.all_cards_label)
        self.left_panel.addWidget(self.all_cards_list)
        
       
        self.middle_panel = QVBoxLayout()
        self.add_button = QPushButton("Add →")
        self.add_button.clicked.connect(self.add_to_user_list)
        self.remove_button = QPushButton("← Remove")
        self.remove_button.clicked.connect(self.remove_from_user_list)
        self.middle_panel.addStretch()
        self.middle_panel.addWidget(self.add_button)
        self.middle_panel.addWidget(self.remove_button)
        self.middle_panel.addStretch()
        
       
        self.right_panel = QVBoxLayout()
        
        
        self.user_section = QVBoxLayout()
        self.user_cards_label = QLabel("Your Collection")
        self.user_cards_list = QListWidget()
        self.user_cards_list.itemClicked.connect(self.preview_card)
        self.user_section.addWidget(self.user_cards_label)
        self.user_section.addWidget(self.user_cards_list)
        
        
        self.preview_section = QVBoxLayout()
        self.preview_label = QLabel("Card Preview")
        self.card_preview = QLabel()
        self.card_preview.setAlignment(Qt.AlignCenter)
        self.card_preview.setMinimumSize(300, 400)
        self.preview_section.addWidget(self.preview_label)
        self.preview_section.addWidget(self.card_preview)
        
        self.right_panel.addLayout(self.user_section)
        self.right_panel.addLayout(self.preview_section)
        
      
        self.main_layout.addLayout(self.left_panel, 2)
        self.main_layout.addLayout(self.middle_panel, 1)
        self.main_layout.addLayout(self.right_panel, 2)
        
       
        self.create_menu_bar()
        
        
        self.load_default_cards()
    
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        
        file_menu = menu_bar.addMenu("File")
        
        load_profile_action = file_menu.addAction("Load Profile")
        load_profile_action.triggered.connect(self.load_profile)
        
        save_profile_action = file_menu.addAction("Save Profile")
        save_profile_action.triggered.connect(self.save_profile)
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
       
        card_menu = menu_bar.addMenu("Cards")
        
        load_cards_action = card_menu.addAction("Load Card Directory")
        load_cards_action.triggered.connect(self.load_card_directory)
    
    def load_default_cards(self):
        
        self.all_cards = [
            {"name": "Card 1", "image": "card1.png"},
            {"name": "Card 2", "image": "card2.png"},
            {"name": "Card 3", "image": "card3.png"},
            {"name": "Card 4", "image": "card4.png"},
            {"name": "Card 5", "image": "card5.png"},
        ]
        self.update_all_cards_list()
    
    def load_card_directory(self):
        
        dir_path = QFileDialog.getExistingDirectory(self, "Select Card Directory")
        
        if dir_path:
            self.all_cards = []
            for file in os.listdir(dir_path):
                if file.lower().endswith('.png'):
                    self.all_cards.append({
                        "name": os.path.splitext(file)[0],
                        "image": os.path.join(dir_path, file)
                    })
            self.update_all_cards_list()
    
    def update_all_cards_list(self):
        self.all_cards_list.clear()
        for card in self.all_cards:
            self.all_cards_list.addItem(card["name"])
    
    def update_user_cards_list(self):
        self.user_cards_list.clear()
        for card in self.user_cards:
            self.user_cards_list.addItem(card["name"])
    
    def add_to_user_list(self):
        selected_items = self.all_cards_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            card_name = item.text()
            card = next((c for c in self.all_cards if c["name"] == card_name), None)
            if card and card not in self.user_cards:
                self.user_cards.append(card)
        
        self.update_user_cards_list()
    
    def remove_from_user_list(self):
        selected_items = self.user_cards_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            card_name = item.text()
            card = next((c for c in self.user_cards if c["name"] == card_name), None)
            if card:
                self.user_cards.remove(card)
        
        self.update_user_cards_list()
        self.card_preview.clear()
    
    def preview_card(self, item):
        card_name = item.text()
        card = next((c for c in self.all_cards + self.user_cards if c["name"] == card_name), None)
        
        if card:
            pixmap = QPixmap(card["image"])
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.card_preview.width(), 
                    self.card_preview.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.card_preview.setPixmap(scaled_pixmap)
            else:
                self.card_preview.setText("Image not found")
    
    def save_profile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Profile",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        
        if file_name:
            if not file_name.endswith('.json'):
                file_name += '.json'
            
            profile_data = {
                "profile_name": os.path.splitext(os.path.basename(file_name))[0],
                "user_cards": self.user_cards
            }
            
            try:
                with open(file_name, 'w') as f:
                    json.dump(profile_data, f)
                self.current_profile = profile_data["profile_name"]
                self.setWindowTitle(f"Card Collection Manager - {self.current_profile}")
                QMessageBox.information(self, "Success", "Profile saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save profile: {str(e)}")
    
    def load_profile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load Profile",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    profile_data = json.load(f)
                
                self.user_cards = profile_data.get("user_cards", [])
                self.current_profile = profile_data.get("profile_name", "Untitled Profile")
                self.setWindowTitle(f"Card Collection Manager - {self.current_profile}")
                self.update_user_cards_list()
                QMessageBox.information(self, "Success", "Profile loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load profile: {str(e)}")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'card_preview') and self.card_preview.pixmap():
            current_pixmap = self.card_preview.pixmap()
            scaled_pixmap = current_pixmap.scaled(
                self.card_preview.width(),
                self.card_preview.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.card_preview.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication([])
    window = CardManager()
    window.show()
    app.exec_()