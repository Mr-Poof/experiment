#Created by AI for testing purposes
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, text, select

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

metadata = MetaData()
metadata.reflect(bind=engine)

@app.route("/get_all")
def get_all():
    suburb_table = metadata.tables['Suburbs']

    processedList = [] #list of suburbs after data formatting

    with engine.connect() as conn:
        getStats = text('SELECT "Official Name Suburb", "Tot_P_P", "Geo Point", "Geo Shape", "Median_rent_weekly" FROM Suburbs')

        getMax = text('SELECT MAX("Tot_P_P") FROM Suburbs')

        getMin = text('SELECT MIN("Tot_P_P") FROM Suburbs')

        result = conn.execute(getStats)

        max_result = conn.execute(getMax) 
        min_result = conn.execute(getMin) 

        for row in max_result:
            max = row[0]

        for row in min_result:
            min = row[0]

        
        for row in result:
            print(row)
            shape = json.loads(row[3])
            shape = shape["coordinates"]

            for coords in shape[0]:
                #print("Swapping")
                coords[0], coords[1] = coords[1], coords[0]
                #print(coords)
            #row[0] = name
            #row[1] = population
            #row[2] = point
            #row[3] = shape
            color = color_gradient(min, max, row[1])
            processedList.append((row[0], int(row[1]), row[2], shape, int(row[4]), color))
    
    return (processedList)


@app.route("/get_population/<suburb>")
def get_population(suburb):
    # Access a table (e.g., 'users')
    suburb_table = metadata.tables['Suburbs']

    with engine.connect() as conn:
        #stmt = select(suburb_table.)
        getStats = text('SELECT "Official Name Suburb", "Tot_P_P", "Geo Point", "Geo Shape" FROM Suburbs WHERE "Official Name Suburb" = :suburb_name')

        getMax = text('SELECT MAX("Tot_P_P") FROM Suburbs')

        getMin = text('SELECT MIN("Tot_P_P") FROM Suburbs')

        result = conn.execute(getStats, {"suburb_name": suburb})

        max_result = conn.execute(getMax) 
        min_result = conn.execute(getMin) 

        for row in max_result:
            max = row[0]

        for row in min_result:
            min = row[0]

        found = False
        for row in result:
            found = True
            print(f"{row[0]} has a population of {row[1]} residents")

        #print(row[3].jsonify)
            shape = json.loads(row[3])
            shape = shape["coordinates"]

            for coords in shape[0]:
                #print("Swapping")
                coords[0], coords[1] = coords[1], coords[0]
                #print(coords)

        #add a color-gradient based on population


    if found:
        return jsonify(population = row[1], coords = row[2], shape = shape[0], color = color_gradient(min, max, int(row[1])))
    else:
        return jsonify(population = "No Suburb With That Name Found", coords = "0")

def color_gradient(min, max, value):
    scaled_value = (value - min)/(max - min)
    r = int(175 * (1 - scaled_value))
    g = int(125 * scaled_value)
    b = 0
    return f'rgb({r},{g},{b})'

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(port = 5500, debug = True)