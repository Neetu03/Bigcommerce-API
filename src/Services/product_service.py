from src.Repository import product_repository
import json
from flask import jsonify, request

def get_all_products(client_id,access_token,store_hash):
    try:
        # print("Try of services")
        rep = product_repository.ProductRepository(client_id,access_token,store_hash)
        try:
            products = rep.api.Products.all()
            # print(type(products))
        except Exception as api_error:
            print(f"API Error: {api_error}")
            return jsonify({'error': 'Failed to fetch products'}), 500
        
        product_list = []
        for product in products:
            print(type(product))
            
            images = product.images()
            product_list.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'sku': product.sku,
                'images': [
                    {
                        'description': image.description,
                        "date_modified": image.date_modified,
                        "description": image.description,
                        "id": image.id,
                        "image_file": image.image_file,
                        "is_thumbnail": image.is_thumbnail,
                        "product_id": image.product_id,
                        "sort_order": image.sort_order,

                    }
                    for image in images
                ]
            })
        
        return product_list
    except Exception as e:
        return f"An error occurred: {e}"
    

def get_product_by_id(client_id,access_token,product_id,store_hash):
    try:
        rep = product_repository.ProductRepository(client_id,access_token,store_hash)
        try:
            # Fetch the product by ID
            product = rep.api.Products.get(product_id)
            # print(type(products))
        except Exception as api_error:
            print(f"API Error: {api_error}")
            return jsonify({'error': 'No such Product with productId Exists '}), 500
        try:

            images = product.images()
            
            # Create a response dictionary
            output = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'sku': product.sku,
                'images': [
                    {
                        'description': image.description,
                        "date_modified": image.date_modified,
                        "description": image.description,
                        "id": image.id,
                        "image_file": image.image_file,
                        "is_thumbnail": image.is_thumbnail,
                        "product_id": image.product_id,
                        "sort_order": image.sort_order,
                    }
                    for image in images
                ]
            }
        except Exception as api_error:
            return api_error
        return output
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def search_products(client_id,access_token,query,store_hash):
        try:
            rep = product_repository.ProductRepository(client_id,access_token,store_hash)
            # Use the BigCommerce API to search for products
            try:
                products = rep.api.Products.all()  
            except Exception as api_error:
                return jsonify(api_error)
            product_list = []
            for product in products:
                # print("into products means products are not empty ",product.name)
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                })

            matching_products = [product for product in product_list if query.lower() in product['name'].lower().strip()]
        
            if matching_products:
                # If we find a matching product, return it as a JSON response
                print("Expected product=", matching_products)
                return matching_products
            else:
                # If no products match, return an empty list
                return []

        except Exception as e:
            print(f"An error occurred: {e}")
            return []


def update_product(client_id, access_token, product_id, store_hash, update_data):
    try:
        rep = product_repository.ProductRepository(client_id, access_token, store_hash)
        try:
            updated_product = rep.api.Products.get(product_id).update(name= update_data['name'],price=update_data['price'],description=update_data['description'])
        except Exception as e:
            print("Getting error in api calling")
            return e

        # if 'name' in update_data:
        #     product.name = update_data['name']
        # if 'price' in update_data:
        #     product.price = update_data['price']
        # if 'description' in update_data:
        #     product.description = update_data['description']
        # if 'sku' in update_data:
        #     product.sku = update_data['sku']
        # try:
        #     updated_product = product.update(update_data)
        # except Exception as e:
        #     print("error while updating the product",e)
        #     return e
        try:
            product_data = {
            'id': updated_product.id,
            'name': updated_product.name,
            'price': updated_product.price,
            'description': updated_product.description,
            'sku': updated_product.sku,
            'images': updated_product.images(),
        }

        except Exception as e:
            print("Error during sending the  new data")
            return e

        return {
            'message': 'Product updated successfully',
            'product': product_data
        }

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500
    


def update_product_with_image(client_id, access_token, product_id, store_hash, update_data, image_file):
    try:
        rep = product_repository.ProductRepository(client_id, access_token, store_hash)
        
        # Update product details first (like name, description, etc.)
        updated_product = rep.api.Products.get(product_id).update(
            name=update_data.get('name'),
            price=update_data.get('price'),
            description=update_data.get('description')
        )

        # Upload the image to the product's image gallery
        image_response = rep.api.Products.Images.create(product_id, image_file=image_file)
        
        # Construct the final product data, including the newly uploaded image
        images_data = [image.url for image in updated_product.images()]

        # Add new image to the gallery
        images_data.append(image_response.url)

        product_data = {
            'id': updated_product.id,
            'name': updated_product.name,
            'price': updated_product.price,
            'description': updated_product.description,
            'sku': updated_product.sku,
            'images': images_data
        }

        return {
            'message': 'Product updated successfully with image',
            'product': product_data
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': f"An error occurred: {e}"}), 500


