from . import views
from django.urls import path

urlpatterns = [
    path('search', views.search_events_view, name='search_events'),
    path('filter', views.filter_events_view, name='filter_events'),
    path('create', views.create_event_view, name='create_event'),
    path('<uuid:event_id>', views.get_event_details_view, name='get_event_details'),
    path('<uuid:event_id>/register', views.register_for_event_view, name='register_for_event'),
    path('<uuid:event_id>/update', views.update_event_details_view, name='update_event'),
    path('<uuid:event_id>/delete', views.delete_event_view, name='delete_event'),
    path('all', views.get_all_events_view, name='get_all_events'),
    path('next-7-days', views.events_within_next_7_days_view, name='events_within_next_7_days'),
    path('next-month', views.events_within_next_month_view, name='events_within_next_month'),
]