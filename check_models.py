from models import Session, User, Student, Rank
session = Session()

user1 = User(username = 'solomchaak', first_name='Ivan', last_name='Solomchak',
             email='ivan.solomchak@mail.net', phone='+380999977777', login='solomchaak', super_user=False, password='123123')
user2 = User(username = 'urasuk', first_name='Yurii', last_name='Yanio',
             email='exampl@gmail.com', phone='+380957777777', login='urasuk', super_user=False, password='12345678')
user3 = User(username = 'admin', first_name='name', last_name='surname',
             email='admin@gmail.com', phone='+380922777777', login='adm', super_user=True, password='root')

session.add(user1)
session.add(user2)
session.add(user3)

student1 = Student(id = 1, student_first_name = 'Ivan', student_last_name = 'Solomchak',
                   student_average_grade = 3, student_age = 18)
student2 = Student(id = 2, student_first_name = 'Viktoria', student_last_name = 'Molochii',
                   student_average_grade = 4, student_age = 18)
student3 = Student(id = 3, student_first_name = 'Roman', student_last_name = 'Bilets',
                   student_average_grade = 5, student_age = 19)

session.add(student1)
session.add(student2)
session.add(student3)

rank1 = Rank(rank_id = 1, student_id = 1, last_change = '2008-10-03 10:37:22', changed_by = 'admin')
rank2 = Rank(rank_id = 2, student_id = 2, last_change = '2012-06-11 10:38:22', changed_by = 'admin')
rank3 = Rank(rank_id = 3, student_id = 3, last_change = '2021-11-11 10:37:52', changed_by = 'admin')

session.add(rank1)
session.add(rank2)
session.add(rank3)

session.commit()

print(session.query(User).all())
print(session.query(Student).all())
print(session.query(Rank).all())

session.close()