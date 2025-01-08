from flask import Flask, jsonify, request
from flask_cors import CORS
from moduls.routes.login_route import login
from moduls.routes.auth_route import auth
from moduls.routes.refresh_access_token_route import refresh_access_token
from moduls.routes.register_route import register

# Users
from moduls.routes.users.get_users import get_users
from moduls.routes.users.add_user import add_user

# Deliveries
from moduls.routes.deliveries.get_deliveries import get_deliveries
from moduls.routes.deliveries.add_deliveries import add_deliveries
from moduls.routes.deliveries.update_deliveries import update_deliveries
from moduls.routes.deliveries.delete_deliveries import delete_deliveries

# Delivery Details
from moduls.routes.delivery_details.get_delivery_details import get_delivery_details
from moduls.routes.delivery_details.add_delivery_details import add_delivery_details
from moduls.routes.delivery_details.update_delivery_details import update_delivery_details
from moduls.routes.delivery_details.delete_delivery_details import delete_delivery_details

# Inventory
from moduls.routes.inventory.get_inventory import get_inventory
from moduls.routes.inventory.check_item_number import check_item_number
from moduls.routes.inventory.update_inventory import update_inventory
from moduls.routes.inventory.delete_inventory import delete_inventory
from moduls.routes.inventory.add_inventory import add_inventory
from moduls.routes.inventory.put_back_from_scarce_commodity_inventory import put_back_from_scare_commodity_inventory

# Scarce commodity
from moduls.routes.scare_commoditiy_inventory.get_scarce_commodity_inventory import get_scarce_commodity_inventory
from moduls.routes.scare_commoditiy_inventory.add_scare_commodity_inventory import add_scare_commodity_inventory
from moduls.routes.scare_commoditiy_inventory.update_scarce_commodity_inventory import update_scarce_commodity_inventory
from moduls.routes.scare_commoditiy_inventory.delete_scarce_commodity_inventory import delete_scarce_commodity_inventory



# flask inst.
app = Flask(__name__)

# Initialize CORS with the correct origins
CORS(app, resources={r"/*": {
    "origins": "*",
    "allow_headers": "*",
    "supports_credentials": True
}})

# Login Route
app.add_url_rule('/login', 'login', login, methods=['POST'])

# Auth Route
app.add_url_rule('/auth', 'auth', auth, methods=['POST'])

# Refresh Access Token Route - special for frontend only request
app.add_url_rule('/refresh_access_token', 'refresh_access_token', refresh_access_token, methods=['POST'])

# Register Route
app.add_url_rule('/register', 'register', register, methods=['POST'])


# Users
# Get Users
app.add_url_rule('/get_users', 'get_users', get_users, methods=['GET'])

# Add User
app.add_url_rule('/add_user', 'add_user', add_user, methods=['POST'])


# Inventory
# Get Inventory
app.add_url_rule('/get_inventory', 'get_inventory', get_inventory, methods=['GET'])

# Check Item Number
app.add_url_rule('/check_item_number', 'check_item_number', check_item_number, methods=['POST'])

# Update Inventory
app.add_url_rule('/update_inventory', 'update_inventory', update_inventory, methods=['POST'])

# Delete Inventory
app.add_url_rule('/delete_inventory', 'delete_inventory', delete_inventory, methods=['POST'])

# Add Item Inventory
app.add_url_rule('/add_inventory', 'add_inventory', add_inventory, methods=['POST'])

#put_back_from_scare_commodity_inventory
app.add_url_rule('/put_back_from_scare_commodity_inventory', 'put_back_from_scare_commodity_inventory',
                 put_back_from_scare_commodity_inventory, methods=['POST'])


# Scare Commodity of Inventory
#Get Scarce Commodity Inventory
app.add_url_rule('/get_scarce_commodity_inventory', 'get_scarce_commodity_inventory', get_scarce_commodity_inventory, methods=['GET'])

# Add Scarce Commodity Inventory
app.add_url_rule('/add_scare_commodity_inventory', 'add_scare_commodity_inventory', add_scare_commodity_inventory, methods=['POST'])

# Update Scarce Commodity Inventory
app.add_url_rule('/update_scarce_commodity_inventory', 'update_scarce_commodity_inventory',
                 update_scarce_commodity_inventory, methods=['POST'])

# Delete Scarce Commodity Inventory and Inventory
app.add_url_rule('/delete_scarce_commodity_inventory', 'delete_scarce_commodity_inventory', delete_scarce_commodity_inventory, methods=['POST'])


# Deliveries
# Get Deliveries
app.add_url_rule('/get_deliveries', 'get_deliveries', get_deliveries, methods=['GET'])

# Get Deliveries
app.add_url_rule('/add_deliveries', 'add_deliveries', add_deliveries, methods=['POST'])

# Update Deliveries
app.add_url_rule('/update_deliveries', 'update_deliveries', update_deliveries, methods=['POST'])

# Delete Deliveries
app.add_url_rule('/delete_deliveries', 'delete_deliveries', delete_deliveries, methods=['POST'])


# Delivery Details
# Get Delivery Details
app.add_url_rule('/get_delivery_details', 'get_delivery_details', get_delivery_details, methods=['POST'])

# Add Delivery Details
app.add_url_rule('/add_delivery_details', 'add_delivery_details', add_delivery_details, methods=['POST'])

# Update Delivery Details
app.add_url_rule('/update_delivery_details', 'update_delivery_details', update_delivery_details, methods=['POST'])

# Delete Delivery Details
app.add_url_rule('/delete_delivery_details', 'delete_delivery_details', delete_delivery_details, methods=['POST'])


# Users
# Get Users
app.add_url_rule('/get_users', 'get_users', get_users, methods=['POST'])


# run flask server
if __name__ == '__main__':
    app.run(debug=True, port=5001)
