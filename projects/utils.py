from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search_projects(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    
    return projects, search_query


def paginate_projects(request, projects):
    
    per_page = 3
    page_number = request.GET.get("page") or 1

    paginator = Paginator(projects, per_page)
    total_pages = paginator.num_pages
    # page_range = paginator.page_range

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(total_pages)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    current_page = page_obj.number

    left_index = current_page - 2 if current_page > 2 else 1
    right_index = current_page + 2 if current_page < total_pages - 1 else total_pages

    custom_range = range(left_index, right_index + 1)

    return page_obj, custom_range, total_pages