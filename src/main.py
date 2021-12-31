import serial
import config
import asyncio
import time
import emoji

def de_emoji(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text

from datetime import datetime
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

def time_now():
    dt = datetime.now()
    return(dt.strftime("%D | %H:%M"))

try:
    ser = serial.Serial(config.port,config.speed)

except:
    print(f'{time_now()} Connection Failed!')
print('setup complete')

def get_status():
    async def get_playback_status():
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:
            status = current_session.get_playback_info()
            return status
    func = asyncio.run(get_playback_status())
    try:
        return func.playback_status
    except:
        return 0
def get_info():
    async def get_media_info():
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:  # there needs to be a media session running
            info = await current_session.try_get_media_properties_async()
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            return info_dict
    if not asyncio.run(get_media_info()) == None:
        return asyncio.run(get_media_info())
    else:
        return 0
print('skip_async')
status_dict = {0:'Нет открытых плееров',1:'Открыт плеер(ы)',2:'Переключение трека',3:'Остановлено',4:'Воспроизводится',5:'Приостановлено'}


print('skip_time')
while True == True:
    print('begin loop')
    print(f'status = {type(get_status())}')
    #try:
    status = status_dict.get(get_status())        
    print(f'status = {type(status)}')
    print('get status')
        
    if not get_info() == 0:
            artist = de_emoji(get_info().get('artist').encode('utf-8'))
            title = de_emoji(get_info().get('title').encode('utf-8'))
            print('get info')
    else:
            artist, title = 'None','None'

    ser.write(f'{status}\n\r{artist} - {title}'.encode('utf-8'))
    print(f'{status}\n{artist} - {title}\n')
    time.sleep(2)
    #except:
     #   print(f'{time_now()} Перезапуск через 5 секунд')
      #  time.sleep(5)
       # try:
       #     ser = serial.Serial(config.port,config.speed)
       # except:
       #     pass