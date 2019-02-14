from jira import JIRA, JIRAError
from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import *
from .serializers import *
from .utilities import *



# Rest API View
@api_view(['GET'])
def current_user(request):
    '''
    Determine the current user by their token, and return their data
    '''

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserAuthentication(APIView):
    '''
    Handle authentication with tokens
    '''

    permission_classes = (AllowAny,)

    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        response_data = ({
            'message': "Unknown error"
        })
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            # Login with Jira Auth
            jac = JIRA(
                'https://agilecommandcentralgroup10.atlassian.net',
                basic_auth=(email, password),
                max_retries=1, timeout=5
            )
            jac_username = jac.myself().get('displayName')
            user = self.get_object(email)
            if user is None:
                # Signup with ACC
                # convert the user data to a byte stream
                serializer = UserSerializerWithToken(data={
                    'email': email,
                    'username': jac_username,
                    'password': password
                })
                # if it is possible to deserialize the data then success
                if serializer.is_valid():
                    serializer.save()
                    response_data = ({
                        'message': "Successfully logged in user for the first time"
                    })
                    response_data = {**response_data, **serializer.data}
                    status_code = status.HTTP_201_CREATED
                # otherwise get the errors
                else:
                    response_data = ({
                        'message': "There was a problem creating the details for this user"
                    })
                    response_data = {**response_data, **serializer.errors}
                    status_code = status.HTTP_400_BAD_REQUEST
            else:
                # generate a token for the session if the credentials were valid
                token = generate_new_token(user)
                user_data = ({
                    'token': token,
                    'email': user.email,
                    'username': user.username
                })
                response_data = ({
                    'message': "Successfully logged in",
                })
                response_data = {**response_data, **user_data}
                status_code = status.HTTP_200_OK
        except JIRAError as e:
            if e.status_code == 401:
                response_data = ({
                    'message': "Wrong username/password",
                })
                status_code = status.HTTP_401_UNAUTHORIZED
            elif e.status_code == 408:
                response_data = ({
                    'message': "The request timed out during authentication with Jira",
                })
                status_code = status.HTTP_408_REQUEST_TIMEOUT
            elif e.status_code == 500:
                response_data = ({
                    'message': "There was an internal server error",
                })
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                response_data = ({
                    'message': "Unknown error",
                })
                status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(response_data, status=status_code)


class RetroBoardItemsList(generics.ListAPIView):
    '''
    Returns all retro board items
    '''

    queryset = RetroBoardItems.objects.all()
    serializer_class = RetroBoardItemsSerializer


@api_view(['POST'])
def check_session_owner(request):
    current_session = Session.objects.get(title=request.data['session_title'])
    if request.user == current_session.owner:
        data = {
            'is_owner': True
        }
    else:
        data = {
            'is_owner': False
        }

    return Response(data)


class SessionCreate(APIView):
    '''
    Fetch and create sessions
    '''

    def get(self, request, format=None):
        sessions = Session.objects.all()
        session_serializer = SessionSerializer(sessions, many=True)
        return Response(session_serializer.data)

    def post(self, request, format=None):
        session_serializer = SessionSerializer(
            data=request.data,
            context={'request': request}
        )
        if session_serializer.is_valid():
            session_serializer.save()
            return Response(
                session_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            session_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SessionMemberList(generics.ListAPIView):
    queryset = SessionMember.objects.all()
    serializer_class = SessionMemberSerializer


# Test deploy
@api_view(['GET'])
@permission_classes((AllowAny, ))
def test_deploy(request):
    return HttpResponse(content='You made it')
