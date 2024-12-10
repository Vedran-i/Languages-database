import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QWidget, QMessageBox
)

# Function to load data from the skills.txt file
def load_data_from_file(file_path):
    people = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Split the line into name and languages
                if ":" in line:
                    name, languages = line.strip().split(":", 1)
                    people.append({"Name": name.strip(), "Languages": [lang.strip() for lang in languages.split(",")]})
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit()
    return people

# Search function
def search_by_language(language, people):
    language = language.lower()
    matching_people = []
    for person in people:
        # Check if the language is in the person's list of languages
        if language in [lang.lower() for lang in person["Languages"]]:
            matching_people.append(person["Name"])
    return matching_people

# PyQt5 GUI
class SearchableDatabaseApp(QMainWindow):
    def __init__(self, people):
        super().__init__()
        self.setWindowTitle("Searchable Database")
        self.setGeometry(100, 100, 600, 400)
        self.people = people  # Store the loaded data

        # Set up the main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add a label for instructions
        self.label = QLabel("Enter a language to search:")
        layout.addWidget(self.label)

        # Add an input field for the language
        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("e.g., Japanese, English, Dutch")
        layout.addWidget(self.language_input)

        # Add a button to perform the search
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_button)

        # Add a text box to display the results
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

    def perform_search(self):
        # Get the language from the input field
        language = self.language_input.text().strip()
        if not language:
            QMessageBox.warning(self, "Input Error", "Please enter a language.")
            return

        # Perform the search
        matching_people = search_by_language(language, self.people)

        # Display the results
        self.result_text.clear()
        if matching_people:
            self.result_text.append(f"People who know {language.capitalize()}:\n")
            for name in matching_people:
                self.result_text.append(name)
        else:
            self.result_text.append(f"No people found who know {language.capitalize()}.")

if __name__ == "__main__":
    # Load data from the skills.txt file
    people = load_data_from_file("skills.txt")
    if not people:
        print("No data loaded. Exiting...")
        sys.exit()

    app = QApplication(sys.argv)
    window = SearchableDatabaseApp(people)
    window.show()
    sys.exit(app.exec_())
