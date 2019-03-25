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
from .oauth import *


JIRA_SERVER = 'https://agilecommandcentralgroup10.atlassian.net'
CONSUMER_KEY = 'OauthKey'
CONSUMER_SECRET = 'dont_care'
VERIFIER = 'jira_verifier'
RSA_KEY = read('jira_privatekey.pem')


class Login(APIView):
    '''
    Handle Login Submission
    '''

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        response_data = ({
            'message': "Successful"
        })
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            access_tokens = connect_1()
            response_data = {**response_data, **access_tokens}
            status_code = status.HTTP_200_OK
        except JIRAError as e:
            response_data = ({
                'message': 'Cannot connect to JIRA Server. Please try again later.'
            })
        finally:
            return Response(response_data, status=status_code)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def oauth_user(request):
    response_data = {
        'message': "Success"
    }
    status_code = status.HTTP_400_BAD_REQUEST
    try:
        try:
            oauth_token = request.data['oauth_token']
            oauth_token_secret = request.data['oauth_token_secret']
        except:
            oauth_token = request.query_params['oauth_token']
            oauth_token_secret = request.query_params['oauth_token_secret']

        jira_options = connect_2(oauth_token, oauth_token_secret)
        jac = JIRA(
            options={'server': JIRA_SERVER},
            oauth=jira_options
        )
        jac_username = jac.myself().get('displayName')
        jac_email = jac.myself().get('emailAddress')
        access_tokens = {
            'access_token': jira_options['access_token'],
            'secret_access_token': jira_options['access_token_secret']
        }

        user = get_user_object(jac_email)
        if user is None:
            # Signup with ACC
            # convert the user data to a byte stream
            serializer = UserSerializerWithToken(data={
                'email': jac_email,
                'username': jac_username,
            })
            # if it is possible to deserialize the data then success
            if serializer.is_valid():
                serializer.save()
                response_data = ({
                    'message': "Successfully logged in user for the first time"
                })
                response_data = {**response_data, **
                                 serializer.data, **access_tokens}
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
            response_data = {**response_data, **user_data, **access_tokens}
            status_code = status.HTTP_200_OK
        return Response(data=response_data, status=status.HTTP_200_OK)
    except:
        response_data = {
            'message': "Error"
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    '''
    Determine the current user by their token, and return their data
    '''

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def delete_session(request):
    try:
        session = Session.objects.get(id=request.data['session'])
        session.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SessionCreate(APIView):
    '''
    Fetch and create sessions
    '''

    def get(self, request, format=None):
        sessions = Session.objects.all()
        session_serializer = SessionSerializer(sessions, many=True)
        return Response(session_serializer.data)

    def post(self, request, format=None):
        try:
            owner = get_user_object(request.data['email'])
            session = get_session_object(request.data['title'])
            if session is None:
                session_type = 'R'
                if request.data['session_type'] == 'poker':
                    session_type = 'P'
                session = Session(
                    title=request.data['title'],
                    session_type=session_type,
                    owner=owner
                )
                session.save()
                response_data = ({
                    'id': session.id,
                    'title': session.title,
                    'session_type': session.session_type,
                    'owner': owner.username
                })
                return Response(
                    data=response_data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={'error_message': "Duplicate title. Please choose another name for title"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RetroBoardItemsList(generics.ListAPIView):
    '''
    Returns all retro board items
    '''

    queryset = RetroBoardItems.objects.all()
    serializer_class = RetroBoardItemsSerializer


@api_view(['POST'])
def remove_stories(request):
    try:
        stories = request.data['stories']
        for story in stories:
            if(story['selected'] is False):
                Story.objects.get(id=story['id']).delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StoryItemList(generics.ListAPIView):
    '''
    Returns all story items
    '''

    queryset = Story.objects.all()
    serializer_class = StorySerializer


class StorySelectList(APIView):
    '''
    Returns all stories from Jira backlog for Planning Poker
    '''

    def post(self, request, format=None):
        try:
            jira_options = {
                'access_token': request.data['access_token'],
                'access_token_secret': request.data['secret_access_token'],
                'consumer_key': CONSUMER_KEY,
                'key_cert': RSA_KEY
            }
            jac = JIRA(
                options={'server': JIRA_SERVER},
                oauth=jira_options
            )
            stories = jac.search_issues('issueType=Story')
            session_id = Session.objects.get(id=request.data['session'])
            for story in stories:
                story = Story(
                    title=story.fields.summary,
                    description=story.fields.description,
                    story_points=story.fields.customfield_10024,
                    session=session_id,
                    key=story.key
                )
                story.save()
            return Response(data={'message': "Successfully retrieved from Jira"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


class SessionMemberList(APIView):
    '''
        Retrieve all members of a specific session
    '''

    def get(self, request, session_id, format=None):
        member_list = SessionMember.objects.filter(session_id=session_id)
        serializer = SessionMemberSerializer(member_list, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def end_retro(request):
    '''
    When a retro session ends, post all action items to Jira
    '''

    try:
        items = list(
            RetroBoardItems.objects.filter(
                item_type='AI', session=request.data['session']
            )
        )
        jira_options = {
            'access_token': request.data['access_token'],
            'access_token_secret': request.data['secret_access_token'],
            'consumer_key': CONSUMER_KEY,
            'key_cert': RSA_KEY
        }
        jac = JIRA(
            options={'server': JIRA_SERVER},
            oauth=jira_options
        )
        session = Session.objects.get(id=request.data['session'])
        for i in items:
            jac.create_issue(
                project='AG',
                summary=i.item_text,
                issuetype={'name': 'Task'},
                description="Access Item from Retro Session: " + session.title
            )
        session.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Stories(APIView):
    '''
        Retrieve a specific story
    '''

    def get(self, request, session_id, format=None):
        story_list = Story.objects.filter(session_id=session_id)
        serializer = StorySerializer(story_list, many=True)
        return Response(serializer.data)


class Cards(APIView):
    '''
        Retrive cards for a specif story and session
    '''

    def get(self, request, session_id, story_id, format=None):
        card_list = Card.objects.filter(
            session_id=session_id,
            story_id=story_id
        )
        serializer = CardSerializer(card_list, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def update_points(request):
    try:
        story = Story.objects.get(id=request.data['id'])
        story.story_points = request.data['points']
        story.save(update_fields=["story_points"])
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def end_poker(request):
    '''
    Update all stories in the database in Jira when Planning Poker session ends
    '''

    try:
        jira_options = {
            'access_token': request.data['access_token'],
            'access_token_secret': request.data['secret_access_token'],
            'consumer_key': CONSUMER_KEY,
            'key_cert': RSA_KEY
        }
        jac = JIRA(
            options={'server': JIRA_SERVER},
            oauth=jira_options
        )
        current_session = Session.objects.get(id=request.data['session'])
        stories = Story.objects.filter(session=current_session)
        for story in stories:
            jac.issue(story.key).update(customfield_10024=story.story_points)
        current_session.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_session_started(request):
    try:
        current_session = Session.objects.get(
            title=request.data['session_title']
        )
    except Session.DoesNotExist:
        current_session = None

    if current_session is None:
        data = {
            'error': 'Session does not exits'
        }
    else:
        if current_session.is_started is True:
            data = {
                'is_started': True
            }
        else:
            data = {
                'is_started': False
            }

    return Response(data)
