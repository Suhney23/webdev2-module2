from flask import Flask, send_from_directory, jsonify, make_response, request, g

#Creates flask application
def create_app():
    #Intialize app and data
    app = Flask(__name__)
    app.config['resume'] = {}

    #Route for home page
    @app.route('/')
    def hello_world():
        return "Hello, World!"
    
    #Validating the resume content
    def validate_resume(resume):
        #Expected keys in resume json
        keys = ['name', 'tagline', 'email', 'phone', 'address', 'socialLinks', 'objective', 'education', 'experience', 'skills']
        #Looping through keys and checking if key exists in resume
        for key in keys:
            #Returns False if key is not in the resume json
            if key not in resume:
                return False
        return True
    
    #Route for resume page. Includes all REST API methods
    @app.route('/resume', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def handle_resume():
        #switch case to handle all methods
        match request.method:
            case 'GET':
                if app.config['resume']:
                     return jsonify(app.config['resume']), 200
                else:
                    return make_response(jsonify({'error': 'Resume Not Found'}), 404)

            case 'POST':
                #gets resume from request
                resume = request.get_json()
                #if the resume is not valid return a 400 status code
                if not validate_resume(resume):
                    return make_response(jsonify({'error': 'Bad Request'}), 400)
                
                #if the resume exists return a 409 status code
                if app.config['resume']:
                    return make_response(jsonify({'error': 'Resume already exists'}), 409)
                else:
                    #set the resume equal to the requested one and return a 201 success status
                    app.config['resume'] = resume
                    return jsonify(app.config['resume']), 201

            case 'PUT':
                #if the resume does not exist return a 400 error
                if not app.config['resume']:
                    return make_response(jsonify({'error': 'No resume to update'}), 404)
                
                #get the resume 
                resume = request.get_json()

                #validate the resume
                if validate_resume(resume):
                    #if the resume is valid return a 200 success status code
                    app.config['resume'] = resume
                    return jsonify(app.config['resume']), 200
                else:
                    #if the data is invalid return a 400 error
                    return make_response(jsonify({'error': 'Bad Request'}), 400)

            case 'DELETE':
                #if there is not resume return a 404 status code
                if not app.config['resume']:
                    return make_response(jsonify({'error': 'No resume to delete'}), 404)
                
                #delete the resume and return a 204 status
                app.config['resume'] = {}
                return make_response('', 204)
            
            
    return app


