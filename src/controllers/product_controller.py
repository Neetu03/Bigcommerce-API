from src.Services import product_service
from flask import render_template,url_for
# from src.controllers.token_controller import token_exist
from src.controllers.token_controller import get_token_from_db
# from src.Repository.token_repository import TokenRepository
from flask import request,redirect,session
import requests
# import urllib.parse
from flask import jsonify

import base64
import io
from PIL import Image


REDIRECT_URI = 'https://9f93-14-139-105-18.ngrok-free.app/oauth/callback'
CLIENT_ID = '2dp4fv2foqurk0c9jdow7q6x2yqg2h5' 
CLIENT_SECRET = 'a06b19b8e079f7369bb5487a3d14a3a2b62291de197283cbeed339b08fa21922'

def login():
    auth_url = (
        f'https://login.bigcommerce.com/oauth2/authorize'
        f'?client_id={CLIENT_ID}&scope=store_v2_products'
        f'&redirect_uri={REDIRECT_URI}&response_type=code'
    )
    return redirect(auth_url)


def callback():
    code = request.args.get('code')
    context = request.args.get('context')

    if not code or not context:
        return "Missing authorization code or context.", 400

    token_url = 'https://login.bigcommerce.com/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'context': context,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, json=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        store_hash = context.split('/')[1]

        # Store in session
        session['access_token'] = access_token
        session['store_hash'] = store_hash

        print(f'Access token: {access_token} for store {store_hash}')
        print(f'Callback session: {session}')  # Check what session stores after callback

        return redirect(url_for('dashboard'))
    else:
        return 'Failed to fetch access token.', response.status_code



def dashboard():
    # Fetch access token from session
    print(f'Dashboard session: {session}')
    access_token = session.get('access_token')
    store_hash = session.get('store_hash')

    print(access_token)
    print(store_hash)

    if not access_token or not store_hash:
        return "Unauthorized access", 403

    # Proceed with rendering the dashboard if token exists
    return render_template('index.html')




def all_product_controller():
    print("all products called correctly")
    bigcommerce_store_hash = session['store_hash'].strip()

    # client_id=session['client_id']
    if not bigcommerce_store_hash:
        return jsonify({'error': 'Missing store hash in session'}), 400
    
    access_token =  session['access_token']
    
    if access_token:
        try:
            print("Store hash in allpc=",bigcommerce_store_hash.split()[0])
            products = product_service.get_all_products(CLIENT_ID,access_token, bigcommerce_store_hash.split()[0])
            # print(type(products))
            return jsonify({'data': products}), 200  # Return as JSON
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No access token found'}), 401
    




def product_controller(product_id):
    bigcommerce_store_hash = session['store_hash'].strip()
    if not bigcommerce_store_hash:
        return jsonify({'error': 'Missing store hash in session'}), 400
    
    access_token =  session['access_token']   
    if access_token:
        product= product_service.get_product_by_id(CLIENT_ID,access_token,product_id,bigcommerce_store_hash.split()[0])
        return jsonify({'data': product}), 200
    else:
        return {'error': 'No access token found'}, 401
    


def product_search_controller(query):
    bigcommerce_store_hash = session['store_hash'].strip()
    if not bigcommerce_store_hash:
        return jsonify({'error': 'Missing store hash in session'}), 400
    access_token = session['access_token'] 
    if access_token:
       product= product_service.search_products(CLIENT_ID,access_token,query,bigcommerce_store_hash.split()[0])
       if product:
        return jsonify({'data': product}), 200
       else:
           return jsonify({'message': 'No products found'}), 404
    else:
        return {'error': 'No access token found'}, 401
    


def product_update_controller(product_id):
    bigcommerce_store_hash = session['store_hash'].strip()
    try:
        data = request.json
    except Exception as e:
        print("Request cannot be json")
        return jsonify({'error': 'Request cannot be json'}), 400

    if not bigcommerce_store_hash:
        return jsonify({'error': 'Missing store hash in session'}), 400

    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'No access token found'}), 401

    # Decode base64 image if it's present
    image_base64 = data.get('image_base64')
    if image_base64:
        try:
            # Decode the base64 string to bytes
            image_data = base64.b64decode(image_base64)

            # Convert the byte data into an image
            image = Image.open(io.BytesIO(image_data))

            # Save the image to a file or pass it as a stream (BigCommerce requires a file-like object)
            image_file = io.BytesIO()
            image.save(image_file, format='PNG')  # You can change the format if needed
            image_file.seek(0)  # Reset the stream's position

            # Upload the image to BigCommerce (using their API)
            product = product_service.update_product_with_image(
                CLIENT_ID, access_token, product_id, bigcommerce_store_hash.split()[0], data, image_file
            )
        except Exception as e:
            print("Error decoding or uploading image:", e)
            return jsonify({'error': f"Failed to upload image: {e}"}), 500
    else:
        product = product_service.update_product(CLIENT_ID, access_token, product_id, bigcommerce_store_hash.split()[0], data)

    return {'data': product}, 200

