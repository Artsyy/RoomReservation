from wtforms import Form, StringField, SelectField
 
class RoomSearchForm(Form):
    choices = [('Building', 'Building'),
               ('Room Name', 'Room Name'),
               ('Room Number', 'Room Number')]
    select = SelectField('Search for a room?:', choices = choices)
    search = StringField('')