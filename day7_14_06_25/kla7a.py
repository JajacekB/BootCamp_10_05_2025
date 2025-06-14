class Printer:
    def print_message(self, message):
        print(f"Drukowanie wiadomości: {message}")


class Scanner:
    def scan_document(self):
        print("Skanowanie dokumentu")
        return "Zawartość dokumentu"


class MultifuctionalDevice(Printer, Scanner):

    def photocopy(self):
        content = self.scan_document()
        self.print_message(content)


device = MultifuctionalDevice()
device.photocopy()


device.print_message("Komunikat")

message = device.scan_document()
print("Odczytany komunikat:", message)

print(MultifuctionalDevice.__mro__)

