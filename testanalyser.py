import analyser

print(analyser.summary([100, 200, 300, 400]))
print(analyser.summary([]))

print(analyser.by_department([
    {"department": "A", "salary": 100},
    {"department": "A", "salary": 300},
    {"department": "B", "salary": 500},
]))
