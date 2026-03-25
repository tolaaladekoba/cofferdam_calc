# Cofferdam Calculator

The Cofferdam Calculator is a Python-based senior design project developed to support cofferdam engineering calculations through a graphical user interface. The goal of the project is to separate the calculation logic from the UI so the program is easier to develop, test, and expand.

## Requirements

Before running the project, make sure you have the following installed:

- Python 3.10 or later
- VS Code or another code editor
- Git (optional, if cloning from GitHub)

You can check if Python is installed by running:

```bash
python3 --version

Project Setup
Download or clone the project files.
Open the project folder in VS Code.
Open a terminal inside the project folder.
Make sure you are inside the cofferdam_calc folder.
How to Run the App
Run the following command in the terminal:
python3 main.py
If you are using a virtual environment, activate it first:
source .venv/bin/activate
python3 main.py

Project Structure
main.py – starts the application
ui/app_ui.py – contains the graphical user interface
CofferdamLibrary.py – contains calculation logic for cofferdam cases

Current Status
The user interface structure has been set up, and the calculation logic is being developed and tested. The calculation code currently works separately, while full integration of all cases into the UI is still in progress.
