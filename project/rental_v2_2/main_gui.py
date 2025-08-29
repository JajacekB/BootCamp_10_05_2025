import sys
from gui.start_window_controller import StartWindowController

def main():
    """
    Main entry point for the GUI application.
    Initializes and runs the AppController.
    """
    controller = StartWindowController()
    controller.run()

if __name__ == "__main__":
    main()
