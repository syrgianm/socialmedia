

#Create A Personal/Page User


/* //If we have already created User then DROP is neccesary so we uncomment the following commands:(If Exists doesnt work!)
DROP USER  User;
FLUSH PRIVILEGES;
*/
CREATE USER 'User'@'%' IDENTIFIED BY 'password';
GRANT SELECT,INSERT,DELETE,UPDATE,DROP,CREATE ON socialmedia.* TO 'User'@'%';


#Create Admin User

/* //If we have already created admin then DROP is neccesary so we uncomment the following commands:(If Exists doesnt work!)
DROP USER  admin@localhost;
FLUSH PRIVILEGES;
*/
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminpass';
GRANT ALL PRIVILEGES ON socialmedia.* TO 'admin'@'localhost';


