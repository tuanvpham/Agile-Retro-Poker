from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('username')._unique = False


class UsernameValidatorAllowSpace(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'


class TrackableDateModel(models.Model):
    '''
    Abstract model to Track the creation/updated date for a model.
    '''

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Session(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    TYPES = (
            ('R', 'Retro'),
            ('P', 'Poker'),
        )
    session_type = models.CharField(max_length=10, choices=TYPES)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    @property
    def group_name(self):
        '''
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        '''
        return "session-%s" % self.id


class User(AbstractUser):
    username_validator = UsernameValidatorAllowSpace()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class SessionMember(TrackableDateModel):
    '''
    Store all users from a session
    '''

    session = models.ForeignKey(
        Session, on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class RetroBoardItems(TrackableDateModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE
    )
    RETRO_BOARD_ITEMS_CHOICES = (
        ('WWW', 'What Went Well'),
        ('WDN', 'What Did Not'),
        ('AI', 'Action Items')
    )
    item_type = models.CharField(
        max_length=3,
        choices=RETRO_BOARD_ITEMS_CHOICES,
        default='AI'
    )
    item_text = models.TextField(
        max_length=2000,
    )


class Story(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    story_points = models.IntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    key = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title
