from flask import Flask,request,jsonify
import mysql.connector
import json
from mysql.connector import cursor
from waitress import serve

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
    cursor.execute("INSERT INTO `tb_config`(`idObj`, `lampu`) VALUES (%s,%s)",(idL,lampu))
    db.commit()

def cek_data_input(idL):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `idObj` FROM `tb_config` WHERE `idObj`=%s",(idL,))
    c = cursor.fetchone()
    if c == None:
        return True
    else:
        return False

def update_data(lampu,idL):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE `tb_config` SET `lampu`=%s WHERE `idObj`=%s",(lampu,idL))
    db.commit()

def get_data():
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `idObj`, `lampu` FROM `tb_config`")
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

def input_awal(IdObj):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO `tb_data`(`IdObj`, `Horizontal`, `Vertikal`, `Speed`) VALUES (%s,0,0,0)",(IdObj,))
    db.commit()

def update_for_refresh(IdObj):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE `tb_data` SET `Horizontal`=0,`Vertikal`=0,`Speed`=0 WHERE `IdObj`=%s",(IdObj,))
    db.commit()
    
def update_data_horizontal(value_horizontal,IdObj):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE `tb_data` SET `Horizontal`=%s WHERE `IdObj`=%s",(value_horizontal,IdObj))
    db.commit()
    
def cek_exist(IdObj):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `IdObj` FROM `tb_data` WHERE `IdObj`=%s",(IdObj,))
    c = cursor.fetchone()
    if c==None:
        return False
    else:
        return True
    
def update_data_vertikal(value_vertikal,IdObj):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE `tb_data` SET `Vertikal`=%s WHERE `IdObj`+%s",(value_vertikal,IdObj))
    db.commit()
    
def update_data_speed(value_speed,IdObj):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE `tb_data` SET `Speed`=%s WHERE `IdObj`=%s",(value_speed,IdObj))
    db.commit()
    
############################################################################################################

@app.route('/remote/starting',methods=['POST'])
def starting_get():
    json_data = request.json
    if json==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'IdObj' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            IdObj = json_data['IdObj']
            cek = cek_exist(IdObj)
            if cek==False:
                input_awal(IdObj)
                result={"message":"Object created"}
                resp = jsonify(result)
                return resp,202
            else:
                update_for_refresh(IdObj)
                result={"message":"Object refreshed"}
                resp = jsonify(result)
                return resp,200


@app.route('/remote/input/horizontal',methods=['POST'])
def input_horizontal():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'horizontal' not in json_data or 'IdObj' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            horizontal = json_data['horizontal']
            IdObj = json_data['IdObj']
            cek = cek_exist(IdObj)
            if cek==False:
                result = {"message":"No-Object"}
                resp = jsonify(result)
                return resp,204
            else:
                update_data_horizontal(horizontal,IdObj)
                result = {"message":"Success"}
                resp = jsonify(result)
                return resp,200


@app.route('/remote/input/vertikal',methods=['POST'])
def input_vertikal():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'vertikal' not in json_data or 'IdObj' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            vertikal = json_data['vertikal']
            IdObj = json_data['IdObj']
            cek = cek_exist(IdObj)
            if cek==False:
                result = {"message":"No-Object"}
                resp = jsonify(result)
                return resp,204
            else:
                update_data_vertikal(vertikal,IdObj)
                result = {"message":"Success"}
                resp = jsonify(result)
                return resp,200

@app.route('/remote/input/speed',methods=['POST'])
def input_speed():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'speed' not in json_data or 'IdObj' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            speed = json_data['speed']
            IdObj = json_data['IdObj']
            cek = cek_exist(IdObj)
            if cek==False:
                result = {"message":"No-Object"}
                resp = jsonify(result)
                return resp,204
            else:
                update_data_speed(speed,IdObj)
                result = {"message":"Success"}
                resp = jsonify(result)
                return resp,200


@app.route('/remote/get',methods=['GET'])
def get_remote():
    data = get_data()
    return data,200


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8001)
    app.run(port=8001, debug=True)