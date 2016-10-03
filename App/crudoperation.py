from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as sql
app=Flask(__name__)

#home page
@app.route('/')
def home():
    return render_template('home.html')

#Enter customer info
@app.route('/enternew')
def new_cust():
    return render_template('customer.html')

#add record into customer table
@app.route('/added', methods=['POST'])
def addrec():
    name = request.form['name']
    email = request.form['email']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']
    country= request.form['country']
    with sql.connect('test.db') as con:
        cur = con.cursor()
	cur.execute("select EMAIL from customer where Email=?", (email,))
        data = cur.fetchall()
       	if data:
	    msg= " Email Id already exist !"
            return render_template("customer.html",msg = msg)
        else:
	    cur.execute('''insert into customer(NAME,EMAIL,STREET,CITY,STATE,PINCODE,COUNTRY,
				CREATED_AT,UPDATED_AT)
		                 values(?,?,?,?,?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)''',
		                 (name,email,street,city,state,pincode,country))
            con.commit()
	    return redirect(url_for('list'))
	    
#list customer info 
@app.route('/list')
def list():
    con = sql.connect("test.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from customer")

    rows = cur.fetchall()
    return render_template("list.html",rows1 = rows)

#update and delete customer info 
@app.route('/deleteupdate' , methods=['POST'])
def delete_update_record():
    if request.form['submit'] == 'Delete':
        con= sql.connect('test.db')
        cur = con.cursor()
        cur.execute("delete from customer where Email = ?",[request.form['entry_id']])
	con.commit()
	con.close()
	return redirect(url_for('list'))

    elif request.form['submit'] == 'Edit':
	con = sql.connect("test.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from customer where Email = ?",[request.form['entry_id']])
        rows = cur.fetchall()
	con.commit()
	con.close()
        return render_template("listupdate.html",rows1 = rows)

    elif request.form['submit'] == 'Update':
	name = request.form['name']
	email = request.form['email']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	pincode = request.form['pincode']
	country= request.form['country']
	emid=request.form['entry_id']
	con = sql.connect("test.db")
	cur = con.cursor()
	cur.execute('''update customer SET Name=?,Email=?,Street=?,City=?,State=?,Pincode=?,Country=?,
				Updated_at=CURRENT_TIMESTAMP where Email=?''',
	                      (name,email,street,city,state,pincode,country,emid))
	con.commit()
	con.close()
	return redirect(url_for('list'))

    elif request.form['submit'] == 'Cancel':
	return redirect(url_for('list'))

    elif request.form['submit'] == 'Add': #Add requirement to customer requirement table
	con = sql.connect("test.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select ID from customer where Email = ?",[request.form['entry_id']])
        rows = cur.fetchone()
	con.commit()
	con.close()
        return render_template("cust_requi.html",rows1 = rows)
    
    elif request.form['submit'] == 'Details': #Display customer Requirement
        con = sql.connect("test.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select ID from customer where Email = ?",[request.form['entry_id']])
	row1 = cur.fetchone()
	for row in row1:
	    cid=row;
	cur.execute("select * from CUST_R where ID=?",(cid,))
        row = cur.fetchall()
	return render_template("list1.html",rows1 = row) 

#search record
@app.route('/searchnew')
def search_record():
    return render_template('search.html')

#list search info
@app.route('/searchrecord', methods=['POST'])
def search():
    if request.form['submit'] == 'Cancel':
        return redirect(url_for('home'))
    elif request.form['submit'] == 'Search':
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        con = sql.connect("test.db")
    	con.row_factory = sql.Row
        cur = con.cursor()
	cur.execute('''select * from customer where Email LIKE ? or City LIKE ? or State LIKE ? or
			 Pincode LIKE ? ''',(email,city,state,pincode,))
        data = cur.fetchall()
	if not email and not city and not state and not pincode:
	   msg= "Please enter something..!"
	   return render_template("search.html",msg = msg)
	elif not data:
           msg= " Ooops record is not exist try again!"
           return render_template("search.html",msg = msg)
        else:
            return render_template("list.html",rows1 = data)

#Add requirement to customer requirement table
@app.route('/addedreq', methods=['POST'])
def addrequire():
    selected_val = request.form['laptop']
    cid = request.form['cid']
    with sql.connect('test.db') as con:
        cur = con.cursor()
	cur.execute('''insert into CUST_R(ID,CustRequirement,CREATED_AT,UPDATED_AT)
		          values(?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)''',(cid,selected_val,))
        con.commit()
	return redirect(url_for('list'))	

#Approve Disapprove requirement
@app.route('/deleteupdaterequire' , methods=['POST'])
def update_require():
    if request.form['submit'] == 'Edit':
	con = sql.connect("test.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select ID,Approved from CUST_R where ID = ?",[request.form['cid']])
        rows = cur.fetchone()
	con.commit()
        return render_template("updaterequire.html",rows1 = rows)

    elif request.form['submit'] == 'Update':
	approved1 = request.form['approved']
	idd=request.form['cid']
	con = sql.connect("test.db")
	cur = con.cursor()
	cur.execute('''update CUST_R SET Approved=?,Updated_at=CURRENT_TIMESTAMP where ID=?''',(approved1,idd,))
	con.commit()
	con.close()
	return redirect(url_for('list'))
	
    elif request.form['submit'] == 'Cancel':
	return redirect(url_for('list'))


if __name__=='__main__':
    app.run()

