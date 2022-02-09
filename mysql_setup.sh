DB_USER=root
DB_PASSWD=password
DB_NAME=courseFinder
DB_PORT=3306
DB_HOST=localhost

# mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER --password=$DB_PASSWD <<EOF
# CREATE DATABASE $DB_NAME;
# EOF

mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER --password=$DB_PASSWD --database=$DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS Universities (
    id int NOT NULL auto_increment,
    name varchar(250)  NOT NULL default '',
    city varchar(250)  NOT NULL default '',
    state varchar(250)  NOT NULL default '',
    PRIMARY KEY (id)
);
EOF


mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER --password=$DB_PASSWD --database=$DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS Departments (
    id int NOT NULL auto_increment,
    name varchar(250)  NOT NULL default '',
    college_name varchar(250) default '',
    u_id int,
    PRIMARY KEY (id),
    FOREIGN KEY(u_id) REFERENCES Universities(id)
);
EOF


mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER --password=$DB_PASSWD --database=$DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS Degrees (
    id int NOT NULL auto_increment,
    name varchar(250)  NOT NULL default '',
    type varchar(250)  NOT NULL default '',
    descipline varchar(250) default '',
    u_id int,
    dept_id int,
    PRIMARY KEY (id),
    FOREIGN KEY(u_id) REFERENCES Universities(id),
    FOREIGN KEY(dept_id) REFERENCES Departments(id)
);
EOF


mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER --password=$DB_PASSWD --database=$DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS Courses(
    id int NOT NULL auto_increment,
    name varchar(250)  NOT NULL default '',
    description varchar(250) default '',
    code varchar(250) default '',
    term varchar(250) default '',
    u_id int,
    dept_id int,
    degree_id int,
    PRIMARY KEY (id),
    FOREIGN KEY(u_id) REFERENCES Universities(id),
    FOREIGN KEY(dept_id) REFERENCES Departments(id),
    FOREIGN KEY(degree_id) REFERENCES Degrees(id)
);
EOF