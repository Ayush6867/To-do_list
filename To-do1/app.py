from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from datetime import timedelta
import stripe
from dotenv import load_dotenv
import os

from models import db, Todo
from schema import schema

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['UPLOADED_IMAGES_DEST'] = os.getenv('UPLOADS_DEST')

db.init_app(app)
CORS(app)

# Configure JWT manager
jwt = JWTManager(app)

# Create an UploadSet for handling image uploads
uploaded_images = UploadSet('images', IMAGES)

# Configure the upload settings
configure_uploads(app, uploaded_images)
patch_request_class(app)

# Set your Stripe API keys
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Register GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=jwt_required(GraphQLView.as_view('graphql', schema=schema, graphiql=True))
)


@app.route('/stripe/create-payment-intent', methods=['POST'])
@jwt_required
def create_payment_intent():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency')

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency
    )

    return jsonify(client_secret=intent.client_secret)


@app.route('/todos', methods=['POST'])
@jwt_required
def create_todo():
    current_user = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    time = data.get('time')
    images = data.get('images')
    is_pro = data.get('is_pro')

    if is_pro:
        if 'images' in request.files:
            image_filenames = []
            for file in request.files.getlist('images'):
                try:
                    filename = uploaded_images.save(file)
                    image_filenames.append(filename)
                except UploadNotAllowed:
                    return jsonify({'message': 'Invalid file type'}), 400
        else:
            return jsonify({'message': 'No files uploaded'}), 400
    else:
        image_filenames = []

    todo = Todo(
        title=title,
        description=description,
        time=time,
        images=image_filenames,
        user=current_user
    )
    db.session.add(todo)
    db.session.commit()

    return jsonify({'message': 'Todo created successfully'})


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required
def delete_todo(todo_id):
    current_user = get_jwt_identity()
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    if todo.user != current_user:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})


@app.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required
def get_todo(todo_id):
    current_user = get_jwt_identity()
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    if todo.user != current_user:
        return jsonify({'message': 'Unauthorized'}), 403

    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'time': todo.time,
        'images': todo.images
    })


@app.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required
def update_todo(todo_id):
    current_user = get_jwt_identity()
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    if todo.user != current_user:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.time = data.get('time', todo.time)
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'})


if __name__ == '__main__':
    app.run(debug=True)
