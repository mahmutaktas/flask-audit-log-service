def populate_db(db):
    with open("tests/test_data.sql", encoding="utf8") as file:
        queries = file.readlines()
        for query in queries:
            db.session.execute(query)
            db.session.commit()
