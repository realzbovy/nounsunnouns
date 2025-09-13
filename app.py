from flask import Flask, request, jsonify, render_template
import re, json, os

app = Flask(__name__)

noun_file = "custom_nouns.json"
non_noun_file = "custom_non_nouns.json"

def load_list(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return set(json.load(f))
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return set()

def save_list(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(list(data), f, ensure_ascii=False, indent=2)

custom_nouns = load_list(noun_file)
custom_non_nouns = load_list(non_noun_file)

def split_input_words(text):
    return [w.strip() for w in re.split(r'[\s,，]+', text) if w.strip()]

@app.route("/")
def index():
    return render_template("play.html")

@app.route("/manage")
def manage():
    return render_template("manage_words.html")

@app.route("/add_custom_nouns", methods=["POST"])
def add_custom_nouns():
    data = request.get_json()
    words = split_input_words(data.get("words", ""))
    added, existed, error = [], [], []
    for word in words:
        if not re.match(r'^[ก-๙]+$', word):
            error.append(word)
            continue
        if word in custom_nouns:
            existed.append(word)
            continue
        custom_nouns.add(word)
        if word in custom_non_nouns:
            custom_non_nouns.discard(word)
        added.append(word)
    save_list(custom_nouns, noun_file)
    save_list(custom_non_nouns, non_noun_file)
    return jsonify({"status": "ok", "added": added, "existed": existed, "error": error})

@app.route("/remove_custom_nouns", methods=["POST"])
def remove_custom_nouns():
    data = request.get_json()
    words = split_input_words(data.get("words", ""))
    removed, notfound = [], []
    for word in words:
        if word in custom_nouns:
            custom_nouns.remove(word)
            removed.append(word)
        else:
            notfound.append(word)
    save_list(custom_nouns, noun_file)
    return jsonify({"status": "ok", "removed": removed, "notfound": notfound})

@app.route("/add_custom_non_nouns", methods=["POST"])
def add_custom_non_nouns():
    data = request.get_json()
    words = split_input_words(data.get("words", ""))
    added, existed, error = [], [], []
    for word in words:
        if not re.match(r'^[ก-๙]+$', word):
            error.append(word)
            continue
        if word in custom_non_nouns:
            existed.append(word)
            continue
        custom_non_nouns.add(word)
        if word in custom_nouns:
            custom_nouns.discard(word)
        added.append(word)
    save_list(custom_non_nouns, non_noun_file)
    save_list(custom_nouns, noun_file)
    return jsonify({"status": "ok", "added": added, "existed": existed, "error": error})

@app.route("/remove_custom_non_nouns", methods=["POST"])
def remove_custom_non_nouns():
    data = request.get_json()
    words = split_input_words(data.get("words", ""))
    removed, notfound = [], []
    for word in words:
        if word in custom_non_nouns:
            custom_non_nouns.remove(word)
            removed.append(word)
        else:
            notfound.append(word)
    save_list(custom_non_nouns, non_noun_file)
    return jsonify({"status": "ok", "removed": removed, "notfound": notfound})

@app.route("/list_custom_nouns")
def list_custom_nouns():
    return jsonify(sorted(list(custom_nouns)))

@app.route("/list_custom_non_nouns")
def list_custom_non_nouns():
    return jsonify(sorted(list(custom_non_nouns)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)