from tortoise import fields, models


class User(models.Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=100)
    username = fields.CharField(max_length=50, null=True)
    role = fields.CharField(max_length=30)
    stars = fields.IntField(default=0)

    class Meta:
        table = "users"
        constraints = [
            "CONSTRAINT stars_nonnegative CHECK (stars >= 0)"
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='user_order')
    min_stars = fields.IntField()
    max_stars = fields.IntField()
    min_supply = fields.IntField()
    max_supply = fields.IntField()
    count = fields.IntField()
    receiver = fields.ForeignKeyField(
        'models.User', related_name='receiver_order')
    completed_count = fields.IntField(default=0)

    class Meta:
        table = "orders"

    def __str__(self):
        receiver_str = (
            f"<a href='https://t.me/{self.receiver.username}'>{self.receiver.name}</a>"
            if self.receiver.username and self.receiver.username != "none"
            else self.receiver.name
        )
        return (
            f" <b>Stars</b>: {self.min_stars}-{self.max_stars}⭐️\n"
            f"\t    <b>Supply</b>: {self.min_supply}-{self.max_supply}\n"
            f"\t    <b>Receiver</b>: {receiver_str}, <b>ID</b>: `{self.receiver.id}`\n"
            f"\t    <b>Remained</b>: {self.count - self.completed_count}, <b>Completed</b>: {self.completed_count}\n"
        )


class Transaction(models.Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='transactions')
    total_amount = fields.IntField()
    transaction_id = fields.CharField(max_length=128, unique=True)
    refund_status = fields.BooleanField(default=False)

    class Meta:
        table = "transactions"

    def __str__(self):
        return ((f"User: {self.user.id}, "
                 f"Amount: {self.total_amount}, "
                 f"Transaction ID: {self.transaction_id}"))
