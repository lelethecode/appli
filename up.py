from main import db
from model import Contact

# Example: Update all users to set `username` as not unique (if it was altered)
# or any other field updates you need.
Contact.query.update({Contact.username: 'new_username_value'})
db.session.commit()
