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
        self.group_name = self.determine_group()

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.age} lat, {self.email}, [{self.group_name}]"

    def calculate_age(self):
        today = datetime.now().date()
        birthdate_date = datetime.strptime(self.birthdate_str, "%Y-%m-%d").date()
        years = today.year - birthdate_date.year

        if (today.month, today.day) < (birthdate_date.month, birthdate_date.day):
            years -= 1
        return years

    def validate_email(self):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, self.email) is not None


    def determine_grup(self):
        age = self.age
        if 6 <= age <=10:
            return "Kadeci"
        elif 11<= age <= 14:
            return "Juniorzy młodsi"
        elif 15<= age <= 18:
            return "Juniorzy"
        else:
            return "Poza zakresem"


class Group:
    def __init__(self, name, age_range, students=None, capacity=32):
        """
        Inicjacja klasy Group:
        :param name: Nazwa grupy wiekowej
        :param age_range: Zakres grupy wiekowej
        :param students: lista obiektów Student zapisanej do grupy
        :param capacity: Wiekość grupy wiekowej ustalone sztywno na 32
        """

        self.name = name
        self.age_range = age_range
        self.capacity = capacity
        self.students = students if students is not None else []

    def __str__(self):
        return f"""{self.name}, 
        wiek: {self.age_range}, 
        zapisanych: {len(self.students)}, 
        wolnych miejsc: {self.capacity - len(self.students)}"""

    def free_space(self):
        return self.capacity - len(self.students)

    def add_student(self, student):
        if self.free_space() > 0 and self.is_age_in_range(student):
            self.students.append(student)
            return True
        else:
            return False

    def is_age_in_range(self, student):
        return self.age_range[0] <= student.age <= self.age_range[1]


class Camp:
    def __init__(self):
        self.students = []
        self.groups = [
            Group("Kadeci", (6, 10)),
            Group("Juniorzy młodsi", (11, 14)),
            Group("Juniorzy", (15, 16))
        ]

    def add_student(self, first_name, last_name, birthdate_str, email):
        first_name = input("\nPodaj imię uczestnika: ").strip()
        last_name = input("\nPodaj nazwisko uczestnika: ").strip()
        birthdate_str = input("\nPodaj datę urodenia w formacie YYYY-MM-DD: ").strip()
        email = input("\nPodaj email uczestnika: ").strip()

        student = Student(first_name, last_name, birthdate_str, email)

        for group in self.groups:
            if group.is_age_in_range(student) and group.free_space() > 0:
                group.add_student(student)
                self.students.append(student)
                print(f"\nUczestnik {student.first_name} {student.last_name} dodany do grupy: {group.name}")
                return True

        print(f"\n Nie znaloeziono grupy wiekowej albo brak wolnych miejsc.")
        return False

    def remove_student(self):
        search_first_name = input("Podaj imię szukanego uczestnika").strip()
        search_last_name = input("Podaj nazwisko szukanego uczestnika").strip()

        for student in self.students:
            if student.first_name == search_first_name and student.last_name == search_last_name:
                self.students.remove(student)

                for group in self.groups:
                    if student in group.students:
                        group.students.remove(student)

            print(f"\nUczestnik {student.first_name} {student.last_name} osunięty z obozu")
            return True

        print(f"\nNie znaleziono uczestnika {search_first_name} {search_last_name}.")
        return False

    def find_student(self, last_name):


    def list_student(self):



    def total_student(self):