from family.adapters.schemas.accounts import AccountDBSchema, AccountSchema

admin = AccountDBSchema(
    user_id=1,
    user_name="admin",
    email="admin@example.com",
    real_name="Testov Test Testovich",
    password="$2b$12$usqMI7jXSGDsOSIhF7s/DedED0px.FqLqjZAYV7GAQi6N3AsukX9S",
    role={"level": 0, "name": "admin"},
)

admin_answer = AccountSchema(
    user_name="admin",
    email="admin@example.com",
    role={"level": 0, "name": "admin"},
)
