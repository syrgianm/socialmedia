from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb
from datetime import datetime
import os



app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminpass'
app.config['MYSQL_DB'] = 'socialmedia'

# Intialize MySQL
mysql = MySQL(app)



@app.route('/', methods= ['GET'])
def start():
    return render_template('/start_screen.html', msg='')

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    logfile = open(os.getcwd() + "/logfile.txt", "a")  # Take IPs of all who open the start screen
    now = datetime.now()
    logfile.write("IP address of client:" + request.remote_addr + " Visited on: " + now.strftime("%d/%m/%Y %H:%M:%S") + "\n")
    logfile.close()
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        # Create variables for easy access
        username = request.form['Username']
        password = request.form['Password']
        # query to check If Username in Database
        query = "SELECT Username,Password FROM profile WHERE Username= %s;"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, [username])
        account = cursor.fetchone()
        cursor.close()
        #If Username exist in database
        if account:
            #If Password matches
            if password == account['Password']:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['username'] = account['Username']
                return redirect(url_for('mainpage'))
            # Password Dont Matches
            else:
                return render_template('/start_screen.html', msg="Wrong Password")
            #If Username doesnt include in Database
        else:
            return render_template('/start_screen.html', msg="Wrong Username")
    return render_template('start_screen.html')

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    if (request.method == "POST") and (("Username" and "Phone" and "Email" and "Password" and "Repeat Password" and "Genre") \
            in request.form):

        # Query To Check If Username,Email,Phone are Unique in Database
        query = "SELECT Username,Email,Phone FROM socialmedia.profile;"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        account = cursor.fetchall()

        for row in account:
            # if username already exist in database
            if request.form['Username'] == row['Username']:
                return render_template('/register.html', msg = 'Username already exist')

            # If E-mail or Phone are already exist in database
            if ((request.form["Email"] == row['Email']) or (int(request.form["Phone"]) == row['Phone'])):
                return render_template('/register.html', msg = 'Email or Phone already in our database')

        # If Password and Passwrd Repeater Doesnt Match
        if request.form["Password"] != request.form["Password-Repeat"]:
            return render_template('/register.html', msg = 'Passwords doesnt match')

            # If Choosed A Personal Profile For Creation Account
        if request.form["Genre"] != "Page":
            # Query To Create The Profile in database
            query = f'INSERT INTO profile(Username,Password,Email,Phone,Street,City,Zip,Private) ' \
                    f'VALUES(%s,%s,' \
                    f'%s,%s,NULL,NULL,NULL,%s);'
            values = [request.form["Username"], request.form["Password"], request.form["Email"],
                      int(request.form["Phone"]), 0]

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.nextset()

            # Start the Personal Profile
            query = f'INSERT INTO personal(Username,DateofBirth,Age,Gender,Job,Status,FirstName,LastName)' \
                    f'Values(%s,"1990-10-19",{20},NULL,NULL,NULL,NULL,NULL);'
            values = [request.form["Username"]]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.nextset()

            #Insert Education
            queryEd = "INSERT INTO education_multiplevalue(Username,Education) VALUES(%s ,' ')"
            values = [request.form["Username"]]
            cursor.execute(queryEd, values)
            mysql.connection.commit()
            cursor.nextset()
            cursor.close()
            session['loggedin'] = True
            session['username'] = request.form['Username']
            return redirect(url_for('mainpage'))
        # If We have a Page Profile
        else:
            # Query for insert profile data
            query = f'INSERT INTO profile(Username,Password,Email,Phone,Street,City,Zip,Private) ' \
                    f'VALUES(%s,%s,' \
                    f'%s,%s,NULL,NULL,NULL,%s);'
            values = [request.form["Username"], request.form["Password"], request.form["Email"],
                      int(request.form["Phone"]), 0]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            # Start Page Profile
            query = f'INSERT INTO page(Username,Genre,Description,PageName) VALUES(%s,NULL,NULL,NULL)'
            values = [request.form["Username"]]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            session['loggedin'] = True
            session['username'] = request.form['Username']
            return redirect(url_for('mainpage'))
    return render_template('/start_screen.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/pythonlogin/MainPage', methods=['GET', 'POST'])
def mainpage():
    # Check if user is loggedin
    if 'loggedin' in session:
        Username = session['username']
        # User is loggedin show them the home page
        query = f'DROP TABLE IF EXISTS D; DROP TABLE IF EXISTS G; DROP TABLE IF EXISTS F;' \
                f'CREATE TEMPORARY TABLE D AS ' \
                f' (SELECT Username_1 AS Username_2, Username_2 AS Username_1 FROM friends ); ' \
                f' CREATE TEMPORARY TABLE G AS (SELECT Username_2 AS Username FROM friends  ' \
                f' WHERE Username_1 = %s) UNION (SELECT Username_2 AS Username ' \
                f' FROM D ' \
                f' WHERE Username_1 = %s); CREATE TEMPORARY TABLE F AS ' \
                f'(SELECT * FROM G) UNION  ' \
                f'(SELECT Page_Username AS Username FROM follow ' \
                f' WHERE Pers_Username = %s);' \
                f' INSERT INTO F(Username) VALUES(%s);'

        values = [Username, Username, Username, Username]
        queryRes = f' SELECT Date_Time,Description,post.Username,Photo_Video,post.PostID ' \
                   f' FROM post LEFT JOIN photo_video_multiplevalue ON post.PostID = photo_video_multiplevalue.PostID' \
                   f' JOIN F ON post.Username = F.Username ORDER BY post.Date_Time DESC LIMIT 20;' \

        queryComs = 'SELECT CommentID,comments.Date_Time,comments.Comment_Username,comments.Photo_Video,' \
                    'comments.Text,post.PostID FROM  post  JOIN F ON post.Username=F.Username ' \
                    'JOIN comments ON comments.PostID = post.PostID ' \
                    'ORDER BY comments.Date_Time;'
        queryLikes = '(SELECT likes_post.PostID,likes_post.Date_Time, likes_post.Likes_Username ' \
                     'FROM post JOIN F ON  post.Username=F.Username ' \
                     'JOIN likes_post ON likes_post.PostID=post.PostID ORDER BY likes_post.Date_Time);'
        queryPageorPers = 'Select Username From page WHERE Username = %s;'

        queryComLikes= f'SELECT Comment_Like_Username,post.PostID,CommentID ' \
                       f'FROM post JOIN F ON post.Username=F.Username ' \
                       f'JOIN likes_comment On likes_comment.PostID = post.PostID;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        cursor.execute(queryRes)
        result = cursor.fetchall()  # Take Posts Of friends and following pages
        cursor.execute(queryComs)
        resultC = cursor.fetchall()  # Take Comments of the above Posts
        cursor.execute(queryLikes)
        resultL = cursor.fetchall()  # Take Likes of the above Posts
        cursor.execute(queryPageorPers, [Username])
        resultisP = cursor.fetchone()  # Check if is Page or Personal Profile
        cursor.execute(queryComLikes)
        resultCl = cursor.fetchall() # Take all Comments_Likes From Above Post
        cursor.close()
        return render_template('MainPage.html', result=result, resultL=resultL, resultC=resultC,
                               Username = session['username'], resultisP=resultisP, resultCl = resultCl)
        # User is not loggedin redirect to login page

    return redirect(url_for('login'))

@app.route('/pythonlogin/profile', methods=['GET', 'POST'])
def profile():
   if 'loggedin' in session:
       # check if page or personal profile
       queryPageorPers = 'Select Username From page WHERE Username = %s;'
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute(queryPageorPers, [session['username']])
       resultisP = cursor.fetchone()  # IS PERSONAL==NONE
       cursor.close()
       if resultisP == None:
           query = f'SELECT DateOfBirth,Gender,Job,Status,FirstName,LastName,Street,City,Zip,Education ' \
                   f'FROM personal JOIN profile ON personal.Username = profile.Username ' \
                   f'JOIN education_multiplevalue ON personal.Username = education_multiplevalue.Username ' \
                   f'WHERE personal.Username = %s;'
           cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
           cursor.execute(query, [session['username']])
           resultInfos = cursor.fetchone()  # Take Info of Username
           cursor.close()
       else:
           query = f'SELECT Genre,Description,PageName,Street,City,Zip ' \
                   f'FROM page JOIN profile ON page.Username = profile.Username ' \
                   f'WHERE page.Username =%s;'
           cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
           cursor.execute(query, [session['username']])
           resultInfos = cursor.fetchone()  # Take Info of Username
           cursor.close()
       return render_template('Profile.html', username=session['username'],resultisP=resultisP,resultInfos=resultInfos)
   return redirect(url_for('login'))

@app.route('/pythonlogin/profile/Edit', methods=['GET', 'POST'])
def edit():
    if 'loggedin' in session:
        # check if page or personal profile
        queryPageorPers = 'Select Username From page WHERE Username = %s;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryPageorPers, [session['username']])
        resultPoP = cursor.fetchone()  # IS PERSONAL==NONE
        cursor.close()
        queryProf = "UPDATE profile SET Street = %s, City = %s, Zip= %s WHERE Username = %s ;"
        values = [request.form["Street"], request.form["City"], int(request.form["Zip"]), session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryProf, values)
        cursor.nextset()
        mysql.connection.commit()

        if resultPoP == None:  # IS PERSONAL
            # Update Personal Info of the Profile
            queryPers = "UPDATE personal SET DateOfBirth = %s, Gender = %s, Job = %s, Status = %s, FirstName = %s, " \
                        "LastName = %s WHERE Username = %s;"
            values = [request.form['DateOfBirth'], request.form["Gender"], request.form["Job"], request.form["Status"],
                      request.form["FName"], request.form["SName"], session['username']]
            cursor.execute(queryPers, values)
            mysql.connection.commit()
            cursor.nextset()
            # Insert Education of the Profile
            queryEd = "UPDATE education_multiplevalue Set Education=%s WHERE Username= %s;"
            values = [request.form["Education"], session['username']]
            cursor.execute(queryEd, values)
            mysql.connection.commit()
            cursor.nextset()
            cursor.close()

        else:

            # query to Update Page Info
            queryPage = "UPDATE page SET Genre=%s,Description=%s,PageName=%s WHERE Username= %s;"
            values = [request.form["Genre"], request.form["Description"], request.form["PageName"], session['username']]
            cursor.execute(queryPage, values)
            cursor.nextset()
            mysql.connection.commit()
            cursor.close()

        return redirect(url_for('profile'))
    return url_for('login')

@app.route('/pythonlogin/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        queryPageorPers = 'Select Username From page WHERE Username = %s;'
        querySearchProf = f'SELECT Username FROM profile WHERE Username LIKE %s;'
        value = [f"%{request.form['search']}%"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(querySearchProf, value)
        result = cursor.fetchall()
        cursor.execute(queryPageorPers, [session['username']])
        resultisP = cursor.fetchone()
        cursor.close()
        return render_template('Search.html', result=result, Username=session['username'], resultisP=resultisP)
    return redirect(url_for('login'))

@app.route('/pythonlogin/<username>', methods=['GET', 'POST'])
def visitprofile(username):
    if 'loggedin' in session:
        visitor = session['username']
        visited = username
        # check if page or personal profile
        queryPageorPers = 'Select Username From page WHERE Username = %s;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryPageorPers, [visited])
        resultisP = cursor.fetchone()  # IS PERSONAL==NONE the visited username
        cursor.close()
        queryvisitor = 'Select Username From page WHERE Username = %s;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryvisitor, [visitor])
        resultisPv = cursor.fetchone()  # IS PERSONAL==NONE the visitor username

        if resultisP == None:  # Visited is Personal
            query = f'SELECT DateOfBirth,Gender,Job,Status,FirstName,LastName,Street,City,Zip,Education ' \
                    f'FROM personal JOIN profile ON personal.Username = profile.Username ' \
                    f'JOIN education_multiplevalue ON personal.Username = education_multiplevalue.Username ' \
                    f'WHERE personal.Username = %s;'
            cursor.execute(query, [username])
            resultInfos = cursor.fetchone()  # Take Info of Username


        else:
            query = f'SELECT Genre,Description,PageName,Street,City,Zip ' \
                    f'FROM page JOIN profile ON page.Username = profile.Username ' \
                    f'WHERE page.Username =%s;'
            cursor.execute(query, [username])
            resultInfos = cursor.fetchone()  # Take Info of Username

        # Queries To Check if the Searched User is Friend,Friend Requested,or Nothing Above
        queryFriends = f'SELECT Username_1,Username_2 FROM friends WHERE (Username_1= %s ' \
                       f'AND Username_2=%s) OR (Username_1= %s ' \
                       f'AND Username_2=%s);'
        values = [visitor, visited, visited, visitor]
        cursor.execute(queryFriends, values)
        resultIsFriend = cursor.fetchone()  # Take If are friends
        queryRequests = f'SELECT From_Username,To_Username FROM friend_request ' \
                        f'WHERE (To_Username= %s AND From_Username =%s) OR' \
                        f'(To_Username = %s AND From_Username=%s);'
        values1 = [visited, visitor, visited, visitor]
        cursor.execute(queryRequests, values1)
        resultIsFriendRequested = cursor.fetchone()  # Take If is friend requested

        # Check if the Page is Followed By the User or not
        # Page_Username the followed and Pers_Username the follower
        query = 'SELECT Page_Username,Pers_Username FROM follow WHERE Page_Username=%s AND Pers_Username=%s ;'
        values = [visited, visitor]
        cursor.execute(query, values)
        resultIsFollowed = cursor.fetchone()
        cursor.close()
        return render_template('VisitProfile.html', visited=username, resultisP=resultisP, resultisPv=resultisPv,
                               resultInfos=resultInfos, visitor=session['username'], resultIsFriend=resultIsFriend,
                               resultIsFriendRequested=resultIsFriendRequested, resultIsFollowed=resultIsFollowed)

    return redirect(url_for('login'))

@app.route('/pythonlogin/<username>/follow', methods = ['GET', 'POST'])
def follow(username):
    if 'loggedin' in session:
        query = f'INSERT INTO follow(Page_Username,Pers_Username,Date_Time) ' \
                f'VALUES(%s, %s, %s);'
        values = [username, session['username'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('visitprofile', username=username))
    return redirect(url_for('login'))

@app.route('/pythonlogin/<username>/addfriend', methods = ['GET', 'POST'])
def addfriend(username):
    if 'loggedin' in session:
        query = f'INSERT INTO friend_request(From_Username,To_Username,Date_Time) ' \
                f'VALUES(%s,%s,%s);'
        values = [session['username'], username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('visitprofile', username=username))
    return redirect(url_for('login'))

@app.route('/pythonlogin/like/<postid>', methods= ['GET', 'POST'])
def like(postid):
    if 'loggedin' in session:
        postid = int(postid)
        # query to Insert the Like From the User
        query = f'INSERT INTO likes_post(PostID,Likes_Username,Date_Time) ' \
                f'VALUES(%s,%s,%s);'

        values = [postid, session['username'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('mainpage'))
    return redirect(url_for('login'))

@app.route('/pythonlogin/unlike/<postid>', methods= ['GET', 'POST'])
def unlike(postid):
    if 'loggedin' in session:
        postid = int(postid)
        # query to Insert the Like From the User
        query = f'DELETE FROM likes_post WHERE PostID = %s AND Likes_Username = %s;'
        values = [postid, session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('mainpage'))

    return redirect(url_for('login'))

@app.route('/pythonlogin/comment/<postid>', methods=['GET', 'POST'])
def comment(postid):
    if 'loggedin' in session:
        postid = int(postid)
        queryCheckComId = f'SELECT max(CommentID) FROM comments WHERE PostID=%s;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryCheckComId, [postid])
        result = cursor.fetchone()
        if result["max(CommentID)"]==None:
            PointerOfCommentID=1
        else:
            PointerOfCommentID = result["max(CommentID)"] + 1

        # Insert The comment in database
        query = f'INSERT INTO comments(CommentID,PostID,Comment_Username,Date_Time,Text,Photo_Video ) ' \
                f'VALUES(%s,%s,%s,' \
                f'%s,%s,"NULL");'
        values = [PointerOfCommentID, postid, session['username'],
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.form["Comment"]]
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('mainpage'))
    return redirect(url_for('login'))

@app.route('/pythonlogin/deletecomment/<postid>/<commentid>', methods=['GET','POST'])
def deletecomment(postid,commentid):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "DELETE FROM likes_comment WHERE CommentID=%s AND PostID=%s;"
        cursor.execute(query, [commentid, postid])
        mysql.connection.commit()
        cursor.nextset()
        query = "DELETE FROM comments WHERE CommentID=%s AND PostID=%s;"
        cursor.execute(query, [commentid,postid])
        mysql.connection.commit()
        cursor.nextset()
        cursor.close()
        return redirect(url_for('mainpage'))

    return redirect(url_for('login'))

@app.route('/pythonlogin/likecomment/<postid>/<commentid>', methods=['GET', 'POST'])
def likecomment(postid,commentid):
    if 'loggedin' in session:
        postid = int(postid)
        commentid = int(commentid)
        # query to Insert the Like From the User
        query = f'INSERT INTO likes_comment(PostID,CommentID,Comment_Like_Username,Date_Time) ' \
                f'VALUES(%s,%s,%s,%s);'

        values = [postid, commentid, session['username'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('mainpage'))
    return redirect(url_for('login'))
@app.route('/pythonlogin/unlikecomment/<postid>/<commentid>', methods=['GET', 'POST'])
def unlikecomment(postid,commentid):
    if 'loggedin' in session:
        postid = int(postid)
        commentid = int(commentid)
        # query to Insert the Comment-Like From the User
        query = f'DELETE FROM likes_comment WHERE PostID = %s AND CommentID=%s AND Comment_Like_Username = %s;'
        values = [postid, commentid, session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('mainpage'))

    return redirect(url_for('login'))
@app.route('/pythonlogin/post', methods =['GET', 'POST'])
def post():
    if 'loggedin' in session:
        queryCheckPostId = f'SELECT max(PostID) FROM post;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryCheckPostId)
        result = cursor.fetchone()
        if result["max(PostID)"] == None:
            PointerOfPostID=1
        else:
            PointerOfPostID = (result["max(PostID)"]) + 1
        cursor.close()
        # Query To Insert The Post From the User
        query = f'INSERT INTO post(PostID,Date_Time,Description,Username) ' \
                f'VALUES(%s, %s, %s, %s);'
        values = [PointerOfPostID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  request.form["WritePost"], session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()


        if request.form['PhotoUrl'] != '':

            # Query To insert Data
            query = f'INSERT INTO photo_video_multiplevalue(PostID,Photo_Video)' \
                    f'Values(%s, %s);'
            values = [PointerOfPostID, request.form["PhotoUrl"]]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()

        return redirect(url_for('mainpage'))
    return redirect(url_for('login'))

@app.route('/pythonlogin/deletepost/<postid>', methods=['GET', 'POST'])
def deletepost(postid):
    if 'loggedin' in session:
        query = "DELETE FROM likes_comment WHERE PostID=%s;"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, [int(postid)])
        mysql.connection.commit()
        cursor.nextset()
        query = "DELETE FROM likes_post WHERE PostID=%s;"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, [int(postid)])
        mysql.connection.commit()
        cursor.nextset()
        query = "DELETE FROM comments WHERE PostID=%s;"
        cursor.execute(query, [int(postid)])
        mysql.connection.commit()
        cursor.nextset()
        query = "DELETE FROM photo_video_multiplevalue WHERE PostID=%s;"
        cursor.execute(query, [int(postid)])
        mysql.connection.commit()
        cursor.nextset()
        query = "DELETE FROM post WHERE PostID=%s;"
        cursor.execute(query, [int(postid)])
        mysql.connection.commit()
        cursor.nextset()
        cursor.close()
        return redirect(url_for('mainpage'))
    return redirect(url_for('login'))

@app.route('/pythonlogin/friendrequests', methods = ['GET', 'POST'])
def friendrequests():
    if 'loggedin' in session:
        query = f'SELECT From_Username FROM friend_request WHERE To_Username=%s;'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, [session['username']])
        result = cursor.fetchall()
        cursor.close()
        return render_template('friendrequests.html', result=result)
    return redirect(url_for('login'))

@app.route('/pythonlogin/AcceptRequest/<username>', methods=['GET', 'POST']) #from username
def acceptrequest(username):
    if 'loggedin' in session:
        # query to delete friends
        query = f'DELETE FROM friend_request WHERE From_Username=%s AND To_Username=%s;'
        values = [username, session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        # query to insert Friends
        query = f'INSERT INTO friends(Username_1,Username_2,Date_Time)' \
                f'VALUES(%s,%s,%s);'
        values = [username, session['username'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('friendrequests'))
    return  redirect(url_for('login'))

@app.route('/pythonlogin/RejectRequest/<username>', methods = ['GET', 'POST'])
def rejectrequest(username):
        if 'loggedin' in session:
            # query to delete friend request:
            query = f'DELETE FROM friend_request WHERE From_Username=%s AND To_Username=%s;'
            values = [username, session['username']]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('friendrequests'))
        return redirect(url_for('login'))

@app.route('/pythonlogin/Unfriend/<username>', methods= ['GET', 'POST'])
def unfriend(username):
    if 'loggedin' in session:
        query = f'DELETE FROM friends WHERE (Username_1=%s AND Username_2=%s) OR (Username_1=%s AND Username_2=%s);'
        values = [username, session['username'], session['username'], username]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('visitprofile', username=username))
    return redirect(url_for('login'))

@app.route('/pythonlogin/Unfollow/<username>', methods= ['GET', 'POST'])
def unfollow(username):
    if 'loggedin' in session:
        query = f'DELETE FROM follow WHERE Page_Username=%s AND Pers_Username=%s;'
        values = [username,session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('visitprofile', username=username))

    return redirect(url_for('login'))

@app.route('/pythonlogin/UnsendRequest/<username>', methods=['GET','POST'])
def unsendrequest(username):
    if 'loggedin' in session:
        # query to delete friend request:
        query = f'DELETE FROM friend_request WHERE From_Username=%s AND To_Username=%s;'
        values = [session['username'],username]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('visitprofile',username=username))
    return redirect(url_for('login'))

@app.route('/pythonlogin/chathead', methods=['GET','POST'])
def chathead():
    if 'loggedin' in session:
        queryPageorPers = 'Select Username From page WHERE Username = %s;'
        query = f'DROP TABLE IF EXISTS G;DROP TABLE IF EXISTS D;DROP TABLE IF EXISTS F;CREATE TABLE G AS ' \
                f' SELECT DISTINCT From_Username AS Username FROM send_message WHERE From_Username = %s OR ' \
                f'To_Username = %s; CREATE TABLE D AS SELECT DISTINCT To_Username AS Username FROM send_message WHERE ' \
                f'From_Username = %s OR To_Username = %s; CREATE TABLE F AS (SELECT Username FROM G)  UNION ' \
                f'(SELECT Username FROM D); DELETE FROM F WHERE Username=%s;'
        values = [session['username'], session['username'], session['username'], session['username'],
                  session['username']]
        querychat = f'SELECT * FROM F'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryPageorPers, [session['username']])
        resultisP = cursor.fetchone()
        cursor.execute(query, values)
        cursor.execute(querychat)
        resultUserChatted = cursor.fetchall()
        cursor.close()
        return render_template('chathead.html', resultisP=resultisP, result=resultUserChatted)
    return redirect(url_for('login'))
@app.route('/pythonlogin/chat/<username>', methods=['GET','POST'])
def chat(username):
    if 'loggedin' in session:
        queryPageorPers = 'Select Username From page WHERE Username = %s;'
        query = f'SELECT Text,From_Username,To_Username,Date_Time FROM send_message WHERE (From_Username=%s AND To_Username =%s)'\
                f'OR (From_Username=%s AND To_Username=%s) ORDER BY Date_Time DESC LIMIT 50;'
        values = [session['username'], username, username, session['username']]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(queryPageorPers, [session['username']])
        resultisP = cursor.fetchone()
        cursor.execute(query, values)
        resultmes = cursor.fetchall()
        return render_template('chat.html', resultisP=resultisP, resultmes=resultmes, Username=session['username'],
                               chatwith=username)
    return url_for('login')
@app.route('/pythonlogin/sendmessage/<username>', methods=['GET', 'POST'])
def sendmessage(username):
    if 'loggedin' in session:
        # Query To Insert The Message From the User
        query = f'INSERT INTO send_message(Date_Time,Text,Was_Read,From_Username,To_Username) ' \
                f'VALUES(%s, %s, %s, %s,%s);'
        values = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.form["WriteMessage"], 1, session['username'],
                  username]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('chat', username=username))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()