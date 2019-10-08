import configparser

config = configparser.ConfigParser()
config.read('config.ini')

try:
    token = config['bot']['token']
except:
    raise Exception('É necessário adicionar o "token" no config.ini')

try:
    db_params = config['database']
except:
    raise Exception('É necessário criar a sessão "database" do config.ini')
