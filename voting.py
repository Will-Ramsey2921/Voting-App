import csv
from typing import Dict

class VoteManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.votes: Dict[str, str] = {}
        self.load_votes()

    def has_voted(self, voter_id: str) -> bool:
        return voter_id in self.votes

    def cast_vote(self, voter_id: str, candidate: str) -> bool:
        if self.has_voted(voter_id):
            return False
        self.votes[voter_id] = candidate
        self.save_votes()
        return True

    def save_votes(self) -> None:
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            for voter_id, candidate in self.votes.items():
                writer.writerow([voter_id, candidate])

    def load_votes(self) -> None:
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        voter_id, candidate = row
                        self.votes[voter_id] = candidate
        except FileNotFoundError:
            self.save_votes()
