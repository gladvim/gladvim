import sqlite3


class DB:
    MIGRATIONS = """
    CREATE TABLE plugins
    (
        name TEXT UNIQUE,
        hash TEXT,
        local INTEGER,
        plug INTEGER
    );
    """

    RECORD = """
    INSERT INTO plugins (name, hash, local, plug)
    VALUES (?, ?, ?, ?);
    """

    RECORDED = """
    SELECT COUNT(*)
    FROM plugins
    WHERE name=?;
    """

    FETCHED = """
    SELECT local
    FROM plugins
    WHERE name=?;
    """

    PLUGGED = """
    SELECT plug
    FROM plugins
    WHERE name=?;
    """

    SET_FETCHED = """
    UPDATE plugins
    SET local=?
    WHERE name=?;
    """

    SET_PLUGGED = """
    UPDATE plugins
    SET plug=?
    WHERE name=?;
    """

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()

    def migrate(self):
        self.execute(DB.MIGRATIONS)

    def execute(self, *args):
        self.curs.execute(*args)
        self.conn.commit()

    def record(self, package, hash):
        self.execute(DB.RECORD, (package, hash, 1, 0))

    def recorded(self, package):
        self.execute(DB.RECORDED, (package,))
        count = self.curs.fetchone()
        return bool(count[0])

    def set_fetched(self, package, status=True):
        self.execute(DB.SET_FETCHED, (int(status), package))

    def set_plugged(self, package, status=True):
        self.execute(DB.SET_PLUGGED, (int(status), package))

    def fetched(self, package):
        self.execute(DB.FETCHED, (package,))
        boolean = self.curs.fetchone()
        return boolean and boolean[0]

    def plugged(self, package):
        self.execute(DB.PLUGGED, (package,))
        boolean = self.curs.fetchone()
        return boolean and boolean[0]
