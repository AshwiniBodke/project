#Tables 1.CUSTOMER , 2.CUST_R
import sqlite3
conn=sqlite3.connect('test.db')
conn.execute('''CREATE TABLE CUSTOMER
	(ID integer PRIMARY KEY AUTOINCREMENT,NAME TEXT,
	EMAIL VARCHAR(320),
	STREET CHAR(50),
	CITY CHAR(50),
	STATE CHAR(50),
	PINCODE INT,
	COUNTRY CHAR(50),
	CREATED_AT TEXT,UPDATED_AT TEXT);''')
print "Table Created Successfully";

conn.execute('''CREATE TABLE CUST_R
	(ID INTEGER,
	CustRequirement varchar(100),
	Approved BOOLEAN 
	CHECK(Approved IN (0,1)) DEFAULT 0,
	CREATED_AT TEXT,UPDATED_AT TEXT,
	 FOREIGN KEY(ID) REFERENCES CUSTOMER(ID)  );''')
print "Table Created Successfully";

"""
conn.execute('''INSERT INTO CUSTOMER1(EMAIL,STREET,CITY,STATE,PINCODE,
COUNTRY,CREATED_AT,UPDATED_AT)
VALUES
 ("abc@gmail.com","abc","abc","abc",123456,"abc",CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),
("xyz@gmail.com","xyz","xyz","xyz",123456,"xyz",CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);''')

conn.execute('''insert into CUST_R1
(ID,CustRequirement,CREATED_AT,UPDATED_AT)values(1,"abc",CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),
(2,"abc",CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);''')

cursor=conn.execute('''SELECT CUSTOMER1.ID,CUST_R1.CustRequirement,CUST_R1.Approved,CUST_R1.CREATED_AT,
CUST_R1.UPDATED_AT
FROM CUSTOMER1
INNER JOIN CUST_R1
ON CUSTOMER1.ID=CUST_R1.ID''')
print "data inserted"
"""
conn.close()
