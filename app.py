from flask import *
import boto3
import json
from sqlalchemy import true
from werkzeug.utils import secure_filename
import os
from cnxpool import cnxpool
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")

app.secret_key="gkiodgewrwjguiteirjj"



s3 = boto3.client('s3',
                    aws_access_key_id = ACCESS_KEY_ID,
                    aws_secret_access_key = ACCESS_SECRET_KEY,
                     )

BUCKET_NAME='aws-test-learn-s3'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/board' ,methods=['POST'])
def input_message():
  x = request.form
  print(x)
  message = request.form['message']
  print('留言', message)  
  if(len(request.files) != 0):
    img = request.files['file']
    filename = secure_filename(img.filename)
    print('圖檔',img)
    print('圖檔名稱',filename)
  try:
    s3.upload_fileobj(img,BUCKET_NAME,filename)
  except:
    return {"error": True, "message": "伺服器內部錯誤"}, 500
  try:
    cnx = cnxpool.get_connection()
    mycursor=cnx.cursor(dictionary = True)
    mycursor.execute("INSERT INTO board (message, image) VALUES (%s, %s)", (message, "https://d1kfzndf9j846w.cloudfront.net/"+filename))
  except:
    cnx.rollback()
    return {"error": True, "message": "伺服器內部錯誤"}, 500
  finally:
    mycursor.close()
    cnx.commit()
    cnx.close()
        
  return {'ok': True}, 200

@app.route('/api/board', methods=['GET'])
def get_message():
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(buffered = True, dictionary = True)
        cursor.execute("SELECT message, image FROM board")
        result = cursor.fetchall()
        print(result)
    except:
        return {"error": True, "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        cnx.close()

    return {'data': result}, 200


app.run(host='0.0.0.0', port=3306)
# app.run(debug=True, port=3000)