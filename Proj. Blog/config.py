ambiente = "teste" #TESTE OU PRODUÇÃO
if ambiente == 'teste':
#CONFIG BANCO DE DADOS
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'senai'
    DB_NAME = 'blog'

if ambiente == 'produção':
#CONFIG BANCO DE DADOS
    DB_HOST = 'thimotio.mysql.pythonanywhere-services.com'
    DB_USER = 'thimotio'
    DB_PASSWORD = 'tHimo@8002'
    DB_NAME = 'thimotio$BlogThimo'

#CONFIG CHAVE SECRETA DA SESSÃO
SECRET_KEY = 'blog'

#SENHA DO ADM
MASTER_EMAIL = "thimo@gmail.com"
MASTER_PASSWORD = "Thim@123"