from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QButtonGroup, QDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from voting import VoteManager

from PyQt6.QtCharts import (
    QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
)
from PyQt6.QtGui import QPainter


class VotingApp(QMainWindow):
    """GUI window for voting application."""

    def __init__(self, vote_manager: VoteManager) -> None:
        super().__init__()
        self.vote_manager = vote_manager
        self.setWindowTitle("Voting Application")
        self.setFixedSize(400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("VOTING APPLICATION")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter your voter ID")
        self.layout.addWidget(self.id_input)

        self.candidates = ["Bianca", "Edward", "Felicia"]
        self.radio_buttons = []
        self.button_group = QButtonGroup()
        for i, name in enumerate(self.candidates):
            btn = QRadioButton(name)
            self.radio_buttons.append(btn)
            self.button_group.addButton(btn, i)
            self.layout.addWidget(btn)

        self.submit_btn = QPushButton("SUBMIT VOTE")
        self.submit_btn.clicked.connect(self.submit_vote)
        self.layout.addWidget(self.submit_btn)

        self.results_btn = QPushButton("SHOW RESULTS")
        self.results_btn.clicked.connect(self.show_results)
        self.layout.addWidget(self.results_btn)

        self.clear_btn = QPushButton("CLEAR VOTES")
        self.clear_btn.clicked.connect(self.clear_votes)
        self.layout.addWidget(self.clear_btn)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.message_label)

    def submit_vote(self) -> None:
        """Handles vote submission and feedback."""
        voter_id = self.id_input.text().strip()
        selected_button = self.button_group.checkedButton()

        if not voter_id:
            self.set_message("Please enter your voter ID.", "red")
            return
        if selected_button is None:
            self.set_message("Please select a candidate.", "red")
            return

        candidate = selected_button.text()
        if self.vote_manager.has_voted(voter_id):
            self.set_message("Already Voted.", "red")
            return

        self.vote_manager.cast_vote(voter_id, candidate)
        self.set_message(f"Vote submitted for {candidate}!", "green")
        self.id_input.clear()
        self.button_group.setExclusive(False)
        for btn in self.radio_buttons:
            btn.setChecked(False)
        self.button_group.setExclusive(True)

    def set_message(self, message: str, color: str) -> None:
        """Displays feedback to the user."""
        self.message_label.setText(message)
        self.message_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def show_results(self) -> None:
        """Opens a window showing a bar chart of vote totals."""
        results = self.vote_manager.votes
        chart_window = ResultsWindow(results)
        chart_window.exec()

    def clear_votes(self):
        """Clears all stored votes after user confirmation."""
        reply = QMessageBox.question(
            self,
            'Confirm Clear',
            'Are you sure you want to clear all votes?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            with open('votes.csv', 'w') as f:
                f.write('')
            self.vote_manager.votes.clear()
            self.set_message("All votes have been cleared.", "green")


class ResultsWindow(QDialog):
    def __init__(self, votes: dict):
        """Creates and displays a bar chart of voting results."""
        super().__init__()
        self.setWindowTitle("Vote Results")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        categories = ["Bianca", "Edward", "Felicia"]
        counts = [list(votes.values()).count(name) for name in categories]
        total_votes = sum(counts)

        bar_set = QBarSet("Votes")
        for count in counts:
            bar_set.append(count)

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.setTitle("Vote Counts")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max(counts + [1]))  # prevents zero range
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(chart_view)

        
        for i, count in enumerate(counts):
            percent = (count / total_votes * 100) if total_votes > 0 else 0
            label = QLabel(f"{categories[i]}: {percent:.1f}%")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
