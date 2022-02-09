from flask import Flask
from routes.university import universities_blueprint
from routes.department import departments_blueprint
from routes.degree import degrees_blueprint
from routes.course import course_blueprint, independent_course_blueprint

# create and configure the app
app = Flask(__name__)
app.register_blueprint(universities_blueprint, url_prefix='/university')
app.register_blueprint(departments_blueprint,
                       url_prefix='/university/<int:u_id>/department')
app.register_blueprint(degrees_blueprint,
                       url_prefix='/university/<int:u_id>/department/<int:dept_id>/degree')
app.register_blueprint(course_blueprint,
                       url_prefix='/university/<int:u_id>/department/<int:dept_id>/degree/<int:degree_id>/course')
app.register_blueprint(independent_course_blueprint, url_prefix='/courses')

if __name__ == '__main__':
    app.run(debug=True)
