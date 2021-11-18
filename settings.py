import configparser


conf = configparser.ConfigParser()
conf.read('settings.ini', encoding='UTF-8')

api_key = conf['twitter']['API_KEY']
api_secret = conf['twitter']['API_SECRET']
access_token = conf['twitter']['ACCESS_TOKEN']
access_token_secret = conf['twitter']['access_token_secret']

es_host = conf['es']['ES_HOST']
es_region = conf['es']['ES_REGION']

ch_lang_code = conf['comprehend']['LANGUAGE_CODE']
ch_region = conf['comprehend']['CH_REGION']
