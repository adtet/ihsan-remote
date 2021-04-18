from flask import Flask,request,jsonify
import mysql.connector

app = Flask(__name__)


def sql_connection():
    sql = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="",
                                  database="db_remote")
    return sql

@app.route('/remote/input',methods=['POST'])
def input_remote():
    json_data = request.json
    if json_data==None:
        



if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=6008)
    app.run(port=6008, debug=True)