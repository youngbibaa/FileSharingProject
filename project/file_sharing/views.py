from django.views.generic import ListView, CreateView, DetailView, DeleteView, View, UpdateView, FormView
from .models import CustomUser, Comment, Review, File
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentChangeForm, CommentCreationForm, ReviewChangeForm, ReviewCreationForm, FileChangeForm, FileCreationForm, CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import StreamingHttpResponse

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'file_sharing/home.html')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  
    template_name = 'file_sharing/register.html'

    def form_valid(self, form):
        user = form.save() 
        print("Пользователь сохранён:", user)  
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Форма не валидна:", form.errors)
        return super().form_invalid(form)


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    

class ProfileView(LoginRequiredMixin, ListView):
    model = File
    template_name = 'file_sharing/profile.html'
    context_object_name = "files"

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering', '-uploaded_at')  
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset.order_by(ordering)


class CreateFileView(LoginRequiredMixin, CreateView):
    model = File
    form_class = FileCreationForm
    template_name = 'file_sharing/create_file.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = CustomUser.objects.get(id=self.request.user.id) 
        return super().form_valid(form)

class FileDetailView(LoginRequiredMixin, DetailView, FormView):
    model = File
    form_class = ReviewCreationForm
    template_name = 'file_sharing/file_detail.html'
    context_object_name = 'file'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Получаем форму для отзыва
        context['comments'] = self.get_object().review_set.all()  # Получаем все отзывы для данного файла
        return context

    def form_valid(self, form):
        review = form.save(commit=False)  # Создаем объект, но не сохраняем его в базе данных
        review.file = self.get_object()  # Устанавливаем файл
        review.author = CustomUser.objects.get(id=self.request.user.id)   # Устанавливаем автора комментария
        review.save()  # Сохраняем отзыв
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('file_detail', kwargs={'pk': self.get_object().pk}) 


@login_required
def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk)  
    file.delete()
    return redirect("profile") 


@login_required
def download_file(request, pk):
    # Получаем файл по первичному ключу
    file = get_object_or_404(File, pk=pk)

    # Увеличиваем счетчик загрузок
    file.downloads += 1
    file.save(update_fields=['downloads'])

    # Создаем генератор для потоковой передачи файла
    def file_iterator(file_obj, chunk_size=8192):
        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break
            yield chunk

    # Настраиваем StreamingHttpResponse для отправки файла
    response = StreamingHttpResponse(file_iterator(file.file), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.title}"'

    # Обновление истории загрузок в сессии пользователя
    if request.user.is_authenticated:
        if 'download_history' not in request.session:
            request.session['download_history'] = []

        download_info = {
            'file_name': file.title,
            'timestamp': timezone.now().strftime("%d.%m.%Y %H:%M")
        }
        request.session['download_history'].append(download_info)
        request.session.modified = True  

    return response
@login_required
def view_download_history(request):
    download_history = request.session.get('download_history', [])
    return render(request, 'file_sharing/download_history.html', {'download_history': download_history})




    
    
    