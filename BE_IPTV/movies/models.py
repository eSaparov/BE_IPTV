import ast
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, telnumber, name, surname, email, password, **other_fields):

        if int(str(telnumber[1:])) < 420000000000 or int(str(telnumber[1:])) > 420999999999:
            raise ValueError('Prosim napiste spravne telefonni cislo')
        elif not str(telnumber[1:]).isdigit:
            raise ValueError('Prosim napiste telefonni cislo cisly')
        email = self.normalize_email(email)
        user = self.model(telnumber=telnumber, name=name,
                          surname=surname, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, telnumber, name, surname, email, password, **other_fields):

        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(telnumber, name, surname, email, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    telnumber = models.CharField(
        max_length=13, unique=True, verbose_name="Telefonni cislo")
    name = models.CharField(
        max_length=25, verbose_name="Jmeno")
    surname = models.CharField(
        max_length=25, verbose_name="Primeni")
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(
        default=True, verbose_name="Aktivni uzivatel")
    is_staff = models.BooleanField(default=False, verbose_name="Operator")

    objects = UserManager()

    USERNAME_FIELD = 'telnumber'
    REQUIRED_FIELDS = ['name', 'surname', 'email']

    class Meta:
        ordering = ['-id']
        verbose_name = "Uzivatel"
        verbose_name_plural = "Uzivatele"

    def __str__(self):
        return str(str(self.name)+" "+str(self.surname))
    
class tracks(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    bandwidth = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=2, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    kind = models.CharField(max_length=50, blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    frameRate = models.PositiveIntegerField(blank=True, null=True)
    pixelAspectRatio = models.FloatField(blank=True, null=True)
    hdr = models.FloatField(blank=True, null=True)
    mimeType = models.CharField(max_length=50, blank=True, null=True)
    audioMimeType = models.CharField(max_length=50, blank=True, null=True)
    videoMimeType = models.CharField(max_length=50, blank=True, null=True)
    codecs = models.CharField(max_length=50, blank=True, null=True)
    audioCodec = models.CharField(max_length=50, blank=True, null=True)
    videoCodec = models.CharField(max_length=50, blank=True, null=True)
    primary = models.BooleanField(blank=True, null=True)
    roles = models.JSONField(blank=True, null=True)
    audioRoles = models.JSONField(blank=True, null=True)
    forced = models.BooleanField(blank=True, null=True)
    videoId = models.PositiveIntegerField(blank=True, null=True)
    audioId = models.PositiveIntegerField(blank=True, null=True)
    channelsCount = models.PositiveIntegerField(blank=True, null=True)
    audioSamplingRate = models.PositiveIntegerField(blank=True, null=True)
    spatialAudio = models.BooleanField(blank=True, null=True)
    tilesLayout = models.CharField(max_length=50, blank=True, null=True)
    audioBandwidth = models.CharField(max_length=50, blank=True, null=True)
    videoBandwidth = models.CharField(max_length=50, blank=True, null=True)
    originalVideoId = models.CharField(max_length=50, blank=True, null=True)
    originalAudioId = models.CharField(max_length=50, blank=True, null=True)
    originalTextId = models.CharField(max_length=50, blank=True, null=True)
    originalImageId = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "track"
        verbose_name_plural = "tracks"

class appMetadata(models.Model):
    identifier = models.CharField(max_length=256, blank=True, null=True)
    downloaded = models.DateTimeField(blank=True, null=True)

class storedContent(models.Model):
    offlineUri = models.URLField(max_length=200, blank=True, null=True)
    originalManifestUri = models.URLField(max_length=200, blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    size = models.PositiveIntegerField( blank=True, null=True)
    expiration = models.CharField(max_length=50, blank=True, null=True)
    tracks = models.ManyToManyField(tracks)
    appMetadata = models.ForeignKey(appMetadata, on_delete=models.CASCADE, blank=True, null=True)
    isIncomplete = models.BooleanField(blank=True, null=True)
    
class videos(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    shortName = models.CharField(max_length=50, blank=True, null=True)
    iconUri = models.URLField(max_length=200, blank=True, null=True)
    manifestUri = models.URLField(max_length=200, blank=True, null=True)
    iconFile = models.ImageField(upload_to='../static/images')
    source = models.CharField(max_length=50, blank=True, null=True)
    focus = models.BooleanField(blank=True, null=True)
    disabled = models.BooleanField(blank=True, null=True)
    extraText = models.JSONField(blank=True, null=True)
    certificateUri = models.URLField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    isFeatured = models.BooleanField(blank=True, null=True)
    drm = models.JSONField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    licenseServers = models.JSONField(blank=True, null=True)
    licenseRequestHeaders = models.JSONField(blank=True, null=True)
    requestFilter = models.CharField(max_length=100, blank=True, null=True)
    responseFilter = models.CharField(max_length=100, blank=True, null=True)
    clearKeys = models.JSONField(blank=True, null=True)
    extraConfig = models.CharField(max_length=100, blank=True, null=True)
    adTagUri = models.URLField(max_length=200, blank=True, null=True)
    imaVideoId = models.CharField(max_length=100, blank=True, null=True)
    imaAssetKey = models.CharField(max_length=100, blank=True, null=True)
    imaContentSrcId = models.CharField(max_length=100, blank=True, null=True)
    mimeType = models.CharField(max_length=100, blank=True, null=True)
    mediaPlaylistFullMimeType = models.CharField(max_length=100, blank=True, null=True)
    storedProgress = models.PositiveIntegerField(blank=True, null=True)
    storedContent = models.ForeignKey(storedContent, on_delete=models.CASCADE, blank=True, null=True)

