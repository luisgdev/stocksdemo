from django.http import JsonResponse


def welcome_response(request) -> JsonResponse:
    return JsonResponse(
        {
            "status": 200,
            "message": "Welcome to Stockdemo."
        }
    )


def list_pets(request) -> JsonResponse:
    return JsonResponse(
        {
            "status": 200,
            "items": [
                {
                    "name": "Mac",
                    "species": "dog",
                    "age": 4,
                },
                {
                    "name": "Tom",
                    "species": "cat",
                    "age": 6,
                },
            ],
        }
    )
