from telethon import TelegramClient, events, sync
import os
import logging
import configparser
import json
from datetime import datetime


gRoot_path = os.path.abspath(os.path.dirname(__file__))+'/'
gSys_file_name = os.path.splitext(os.path.basename(__file__))[0]



##########################################################################################
##                                     CONFIG FILE                                      ##
##########################################################################################

if not os.path.exists( gRoot_path + 'config.ini' ):
    print( 'Config File (config.ini) not found!!' )
    ## Temp Loggin File
    
    lgging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s - %(message)s', 
                        datefmt=c, 
                        filename=( gRoot_path + '/' + gSys_file_name+'.log'))

    logging.info( 'Config File (config.ini) not founded!!' )
    logging.shutdown()
    exit()

gConfigFile = gRoot_path + 'config.ini'

gConfig = configparser.ConfigParser()
gConfig.read( gConfigFile )
gSections = gConfig.sections()
if not 'global' in gSections:
    print( 'Error in Config File: "global" Section Not Found!')
    print()
    exit()


###############################################################
##                 GLOBAL CONFIGURATIONS                     ##
###############################################################
gDebug_level = gConfig['global']['logging_level']

if 'gDownload_path' in gConfig['global']:
    gDownload_path = gConfig['global']['download_path']
else:
    gDownload_path = gRoot_path + 'Downloads'

if not os.path.isdir( gDownload_path )    :
    os.mkdir( gDownload_path )

gApi_id = gConfig['global']['api_id'] if 'api_id' in gConfig['global'] else None
gApi_hash = gConfig['global']['api_hash'] if 'api_hash' in gConfig['global'] else None
gPhone_number = gConfig['global']['phone_number'] if 'phone_number' in gConfig['global'] else None
gTimestamp_name = gConfig['global']['timestamp_name'] if 'timestamp_name' in gConfig['global'] else None

logging.basicConfig(level=gDebug_level, 
                    format='%(asctime)s %(levelname)s - %(message)s', 
                    datefmt='%Y/%m/%d %I-%M:%S', 
                    filename=( gRoot_path + '/' + gSys_file_name+'.log'))


logging.info('')
logging.info('###########################################################')
logging.info('Starting Process!')

if len( gSections ) < 1 :
    logging.error( 'None Channel/Group defined in Config File!!!' )
    exit()


gDownload_path = gConfig['global']['download_path'] if 'download_path' in gConfig['global'] else 'Downloads'
if gDownload_path[1] != '/':
    gDownload_path = gRoot_path + gDownload_path


if not os.path.isdir( gDownload_path ):
    os.mkdir( gDownload_path)
    logging.info('Creating Download Dir: ' + gDownload_path)
else:
    logging.info( 'Using Download Dir: ' + gDownload_path)






######################################.BEGIN

def writeBackConfig( pSection=None, pUpdateLastAccess=True):
    if pSection and pUpdateLastAccess:
        logging.info('Updating Last Access in Section')
        pSection['Last Update'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    

    logging.degug('Writing back Config File!')
    with open( gConfigFile, 'w') as configfile:
        gConfig.write( gconfigFile )


######################################.END


######################################.BEGIN

def download_media( pSection_config ):

    if not 'name' in pSection_config:
        logging.error('The Section Name not especified! Aborting section')
        return

    
    ## Geting download path
    if not 'download_path' in pSection_config:
        lDownload_path = gDownload_path + '/' + pSection_config['name']
    else:
        lDownload_path = pSection_config['download_path']
        if lDownload_path[1] != '/':
            lDownload_path = gRoot_path + lDownload_path


    if not os.path.isdir( lDownload_path ):
        os.mkdir( lDownload_path)
        logging.info('Creating Download Dir: ' + lDownload_path)
    else:
        logging.info( 'Using Download Dir: ' + lDownload_path)


    lDownload_path = lDownload_path + '/' if lDownload_path[-1] != '/' else ''

    

    lApi_id = pSection_config['api_id'] if 'api_id' in pSection_config else gApi_id
    lApi_hash = pSection_config['api_hash'] if 'api_hash' in pSection_config else gApi_hash
    lPhone_number = pSection_config['phone_number'] if 'phone_number' in pSection_config else gPhone_number

    if not ( lApi_hash and lApi_id and lPhone_number ):
        logging.error( 'Authentication data not Set!' )
        logging.error( 'Stopping import for' + pSection_config['name']
         )
        return

    if not 'channel_username' in pSection_config or not pSection_config['channel_username']:
        logging.warning('Channel User Name not valid for ' + pSection_config['name'] )
        return


    lSession_name = lPhone_number[1:]
    lLimit = int(pSection_config['messages_limit']) if 'messages_limit' in pSection_config else 10
    lExtensions = pSection_config['filter'] if 'filter' in pSection_config else None
    lTimestamp_name = pSection_config['timestamp_name'] if 'timestamp_name' in pSection_config else gTimestamp_name

    # Log in to Telegram and create a client object to use for getting data

        # Create the client and connect
    client = TelegramClient( lSession_name, lApi_id, lApi_hash)
    client.start()
    logging.info("Client Created")

        # Ensure you're authorized
    if not client.is_user_authorized():
        logging.info( 'Requesting new Code!')
        client.send_code_request( lPhone_number )
        try:
            logging.info( 'Gettign from user new telegram code')
            client.sign_in( lPhone_number, input('Enter the code: '))
        except SessionPasswordNeededError:
            logging.info( 'Getting MFA Password')
            client.sign_in(password=input('Password: '))


    logging.info('Starting get Messages one by one')
        #Get last "messages_limit" messages from channel/group
    lItemsCount = 0        
    for msg in client.get_messages( pSection_config['channel_username'], limit=lLimit):
        if msg.media is not None:
            if lExtensions:
                if msg.file.ext in lExtensions:
                    logging.info( msg.sender.title, msg.text)
                    lMediaFile = msg.file.name
                    if lMediaFile == None:
                        lMediaFile = lDownload_path+msg.file.media.date.strftime('%Y-%m-%d_%I-%M-%S')+msg.file.ext
                    else:
                        if lTimestamp_name:
                            lMediaFile = lDownload_path+msg.file.media.date.strftime('%Y-%m-%d_%I-%M-%S-') + lMediaFile
                        else:
                            lMediaFile = lDownload_path + lMediaFile


                    logging.info('Download File: ' + lMediaFile )
                    if os.path.isfile( lMediaFile ):
                        localSize = os.path.getsize( lMediaFile ) 
                        remoteSize = msg.file.size
                        if localSize < remoteSize:
                            logging.info('Deleting incompleted Download!')
                            os.remove( lMediaFile )
                        else:
                            logging.info( 'Skiping Download: File already exists!' )
                            continue
                    client.download_media(message=msg, file=lMediaFile )
                    lItemsCount += 1
                else:
                    logging.info('Ignoring Media "' + msg.text + '" due Filter Config')


    logging.info('Finish process')
    logging.info('Items Downloaded: ' + str(lItemsCount))

####################.END


####################################################################
##             FOR EACH SECTION, LOAD, CHECK AND DOWNLOAD         ##
####################################################################



logging.info( 'Sections found: %(len(gSections))s' )

for section in gSections:
    if section == 'global':
        continue

    section_config = {}
    for item in gConfig[section] :
        section_config[item] = gConfig[section][item]

    download_media( section_config )

