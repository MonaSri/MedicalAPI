from flask import Flask, jsonify, request, abort
import json

SEARCH_TERMS = ['id', 'first_name', 'last_name', 'gender', 'phone_number', 'email', 'address', 'visit_date',
                'diagnosis', 'drug code']
SEARCH_TERMS2 = ['ssn', 'new_patient', 'race']

app = Flask(__name__)

# Read in JSON file
with open('MOCK_DATA.json') as json_data:
    patients = json.load(json_data)
    json_data.close()


# Return entire list of patients
@app.route('/search/all', methods=['GET'])
def api_all():
    return jsonify(patients)


# Search by key 'curl http://localhost:3000/search?first_name=Cyrill'
@app.route('/search', methods=['GET'])
def api_search():
    results = []
    args = request.args
    search_key = list(args.keys())[0]
    if search_key in SEARCH_TERMS:
        if search_key == 'id':
            search_value = int(request.args[search_key])
        else:
            search_value = str(request.args[search_key])
        for person in patients:
            if person[search_key] == search_value:
                results.append(person)
    elif search_key in SEARCH_TERMS2:
        search_value = str(request.args[search_key])
        for person in patients:
            if person['additional_information'][0][search_key] == search_value:
                results.append(person)
    else:
        return "Not a valid search term"

    if results:
        return jsonify(results)
    else:
        return "No records found"


# Function to create a patient
@app.route('/search', methods=['POST'])
def create_patient():
    if not request.json:
        abort(400)
    person = dict(id=patients[-1]['id'] + 1, first_name=request.json.get('first_name', ""),
                  last_name=request.json.get('last_name', ""), gender=request.json.get('gender', ""),
                  phone_number=request.json.get('phone_number', ""), email=request.json.get('email', ""),
                  address=request.json.get('address', ""), visit_date=request.json.get('visit_date', ""),
                  diagnosis=request.json.get('diagnosis', ""), drug_code=request.json.get('drug_code', ""),
                  additional_information=[
                      {
                          'notes': request.json.get('notes', ""),
                          'new_patient': request.json.get('new_patient', True),
                          'race': request.json.get('race', ""),
                          'ssn': request.json.get('ssn', "")
                      }
                  ])
    patients.append(person)
    with open('MOCK_DATA.json', 'w') as outfile:
        json.dump(patients, outfile)
    return jsonify({'person': person}), 201


# Function to update patient information by using their id number
@app.route('/search/<int:patient_id>', methods=['PUT'])
def update_person(patient_id):
    person = [person for person in patients if person['id'] == patient_id]
    if len(person) == 0:
        abort(404)
    if not request.json:
        abort(400)
    person[0]['first_name'] = request.json.get('first_name', person[0]['first_name'])
    person[0]['last_name'] = request.json.get('last_name', person[0]['last_name'])
    person[0]['gender'] = request.json.get('gender', person[0]['gender'])
    person[0]['phone_number'] = request.json.get('phone_number', person[0]['phone_number'])
    person[0]['email'] = request.json.get('email', person[0]['email'])
    person[0]['address'] = request.json.get('address', person[0]['address'])
    person[0]['visit_date'] = request.json.get('visit_date', person[0]['visit_date'])
    person[0]['diagnosis'] = request.json.get('diagnosis', person[0]['diagnosis'])
    person[0]['gender'] = request.json.get('gender', person[0]['gender'])
    person[0]['drug_code'] = request.json.get('drug_code', person[0]['drug_code'])
    person[0]['additional_information'][0]['race'] = request.json.get('race',
                                                                      person[0]['additional_information'][0]['race'])
    person[0]['additional_information'][0]['new_patient'] = request.json.get('new_patient',
                                                                             person[0]['additional_information'][0][
                                                                                 'new_patient'])
    person[0]['additional_information'][0]['ssn'] = request.json.get('ssn',
                                                                     person[0]['additional_information'][0]['ssn'])
    new_notes = person[0]['additional_information'][0]['notes'] + str('\n\n') + str(request.json.get('notes'))
    person[0]['additional_information'][0]['notes'] = new_notes
    with open('MOCK_DATA.json', 'w') as outfile:
        json.dump(patients, outfile)
    return jsonify({'person': person[0]})


# Function to delete patient by their id number
@app.route('/search/<int:patient_id>', methods=['DELETE'])
def delete_person(patient_id):
    person = [person for person in patients if person['id'] == patient_id]
    if len(person) == 0:
        abort(404)
    patients.remove(person[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
