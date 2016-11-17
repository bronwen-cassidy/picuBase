CREATE USER 'picuadmin'@'localhost' IDENTIFIED BY 'picuadmin';
create database picubase;

GRANT ALL ON picubase.* TO 'picuadmin'@'localhost';
FLUSH PRIVILEGES;