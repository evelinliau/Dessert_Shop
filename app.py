from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="dessert_shop",
    password="")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from chef where username = %s and password = %s")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["chef"] = username
        return redirect(url_for('admin'))
    else:
        return f"salah !!!"

@app.route('/logout')
def logout():
    session.pop("chef", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("chef"):
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    if session.get("chef"):
        cursor = mydb.cursor()
        name = request.form["Name"]
        description = request.form["Description"]
        allergens = request.form["Allergens"]
        calories = request.form["Calories"]
        price = request.form["Price"]
        rating = request.form["Rating"]
        query = ("insert into menu value( %s, %s, %s, %s, %s, %s, %s))")
        data = ( "", name, description, allergens, calories, price, rating)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect("/tampil")
    else:
        return redirect(url_for("home"))

@app.route('/tampil')
def tampil():
    if session.get("chef"):
        cursor = mydb.cursor()
        cursor.execute("select * from menu")
        data = cursor.fetchall()
        return render_template('tampil.html',datas=data) 
    else:
        return redirect(url_for("home"))
    
@app.route('/hapus/<id>')
def hapus(id):
    if session.get("chef"):
        cursor = mydb.cursor()
        query = ("delete from menu where id = %s")
        data = (id,)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

@app.route('/update/<id>')
def update(id):
    if session.get("chef"):
        cursor = mydb.cursor()
        query = ("select * from menu where id = %s")
        data = (id,)
        cursor.execute( query, data )
        value = cursor.fetchone()
        return render_template('update.html',value=value) 
    else:
        return redirect(url_for("home"))
    

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    if session.get("chef"):
        cursor = mydb.cursor()
        id = request.form["id"]
        name = request.form["Name"]
        description = request.form["Description"]
        allergens = request.form["Allergens"]
        calories = request.form["Calories"]
        price = request.form["Price"]
        rating = request.form["Rating"]
        query = ("update menu set name = %s, description = %s, allergens = %s, calories = %s, price = %s, rating = %s where id = %s")
        data = ( name, description, allergens, calories, price, rating, id, )
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(debug=True)