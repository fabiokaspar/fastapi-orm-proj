COMO EXECUTAR 

Instale o docker e o python versão 3.9

DESENVOLVIMENTO
- Adicione a variável de ambiente ENV_MODE=development no arquivo ~/.bashrc
ou no terminal: export ENV_MODE=development
- caso for no arquivo, feche e abra o terminal para ler as variáveis de ambiente
- edite o arquivo .env.development com as credenciais do banco de dados como serviço docker

DB_HOST=localhost
DB_NAME=?
DB_PORT=5432
DB_USER=?
DB_PASSWORD=?

Rode o script ./start.sh

PRODUÇÃO
- Conecte a instância EC2 da AWS via ssh, adicionando a chave pública .pem ao agent
- Adicione a variável de ambiente ENV_MODE=production no arquivo /etc/environment
ou no terminal: export ENV_MODE=development 
- edite o arquivo .env.production com as credenciais do banco de dados rodando na instância RDS
- reinicie o SO da instância EC2: sudo reboot

DB_HOST=<endereço instancia rds>
DB_NAME=<nome banco>
DB_PORT=<porta banco>
DB_USER=<user banco>
DB_PASSWORD=<senha banco>

Rode o script ./start.sh