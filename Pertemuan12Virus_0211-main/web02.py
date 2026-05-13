import os
import sqlite3
from flask import Flask, redirect, request, session, render_template

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_aman'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS time_line(id INTEGER PRIMARY KEY, content TEXT)')
    conn.execute('INSERT OR IGNORE INTO user VALUES (1, "alice", "alicepw")')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'username' in session:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        tl = conn.execute('SELECT * FROM time_line ORDER BY id DESC').fetchall()
        conn.close()
        return render_template('index.html', user=session['username'], tl=tl)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == 'admin' and p == '123':
            session['username'] = u
            return redirect('/')
    
    return '''
    <!DOCTYPE html>
    <html style="background:#0f172a; font-family:sans-serif; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
    <div style="background:rgba(255,255,255,0.05); padding:40px; border-radius:20px; border:1px solid rgba(255,255,255,0.1); width:320px; text-align:center;">
        <h2 style="color:#38bdf8; margin-bottom:25px;">Sign In</h2>
        <form method="post">
            <input name="username" placeholder="alice" style="width:100%; margin-bottom:15px; padding:12px; border-radius:8px; border:none; box-sizing:border-box;">
            <input name="password" type="password" placeholder="alicepw" style="width:100%; margin-bottom:25px; padding:12px; border-radius:8px; border:none; box-sizing:border-box;">
            <button type="submit" style="width:100%; padding:12px; background:#38bdf8; border:none; color:white; font-weight:bold; border-radius:8px; cursor:pointer;">LOGIN</button>
        </form>
    </div>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)