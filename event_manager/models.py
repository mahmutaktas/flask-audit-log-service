from models import db, Base


class EventType(Base):
    __tablename__ = 'event_types'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    service_name = db.Column(db.String(255), nullable=False)


class EventTypeField(Base):
    __tablename__ = 'event_type_fields'

    __table_args__ = (
        db.UniqueConstraint('event_type_id', 'field_name'),
    )

    event_type_id = db.Column(db.Integer, db.ForeignKey('event_types.id'), primary_key=True)
    event_type = db.relationship('EventType', foreign_keys=[event_type_id], lazy=True)

    field_name = db.Column(db.String(255), primary_key=True)

    field_type = db.Column(db.String(255), nullable=False)
