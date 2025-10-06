import csv

with open("student_grades.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    data = list(reader)

averages = {}
for row in data:
    name = row[0]
    scores = list(map(float, row[1:]))
    avg = round(sum(scores) / len(scores), 2)
    averages[name] = avg


with open("student_average_grades.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Average"])
    for name, avg in averages.items():
        writer.writerow([name, avg])

print("Done! 'student_average_grades.csv' created.")
