from flask import Flask,request,jsonify
import mysql.connector
import json

app = Flask(__name__)


def sql_connection():
    sql = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="",
                                  database="db_remote")
    return sql

def input_data(idL,lampu):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO `tb_config`(`id`, `lampu`) VALUES (%s,%s)",(idL,lampu))
    db.commit()

def cek_data_input(idL):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `id` FROM `tb_config` WHERE `id`=%s",(idL,))
    c = cursor.fetchone()
    if c == None:
        return True
    else:
        return False

def update_data(lampu,idL):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE `tb_config` SET `lampu`=%s WHERE `id`=%s",(lampu,idL))
    db.commit()

def get_data():
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `id`, `lampu` FROM `tb_config`")
    rows = [x for x in cursor]
    cols = [x[0] for x in cursor.description]
    datas = []
    for row in rows:
        data = {}
        for prop, val in zip(cols, row):
            data[prop] = val
        datas.append(data)
    dataJson = json.dumps(datas)
    return dataJson


@app.route('/remote/input',methods=['POST'])
def input_remote():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'id' not in json_data or 'lampu' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            idL = json_data['id']
            lampu = json_data['lampu']
            cek = cek_data_input(idL)
            if cek==False:
                update_data(lampu,idL)
                result = {"message": "Update Success"}
                resp = jsonify(result)
                return resp, 208
            else:
                input_data(idL,lampu)
                result = {"message": "Update Success"}
                resp = jsonify(result)
                return resp, 202

@app.route('/remote/get',methods=['GET'])
def get_remote():
    data = get_data()
    return data,200

if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8001)
    app.run(port=8001, debug=True)