from django.db.models import Count

from .models import Rubric

def rubrics(request):
    return{'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}


class RubricMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        def __call__ (self, request):
            return self,get_response(request)

        def process_template_response(self, requset, response):
            response.context_data['rubrics'] = Rubric.objects.all()
            return response


def test_middleware(next):
    def core_middleware(request):
        response = next(request)

        return response
    return core_middleware

class TestMiddleware:
    def __init__(self, request):
        self.next = next
        responce = self.next(request)
        return responce
