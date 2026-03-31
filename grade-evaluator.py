import csv
import sys
import os

def load_csv_data():
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print("Error: The file '{}' was not found.".format(filename))
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })

        if not assignments:
            print("Error: CSV file is empty.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print("An error occurred: {}".format(e))
        sys.exit(1)


def evaluate_grades(data):
    print("\n--- Processing Grades ---")

    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    formative_score = 0
    summative_score = 0
    total_score = 0

    failed_formatives = []

    for item in data:
        score = item['score']
        weight = item['weight']
        group = item['group']

        if score < 0 or score > 100:
            print("Invalid score: {}".format(score))
            return

        total_weight += weight

        weighted = (score * weight) / 100
        total_score += weighted

        if group == "Formative":
            formative_weight += weight
            formative_score += weighted

            if score < 50:
                failed_formatives.append(item)

        elif group == "Summative":
            summative_weight += weight
            summative_score += weighted

    if total_weight != 100:
        print("Error: Total weight must be 100")
        return

    if formative_weight != 60:
        print("Error: Formative weight must be 60")
        return

    if summative_weight != 40:
        print("Error: Summative weight must be 40")
        return

    gpa = (total_score / 100) * 5.0

    if formative_score >= 30 and summative_score >= 20:
        status = "PASSED"
    else:
        status = "FAILED"

    print("Final Score: {:.2f}%".format(total_score))
    print("GPA: {:.2f}".format(gpa))
    print("Status: {}".format(status))

    if status == "FAILED" and failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)

        print("\nResubmit:")
        for item in failed_formatives:
            if item['weight'] == max_weight:
                print("- {}".format(item['assignment']))


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
