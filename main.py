from PyQt6.QtWidgets import QApplication
import sys
from ui import VotingApp
from voting import VoteManager

def main() -> None:
    """Starts the voting application with custom styles and GUI."""
    app = QApplication(sys.argv)

    
    app.setStyle('Fusion')
    app.setStyleSheet("""
        QWidget {
            background-color: white;
            color: black;
        }
        QPushButton {
            background-color: #1E90FF;  /* Dodger Blue */
            color: white;
            border: 1px solid #00008B;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #FF4500;  /* Red hover */
        }
        QLineEdit {
            background-color: #F0F8FF;  /* Alice Blue */
            color: black;
            border: 1px solid #00008B;
            padding: 4px;
        }
        QRadioButton {
            background-color: white;
            color: black;
            padding: 3px;
        }
        QLabel {
            color: #00008B;
            font-weight: bold;
        }
    """)

    vote_manager = VoteManager("votes.csv")
    window = VotingApp(vote_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
