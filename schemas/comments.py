def commentEntity(comm: dict) -> dict:
    return {
        "content":comm["content"]
    }


def commentsEntity(comms: list) -> list:
    return [commentEntity(comm) for comm in comms]