from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from website.tasks import generate_report


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "website/home.html"

    def get(self, request, *args, **kwargs):
        generate_report.delay(request.user.id)

        return super().get(request, *args, **kwargs)
