from mongoengine import *
import datetime as dt
import uuid
import bcrypt

DEVICE_STATUS = ('good', 'bad', 'offline')
CARD_TYPES = (
    'simple-slider', 'simple-message', 'simple-value',
    'simple-switch', 'simple-button', 'rgb-slider',
    'video-stream', 'donut-chart', 'timeseries'
)

class Organization(Document):
    name = StringField(max_length=60, required=True)
    description = StringField(max_length=120, required=True)
    auth_key = StringField()
    devices = ListField(ReferenceField('Device'))
    updated_at = DateTimeField(default=dt.datetime.utcnow)
    created_at = DateTimeField()

    def save(self, *args, **kwargs):
        # Updates the creation date if not existing
        if not self.created_at:
            self.created_at = dt.datetime.utcnow()
        # Generates a hash password if one is not provided
        if not self.auth_key:
            salt = bcrypt.gensalt()
            self.auth_key = bcrypt.hashpw(uuid.uuid4(), salt)
        self.updated_at = dt.datetime.utcnow()
        return super(Organization, self).save(*args, **kwargs)

class Endpoint(EmbeddedDocument):
    name = StringField(max_length=20, required=True)
    description = StringField(max_length=120, required=True)
    # Title of the card display
    title = StringField(max_length=20, required=True)
    # Type of chart card
    card_type = StringField(max_length=30, choices=CARD_TYPES, required=True)
    # Measurement unit used for the card display
    unit = StringField(max_length=8, default="%")
    # Values expected on the Enpoint
    values = ListField(StringField(max_length=12), required=True)
    # In case the cardType is a simple switch
    labelSwitch = ListField(StringField())
    # Icons to show for switch or button types
    iconButton = ListField(StringField())

    def clean(self):
        """Ensures that the endpoints corresponds to each of the cards"""
        if str(self.card_type).startswith('simple-'):
            self.values = ['value']
        elif self.card_type is 'rgb-slider':
            self.values = ['r', 'g', 'b']
        elif self.card_type is 'video-stream':
            self.values = ['stream']
        elif self.card_type is 'donut-chart':
            self.values = ['labels', 'data']
        elif self.card_type is 'timeseries':
            self.values = ['x', 'y']
        else:
            raise ValidationError("Invalid card type for endPoint")

class Device(Document):
    id = ObjectIdField(primary_key=True, unique=True, required=True)
    name = StringField(max_length=60, required=True)
    description = StringField(max_length=120)
    status = StringField(max_length=10,
                        default=DEVICE_STATUS[-1],
                        choices=DEVICE_STATUS)
    updated_at = DateTimeField(default=dt.datetime.utcnow)
    created_at = DateTimeField()
    endpoints = EmbeddedDocumentListField(Endpoint)

    def save(self, *args, **kwargs):
        # Updates the creation date if not existing
        if not self.created_at:
            self.created_at = dt.datetime.utcnow()
        self.updated_at = dt.datetime.utcnow()
        return super(Device, self).save(*args, **kwargs)
