<p align="center">
  <img src="assets/logo-vassouras.png" alt="Universidade de Vassouras" width="400"/>
</p>

<h3 align="center">
  Universidade de Vassouras  
</h3>

---

### 📚 Curso: **Engenharia de Software**  
### 🖥️ Disciplina: **Banco de Dados Não Relacionais**  
### 👨‍🎓 Autor: **Matheus Beiruth**

---


# FastAPI Chat (Refactor)

Projeto refatorado de um chat em tempo real usando FastAPI + MongoDB + WebSockets.

## Estrutura
```bash
- `main.py` - inicialização do FastAPI e montagem das rotas/websockets
- `config.py` - configurações (MONGO_URL, MONGO_DB)
- `database.py` - conexão com MongoDB (motor) e funções auxiliares
- `models.py` - modelos Pydantic e funções de serialização
- `ws_manager.py` - classe `WSManager` para gerenciar conexões WebSocket
- `routes/messages.py` - rotas REST relacionadas a mensagens
- `requirements.txt` - dependências necessárias
```


## Como rodar
1. Crie um virtualenv e ative:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure variáveis de ambiente **ou** edite `config.py`:
   - `MONGO_URL` - string de conexão do MongoDB (ex: Atlas)
   - `MONGO_DB` - nome do banco
4. Rode a aplicação:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
5. Endpoints:
   - `POST /messages` - enviar mensagem (JSON com `sender` e `content`)
   - `GET  /messages` - listar mensagens (params: `limit`, `before_id`)
   - WebSocket em `/ws` - conexão WS para receber broadcasts de mensagens

## Observações
- Antes de usar, certifique-se de ter um MongoDB disponível e de ter atualizado `MONGO_URL`.s