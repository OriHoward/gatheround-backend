from Resources.Event import Event
from Resources.User import User
from Resources.Login import Login
from Resources.Refresh import Refresh
from Resources.Business import Business
from Resources.BusinessSearch import BusinessSearch
from Resources.BusinessSearchMetadata import BusinessSearchMetadata
from Resources.BusinessPackage import BusinessPackage
from Resources.RequestRouter import RequestRouter
from Resources.BookedDates import BookedDates
from server import api, app, db

# This initializes the routers
api.add_resource(Event, '/events', endpoint='events')
api.add_resource(Event, '/events/<int:event_id>', endpoint='event')
api.add_resource(User, '/users')
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')
api.add_resource(RequestRouter, '/requests')
api.add_resource(Business, '/business')
api.add_resource(BusinessSearch, '/business-search')
api.add_resource(BusinessSearchMetadata, '/business-search-meta')
api.add_resource(BusinessPackage, '/business-package')
api.add_resource(BookedDates, '/booked-dates')

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True)
