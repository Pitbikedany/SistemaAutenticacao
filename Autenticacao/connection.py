import mysql.connector
#conexao com a database
mydatabase = mysql.connector.connect(host="localhost", user="root", database="autenticacao")
myqueries = mydatabase.cursor()