def userEntity(item: dict) -> dict:
    return {
        'nickname': str(item['nickname']),
        'email': str(item['email']),
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
