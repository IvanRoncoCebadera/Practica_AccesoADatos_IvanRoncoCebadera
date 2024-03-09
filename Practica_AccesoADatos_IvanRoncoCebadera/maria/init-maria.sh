#!/bin/bash

echo "Creating MariaDB user ..."

mysql -u${MYSQL_USER} -p${MYSQL_ROOT_PASSWORD} <<EOF
CREATE USER '${MARIA_API_USER}'@'%' IDENTIFIED BY '${MARIA_API_PWD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MARIA_API_USER}'@'%';
FLUSH PRIVILEGES;
EOF
