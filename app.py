import sqlite3
# Nový import:
import os
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, length
from wtforms import TextAreaField

app = Flask(__name__)
app.debug = True
app.secret_key = 'svsdfvsdfvbadb  sfgsgsrg'




aktualni_adresar = os.path.abspath(os.path.dirname(__file__))
databaze = (os.path.join(aktualni_adresar, 'poznamky.db'))

class PoznamkaForm(FlaskForm):
    poznamka = TextAreaField('Poznámka', validators=[DataRequired(), length(max=250)])


@app.route('/', methods=['GET', 'POST'])
def vloz_poznamku():
 
    form = PoznamkaForm()
    poznamka_text = form.poznamka.data
    if form.validate_on_submit():
        conn = sqlite3.connect(databaze)
        c = conn.cursor()
      
        c.execute("INSERT INTO poznamka(telo) VALUES (?)", (poznamka_text,))
        conn.commit()
        conn.close()
        return redirect('/poznamky')
    return render_template('vloz_poznamku.html', form=form)


@app.route('/poznamky')
def zobraz_poznamky():
 
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
   
    c.execute("SELECT rowid, telo, kdy FROM poznamka ORDER BY kdy desc")
   
    poznamky = c.fetchall()
    conn.close()
    return render_template('zobraz_poznamky.html', poznamky=poznamky)



@app.route('/smaz/<int:poznamka_id>')
def smaz_poznamku(poznamka_id):
   
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
  
    c.execute("DELETE FROM poznamka WHERE rowid=?", (poznamka_id,))
    conn.commit()
    conn.close()
    return redirect('/poznamky')




@app.route('/uprav/<int:poznamka_id>', methods=['GET', 'POST'])
def uprav_poznamku(poznamka_id):
  
    conn = sqlite3.connect(databaze)
    c = conn.cursor()
   
    c.execute("SELECT telo, kdy FROM poznamka WHERE rowid=?", (poznamka_id,))
   
    poznamka_tuple = c.fetchone()
    conn.close()
   
    form = PoznamkaForm(poznamka=poznamka_tuple[0])
    poznamka_text = form.poznamka.data
    if form.validate_on_submit():
        conn = sqlite3.connect(databaze)
        c = conn.cursor()
    
        c.execute("UPDATE poznamka SET telo=? WHERE rowid=?", (poznamka_text, poznamka_id,))
        conn.commit()
        conn.close()
        return redirect('/poznamky')
    return render_template('vloz_poznamku.html', form=form)


if __name__ == '__main__':
    app.run()
