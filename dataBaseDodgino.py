import mysql.connector as mysqlConnector


def commit_score(name,final_score):
    conn = mysqlConnector.connect(host = "localhost",
                              user = "root",
                              passwd = "",
                              database = "dodgino" 
                              )

    my_cursor = conn.cursor()

    my_cursor.execute(f"INSERT INTO score VALUES ('{name}',{final_score})")

    conn.commit()
    conn.close()

def get_score():
    conn = mysqlConnector.connect(host = "localhost",
                              user = "root",
                              passwd = "",
                              database = "dodgino" 
                              )

    my_cursor = conn.cursor()

    query = (f"SELECT name, points FROM score ORDER BY points DESC LIMIT 10")

    # Ejecutar la consulta y obtener los resultados
    my_cursor.execute(query)
    top_scores = my_cursor.fetchall()

    conn.close()

    return top_scores

    










