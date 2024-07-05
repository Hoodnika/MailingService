from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blogapp.forms import BlogForm, CommentForm
from blogapp.models import Blog, Comment
from clientapp.views import CustomLoginRequiredMixin


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CustomLoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blogapp:blog_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BlogUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blogapp:blog_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        CommentFormset = inlineformset_factory(Blog, Comment, form=CommentForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = CommentFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = CommentFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        if self.request.user == self.object.owner:
            return BlogForm


class BlogDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blogapp:blog_list')
