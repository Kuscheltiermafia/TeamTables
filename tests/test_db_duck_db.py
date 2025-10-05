import duckdb

# create a connection to a file called 'file.db'
con = duckdb.connect(f"file.db")
# create a table and load data into it
con.sql("CREATE TABLE test2 (name STRING, age INTEGER)")
con.sql("INSERT INTO test2 VALUES ('Tom', 69)")
# query the table
con.table("test2").show()
# explicitly close the connection
con.close()
# Note: connections also closed implicitly when they go out of scope