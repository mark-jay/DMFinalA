@ECHO OFF
:: [PTS: ADAPT]
set psqlPath="C:\Program Files\PostgreSQL\9.2\bin"


:: Database, Username and Port
SET dataBase=my_db
SET userName=postgres
SET portNumber=5432

::________________________________________________________________________
:: Connect to database and execute the instructions within psqlFile
:: psql -h host -p port -d database -U user -f psqlFile
:: (cf. postgresql-9.2-A4.pdf)
::________________________________________________________________________
%psqlPath%\psql -h localhost -p %portNumber% -d %dataBase% -U %userName% -f %1


:: uncomment next line in case there is a warning regarding the "code page"
:: cmd.exe /c chcp 1252


pause