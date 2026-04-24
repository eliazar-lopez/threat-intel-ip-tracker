from flask import Flask, render_template, request, send_file
from threat_checker import check_ip
import re
import csv

app = Flask(__name__)

results = []

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        ip = request.form.get("ip")
        log_data = request.form.get("log_data")
        file = request.files.get("file")

        if ip:
            results.append(check_ip(ip))

        elif log_data:
            ips = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", log_data)
            for ip in set(ips):
                results.append(check_ip(ip))

        elif file and file.filename != "":
            content = file.read().decode("utf-8")
            ips = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", content)
            for ip in set(ips):
                results.append(check_ip(ip))

    return render_template("dashboard.html", results=results)

@app.route("/export")
def export():

    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["IP", "Country", "Organization", "Reports", "Threat Level"])

        for r in results:
            writer.writerow([
                r["ip"],
                r["country"],
                r["org"],
                r["reports"],
                r["threat_level"]
            ])

    return send_file("report.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)