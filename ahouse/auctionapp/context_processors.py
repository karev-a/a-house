from .models import Category


def category_header(request):
    return {'categories': Category.objects.all()}
