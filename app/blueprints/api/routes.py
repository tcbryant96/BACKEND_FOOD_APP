from . import api
from flask import jsonify, request
from app.models import User, Cart, Fridge, Recipes
from .auth import basic_auth, token_auth
from flask_cors import cross_origin

@api.route('/token',  methods=['POST'])
@basic_auth.login_required
def get_token():
    user =basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})

@api.route('/users/')
@token_auth.login_required
def get_user():    
    user = token_auth.current_user()
    return user.to_dict()

@api.route('/user', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for user in ['username', 'email','password']:
        if user not in data:
            return jsonify({'error': f'{user} must be in request body'}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get("password")
    new_user= User(username=username, email=email, password=password)
    return jsonify(new_user.to_dict()), 201


@api.route('/cart', methods=["POST"])
@token_auth.login_required
def add_item():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for field in ['item', 'quantity']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    item = data.get('item')
    quantity = data.get('quantity')
    user = token_auth.current_user()
    user_id = user.id

    new_item = Cart(item =item, quantity=quantity, user_id=user_id)
    return jsonify(new_item.to_dict()), 201



@api.route('/cart/<id>')
def get_item(id):
    item = Cart.query.get_or_404(id)
    return jsonify(item.to_dict())

@api.route('/cart/<id>', methods=['PUT'])
@token_auth.login_required    
def edit_cart(id):
    item = Cart.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != item.user_id:
        return jsonify({'error': 'You are not allowed to edit this.'}), 403
    data = request.json
    item.update(data)
    return jsonify(item.to_dict())

@api.route('/cart/<id>', methods=['DELETE'])
@token_auth.login_required
def delete_item_cart(id):
    item = Cart.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != item.user_id:
        return jsonify({'error': 'You are not allowed to delete this'}), 403
    item.delete()
    return jsonify({'success': f'{item.item} has been deleted'})

@api.route('/cart/user/')
@cross_origin()
@token_auth.login_required
def my_cart():
    user = token_auth.current_user()
    cart = Cart.query.filter_by(user_id=user.id).all()
    items = []
    for c in cart:
        items.append(c.to_dict())
    
    return jsonify(items)

@api.route('/fridge/user')
@token_auth.login_required
def my_fridge():
    user = token_auth.current_user()
    fridge = Fridge.query.filter_by(user_id=user.id).all()
    items =  []
    for f in fridge:
        items.append(f.to_dict())
    return jsonify(items)

@api.route('/fridge/<id>', methods=['PUT'])
@token_auth.login_required    
def edit_fridge(id):
    item = Fridge.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != item.user_id:
        return jsonify({'error': 'You are not allowed to edit this.'}), 403
    data = request.json
    item.update(data)
    return jsonify(item.to_dict())

@api.route('/fridge/<id>', methods=['DELETE'])
@token_auth.login_required
def delete_item_fridge(id):
    item = Fridge.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != item.user_id:
        return jsonify({'error': 'You are not allowed to delete this'}), 403
    item.delete()
    return jsonify({'success': f'{item.item} has been deleted'})

@api.route('/fridge', methods=["POST"])
@token_auth.login_required
def add_fridge():
    
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for field in ['item', 'quantity']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    item = data.get('item')
    quantity = data.get('quantity')
    user = token_auth.current_user()
    user_id = user.id
    new_item = Fridge(item=item, quantity=quantity, user_id=user_id)
    return jsonify(new_item.to_dict()), 201

@api.route('/recipes')
@token_auth.login_required
def get_recipes():
    user = token_auth.current_user()
    recipe = Recipes.query.filter_by(user_id=user.id).all()
    recipes = []
    for r in recipe:
        recipes.append(r.to_dict())
    
    return jsonify(recipes)


@api.route('/recipes', methods=["POST"])
@token_auth.login_required
def add_recipe():
    
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for field in ['recipe']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    recipe = data.get('recipe')
    user = token_auth.current_user()
    user_id = user.id
    new_item = Recipes(recipe=recipe, user_id=user_id)
    return jsonify(new_item.to_dict()), 201
