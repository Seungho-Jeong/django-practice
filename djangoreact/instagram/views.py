from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView
from django.shortcuts import render, get_object_or_404
from .models import Post


# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))

# @method_decorator(login_required, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10


post_list = PostListView.as_view()

# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', None)
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     return render(request, 'instagram/post_list.html', {
#         'post_list': qs,
#         'q': q,
#     })

# post_detail = DetailView.as_view(model=Post)

class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_published=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_published=True)
        return qs


post_detail = PostDetailView.as_view()

# def post_detail(request: HttpResponse, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'instagram/post_detail.html', {
#         'post': post
#     })


# def archives_year(request, year):
#     return HttpResponse(f"{year}년 archive")


post_archive = ArchiveIndexView.as_view(model=Post,
                                        date_field='created_at',
                                        paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post,
                                            date_field='created_at',
                                            make_object_list=True)
