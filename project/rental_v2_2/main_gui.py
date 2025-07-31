import sys
from gui.app_controller import AppController # Import the new AppController

def main():
    """
    Main entry point for the GUI application.
    Initializes and runs the AppController.
    """
    controller = AppController()
    controller.run()

if __name__ == "__main__":
    main()
