from flask import Flask, redirect, render_template, url_for, request, flash, g
import os
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomethingWhatNoOneWillGuess'

app_info = {
    'db_file': 'C:/Users/szczy/Desktop/STUDIA/dodat/Esatto/data/patients.db'
}


def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


class Patient:
    def __init__(self, id, first_name, last_name, PESEL, street, city, zip_code):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.PESEL = PESEL
        self.street = street
        self.city = city
        self.zip_code = zip_code

    def __repr__(self) -> str:
        return f'<Patient first and last name: {self.first_name} {self.last_name}>'


class Medical_clinic:
    def __init__(self):
        self.patients = []

    def load_patients_from_db(self):
        db = get_db()
        cur = db.execute('SELECT * FROM Patients')
        rows = cur.fetchall()
        if not rows:
            self.load_patients()
            db = get_db()
            for patient in self.patients:
                db.execute('INSERT INTO Patients (first_name, last_name, PESEL, street, city, zip_code) VALUES (?, ?, ?, ?, ?, ?)',
                           (patient.first_name, patient.last_name, patient.PESEL, patient.street, patient.city, patient.zip_code))
            db.commit()

            cur = db.execute('SELECT * FROM Patients')
            rows = cur.fetchall()

        for row in rows:
            patient = Patient(row['id'], row['first_name'], row['last_name'],
                              row['PESEL'], row['street'], row['city'], row['zip_code'])
            self.patients.append(patient)

    def load_patients(self):
        self.patients.append(Patient(
            None, 'Łukasz', 'Kowalski', '11111111111', 'Budryka', 'Warszawa', '30-300'))
        self.patients.append(
            Patient(None, 'Jakub', 'Nowak', '22222222222', '3 maja', 'Kraków', '35-400'))
        self.patients.append(
            Patient(None, 'Igor', 'Wójcik', '33333333333', 'Wolności', 'Gdańsk', '22-220'))
        self.patients.append(Patient(None, 'Mateusz', 'Moskal',
                             '44444444444', 'Armii Krajowej', 'Wrocław', '45-300'))

    def add_patient_to_database(self, patient):
        db = get_db()
        sql_command = 'INSERT INTO Patients (first_name, last_name, PESEL, street, city, zip_code) VALUES (?, ?, ?, ?, ?, ?)'
        db.execute(sql_command, (patient.first_name, patient.last_name,
                   patient.PESEL, patient.street, patient.city, patient.zip_code))
        db.commit()

    def checking_if_someone_is_in_database(self, PESEL):
        for patient in self.patients:
            if patient.PESEL == PESEL:
                return True
        return False


@app.route('/')
def index():
    return render_template('index.html', active_menu='home')


@app.route("/adding_new_patient", methods=["GET", "POST"])
def adding_new_patient():

    Clinic = Medical_clinic()
    Clinic.load_patients_from_db()

    if request.method == "GET":
        return render_template("new_patient.html", active_menu='new_patient', Clinic=Clinic)
    else:
        first_name = ""
        if "first_name" in request.form:
            first_name = request.form["first_name"]

        last_name = ""
        if "last_name" in request.form:
            last_name = request.form["last_name"]

        PESEL = ""
        if "PESEL" in request.form:
            PESEL = request.form["PESEL"]

        street = ""
        if "street" in request.form:
            street = request.form["street"]

        city = ""
        if "city" in request.form:
            city = request.form["city"]

        zip_code = ""
        if "zip_code" in request.form:
            zip_code = request.form["zip_code"]

        if Clinic.checking_if_someone_is_in_database(PESEL):
            flash('The selected Patient is already in the database')
        else:
            db = get_db()
            sql_command = 'INSERT INTO Patients (first_name, last_name, PESEL, street, city, zip_code) VALUES (?, ?, ?, ?, ?, ?)'
            db.execute(sql_command, [first_name,
                       last_name, PESEL, street, city, zip_code])
            db.commit()
            flash('Request to add patient {} {} was accepted'.format(
                first_name, last_name))

        return render_template("patient_results.html", active_menu='new_patient',
                               first_name=first_name, last_name=last_name, PESEL=PESEL,
                               street=street, city=city, zip_code=zip_code,
                               patient_info=Clinic.checking_if_someone_is_in_database(PESEL))


@app.route("/our_patients", methods=["GET", "POST"])
def our_patients():
    db = get_db()

    if request.method == "GET":
        sql_command = 'SELECT * FROM Patients'
        cur = db.execute(sql_command)
        patients = cur.fetchall()
        return render_template('our_patients.html', active_menu='our_patients', patients=patients)
    else:
        sort_by = 'id'
        if "sort_by" in request.form:
            sort_by = request.form["sort_by"]

        print('sort_by: ', sort_by)
        if sort_by not in ['id', 'first_name', 'last_name', 'PESEL', 'street', 'city', 'zip_code']:
            sort_by = 'id'

        sql_command = f'SELECT * FROM Patients ORDER BY {sort_by};'
        cur = db.execute(sql_command)
        patients = cur.fetchall()
        return render_template('our_patients.html', active_menu='our_patients', patients=patients)


@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    db = get_db()
    sql_statement = 'DELETE FROM Patients WHERE id = ?;'
    db.execute(sql_statement, [patient_id])
    db.commit()

    return redirect(url_for('our_patients'))


@app.route('/about')
def about():
    return render_template('about.html', activate_menu='about')


@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    Clinic = Medical_clinic()
    Clinic.load_patients_from_db()
    db = get_db()

    if request.method == "GET":
        sql_statement = 'SELECT * FROM Patients WHERE id=?;'
        cur = db.execute(sql_statement, [patient_id])
        patient = cur.fetchone()

        if patient is None:
            flash('No such patient!')
            return redirect(url_for('our_patients'))
        else:
            return render_template("edit_patient.html", patient=patient, Clinic=Clinic, active_menu='new_patient')
    else:
        id = None
        if "id" in request.form:
            id = request.form["id"]

        first_name = ""
        if "first_name" in request.form:
            first_name = request.form["first_name"]

        last_name = ""
        if "last_name" in request.form:
            last_name = request.form["last_name"]

        PESEL = ""
        if "PESEL" in request.form:
            PESEL = request.form["PESEL"]

        street = ""
        if "street" in request.form:
            street = request.form["street"]

        city = ""
        if "city" in request.form:
            city = request.form["city"]

        zip_code = ""
        if "zip_code" in request.form:
            zip_code = request.form["zip_code"]

        if Clinic.checking_if_someone_is_in_database(PESEL):
            flash('The selected Patient is already in the database')
        else:
            sql_command = '''UPDATE Patients set first_name=?,
                                                last_name=?,
                                                PESEL=?,
                                                street=?,
                                                city=?,
                                                zip_code=?
                                                WHERE id=?'''
            db.execute(sql_command, [first_name,
                       last_name, PESEL, street, city, zip_code, patient_id])
            db.commit()
            flash('Patient was updated')

        return redirect(url_for('our_patients'))


if __name__ == '__main__':
    app.run()
