# in your app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('members/<int:pk>/', views.MemberRetrieveUpdateView.as_view(), name='member-retrieve-update'),
    path('members/', views.MemberListAPIView.as_view(), name='member-list'),
    path('workspaces/<int:workspace_pk>/members/', views.MemberInWorkspaceListView.as_view(), name='member-list'),
    path('join-workspace/', views.JoinWorkspaceAPIView.as_view(), name='join-workspace'),
    path('join-workspace/', views.JoinWorkspaceAPIView.as_view(), name='join-workspace'),
    path('workspace/<int:workspace_id>/history/', views.WorkspaceHistoryAPIView.as_view(),),

    path('workspaces/', views.WorkspaceListView.as_view(), name='workspace-list'),
    path('workspaces/<int:pk>/', views.WorkspaceRetrieveView.as_view(), name='workspace-retrieve'),
    path('workspaces/create/', views.WorkspaceCreateView.as_view(), name='workspace-create'),

    path('missions/', views.MissionListView.as_view(), name='mission-list'),
    path('missions/<int:pk>/', views.MissionDetailView.as_view(), name='mission-detail'),

    path('tasks/', views.TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('tasks/<int:pk>/', views.TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail'),
    path('tasks/<int:pk>/download_file/', views.TaskViewSet.as_view({'get': 'download_file'}), name='task-download-file'),

    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),

]
