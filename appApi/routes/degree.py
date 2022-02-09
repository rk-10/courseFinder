# from main import app
from flask import Blueprint, make_response, request
from mysqldb.helper import query_db

degrees_blueprint = Blueprint('degree', __name__)


@degrees_blueprint.route('/all')
def degrees(u_id, dept_id):
    if u_id is None or dept_id is None:
        return handleError("Id not provided")
    query = "SELECT * FROM Degrees WHERE u_id=%s and dept_id=%s"
    try:
        result = query_db(query, (u_id, dept_id,))
    except:
        return handleError("Something went wrong!")
    return sendResponse("", result["data"])


@degrees_blueprint.route('/<int:id>', methods=['GET', 'POST'])
def degreeById(u_id, dept_id, id):
    if id is None or u_id is None:
        return handleError("Id not provided")

    if dept_id is None:
        return handleError("Id not provided")

    if request.method == 'POST':
        requestData = request.get_json()
        name = requestData["name"]
        type = requestData["type"]
        descipline = requestData["descipline"]
        query = """
        UPDATE Degrees SET
        name=%s,
        type=%s,
        descipline=%s
        WHERE id = %s and u_id=%s and dept_id=%s
        """
        args = (name, type, descipline, id, u_id, dept_id)
        try:
            result = query_db(query, args)
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])
    else:
        query = "SELECT * FROM Degrees WHERE id=%s and u_id=%s and dept_id=%s"
        try:
            result = query_db(query, (id, u_id, dept_id,))
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])


@degrees_blueprint.route('/', methods=['PUT'])
def newDegree(u_id, dept_id):
    if u_id is None or dept_id is None:
        return handleError("Id not provided")

    # requestData = request.get_json()
    name = request.form.get("name")
    type = request.form.get("type")
    descipline = request.form.get("discipline")
    query = """
    INSERT INTO Degrees
    (
        name,
        type,
        descipline,
        u_id,
        dept_id
    ) values(%s,%s,%s,%s,%s)
    """
    args = (name, type, descipline, u_id, dept_id)
    # result = query_db(query, args)
    try:
        result = query_db(query, args)
    except:
        return handleError("Something went wrong")
    return sendResponse("Added", {"id": result["lastrowid"]})


def handleError(message):
    return make_response({"status": "Error", "message": message}, 400)


def sendResponse(message, data):
    return make_response({"status": "SUCCESS", "message": message, "data": data}, 200)
