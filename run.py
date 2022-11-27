from Resources.Event import Event
from Resources.User import User
from Resources.Login import Login
from server import api, app, db

# This initializes the routers
api.add_resource(Event, '/events')
api.add_resource(User, '/users')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True)
