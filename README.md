# telegramDownload
Python script for Download Medias from Telegram Channel/Group
<br /> 
<br /> 
<br /> 
## Requirements
* Docker
<br /> 
<br /> 
<br /> 
## Install
<br /> 
Clone repository

```
git clone git@github.com:adrianocortes/telegramDownload.git
```

```
cd telegramDownload
```

<br /> 
Copy config-sample.ini to config.ini

```
cp config-sample.ini to config.ini
```

<br /> 
<br /> 
Get your API Hash and API ID from https://my.telegram.org, under API Development.
If you don't have one hash api, create new one.

update config.ini file with your preferences

Run new container with volume, like this:

```
docker run -d -ti \
    --name telegramDownload \
    --mount type=bind,src="$(pwd)",target=/app \
    adrianocortes/telegramdownload:latest
```
Obs.: In first run you will need stay attached and run script. The script will ask you some authentication informations. The Session will be saved in a file, for futures access.
<br />
<br /> 
<br /> 
in /app folder, run:

```
python telegramDownload.py
```
<br /> 
<br /> 
The Download Process will start.
<br /> 
<br /> 
<br /> 

For run the script before first time, you can:

1 - Attach to container and run manually script

```
docker container attach telegramDownload
cd /app
python telegramDownload.py
``` 
<br />
<br />
2 - Run the command directly 

```
docker exec -it telegramDownload "python /app/telegramDownload.py"
```
<br />
<br />
<br />

# TIP

The download parameters is relative a docker file system. So, is relative to path used in mount parameter when running docker.
For use one folder out volume, like media folder for use in your media server, use one symbolic link.
Ex.: ln -s /media/videos /telegramDownload/Downloads
     ln -s /telegramDownload/Downloads /media/videos
<br />
<br />

## **Attention**

  Be sure about folder permissions for docker can write in Downloads folder passed.

## _Have Fun!_

<br /> 
<br /> 
<br /> 
<br /> 
<br /> 
<br /> 

# Parameters
<br /> 
<br /> 
<br /> 

##Attention
    All parameters can be exist in Global or each channel/group, except 'logging Level'. This one just can be in Global section.
    If some parameter exist in Global section and in channel/group channel, the value in channel/group will orverride global value.
<br /> 
<br /> 

### download_path
- Path for save media files
  Can be relative or full path.
  Can exist in Global and channel Section.
  If set In Global section like relative path, will be app folder relative.
  If not specified in Channel section, will be used channel_username value like a relative path.
    Ex.:/Downloads/channelName
<br /> 
<br /> 

### logging Level 
- Set Log Level in download process.
    Values: NOTSET DEBUG INFO WARNING ERROR CRITICAL
    logging_level=INFO
<br /> 
<br /> 

### api_id
- API ID from my.telegram.org
    Obs.: Just numbers, withou ""
    Ex.:

    ```
    api_id=154578
    ``` 
<br /> 
<br /> 

### api_hash
-  API Hash from my.telegra.org
    Obs.: Just caracters, without ""
    Ex.:

    ```
    api_hash=1je733420e5fe97804c109ec83ca2909
    ``` 
<br /> 
<br /> 

### phone_number
- Full phone number, like registred in Telegram
  Ex.:

  ``` 
  phone_number= +5562984012013
  ```
<br /> 
<br /> 

### timestamp_name
- If True, the original timestamp from file will add before file name
  Values: True or False
  Ex.:

  ```
    timestamp_name=True
  ```
- Obs.: If telegram inform a media file name it will be used, otherwise will be used original timestamp from media file.
<br /> 
<br /> 

### name
- Folder name for this channel/group
    Ex.:
    
    ```
    name=kara_para_ask
    ``` 

<br /> 
<br /> 

### channel_username
- The channel/Group name for identify the target
  Obs.:
    If channel/group doesn't have a name, should use the link used for get in the channel/group
  Ex.:

    ```
    channel_username=@adrianocortes
    channel_username=https://t.me/usuariosgithubbrasil
    ``` 
<br /> 
<br /> 

### messages_limit
- Up limit messages that should be downloaded, from last to first
  Ex.:

  ```
  messages_limit=10
  ``` 
<br /> 
<br /> 

### filter
- The file type filter tha should be downloaded
  Ex.:

  ```
  filter=.mp4,.jpg
  ``` 

<br /> 
<br /> 
<br /> 
<br /> 
<br /> 
<br /> 

# RoadMap
<br /> 

* Create way for import since last sucessfull process.
* Implement download process with assync method for update progress in Log