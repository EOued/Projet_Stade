from flask import Flask, render_template, request
import json
import base64
import zlib

app = Flask(__name__)

data = {"teams": {
"""
format:
"id": {
"values":["name", portion(int), gametime(int), priority(int), field_type(int)]   
"excluded_days:[mon, tue, wes, thu, fri, sat, sun]
}
"""
}, "fields": {
"""
format:
"id": {
    "type": 0,
    "periods": [249600, 3840, 1036032, 0, 1036032, 1036224, 0]
}
"""

}}

tep_team = ""
fp_field = ""

@app.route("/")
def run():
    return render_template("index.html")

@app.route("/tables-send-data", methods=["POST"])
def tables_submit():
    print(request.get_json())
    return ""


@app.route("/toggable_calendar")
def display_tep():
    return render_template("toggable_calendar.html")


@app.route("/cal-submit-data", methods=["POST"])
def calendar_submit():
    # if request.method == "POST":
    #     day = request.get_json()["day"]
    #     isTeam = request.get_json()["isTeam"]
    #     mkey = "teams" if isTeam else "fields"
    #     key = tep_team if isTeam else fp_field
    #     data[mkey][key][day] ^= 1 << int(request.get_json()["hour"])
    return render_template("toggable_calendar.html")


@app.route("/cal-data-call")
def calendar_data():
    data = []
    for day, mask in team_excluded_periods.items():
        i = 0
        while mask > 0:
            if mask & 1:
                data.append([day, i])
            mask >>= 1
            i += 1
    return data


@app.route("/teams")
def display_t():
    return render_template("teams.html")


@app.route("/fields")
def display_k():
    return render_template("fields.html")


@app.route("/content_decoding", methods=["POST"])
def decode():
    if request.method == "POST":
        print(request)
        content = request.get_json()["content"]
        print(content)
        compressed_back = base64.b64decode(content.encode("utf-8"))
        json_str_back = zlib.decompress(compressed_back).decode("utf-8")
        decoded_dict = json.loads(json_str_back)
        print(decoded_dict)
        return {}, 200
    return {}, 500


@app.route("/content_encoding")
def encode():
    json_str = json.dumps(team_excluded_periods)
    print("uwu", json_str)
    compressed = zlib.compress(json_str.encode("utf-8"))
    encoded = base64.b64encode(compressed).decode("utf-8")
    print(encoded)
    return encoded


if __name__ == "__main__":
    app.run()
