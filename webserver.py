from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

team_excluded_periods = {
    "mon": 0,
    "tue": 0,
    "wed": 0,
    "thu": 0,
    "fri": 0,
    "sat": 0,
    "sun": 0,
}


@app.route("/")
def run():
    return render_template("teams.html")


@app.route("/toggable_calendar")
def display_tep():
    return render_template("toggable_calendar.html")


@app.route("/cal-submit-data", methods=["POST"])
def handle_post():
    if request.method == "POST":
        day = request.get_json()['day']
        team_excluded_periods[day] ^= 1 << int(request.get_json()['hour'])
    return render_template("toggable_calendar.html")

@app.route('/cal-data-call')
def data():
    data = []
    for day, mask in team_excluded_periods.items():
        i = 0
        while mask > 0:
            if mask & 1:
                data.append([day, i])
            mask >>= 1
            i += 1
    return data



@app.route("/fields")
def display_k():
    return render_template("fields.html")


if __name__ == "__main__":
    app.run()
