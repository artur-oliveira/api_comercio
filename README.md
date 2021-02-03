# api_comercio
## Configuração do Ambiente: 
### Pacotes e Versões Necessários:
- Python==3.8.0
- Instalador de pacotes pip

### Passo-a-passo no Shell:
Primeiro será necessário configurar o ambiente virtual, caso não tenha o pacote "virtualenv" instale rodando no terminal o comando abaixo
```
pip install virtualenv
```
Em sistemas linux, talvez seja necessário usar o comando abaixo
```
pip3 install virtualenv
```
Após isso você deve criar o ambiente virtual com o comando
```
virtualenv venv
```
No windows, você precisará rodar o seguinte comando para ativar o ambiente virtual
```
venv\Scripts\activate
```
No Mac ou Linux, o comando é
```
source venv/bin/activate
```
Após isso você deverá instalar os requerimentos
```
pip install -r requirements.txt
```


Então para rodar o projeto, é necessário que sejam feitas as migrações primeiro. Logo, abra o shell de sua preferência dentro da pasta principal do projeto (onde está o arquivo "manage.py"), e digite:
```
python manage.py makemigrations
```

E, então, aplicam-se as migrações:
```
python manage.py migrate
```

Para criar um super usuário, basta executar:
```
python manage.py createsuperuser
```

E fornecer os dados requeridos.

Por fim, para iniciar o servidor:
```
python manage.py runserver 8000
```

### Uso do sistema
Antes de utilizar, seja como vendedor ou como cliente, será preciso criar as credenciais de cada vendedor e/ou cliente no <a href="http://localhost:8000/admin" target="_blank">painel de admin</a>.
Conforme explicado no vídeo de uso neste <a href="https://youtu.be/GsqvygIRUcQ" target="_blank">link</a>