def userEntity(user: dict) -> dict:
    return {
        "nickname": str(user["nickname"]),
        "email": str(user["email"]),
    }


def usersEntity(entity) -> list:
    return [userEntity(user) for user in entity]
