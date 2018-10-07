import csv
import sqlite3

from util import data_for_dept


DATABASE = "force.sqlite3"
TABLES = ["Location", "Incident", "Officer", "Subject"]

# Core tables
CREATE_OFFICER_TABLE = """
    CREATE TABLE Officer (
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        sex TEXT NOT NULL,
        race TEXT NOT NULL,
        hired TEXT NOT NULL,
        exp INTEGER NOT NULL
    );
"""

CREATE_SUBJECT_TABLE = """
    CREATE TABLE Subject (
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        sex TEXT NOT NULL,
        race TEXT NOT NULL
    );
"""

CREATE_LOCATION_TABLE = """
    CREATE TABLE Location (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        state TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT NOT NULL,
        area INTEGER,
        beat INTEGER,
        section INTEGER,
        division TEXT,
        district TEXT,
        latitude REAL,
        longitude REAL
    );
"""

CREATE_INCIDENT_TABLE = """
    CREATE TABLE Incident (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        subject_id INTEGER,
        officer_id INTEGER,
        location_id INTEGER,

        date TEXT NOT NULL,
        time TEXT NOT NULL,

        off_injure_desc TEXT,
        off_hospit INTEGER,

        subj_injure_desc TEXT,

        cit_infl_a TEXT,
        charge TEXT,
        arrested INTEGER,

        FOREIGN KEY(subject_id) REFERENCES Subject(id),
        FOREIGN KEY(officer_id) REFERENCES Officer(id),
        FOREIGN KEY(location_id) REFERENCES Location(id)
    );
"""

TABLE_2_QUERY = {
    "Officer": CREATE_OFFICER_TABLE,
    "Subject": CREATE_SUBJECT_TABLE,
    "Location": CREATE_LOCATION_TABLE,
    "Incident": CREATE_INCIDENT_TABLE
}

# Create the database and its tables.
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
for table, query in TABLE_2_QUERY.items():
    cursor.execute("DROP TABLE IF EXISTS '{0}'".format(table))
    cursor.execute(query)


def insert_officer(cursor, row):
    """Add a column to the Officer table.
    """
    id_ = row[3].strip()
    if int(id_) <= 0:
        print("[WARNING]: Officer with ID = {0}".format(id_))
    sex = row[4].strip()
    race = row[5].strip()
    hired = row[6].strip()
    exp = row[7].strip()

    query = 'SELECT * FROM Officer WHERE id="{0}"'
    officer_id = cursor.execute(query.format(id_)).fetchone()
    if not officer_id:
        # We've never seen this officer before.
        cursor.execute(
            "INSERT INTO Officer(id, sex, race, hired, exp) VALUES (?,?,?,?,?)",
            [id_, sex, race, hired, exp]
        )

    return id_


def insert_subject(cursor, row):
    """Add a column to the Subject table.
    """
    id_ = row[11].strip()
    race = row[12].strip()
    sex = row[13].strip()

    query = 'SELECT * FROM Subject WHERE id="{0}"'
    subject_id = cursor.execute(query.format(id_)).fetchone()
    if not subject_id:
        cursor.execute(
            "INSERT INTO Subject(id, race, sex) VALUES (?,?,?)",
            [id_, race, sex]
        )

    return id_


def insert_location(cursor, row):
    """Add a column to the Location table.
    """
    area = row[19].strip()
    beat = row[20].strip()
    sect = row[21].strip()
    div = row[22].strip()
    dist = row[23].strip()
    addr = row[28].strip()
    city = row[29].strip()
    state = row[30].strip()
    lat = row[31].strip()
    long_ = row[32].strip()

    query = 'SELECT {0} FROM Location WHERE address="{1}"'
    loc_id = cursor.execute(query.format("id", addr)).fetchone()
    if not loc_id:
        cursor.execute("""
            INSERT INTO
            Location(
                state, city, address, area, beat, section, division, district,
                latitude, longitude
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            [state, city, addr, area, beat, sect, div, dist, lat, long_])
        loc_id = cursor.execute(query.format("id", addr)).fetchone()

    return loc_id[0]


CREATE_INCIDENT_TABLE = """
    CREATE TABLE Incident (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,

        date TEXT NOT NULL,
        time TEXT NOT NULL,

        off_injure_desc TEXT,
        off_hospit INTEGER,

        subj_injure_desc TEXT,
        subj_arrested INTEGER,

        cit_infl_a TEXT,
        charge TEXT,

        FOREIGN KEY(subject_id) REFERENCES Subject(id)
        FOREIGN KEY(officer_id) REFERENCES Officer(id)
        FOREIGN KEY(location_id) REFERENCES Location(id)
    );
"""

def insert_incident(cursor, row, off, sub, loc):
    """Add a column to the Incident table.
    """
    date = row[0].strip()
    time = row[1].strip()

    off_injure_desc = row[9].strip()
    off_hospit = row[10].strip()

    subj_injure_desc = row[15].strip()
    arrested = row[16].strip()

    cit_infl_a = row[17].strip()
    charge = row[18].strip()

    cursor.execute("""
            INSERT INTO Incident(
                date, time, off_injure_desc, off_hospit, subj_injure_desc,
                arrested, cit_infl_a, charge, subject_id, officer_id,
                location_id
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, [
                date, time, off_injure_desc, off_hospit, subj_injure_desc,
                arrested, cit_infl_a, charge, sub, off, loc])

if __name__ == "__main__":
    print("Generating SQLlite database ...")
    force = data_for_dept("Dept_37-00049", "**/*_.prepped.csv")[0]
    with open(force, "r") as csv_file:
        reader = csv.reader(csv_file)

        headers1 = next(reader)
        headers2 = next(reader)

        for i, row in enumerate(reader):
            officer_id = insert_officer(cursor, row)
            subject_id = insert_subject(cursor, row)

            location_id = insert_location(cursor, row)
            insert_incident(cursor, row, officer_id, subject_id, location_id)

    connection.commit()
    connection.close()
