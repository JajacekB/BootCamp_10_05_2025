from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DATABASE_URI = "sqlite:///kursy.db"

Base = declarative_base()

# definicja tabeli asocjacyjnej

student_course_table = Table(
    'student_course',
    Base.metadata,
    Column("student_id", Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    courses = relationship('Course', secondary=student_course_table, back_populates='students')


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    students = relationship('Student', secondary=student_course_table, back_populates='courses')


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


student1 = Student(name="Anna Kowalska")
student2 = Student(name="Jan Nowak")
student3 = Student(name="Józek Noga")

course1 = Course(title="Programowanie w Python dla zaawansowanych")
course2 = Course(title="Programowanie w Java")
course3 = Course(title="Programowanie SQL")
student1.courses.append(course1)
student1.courses.append(course2)
student2.courses.append(course1)
student3.courses.append(course2)
student3.courses.append(course3)
session.add(student1)
session.add(student2)
session.add(student3)
session.commit()

our_student = session.query(Student).filter_by(name="Anna Kowalska").first()
print(f"student: {our_student.name}")

for course in our_student.courses:
    print(f"Zapisany na kurs: {course.title}")


print(50 * "_")
our_course = session.query(Course).first()
print(our_course.title)
for student in our_course.students:
    print(f"Uczeń: {student.name}")