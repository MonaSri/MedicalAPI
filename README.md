# MedicalAPI
An API built in flask to provide search functions for a JSON file as well as CRUD operations. First attempt at a Flask project.

Program accepts curl functions to read and write to JSON.

API Commands

View all records
curl -i http://localhost:3000/search/all

View specific record by keyword
curl -i http://localhost:3000search?gender=Male

Delete record by id #
curl -X "DELETE" http://localhost:3000:search/1

Add new record
curl -i -H "Content-Type: application/json" -X POST -d @newperson.json http://localhost:3000/search

Update record by id #
curl -i -H "Content-Type: application/json" -X PUT -d "{"""first_name""":"""Bob"""}" http://localhost:3000/search/1
