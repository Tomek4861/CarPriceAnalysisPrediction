from ydata_profiling import ProfileReport

from utils import DBConnector

def do_profiling():
    db_connector = DBConnector()
    db_connector.connect()

    df = db_connector.fetch_data("SELECT * FROM passats")

    profile = ProfileReport(df, title="Passats Data Profiling Report")
    profile.to_file("passats_profiling.html")

    db_connector.close()

