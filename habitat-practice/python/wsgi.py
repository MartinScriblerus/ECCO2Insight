from flask_init import app

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=5000,use_reloader=True,debug=True)
    print(f"APP is: {app}")
    