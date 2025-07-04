# Prosty system rejestracji uczniów do kursu (Obóz sportowy)
# Program zapisuje kandydatów na obóz do jednej z grup wiekowych (6-10, 11-14, 15_18)
# Sprawdza poprawność wprowadzonych danych i umożliwia przgląd uczestników oraz ich usunięcie.

from datetime import datetime
import re


class Student:
    def __init__(self, first_name, last_name, birthdate_str, email):
        """
        Inicjacja clasy Student:
        :param first_name: imię uczestnika
        :param last_name: nazwisko uczestnika
        :param birthdate_str: data urodzenia jako string
        :param email: email uczstnika
        """

        self.first_name = first_name
        self.last_name = last_name
        self.birthdate_str = birthdate_str
        self.birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        self.age = self.calculate_age()
        self.email = email
        self.grup_name = self.determine_grup()

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.age} lat, {self.email}, [{self.grup_name}]"

    def calculate_age(self):
        today = datetime.now().date()
        birthdate_date = datetime.strptime(self.birthdate_str, "%Y-%m-%d").date()
        age = today.year - birthdate_date.year

        if (today.month, today.day) < (birthdate_date.month, birthdate_date.day):
            age -= 1

        return age

    def validate_email(self):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, self.email) is not None


    def determine_grup(self):
        match age:
            case 6 <= age <= 10:
                grup_name = "Kadeci"

            case 11 <= age <= 14:
                grup_name = "Juniorzy młodsi"

            case 15 <= age <= 18:
                grup_name = "Juniorzy"


class Group:
    def __init__(self, name, age_range, capaciy=32, students):
        """
        Inicjacja klasy Group:
        :param name: Nazwa grupy wiekowej
        :param age_range: Zakres grupy wiekowej
        :param capaciy: Wiekość grupy wiekowej ustalone sztywno na 32
        :param students: lista obiektów Student zapisanej do grupy
        """

    def free_space:


    def add_student(self, student):


class Camp:
    def __init__(self, grups):
        """
        Definiuję grupę Camp
        :param grups: lista trzech obiektów klasy Group
        """

    def add_student(self):

        first_name = input("\nPodaj imię uczestnika: ").strip()
        last_name = input("\nPodaj nazwisko uczestnika: ").strip()
        birthday = input("\nPodaj datę urodenia w formacie YYYY-MM-DD: ")
        email = input("\nPodaj email uczestnika: ")




    def list_student(self):


    def find_student(self, last_name):


    def remove_student(self, last_name):


    def total_student(self):