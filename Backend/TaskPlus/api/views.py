from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, viewsets
from rest_framework.authtoken.models import Token

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import * 
from .serializers import *  # 

import os
from pathlib import Path  # Import Path from pathlib module
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    member_serializer = MemberSerializer(data=request.data)
    if member_serializer.is_valid():
        member = member_serializer.save()

        user_data = {
            'email': request.data.get('email'),
            'username': request.data.get('username', ''),
            'password': request.data.get('password'),
        }

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            member.user = user
            member.save()

            token, _ = Token.objects.get_or_create(user=user)
            member_data = MemberSerializer(member).data
            del member_data['password']

            return Response({"member": member_data, "token": token.key}, status=status.HTTP_201_CREATED)
        else:
            member.delete()
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    member = authenticate(username=data['username'], password=data['password'])

    if member:
        token, created_token = Token.objects.get_or_create(user=member.user)

        response_data = {
            'member': MemberSerializer(member).data,
            'token': token.key,
        }

        del response_data['member']['password']

        return Response(response_data)

    return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.auth.delete()
        return Response({"message": "Logout was successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class MemberRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberListAPIView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberInWorkspaceListView(generics.ListAPIView):
    serializer_class = MemberSerializer

    def get_queryset(self):
        workspace_pk = self.kwargs.get('workspace_pk')
        
        queryset = Member.objects.filter(workspace__id=workspace_pk)
        
        return queryset


class WorkspaceListView(generics.ListAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer1

class WorkspaceRetrieveView(generics.RetrieveAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer1

class WorkspaceCreateView(generics.CreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class MissionListView(generics.ListCreateAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

#maybe not needed
class MissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
   
    @action(detail=True, methods=['get'])
    def download_file(self, request, pk=None):
        task = self.get_object()
        file_path = task.file_attachment.path if task.file_attachment else None

        if file_path and Path(file_path).exists():
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{Path(file_path).name}"'
                return response
        else:
            return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)



class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class JoinWorkspaceAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Get data from request
#         member_id = request.data.get('member_id')
#         invite_code = request.data.get('invite_code')

#         try:
#             # Retrieve the member and workspace
#             member = Member.objects.get(id=member_id)
#             workspace = Workspace.objects.get(invite_code=invite_code)

#             # Associate the member with the workspace
#             member.workspace = workspace
#             member.save()

#             return Response({'detail': f'Member {member.username} joined Workspace {workspace.name}.'}, status=status.HTTP_200_OK)
#         except Member.DoesNotExist:
#             return Response({'detail': 'Member not found.'}, status=status.HTTP_404_NOT_FOUND)
#         except Workspace.DoesNotExist:
#             return Response({'detail': 'Invalid invite code.'}, status=status.HTTP_400_BAD_REQUEST)


class JoinWorkspaceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from request
        member_id = request.data.get('member_id')
        invite_code = request.data.get('invite_code')

        try:
            # Retrieve the member and workspace
            member = Member.objects.get(id=member_id)
            workspace = Workspace.objects.get(invite_code=invite_code)

            # Associate the member with the workspace
            member.workspace = workspace
            member.save()

            # Send notification to all workspace members
            self.send_notification_to_workspace_members(workspace, f'Member {member.username} joined Workspace {workspace.name}.')

            return Response({'detail': f'Member {member.username} joined Workspace {workspace.name}.'}, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({'detail': 'Member not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Workspace.DoesNotExist:
            return Response({'detail': 'Invalid invite code.'}, status=status.HTTP_400_BAD_REQUEST)

    def send_notification_to_workspace_members(self, workspace, message):
        # Replace this with your Firebase Cloud Messaging (FCM) server key
        fcm_server_key = 'your_fcm_server_key'

        # Get all members in the workspace
        members = Member.objects.filter(workspace=workspace).exclude(device_token__in=['', None])

        # Send a separate notification for each member
        for member in members:
            # Prepare the FCM notification payload for the current member
            notification_payload = {
                'registration_ids': [member.device_token],
                'notification': {
                    'title': 'Workspace Notification',
                    'body': message,
                },
            }

            # Print the notification payload for the current member
            print(f'Notification Payload for {member.username}: {notification_payload}')

            # Send the HTTP request to FCM server for the current member
            response = requests.post(
                'https://fcm.googleapis.com/fcm/send',
                json=notification_payload,
                headers={'Authorization': f'key={fcm_server_key}', 'Content-Type': 'application/json'}
            )

            # Check the response status for the current member
            if response.status_code == 200:
                print(f'Notification sent successfully to {member.username}!')
            else:
                print(f'Failed to send notification to {member.username}. Status code:', response.status_code)
                print(f'Response content for {member.username}:', response.content)





class WorkspaceHistoryAPIView(APIView):
    def get(self, request, workspace_id, format=None):
        # Get all completed and missed tasks for the given workspace, combined and ordered by deadline
        tasks = Task.objects.filter(mission__workspace_id=workspace_id, state__in=['complete', 'missed']).order_by('deadline')

        # Serialize the tasks
        task_serializer = TaskSerializer(tasks, many=True)

        # Return the serialized data
        return Response({'tasks': task_serializer.data}, status=status.HTTP_200_OK)