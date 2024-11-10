from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()
    first_name = fields.CharField(max_length=255)
    phone = fields.BigIntField()
    is_admin = fields.BooleanField(default=False, null=True)

    class Meta:
        table = "user"
