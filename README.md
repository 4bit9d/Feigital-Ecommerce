# 🛒 Feigital Ecommerce

Um sistema completo de **ecommerce desenvolvido em Django**, incluindo autenticação de usuários, cadastro de produtos, carrinho, sistema de pedidos e painel administrativo para vendedores.

Este README foi gerado com base no código real presente no projeto enviado (pasta **feigital/**). Abaixo está exatamente a documentação correspondente à estrutura, funcionalidades e tecnologias usadas no seu projeto.

---

## 📦 Sobre o Projeto

O **Feigital Ecommerce** é um marketplace simples onde vendedores podem cadastrar seus produtos e usuários podem navegar, adicionar ao carrinho e finalizar pedidos.

O projeto contém:

* Sistema completo de cadastro/login (Django Auth)
* CRUD de produtos
* Upload de imagens (pasta **media/**)
* Carrinho de compras persistente
* Sistema de pedidos
* Painel de administração Django
* Templates HTML com layout pronto
* Rotas bem estruturadas

---

## 📁 Estrutura do Projeto (Real)

```
feigital/
├── core/                 # App principal do ecommerce
│   ├── admin.py          # Registro de modelos
│   ├── apps.py
│   ├── forms.py          # Formulários
│   ├── models.py         # Banco de dados: Produtos, Pedidos etc.
│   ├── templates/        # Templates HTML
│   ├── urls.py           # Rotas
│   └── views.py          # Lógica das páginas
│
├── feigital_project/     # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/                # Imagens de produtos
├── static/               # CSS, JS, imagens
├── manage.py             # Comando principal
└── db.sqlite3            # Banco de dados
```

---

## 📦 Modelos Principais

### **Produto**

* Nome
* Descrição
* Preço
* Imagem
* Estoque

### **Pedido e Itens do Pedido**

* Carrinho
* Quantidade
* Total

### **Usuários**

* Cadastro/login via Django Authentication

---

## 🚀 Como Rodar o Projeto

### **1. Criar o ambiente virtual (opcional mas recomendado)**

```
python -m venv venv
venv/Scripts/activate  # Windows
```

### **2. Instalar dependências**

```
pip install django pillow
```

### **3. Rodar migrações**

```
python manage.py migrate
```

### **4. Executar o servidor**

```
python manage.py runserver
```

Acesse em:

```
http://127.0.0.1:8000/
```

---

## 🧩 Funcionalidades

* Login e cadastro de usuários
* Listagem de produtos
* Página individual do produto
* Carrinho com adicionar/remover itens
* Finalização de pedido
* Painel admin com CRUD de produtos
* Upload de imagens

---

## 🖼️ Templates HTML

Todo o frontend está localizado em:

```
core/templates/
```

Com páginas como:

* home.html
* produto.html
* carrinho.html
* pedido_finalizado.html

---

## 🛠️ Tecnologias

* **Python 3**
* **Django**
* **SQLite**
* **Pillow** (upload de imagens)
* HTML, CSS, JavaScript

---

## 📜 Licença

Este projeto é aberto para estudo e personalização.

---

Se quiser, posso também:
✅ Criar um **logo** para o projeto
✅ Criar **badges** para o README
✅ Gerar **prints das telas** automaticamente
