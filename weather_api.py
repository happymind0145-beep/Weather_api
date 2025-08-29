from flask import Flask, render_template, request
import requests
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Cgir@j2025",  # your MySQL password
        database="Weather_db"
    )
    return conn

API_KEY = "98057c5b85e8b1d8e052e7dbddb5ae05"  

# Function to save weather data in DB
def save_weather_data(weather):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO weather_tbl 
        (city, country, temperature, feels_like, humidity, pressure, weather_main, weather_desc, wind_speed) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        weather["name"],
        weather["sys"]["country"],
        weather["main"]["temp"],
        weather["main"]["feels_like"],
        weather["main"]["humidity"],
        weather["main"]["pressure"],
        weather["weather"][0]["main"],
        weather["weather"][0]["description"],
        weather["wind"]["speed"]
    )

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
            save_weather_data(weather)  # Save each search into DB
        else:
            weather = None
    return render_template("index.html", weather=weather)



if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = 5000,debug=True)
