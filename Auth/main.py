from flask import Flask
from moduls.routes.login_route import login
from moduls.routes.auth_route import auth
from moduls.routes.refresh_access_token_route import refresh_access_token
from moduls.routes.refresh_route import refresh
from moduls.routes.register_route import register

# Create Flask Instance
app = Flask(__name__)


# Login Route
app.add_url_rule('/login', 'login', login, methods=['GET'])

# Auth Route
app.add_url_rule('/auth', 'auth', auth, methods=['POST'])

# Refresh Access Token Route - special for frontend only request
app.add_url_rule('/refresh_access_token', 'refresh_access_token', refresh_access_token, methods=['POST'])

# Refresh Token Route
app.add_url_rule('/refresh', 'refresh', refresh, methods=['POST'])

# Register Route
app.add_url_rule('/register', 'register', register, methods=['POST'])

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True, port=5000)