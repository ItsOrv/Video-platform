from django.shortcuts import render

def categories_list(request):
    # Default categories
    categories = [
        {'name': 'Action', 'icon': 'fas fa-fire', 'video_count': 0},
        {'name': 'Comedy', 'icon': 'fas fa-laugh', 'video_count': 0},
        {'name': 'Drama', 'icon': 'fas fa-theater-masks', 'video_count': 0},
        {'name': 'Documentary', 'icon': 'fas fa-film', 'video_count': 0},
        {'name': 'Horror', 'icon': 'fas fa-ghost', 'video_count': 0},
        {'name': 'Sci-Fi', 'icon': 'fas fa-rocket', 'video_count': 0},
        {'name': 'Romance', 'icon': 'fas fa-heart', 'video_count': 0},
        {'name': 'Thriller', 'icon': 'fas fa-exclamation-triangle', 'video_count': 0},
    ]
    context = {'categories': categories}
    return render(request, 'categories.html', context)

