from urllib.request import urlopen
import urllib.request
import os
import json
import time
from .models import *
from urllib import error

url = "https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json"

response = urlopen(url)
data_json = json.loads(response.read())


def update_database():
    for data in data_json:
        if "storedContent" in data and data["storedContent"] != None:
            new_track = data["storedContent"]["tracks"][0]
            new_meta = data["storedContent"]["appMetadata"]
            new_content = data["storedContent"]
            if not appMetadata.objects.filter(
                identifier=new_meta["identifier"]
            ).exists():
                appMetadata.objects.create(
                    identifier=new_meta["identifier"], downloaded=new_meta["downloaded"]
                )
            elif appMetadata.objects.filter(identifier=new_meta["identifier"]).exists():
                appMetadata.objects.filter(identifier=new_meta["identifier"]).update(
                    identifier=new_meta["identifier"], downloaded=new_meta["downloaded"]
                )

            if not tracks.objects.filter(id=int(new_track["id"])).exists():
                tracks.objects.create(
                    id=new_track["id"],
                    active=new_track["active"],
                    type=new_track["type"],
                    bandwidth=new_track["bandwidth"],
                    language=new_track["language"],
                    label=new_track["label"],
                    kind=new_track["kind"],
                    width=new_track["width"],
                    height=new_track["height"],
                    frameRate=new_track["frameRate"],
                    pixelAspectRatio=new_track["pixelAspectRatio"],
                    hdr=new_track["hdr"],
                    mimeType=new_track["mimeType"],
                    audioMimeType=new_track["audioMimeType"],
                    videoMimeType=new_track["videoMimeType"],
                    codecs=new_track["codecs"],
                    audioCodec=new_track["audioCodec"],
                    videoCodec=new_track["videoCodec"],
                    primary=new_track["primary"],
                    roles=new_track["roles"],
                    audioRoles=new_track["audioRoles"],
                    forced=new_track["forced"],
                    videoId=new_track["videoId"],
                    audioId=new_track["audioId"],
                    channelsCount=new_track["channelsCount"],
                    audioSamplingRate=new_track["audioSamplingRate"],
                    spatialAudio=new_track["spatialAudio"],
                    tilesLayout=new_track["tilesLayout"],
                    audioBandwidth=new_track["audioBandwidth"],
                    videoBandwidth=new_track["videoBandwidth"],
                    originalVideoId=new_track["originalVideoId"],
                    originalAudioId=new_track["originalAudioId"],
                    originalTextId=new_track["originalTextId"],
                    originalImageId=new_track["originalImageId"],
                )
            elif tracks.objects.filter(id=int(new_track["id"])).exists():
                tracks.objects.filter(id=int(new_track["id"])).update(
                    active=new_track["active"],
                    type=new_track["type"],
                    bandwidth=new_track["bandwidth"],
                    language=new_track["language"],
                    label=new_track["label"],
                    kind=new_track["kind"],
                    width=new_track["width"],
                    height=new_track["height"],
                    frameRate=new_track["frameRate"],
                    pixelAspectRatio=new_track["pixelAspectRatio"],
                    hdr=new_track["hdr"],
                    mimeType=new_track["mimeType"],
                    audioMimeType=new_track["audioMimeType"],
                    videoMimeType=new_track["videoMimeType"],
                    codecs=new_track["codecs"],
                    audioCodec=new_track["audioCodec"],
                    videoCodec=new_track["videoCodec"],
                    primary=new_track["primary"],
                    roles=new_track["roles"],
                    audioRoles=new_track["audioRoles"],
                    forced=new_track["forced"],
                    videoId=new_track["videoId"],
                    audioId=new_track["audioId"],
                    channelsCount=new_track["channelsCount"],
                    audioSamplingRate=new_track["audioSamplingRate"],
                    spatialAudio=new_track["spatialAudio"],
                    tilesLayout=new_track["tilesLayout"],
                    audioBandwidth=new_track["audioBandwidth"],
                    videoBandwidth=new_track["videoBandwidth"],
                    originalVideoId=new_track["originalVideoId"],
                    originalAudioId=new_track["originalAudioId"],
                    originalTextId=new_track["originalTextId"],
                    originalImageId=new_track["originalImageId"],
                )

            if not storedContent.objects.filter(
                offlineUri=new_content["offlineUri"]
            ).exists():
                this_meta = appMetadata.objects.get(
                    identifier=new_content["appMetadata"]["identifier"]
                )
                stored_track = int(new_content["tracks"][0]["id"])
                saved_content = storedContent.objects.create(
                    offlineUri=new_content["offlineUri"],
                    originalManifestUri=new_content["originalManifestUri"],
                    duration=new_content["duration"],
                    size=new_content["size"],
                    expiration=new_content["expiration"],
                    appMetadata_id=this_meta.pk,
                )
                track = tracks.objects.get(id=stored_track)
                saved_content.tracks.add(track)
            elif storedContent.objects.filter(
                offlineUri=new_content["offlineUri"]
            ).exists():
                this_meta = appMetadata.objects.get(
                    identifier=new_content["appMetadata"]["identifier"]
                )
                stored_track = int(new_content["tracks"][0]["id"])
                saved_content = storedContent.objects.filter(
                    offlineUri=new_content["offlineUri"]
                ).update(
                    offlineUri=new_content["offlineUri"],
                    originalManifestUri=new_content["originalManifestUri"],
                    duration=new_content["duration"],
                    size=new_content["size"],
                    expiration=new_content["expiration"],
                    appMetadata_id=this_meta.pk,
                )

            if not videos.objects.filter(name=data["name"]).exists():
                photoUrl = data["iconUri"]
                icon_name = photoUrl.rsplit("/", 1)[-1]
                photoname = (
                    os.path.abspath(os.curdir)
                    + "\\static\\images\\"
                    + icon_name
                )
                pictures_list = os.listdir(
                    os.path.abspath(os.curdir) + "\\static\\images\\"
                )
                if not icon_name in pictures_list:
                    try:
                        urllib.request.urlretrieve(photoUrl, photoname)
                    except error.URLError as e:
                        print(e.reason)
                        pass
                this_content = storedContent.objects.get(
                    offlineUri=new_content["offlineUri"]
                )
                if "requestFilter" in data:
                    requestFilterdata = data["requestFilter"]
                else:
                    requestFilterdata = None
                if "responseFilter" in data:
                    responseFilterdata = data["responseFilter"]
                else:
                    responseFilterdata = None

                videos.objects.create(
                    name=data["name"],
                    shortName=data["shortName"],
                    iconUri=data["iconUri"],
                    iconFile=photoname,
                    manifestUri=data["manifestUri"],
                    source=data["source"],
                    focus=data["focus"],
                    disabled=data["disabled"],
                    extraText=data["extraText"],
                    certificateUri=data["certificateUri"],
                    description=data["description"],
                    isFeatured=data["isFeatured"],
                    drm=data["drm"],
                    features=data["features"],
                    licenseServers=data["licenseServers"],
                    licenseRequestHeaders=data["licenseRequestHeaders"],
                    requestFilter=requestFilterdata,
                    responseFilter=responseFilterdata,
                    clearKeys=data["clearKeys"],
                    extraConfig=data["extraConfig"],
                    adTagUri=data["adTagUri"],
                    imaVideoId=data["imaVideoId"],
                    imaAssetKey=data["imaAssetKey"],
                    imaContentSrcId=data["imaContentSrcId"],
                    mimeType=data["mimeType"],
                    mediaPlaylistFullMimeType=data["mediaPlaylistFullMimeType"],
                    storedProgress=data["storedProgress"],
                    storedContent_id=this_content.pk
                )
            elif videos.objects.filter(name=data["name"]).exists():
                photoUrl = data["iconUri"]
                icon_name = photoUrl.rsplit("/", 1)[-1]
                photoname = (
                    os.path.abspath(os.curdir)
                    + "\\static\\images\\"
                    + icon_name
                )
                pictures_list = os.listdir(
                    os.path.abspath(os.curdir) + "\\static\\images\\"
                )
                if not icon_name in pictures_list:
                    try:
                        urllib.request.urlretrieve(photoUrl, photoname)
                    except error.URLError as e:
                        print(e.reason)
                        pass
                this_content = storedContent.objects.get(
                    offlineUri=new_content["offlineUri"]
                )
                if "requestFilter" in data:
                    requestFilterdata = data["requestFilter"]
                else:
                    requestFilterdata = None
                if "responseFilter" in data:
                    responseFilterdata = data["responseFilter"]
                else:
                    responseFilterdata = None

                videos.objects.filter(name=data["name"]).update(
                    name=data["name"],
                    shortName=data["shortName"],
                    iconUri=data["iconUri"],
                    iconFile=photoname,
                    manifestUri=data["manifestUri"],
                    source=data["source"],
                    focus=data["focus"],
                    disabled=data["disabled"],
                    extraText=data["extraText"],
                    certificateUri=data["certificateUri"],
                    description=data["description"],
                    isFeatured=data["isFeatured"],
                    drm=data["drm"],
                    features=data["features"],
                    licenseServers=data["licenseServers"],
                    licenseRequestHeaders=data["licenseRequestHeaders"],
                    requestFilter=requestFilterdata,
                    responseFilter=responseFilterdata,
                    clearKeys=data["clearKeys"],
                    extraConfig=data["extraConfig"],
                    adTagUri=data["adTagUri"],
                    imaVideoId=data["imaVideoId"],
                    imaAssetKey=data["imaAssetKey"],
                    imaContentSrcId=data["imaContentSrcId"],
                    mimeType=data["mimeType"],
                    mediaPlaylistFullMimeType=data["mediaPlaylistFullMimeType"],
                    storedProgress=data["storedProgress"],
                    storedContent_id=this_content.pk
                )
        else:
            if not videos.objects.filter(name=data["name"]).exists():
                photoUrl = data["iconUri"]
                icon_name = photoUrl.rsplit("/", 1)[-1]
                photoname = (
                    os.path.abspath(os.curdir)
                    + "\\static\\images\\"
                    + icon_name
                )

                pictures_list = os.listdir(
                    os.path.abspath(os.curdir) + "\\static\\images\\"
                )
                if not icon_name in pictures_list:
                    try:
                        urllib.request.urlretrieve(photoUrl, photoname)
                    except error.URLError as e:
                        print(e.reason)
                        pass
                
                if "requestFilter" in data:
                    requestFilterdata = data["requestFilter"]
                else:
                    requestFilterdata = None
                if "responseFilter" in data:
                    responseFilterdata = data["responseFilter"]
                else:
                    responseFilterdata = None

                videos.objects.create(
                    name=data["name"],
                    shortName=data["shortName"],
                    iconUri=data["iconUri"],
                    iconFile=photoname,
                    manifestUri=data["manifestUri"],
                    source=data["source"],
                    focus=data["focus"],
                    disabled=data["disabled"],
                    extraText=data["extraText"],
                    certificateUri=data["certificateUri"],
                    description=data["description"],
                    isFeatured=data["isFeatured"],
                    drm=data["drm"],
                    features=data["features"],
                    licenseServers=data["licenseServers"],
                    licenseRequestHeaders=data["licenseRequestHeaders"],
                    requestFilter=requestFilterdata,
                    responseFilter=responseFilterdata,
                    clearKeys=data["clearKeys"],
                    extraConfig=data["extraConfig"],
                    adTagUri=data["adTagUri"],
                    imaVideoId=data["imaVideoId"],
                    imaAssetKey=data["imaAssetKey"],
                    imaContentSrcId=data["imaContentSrcId"],
                    mimeType=data["mimeType"],
                    mediaPlaylistFullMimeType=data["mediaPlaylistFullMimeType"],
                    storedProgress=data["storedProgress"],
                    storedContent_id=None
                )
            elif videos.objects.filter(name=data["name"]).exists():
                photoUrl = data["iconUri"]
                icon_name = photoUrl.rsplit("/", 1)[-1]
                photoname = (
                    os.path.abspath(os.curdir)
                    + "\\static\\images\\"
                    + icon_name
                )
                pictures_list = os.listdir(
                    os.path.abspath(os.curdir) + "\\static\\images\\"
                )
                if not icon_name in pictures_list:
                    try:
                        urllib.request.urlretrieve(photoUrl, photoname)
                    except error.URLError as e:
                        print(e.reason)
                        pass

                if "requestFilter" in data:
                    requestFilterdata = data["requestFilter"]
                else:
                    requestFilterdata = None
                if "responseFilter" in data:
                    responseFilterdata = data["responseFilter"]
                else:
                    responseFilterdata = None

                videos.objects.filter(name=data["name"]).update(
                    name=data["name"],
                    shortName=data["shortName"],
                    iconUri=data["iconUri"],
                    iconFile=photoname,
                    manifestUri=data["manifestUri"],
                    source=data["source"],
                    focus=data["focus"],
                    disabled=data["disabled"],
                    extraText=data["extraText"],
                    certificateUri=data["certificateUri"],
                    description=data["description"],
                    isFeatured=data["isFeatured"],
                    drm=data["drm"],
                    features=data["features"],
                    licenseServers=data["licenseServers"],
                    licenseRequestHeaders=data["licenseRequestHeaders"],
                    requestFilter=requestFilterdata,
                    responseFilter=responseFilterdata,
                    clearKeys=data["clearKeys"],
                    extraConfig=data["extraConfig"],
                    adTagUri=data["adTagUri"],
                    imaVideoId=data["imaVideoId"],
                    imaAssetKey=data["imaAssetKey"],
                    imaContentSrcId=data["imaContentSrcId"],
                    mimeType=data["mimeType"],
                    mediaPlaylistFullMimeType=data["mediaPlaylistFullMimeType"],
                    storedProgress=data["storedProgress"],
                    storedContent_id=None
                )