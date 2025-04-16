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

Crie o arquivo /etc/systemd/system/fastapi.service com o seguinte conteudo:

[Unit]
Description=FastAPI App
After=network.target

[Service]
User=root
WorkingDirectory=/app/fastapi-orm-proj
ExecStart=/app/fastapi-orm-proj/start.sh
Restart=always
RestartSec=5
Environment=PATH=/app/fastapi-orm-proj/venv/bin
Environment=ENV_MODE=production

[Install]
WantedBy=multi-user.target

Salve e rode os comandos:

chmod +x /app/fastapi-orm-proj/start.sh

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl restart fastapi
sudo systemctl status fastapi

Para testar, no navegador cole:

http://<IP_PUBLICO>:8000/docs 

A api deve estar respondendo normalmente sempre que a instância ec2
configurada for reiniciada. Lembrando que a instância RDS deve estar de pé também;