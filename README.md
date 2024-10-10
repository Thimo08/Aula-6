### Curso Técnico de Desenvolvimento de Sistemas - Senai Itapeva
# Projeto Blog
![aa](Proj.%20Blog/static/img_blog.jpg)

## Propósito
Este projeto é uma aplicação web desenvolvida em Python utilizando o framework Flask. Seu propósito é criar uma plataforma de blog onde usuários podem se registrar, fazer login, criar postagens e, para administradores, gerenciar usuários e posts. O sistema permite que os usuários interajam através da criação e visualização de postagens, enquanto os administradores têm controle total sobre o gerenciamento de usuários e conteúdos.

## Descrição
A aplicação é estruturada de forma a facilitar a navegação e o gerenciamento de conteúdo. Com uma interface amigável, os usuários podem facilmente acessar as funcionalidades de login, criação de postagens, e os administradores têm acesso a uma área exclusiva para gerenciar usuários e posts. A conexão ao banco de dados é realizada via MySQL, garantindo um armazenamento seguro e eficiente das informações.

## Índice
1. [Instalação](#instalação)
2. [Funcionalidades](#funcionalidades)
3. [Estrutura do Código](#estrutura-do-código)
4. [Problema Resolvido](#problema-resolvido)
5. [Tecnologias Utilizadas](#tecnologias-utilizadas)
6. [Como Contribuir](#como-contribuir)

## Funcionalidades
- **Login e Logout**: Usuários podem se registrar e fazer login para acessar suas contas.
- **Criação de Postagens**: Usuários autenticados podem criar novas postagens no blog.
- **Gerenciamento de Usuários**: Administradores podem visualizar, editar e excluir usuários.
- **Gerenciamento de Postagens**: Administradores podem visualizar, editar e excluir postagens.
- **Interface Amigável**: Design simples e intuitivo para facilitar a navegação.
- **Tratamento de Erros**: Implementação de páginas de erro, como a 404 para páginas não encontradas.

## Estrutura do Código
O código é organizado em várias rotas que correspondem às diferentes funcionalidades do site. As principais rotas incluem:
* /: Página principal que exibe postagens.
* /login: Página de login para usuários.
* /logout: Rota para realizar logout e limpar a sessão do usuário.
* /novopost: Página para criação de novas postagens (acessível apenas para usuários autenticados).
* /cadastro_post: Rota para receber dados de postagem do formulário.
* /acesso: Rota para verificar o acesso do usuário (login).
* /adm: Área administrativa para gerenciamento de usuários e postagens (acessível apenas para administradores).
* /novousuario: Página para registro de novos usuários (acessível apenas para administradores).
* /cadastro_usuario: Rota para receber os dados e cadastrar um novo usuário (acessível apenas para administradores).
* /editar-user/<int:id>: Rota para abrir o formulário de edição de um usuário específico (acessível apenas para administradores).
* /atualizar_usuario: Rota para atualizar os dados do usuário (acessível apenas para administradores).
* /excluir-user/<int:id>: Rota para excluir um usuário e seus posts (acessível apenas para administradores).
* /excluir-post/<int:id>: Rota para excluir um post (acessível para administradores e para usuários que criaram o post).
* /404: Tratamento de erro 404 - Página não encontrada.

As funções de conexão e encerramento do banco de dados são centralizadas, garantindo um código mais limpo e evitando duplicação.

## Problema Resolvido
A aplicação resolve o problema de gerenciamento de conteúdo e interação em um blog, permitindo que usuários comuns publiquem suas opiniões e pensamentos, enquanto proporciona a administradores a capacidade de manter a ordem e segurança da plataforma. Isso é especialmente útil para sites que precisam de um controle eficaz sobre o que é publicado e por quem, oferecendo uma solução prática e eficiente para blogs e plataformas de conteúdo.

## Tecnologias Utilizadas
- ![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white): Framework para desenvolvimento web em Python.
- ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white): Sistema de gerenciamento de banco de dados.
- ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white): Para a construção da interface do usuário.
- ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white): Para a construção da interface gráfica do usuário.
- ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue): Linguagem de programação utilizada no backend.

---