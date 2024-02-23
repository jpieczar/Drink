import re
import sqlite3
import requests
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html"), 200

def drink_info(drink):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={drink}"
    response = requests.get(url)
    if response.status_code == 200:
        abv = response.json()
        if abv['ingredients'] == None:
            return 0
        abv = abv['ingredients'][0]['strABV']
        return abv
    return 0

@app.route("/add_patron", methods=["POST"])
def add_patron():
    username = request.form['username']
    id_number = request.form['id_number']
    weight = request.form['weight']
    conn = sqlite3.connect("dataBase.db")

    if re.fullmatch(r"^[a-zA-Z\s]{2,10}$", username) == None:
        return redirect("/add")
    if re.fullmatch(r"^[0-9]{13}$", id_number) == None:
        return redirect("/add")
    if re.fullmatch(r"^[0-9]{1,3}$", weight) == None:
        return redirect("/add")

    c = conn.cursor()
    c.execute(f"INSERT INTO `patrons` (patron, id_number, saturation, weight) VALUES ('{username}', '{id_number}', 0, {int(weight)})")
    conn.commit()
    return redirect("/add")

# also delete all drinks for specified patron
@app.route("/delete_patron", methods=["POST"])
def delete_patron():
    patron = next(iter(dict(request.form.items())))
    conn = sqlite3.connect("dataBase.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM `patrons` WHERE patron = '{patron}'")
    c.execute(f"DELETE FROM `drinks` WHERE patron = '{patron}'")
    conn.commit()
    return redirect("/add")

@app.route("/add", methods=["GET"])
def create_patron():
    conn = sqlite3.connect("dataBase.db")
    c = conn.cursor()
    c.execute(f"SELECT patron FROM `patrons`")
    res = c.fetchall()
    res = [name[0] for name in res]
    return render_template("add.html", patron_list = res), 200

# list patrons
@app.route("/patron", methods=["GET"]) # GET
def list_patrons():
    conn = sqlite3.connect("dataBase.db")
    c = conn.cursor()
    c.execute(f"SELECT patron FROM `patrons`")
    res = c.fetchall()
    res = [name[0] for name in res]
    return render_template("patrons.html", patron_list = res), 200

@app.route("/patron/<user_id>", methods=["GET"]) # GET
def get_patron(user_id):
    conn = sqlite3.connect("dataBase.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM `patrons` WHERE `patron` = '{user_id}'")
    patron_res = c.fetchall()

    if len(patron_res) != 0:
        patron_id = patron_res[0][2]
        patron_saturation = patron_res[0][3]
        c.execute(f"SELECT price, drink FROM `drinks` WHERE patron = '{user_id}'")
        res = c.fetchall()
        return render_template("patron.html", patron = user_id, patron_id = patron_id, patron_saturation = patron_saturation, drink_list = res), 200
    return redirect("/patron")

@app.route("/add_drink", methods=["POST"])
def add_drink():
    patron = next(iter(dict(request.form.items())))
    drink = request.form[f'{next(iter(dict(request.form.items())))}']
    if re.fullmatch(r"^[a-zA-Z\s]{2,10}$", drink) == None:
        return redirect(f"/patron/{patron}")
    ABV = drink_info(drink)
    if ABV == None:
        ABV = 0
    conn = sqlite3.connect("dataBase.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO `drinks` (price, drink, ABV, patron) VALUES (10, '{drink}', {int(ABV)}, '{patron}')")
    conn.commit()
    c.execute(f"UPDATE `patrons` SET saturation = saturation + {float(ABV)} / (SELECT weight FROM `patrons` WHERE patron = '{patron}') WHERE patron = '{patron}'")
    conn.commit()
    return redirect(f"/patron/{patron}")

@app.route("/delete_drink", methods=["POST"])
def delete_drink():
    short_list = next(iter(dict(request.form.items()))).split('_')
    patron = short_list[0]
    drink = short_list[1]
    conn = sqlite3.connect("dataBase.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM `drinks` WHERE id = (SELECT id FROM `drinks` WHERE patron = '{patron}' AND drink = '{drink}' LIMIT 1)")
    conn.commit()
    return redirect(f"/patron/{patron}")

@app.route("/error")
@app.route("/error/<error_opt>")
def error(error_opt = ''):
    if error_opt == '':
        return render_template("error.html", error_opt = 500, msg = " "), 500
    if error_opt == "404":
        msg = "Page does not exist"
    else:
        msg = " "
    return render_template("error.html", error_opt = error_opt, msg = msg), error_opt

@app.errorhandler(Exception)
def page_not_found(error):
    try:
        code = getattr(error, 'code')
        print(f"{code} <- status of the request")
        return redirect(f"/error/{code}")
    except:
        return redirect("/error")

if __name__ == "__main__":
    app.run(debug = True)