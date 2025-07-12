import psycopg2

# pip install psycopg2

# docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
# localhost - 127.0.0.1
# \l - lista baz
# \q - wyjscie
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydatabase",
    user="myuser",
    password="mypassword"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);")

conn.commit()

cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Jan",))
cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Anna",))
conn.commit()

cursor.execute("SELECT * FROM users;")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
