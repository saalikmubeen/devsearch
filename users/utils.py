from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search_profiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query


def paginate_profiles(request, profiles):

    per_page = 3
    page_number = request.GET.get("page") or 1

    paginator = Paginator(profiles, per_page)
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
