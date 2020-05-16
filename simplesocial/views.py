from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'index.html'

class TestView(TemplateView):
    template_name = 'test.html'

class ThanksView(TemplateView):
    template_name = 'thanks.html'
