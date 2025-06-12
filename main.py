from flask import Flask, render_template, request, redirect
import csv, os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    class_ = request.form['class']
    contact = request.form['contact']
    month = request.form['month']
    year = request.form['year']
    date = request.form['date']
    fee_paid = request.form['fee_paid']
    amount = request.form['amount']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    filename = f"{month}_{year}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Class", "Contact", "Month", "Year", "Date", "Fee Paid?", "Amount", "Start Date", "End Date"])
        writer.writerow([name, class_, contact, month, year, date, fee_paid, amount, start_date, end_date])

    return redirect(f'/students/{month}_{year}')

@app.route('/students/<filename>')
def students(filename):
    filepath = f"{filename}.csv"
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
    else:
        data = [["No records found."]]
    return render_template('students.html', data=data, month=filename.replace('_', ' '))

@app.route('/delete/<filename>/<int:index>')
def delete(filename, index):
    filepath = f"{filename}.csv"
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            rows = list(csv.reader(file))
        if 0 < index < len(rows):
            rows.pop(index)
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
    return redirect(f'/students/{filename}')

@app.route('/report/<filename>')
def report(filename):
    filepath = f"{filename}.csv"
    unpaid_students = []
    today = datetime.today()

    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[6].lower() == "no":
                    try:
                        end_date = datetime.strptime(row[9], "%Y-%m-%d")
                        days_left = (end_date - today).days
                        unpaid_students.append(row + [days_left])
                    except:
                        unpaid_students.append(row + ["Invalid date"])
    return render_template("unpaid_report.html", data=unpaid_students, month=filename.replace('_', ' '))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
