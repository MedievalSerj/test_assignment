from marshmallow import Schema, fields


class SourceSchema(Schema):
    id = fields.Integer()
    sid = fields.String()
    name = fields.String()
    url = fields.String()


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class UserSchema(Schema):
    id = fields.Integer()
    role = fields.Nested(RoleSchema)
    email = fields.String()
    username = fields.String()


class DocumentSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    text = fields.String()
    url = fields.String()
    created = fields.String()
    added_at = fields.Integer()
    updated = fields.Integer()
    times_edited = fields.Integer()
    user = fields.Nested(UserSchema)
    source = fields.Nested(SourceSchema)
