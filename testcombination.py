import db
import analyser

db.init_db()
print(analyser.summary(db.get_salaries()))
print(analyser.by_department(db.get_employees()))
