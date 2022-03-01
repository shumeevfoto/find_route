from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from cities.models import City
from cities.templates.cities.forms import HtmlForm, CityForm


def home(request, pk=None):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    # if pk:
    # city = get_object_or_404(City, id=pk)
    # city = City.objects.filter(id=pk).first()
    #
    # context = {'object': city}
    # return render(request, 'cities/detail.html', context)
    form = CityForm()
    queryset = City.objects.all()
    lst = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'cities/home.html', context)


class ContentDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'

class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город успешно создан"

class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город успешно отредактирован"

class CityDeleteView(DeleteView, LoginRequiredMixin):
    model = City
    # form_class = CityForm
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def get(self, request, *args, **kwargs):
         messages.success(request, 'Город успешно удален')
         return self.post(request, *args, **kwargs)


class CityListView(ListView):
    paginate_by = 3
    model = City
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context
