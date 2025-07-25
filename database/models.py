from tortoise import fields, models

class Order(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    min_stars = fields.IntField()
    max_stars = fields.IntField()
    min_supply = fields.IntField()
    max_supply = fields.IntField()
    count = fields.IntField()
    receiver_id = fields.BigIntField()
    completed_count = fields.IntField(default=0)

    class Meta:
        table = "orders"

    def __str__(self):
        return (f"Stars: {self.min_stars}-{self.max_stars}, "
                f"Supply: {self.min_supply}-{self.max_supply}, "
                f"Count: {self.count}, Receiver: {self.receiver_id}, "
                f"Done: {self.completed_count}")
