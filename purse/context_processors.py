from purse.models import PurseModel


def wallet(request):
    if not request.user.is_anonymous:
        return {'wallet': PurseModel.objects.get(user_id=request.user).money}
    return request