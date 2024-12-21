from src.controllers import product_controller
def initialize_routes(app):
    app.route('/', methods=['GET'])(product_controller.login)
    app.route('/products', methods=['GET'])(product_controller.all_product_controller)
    app.route('/products/<int:product_id>', methods=['GET'])(product_controller.product_controller)
    app.route('/products/search/<string:query>', methods=['GET'])(product_controller.product_search_controller)
    app.route('/products/update/<int:product_id>', methods=['PUT'])(product_controller.product_update_controller)
    app.route('/oauth/callback', methods=['GET'])(product_controller.callback)
    app.route('/dashboard', methods=['GET'])(product_controller.dashboard)