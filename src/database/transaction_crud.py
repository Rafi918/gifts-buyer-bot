from .models import Transaction
from .users_crud import add_user_stars


async def add_transaction(user_id, total_amount, transaction_id):
    await Transaction.create(
        user_id=user_id,
        total_amount=total_amount,
        transaction_id=transaction_id
    )

    return await add_user_stars(user_id, total_amount)


async def get_transaction(transaction_id):
    return await Transaction.filter(transaction_id=transaction_id).first()


async def refund_transaction(transaction_id):
    transaction = await Transaction.filter(transaction_id=transaction_id).first()
    if transaction:
        transaction.refund_status = True
        await transaction.save()
        return True
    return False
