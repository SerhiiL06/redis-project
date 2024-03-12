from src.presentation.DTO import CategoryEnum, PostDTO


def validate_post(data: PostDTO) -> dict:
    error_pack = {}
    if len(data.title) < 5:
        error_pack.update(
            {"error": "Please your title must be  longer or equel then 5 letters"}
        )
    if data.description and len(data.description) < 5:
        error_pack.update(
            {"error": "Please your description must be longer or equel then 5 letters"}
        )

    if data.category not in ["sport", "economy", "news"]:
        error_pack.update({"error": "Incorrect category data"})

    return error_pack
