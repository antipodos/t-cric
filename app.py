from flask import Flask, render_template, request
import csv

app = Flask(__name__)


@app.route("/", methods=["GET"])
def web_home():
    return render_template("main.html")


@app.route("/process", methods = ['POST'])
def process():
    file_name = "data_file"
    data = list()
    labels = list()

    if request.method == 'POST' and file_name in request.files:
        f = request.files[file_name]
        f.save(f.filename)
        try:
            data, labels = read_data(f.filename)
        except (csv.Error, UnicodeDecodeError):
            return "upload a proper csv file you lazy bastards"

    return render_template('chart.html', data=data, labels=labels)


def read_data(filepath):
    data = list()
    labels = list()
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            data.append({"x": row["Completion time"], "y": row["What is your mood today?"]})
            labels.append("{}: {}".format(row["Name"], row["What made you feel that way?"]))

    return data, labels


if __name__ == '__main__':
    app.run()