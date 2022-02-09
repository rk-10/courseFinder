DB_USER=root
DB_PASSWD=password
DB_NAME=courseFinder
DB_PORT=3306
DB_HOST=localhost

mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER --password=$DB_PASSWD --database=$DB_NAME <<EOF
DROP TABLE Courses;
DROP TABLE Degrees;
DROP TABLE Departments;
DROP TABLE Universities;
EOF

# mysql -h $DB_HOST -P $DB_PORT --protocol=tcp -u $DB_USER <<EOF
# DROP DATABASE $DB_NAME;
# EOF