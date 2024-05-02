## Projeto Autenticacao
## Daniel Lourenço
## Maio 2024

import hashlib
import tkinter as tk
from tkinter import *
from connection import * 

#funcao para ocultar e mostrar a password(cadastro)
def showPwcadastro():
    if entrada_pw.cget("show") == "*":
        entrada_pw.config(show="")
    else:
        entrada_pw.config(show="*")

#funcao para ocultar e mostrar a password(login)
def showPwlogin():
    if entrada_pw.cget("show") == "*":
        entrada_pw.config(show="")
    else:
        entrada_pw.config(show="*")

#funcao para esconder a pagina que mostra as contas
def hide_contas():
    root_contas.withdraw()

#funcao para validar o login
def infologin():
    em = entrada_em.get()
    pw = entrada_pw.get()

    #encriptacao da password
    pw_encriptada = hashlib.sha1(pw.encode())
    pass_encript = pw_encriptada.hexdigest()

    email = []
    password = []

    #query para saber todos os emails contidos na database
    email_check = f"SELECT email FROM users"
    myqueries.execute(email_check)
    values = myqueries.fetchall()

    #append dos emails da database num array
    for value in values:
        email.append(str(value[0]))

    #query para saber todas as passwords contidas na database
    pw_check = f"SELECT pw FROM users"
    myqueries.execute(pw_check)
    values_pw = myqueries.fetchall()

    #append das passwords da database num array 
    for value_pw in values_pw:
        password.append(str(value_pw[0]))

    #contador para o email e password coicidirem na mesma posicao do array
    i = 0

    #while que vai percorrer o array do email para saber se os dados introduzidos correspondem
    while (i<=len(email)-1):
            
            # if para dar check ao email e password inseridos pelo user
            if em == email[i] and  pass_encript == password[i]:
                em_check = em
                label_check.config(fg="green",text="Login efetuado com sucesso")
                botao_login.config(text="Ver Conta",command=verconta)

                #query para selecionar as informacoes da conta
                info = f"SELECT * FROM users WHERE email = '{em_check}'"
                myqueries.execute(info)
                records = myqueries.fetchall()
                save_info = []
                
                #append das informacoes no array(save_info)
                for value in records:
                    save_info.append(str(value[0]))
                    save_info.append(str(value[1]))
                    save_info.append(str(value[2]))
                    save_info.append(str(value[3]))
                    save_info.append(str(value[4]))
                    save_info.append(str(value[5]))
                
                #query para dar delete as informacoes da table sessoes
                delete_login =  f"DELETE FROM sessoes"
                myqueries.execute(delete_login)
                mydatabase.commit()
                
                #insert de novas informacoes(da conta que s e fez login) na table sessoes
                save_login = f"INSERT INTO sessoes(nome,apelido,idade,telemovel,email,pw) VALUES('{save_info[0]}','{save_info[1]}',{save_info[2]},'{save_info[3]}','{save_info[4]}','{save_info[5]}')"
                myqueries.execute(save_login)
                mydatabase.commit()

                break           
            else: 
                label_check.config(fg="red",text="Credenciais Erradas")
            i+=1

def login():
    #variaveis utilizadas fora desta funcao
    global entrada_em
    global entrada_pw
    global label_check
    global botao_login

    #criacao de uma nova janela Toplevel(root_login)
    root_login = Toplevel()
    root_login.title("Login")
    root_login.geometry("200x190+800+300")
    root_login.resizable(0,0)
    root_login.configure(background="white")
    root_login.iconbitmap("Autenticacao/img/icons/login.ico")
    root_login.columnconfigure(0, weight=1)
    root_login.rowconfigure(0, weight=0)

    Label_login= Label(root_login,bg="white", width=9,text="Email:")
    Label_login.grid(column=0,row=1,padx=2,pady=2)

    entrada_em = Entry(root_login,width=24,bg="ghostwhite")
    entrada_em.grid(column=0,row=2)

    label_pw= Label(root_login,bg="white", width=9,text="Password")
    label_pw.grid(column=0,row=3,padx=2,pady=2)

    entrada_pw = Entry(root_login,width=24,bg="ghostwhite",show='*')
    entrada_pw.grid(column=0,row=4)

    showpw_check = Checkbutton(root_login,bg="white",text="Mostrar Palavra-Passe",command=showPwlogin)
    showpw_check.grid(column=0,row=5,padx=2,pady=2)

    label_check = Label(root_login,bg="white", fg="white",text="Login efetuado com sucesso")
    label_check.grid(column=0,row=6,padx=0,pady=0)

    botao_login= Button(root_login,bg="#e6f3ff", width=9,text="Login",command=infologin)
    botao_login.grid(column=0,row=7,padx=2,pady=2)

def infocadastro():
    email = []
    #query para extrair todos os emails da database
    email_check = f"SELECT email FROM users"
    myqueries.execute(email_check)
    values = myqueries.fetchall()

    #append dos mesmos emails num array
    for value in values:
        email.append(str(value[0])) 

    nome = entrada_nome.get()
    apelido = entrada_apelido.get()
    idade = entrada_idade.get()
    telemovel = entrada_numero.get()
    em = entrada_em.get()
    pw = entrada_pw.get()

    #encriptacao da password inserida pelo user
    pw_encriptada = hashlib.sha1(pw.encode())

    #condicao caso o email inserido pelo user ja exista na database
    if em in email:
        label_check.config(fg="red",text="Email ja está associado a outra conta")
    else:
        #insert dos dados inseridos pelo user na table users
        saveInfo = f"INSERT INTO users(nome,apelido,idade,telemovel,email,pw) VALUES('{nome}','{apelido}',{idade},'{telemovel}','{em}','{pw_encriptada.hexdigest()}')"
        myqueries.execute(saveInfo)
        mydatabase.commit()

        #delete dos registos na table sessos
        delete_login =  f"DELETE FROM sessoes"
        myqueries.execute(delete_login)
        mydatabase.commit()

        #insert dos dados inseridos pelo user na table sessoes
        save_login = f"INSERT INTO sessoes(nome,apelido,idade,telemovel,email,pw) VALUES('{nome}','{apelido}',{idade},'{telemovel}','{em}','{pw_encriptada.hexdigest()}')"
        myqueries.execute(save_login)
        mydatabase.commit()

        botao_registo.config(text="Ver Conta",command=verconta)

        
def cadastro():
    #variaveis utilizadas fora desta funcao
    global entrada_nome
    global entrada_apelido
    global entrada_idade
    global entrada_numero
    global entrada_em
    global entrada_pw
    global label_check
    global botao_registo

    #criacao de uma nova janela Top level(root_cadastro)
    root_cadastro = Toplevel()
    root_cadastro.title("Cadastro")
    root_cadastro.geometry("530x230+800+300")
    root_cadastro.resizable(0,0)
    root_cadastro.configure(background="white")
    root_cadastro.iconbitmap("Autenticacao/img/icons/login.ico")

    Label_nome= Label(root_cadastro,bg="white", width=7,text="Nome :")
    Label_nome.grid(column=1,row=1,padx=2,pady=2)

    entrada_nome = Entry(root_cadastro,width=15,bg="ghostwhite")
    entrada_nome.grid(column=2,row=1,padx=2,pady=2)

    label_apelido= Label(root_cadastro,bg="white", width=7,text="Apelido :")
    label_apelido.grid(column=1,row=2,padx=2,pady=2)

    entrada_apelido = Entry(root_cadastro,width=15,bg="ghostwhite")
    entrada_apelido.grid(column=2,row=2,padx=2,pady=2)

    label_idade= Label(root_cadastro,bg="white", width=7,text="Idade :")
    label_idade.grid(column=1,row=3,padx=2,pady=2)

    entrada_idade = Entry(root_cadastro,width=15,bg="ghostwhite")
    entrada_idade.grid(column=2,row=3,padx=2,pady=2)

    label_numero= Label(root_cadastro,bg="white", width=20,text="Numero de Telemovel :")
    label_numero.grid(column=1,row=4,padx=2,pady=2)

    entrada_numero = Entry(root_cadastro,width=15,bg="ghostwhite")
    entrada_numero.grid(column=2,row=4,padx=2,pady=2)

    label_em= Label(root_cadastro,bg="white", width=9,text="Email :")
    label_em.grid(column=1,row=5,padx=2,pady=2)

    entrada_em = Entry(root_cadastro,width=15,bg="ghostwhite")
    entrada_em.grid(column=2,row=5,padx=2,pady=2)

    label_pw= Label(root_cadastro,bg="white", width=9,text="Password :")
    label_pw.grid(column=1,row=6,padx=2,pady=2)

    entrada_pw = Entry(root_cadastro,width=15,bg="ghostwhite",show='*')
    entrada_pw.grid(column=2,row=6,padx=2,pady=2)

    showpw_check = Checkbutton(root_cadastro,bg="white",text="Mostrar Palavra-Passe",command=showPwcadastro)
    showpw_check.grid(column=3,row=6,padx=2,pady=2)

    label_check = Label(root_cadastro,bg="white", fg="white",text="Email ja está associado a outra conta")
    label_check.grid(column=2,row=7,padx=0,pady=0)

    botao_registo= Button(root_cadastro,bg="#e6f3ff", width=9,text="Registar",command=infocadastro)
    botao_registo.grid(column=2,row=8,padx=2,pady=2)

#funcao info da conta logada
def verconta():
    global root_contas
    show_info = f"SELECT * FROM sessoes"
    myqueries.execute(show_info)
    values = myqueries.fetchall()

    save_info = []

    for value in values:
        save_info.append(str(value[0]))
        save_info.append(str(value[1]))
        save_info.append(str(value[2]))
        save_info.append(str(value[3]))
        save_info.append(str(value[4]))

    root_contas = Toplevel()
    root_contas.title("Conta")
    root_contas.geometry("300x170+800+300")
    root_contas.resizable(0,0)
    root_contas.configure(background="white")
    root_contas.iconbitmap("Autenticacao/img/icons/conta.ico")

    Label_nome= Label(root_contas,bg="white", width=7,text="Nome :")
    Label_nome.grid(column=1,row=1,padx=2,pady=2)

    Label_mostrarnome= Label(root_contas,bg="white", width=7,text=save_info[0])
    Label_mostrarnome.grid(column=2,row=1,padx=2,pady=2)

    label_apelido= Label(root_contas,bg="white", width=7,text="Apelido :")
    label_apelido.grid(column=1,row=2,padx=2,pady=2)

    Label_mostrarapelido= Label(root_contas,bg="white", width=7,text=save_info[1])
    Label_mostrarapelido.grid(column=2,row=2,padx=2,pady=2)

    label_idade= Label(root_contas,bg="white", width=7,text="Idade :")
    label_idade.grid(column=1,row=3,padx=2,pady=2)

    Label_mostraridade= Label(root_contas,bg="white", width=7,text=save_info[2])
    Label_mostraridade.grid(column=2,row=3,padx=2,pady=2)

    label_numero= Label(root_contas,bg="white", width=20,text="Numero de Telemovel :")
    label_numero.grid(column=1,row=4,padx=2,pady=2)

    Label_mostrarnumero= Label(root_contas,bg="white", width=7,text=save_info[3])
    Label_mostrarnumero.grid(column=2,row=4,padx=2,pady=2)

    label_em= Label(root_contas,bg="white", width=9,text="Email :")
    label_em.grid(column=1,row=5,padx=2,pady=2)

    Label_mostraremail= Label(root_contas,bg="white",width=12,text=save_info[4])
    Label_mostraremail.grid(column=2,row=5,padx=2,pady=2)

    botao_fechar = Button(root_contas,bg="#e6f3ff",fg="red",width=9,text="Fechar",command=hide_contas)
    botao_fechar.grid(column=2,row=6,padx=2,pady=2)

###################
# MENU PRINCINPAL #
###################

#criacao da primeira janela(root)
root = Tk()
root.title("Inicio")
root.geometry("200x155+800+300")
root.resizable(0,0)
root.configure(background="white")
root.iconbitmap("Autenticacao/img/icons/inicio.ico")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)

botao_login = Button(root,bg="#e6f3ff", width=9,text="Login",command=login)
botao_login.grid(column=0,row=1,padx=5,pady=5)

botao_registo = Button(root,bg="#e6f3ff",width=9,text="Criar Conta",command=cadastro)
botao_registo.grid(column=0,row=2,padx=2,pady=2)

botao_info = Button(root,bg="#e6f3ff",width=9,text="Ver Conta",command=verconta)
botao_info.grid(column=0,row=3,padx=2,pady=2)

botao_fechar = Button(root,bg="#e6f3ff",fg="red",width=9,text="Fechar",command=exit)
botao_fechar.grid(column=0,row=4,padx=2,pady=2)

root.mainloop()