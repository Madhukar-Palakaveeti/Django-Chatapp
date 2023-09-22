from rest_framework import status
from rest_framework.generics import (ListAPIView, GenericAPIView)
from rest_framework.response import Response
from api.models import Users
from .serializers import OnlineUsersSerializer
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer


class OnlineUsersView(ListAPIView):
    '''
        A view to list all the online users and their channel names. This can only be accessed by authenticated users.
        So the access token must be included in the header for this to return success. As usual the field for the header
        in the request is 'Authorization' : Bearer access_tokenvalue
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineUsersSerializer

    def get_queryset(self):
        return Users.objects.filter(is_online=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'message': 'Online users fetched successfully',
            'data': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)



# Create your views here.
class StartChatView(GenericAPIView):
    '''
    This is a completely deecoupled backend for the real-time messaging. The backend only handles the routing and message logging 
    through django channels. For testing the real-time messaging, the frontend need to have a websocket connection with the 
    backend. This can be done seperately with postman websocket request type.
    The request url will be:
        ws://localhost:8000/ws/chat/send/<user_id>/
    
    For starting the channel layer, this view is created.
    '''
    permission_classes = (IsAuthenticated,)
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if user is None:
            return Response({"message" : "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_online:
            channel_layer = get_channel_layer()
            channel_layer.send(
                user.private_channel_name,
                {
                    'type': 'chatroom.message',
                    'message': 'message',
                    'username': 'self.user_name',
                    'receiver_user_id': 'receiver_user_id',
                    'chat_type': 'private',
                    'sent_by': 'self.user_id'
                }
            

            )
            return Response({'message': 'Message sent!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User is not online'}, status=status.HTTP_400_BAD_REQUEST)