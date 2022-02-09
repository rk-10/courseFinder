# from main import app
from flask import Blueprint, make_response, request
from mysqldb.helper import query_db

departments_blueprint = Blueprint('department', __name__)


@departments_blueprint.route('/all')
def departments(u_id):
    if u_id is None:
        return handleError("Id not provided")
    query = "SELECT * FROM Departments WHERE u_id=%s"
    try:
        result = query_db(query, (u_id,))
    except:
        return handleError("Something went wrong!")
    return sendResponse("", result["data"])


@departments_blueprint.route('/<int:id>', methods=['GET', 'POST'])
def departmentById(u_id, id):
    if id is None or u_id is None:
        return handleError("Id not provided")

    if request.method == 'POST':
        requestData = request.get_json()
        name = requestData["name"]
        college_name = requestData["college_name"]
        query = "UPDATE Departments SET name=%s, college_name=%s WHERE id = %s and u_id=%s"
        args = (name, college_name, id, u_id)
        try:
            result = query_db(query, args)
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])
    else:
        query = "SELECT * FROM Departments WHERE id=%s and u_id=%s"
        try:
            result = query_db(query, (id, u_id,))
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])


@departments_blueprint.route('/', methods=['PUT'])
def newDepartment(u_id):
    if u_id is None:
        return handleError("Id not provided")
    name = request.form.get("name")
    college_name = request.form.get("college_name")
    query = """
    INSERT INTO Departments
    (
        name,
        college_name,
        u_id
    ) values(%s,%s,%s)
    """
    args = (name, college_name, u_id)
    try:
        result = query_db(query, args)
    except:
        return handleError("Something went wrong")
    return sendResponse("Added", {"id": result["lastrowid"]})


def handleError(message):
    return make_response({"status": "Error", "message": message}, 400)


def sendResponse(message, data):
    return make_response({"status": "SUCCESS", "message": message, "data": data}, 200)
