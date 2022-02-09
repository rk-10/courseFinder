# from main import app
from flask import Blueprint, make_response, request
import requests
from mysqldb.helper import query_db

universities_blueprint = Blueprint('university', __name__)


@universities_blueprint.route('/all')
def universities():
    query = "SELECT * FROM Universities"
    try:
        result = query_db(query)
    except:
        return handleError("Something went wrong!")
    return sendResponse("", result["data"])


@universities_blueprint.route('/<int:id>', methods=['GET', 'POST'])
def universityById(id):
    if id is None:
        return handleError("Id not provided")

    if request.method == 'POST':
        requestData = request.get_json()
        name = requestData["name"]
        city = requestData["city"]
        state = requestData["state"]
        query = "UPDATE Universities SET name=%s, city=%s, state=%s WHERE id = %s"
        args = (name, city, state, id)
        try:
            result = query_db(query, args)
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])
    else:
        query = "SELECT * FROM Universities WHERE id=%s"
        try:
            result = query_db(query, (id,))
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])


@universities_blueprint.route('/', methods=['PUT'])
def newUniversity():
    print(request.form.get('name'))
    print(request.data)
    # requestData = request.get_json()
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    query = """
    INSERT INTO Universities
    (
        name,
        city,
        state
    ) values(%s,%s,%s)
    """
    args = (name, city, state)
    try:
        result = query_db(query, args)
    except:
        return handleError("Something went wrong")
    return sendResponse("Added", {"id": result["lastrowid"]})


def handleError(message):
    return make_response({"status": "Error", "message": message}, 400)


def sendResponse(message, data):
    return make_response({"status": "SUCCESS", "message": message, "data": data}, 200)
