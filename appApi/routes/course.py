# from main import app
from flask import Blueprint, make_response, request
from mysqldb.helper import query_db

course_blueprint = Blueprint('course', __name__)
independent_course_blueprint = Blueprint('inpependentcourse', __name__)


@course_blueprint.route('/all')
def courses(u_id, dept_id, degree_id):
    if u_id is None or dept_id is None:
        return handleError("Id not provided")

    if degree_id is None:
        return handleError("Id not provided")

    query = "SELECT * FROM Courses WHERE u_id=%s and dept_id=%s and degree_id=%s"
    try:
        result = query_db(query, (u_id, dept_id, degree_id,))
    except:
        return handleError("Something went wrong!")
    return sendResponse("", result["data"])


@course_blueprint.route('/<int:id>', methods=['GET', 'POST'])
def courseById(u_id, dept_id, degree_id, id):
    if id is None or u_id is None:
        return handleError("Id not provided")

    if dept_id is None or degree_id is None:
        return handleError("Id not provided")

    if request.method == 'POST':
        name = request.form.get("name")
        description = request.form.get("description")
        code = request.form.get("code")
        term = request.form.get("term")
        query = """
        UPDATE Courses SET
        name=%s,
        description=%s,
        code=%s,
        term=%s
        WHERE id = %s and u_id=%s and dept_id=%s and degree_id=%s
        """
        args = (name, description, code, term, id, u_id, dept_id, degree_id)
        try:
            result = query_db(query, args)
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])
    else:
        query = "SELECT * FROM Courses WHERE id=%s and u_id=%s and dept_id=%s and degree_id=%s"
        try:
            result = query_db(query, (id, u_id, dept_id, degree_id,))
        except:
            return handleError("Something went wrong")
        return sendResponse("", result["data"])


@course_blueprint.route('/', methods=['PUT'])
def newCourset(u_id, dept_id, degree_id):
    if u_id is None or dept_id is None:
        return handleError("Id not provided")

    if degree_id is None:
        return handleError("Id not provided")

    name = request.form.get("name")
    description = request.form.get("description")
    code = request.form.get("code")
    term = request.form.get("term")
    query = """
    INSERT INTO Courses
    (
        name,
        description,
        code,
        term,
        u_id,
        dept_id,
        degree_id
    ) values(%s,%s,%s,%s,%s,%s,%s)
    """
    args = (name, description, code, term, u_id, dept_id, degree_id)
    try:
        result = query_db(query, args)
    except:
        return handleError("Something went wrong")
    return sendResponse("Added", {"id": result["lastrowid"]})


@independent_course_blueprint.route('/')
def courses():
    courseName = request.args.get("search")
    u_id = request.args.get("uid")
    dept_id = request.args.get("deptid")
    degree_id = request.args.get("degreeid")
    query = "SELECT C.* FROM Courses C WHERE name LIKE IFNULL(%s,C.name) AND (C.u_id IN (IFNULL(%s, C.u_id)) AND C.dept_id IN (IFNULL(%s, C.dept_id)) AND C.degree_id IN (IFNULL(%s, C.degree_id)))"
    try:
        result = query_db(
            query, ('%'+courseName+'%', u_id, dept_id, degree_id))
    except:
        return handleError("Something went wrong!")
    return sendResponse("", result["data"])


def handleError(message):
    return make_response({"status": "Error", "message": message}, 400)


def sendResponse(message, data):
    return make_response({"status": "SUCCESS", "message": message, "data": data}, 200)
