import socket, time, pickle, pygame, cpuinfo, psutil, os
	
# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#-----------------------------Pygame--------------------------------------
largura_tela = 750
altura_tela = 400
pygame.display.set_caption("Informações do computador")
branco = (255,255,255)
azul = (0, 0, 255)
preto = (0,0,0)
vermelho = (34,177,76)
cinza = (100, 100, 100)
pygame.font.init()
font = pygame.font.Font(None, 32)
s1 = pygame.surface.Surface((largura_tela, altura_tela/2))
s2 = pygame.surface.Surface((largura_tela, altura_tela))
#-----------------------------Pygame--------------------------------------

def fecha_pygame(nomeFuncao,nomeParametro):
#Utilizar para fechar o pygame e atualizar a cada 1 segundo utilizando o nome da função e o nome de seu respectivo parametro
    clock = pygame.time.Clock()
    cont = 60
    terminou = False 
    while not terminou:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True      
        if cont == 60:
            tela.fill(preto)
            nomeFuncao(nomeParametro)
            cont = 0 
        pygame.display.update()
        clock.tick(60)
        cont = cont + 1
    pygame.display.quit()
def mostraMenu(): # Menu de opções
    print("")
    print("1)Porcentagem de uso de memória.")
    print("2)Porcentagem de uso de disco.")
    print("3)Informações da CPU.")
    print("4)Informações de um arquivo ou diretório.")
    print("5)Informações de um processo.")
    print("6)Informações de uma rede.")
    print("0) Finalizar programa.")
    print("")

def mostra_texto(s1, nome, chave, pos_y, lista):
    text = font.render(nome, True, cinza)
    s1.blit(text, (0, pos_y))
    if chave == "freq":
        s = str(lista[2])
    elif chave == "nucleos":
      s = str(lista[3])
      s = s + " (" + str(lista[4]) +  ")"
    else:
      infoCPU = lista[1]
      s = str(infoCPU[chave])
    text = font.render(s, True, cinza)
    s1.blit(text, (200, pos_y))

def mostra_info_cpu(listaCPU): 
    text = font.render("Informações da CPU", 1, branco)
    mostra_texto(s1, "Nome: ", "brand", 30, listaCPU)
    mostra_texto(s1, "Arquitetura: ", "arch", 50, listaCPU)
    mostra_texto(s1, "Palavra (bits): ", "bits", 70, listaCPU)
    mostra_texto(s1, "Frequência (MHz): ", "freq", 90, listaCPU)
    mostra_texto(s1, "Núcleos (físicos): ", "nucleos", 110, listaCPU)
    tela.blit(s1, (0, 0))
    tela.blit(text, (0, 10))

def mostra_uso_memoria(mem): #Informações de uso de memória (Opção 1)
    larg = largura_tela - 2*20
    pygame.draw.rect(s1, azul, (20, 50, larg, 70))
    larg = larg*mem.percent/100
    porcentagem = mem.percent
    pygame.draw.rect(s1, vermelho, (20, 50, larg, 70))
    total = round(mem.total/(1024*1024*1024),2)
    texto_barra = "Memória Utilizada: {:0.2f}% | Total de memória: {:0.2f} GB".format(porcentagem, total)
    texto = "Feche o pygame para continuar..."
    text = font.render(texto_barra, 1, branco)
    text2 = font.render(texto, 1, branco)
    tela.blit(s1, (0, 150))
    tela.blit(text, (20, 180))
    tela.blit(text2, (20, 350))
    pygame.display.set_caption("Informações de uso de memória")
    pygame.display.update()
    
def mostra_uso_disco(disco):  #Informações de uso de memória (Opção 2)
    larg = largura_tela - 2*20
    pygame.draw.rect(s1, azul, (20, 50, larg, 70))
    larg = larg*disco.percent/100
    porcentagem = disco.percent
    pygame.draw.rect(s1, vermelho, (20, 50, larg, 70))
    total = round(disco.total/(1024*1024*1024), 2)
    texto_barra = "Porcentagem de uso do disco: {:0.2f}% | Total: {:0.2f}GB".format(porcentagem, total)
    texto = "Feche o pygame para continuar..."
    text = font.render(texto_barra, 1, branco)
    text2 = font.render(texto, 1, branco)
    tela.blit(s1, (0, 150))
    tela.blit(text, (20, 180))
    tela.blit(text2, (20, 350))
    pygame.display.set_caption("Informações de uso de disco")
    pygame.display.update()
    
def mostra_uso_cpu(lista): #Informações da CPU (gráfico - Opção 4)
    texto = "Feche o pygame para continuar..."
    text = font.render("Porcentagem de uso da CPU por núcleo", 1, branco)
    text2 = font.render(texto, 1, branco)
    num_cpu = len(lista[0])
    x = y = 10
    desl = 10
    alt = s2.get_height() - 2*y
    larg = (s2.get_width()-2*y - (num_cpu+1)*desl)/num_cpu
    d = x + desl
    for i in lista[0]:
        pygame.draw.rect(s2, vermelho, (d, y, larg, alt))
        pygame.draw.rect(s2, azul, (d, y, larg, (1-i/100)*alt))
        d = d + larg + desl
  # parte mais abaixo da tela e à esquerda
    tela.blit(s2, (0, altura_tela/5 + 50))
    tela.blit(text, (0, 200))
    tela.blit(text2, (0, 380))
    mostra_info_cpu(lista)
    pygame.display.set_caption("Informações de CPU")
    pygame.display.update()

def detalheArquivo(status ,caminho): #Informações de arquivo (Opção 4)
    nome = os.path.basename(caminho)
    tamanho = status.st_size / 2**10
    dataCriacao = time.ctime(status.st_ctime)
    dataModificacao = time.ctime(status.st_mtime)
    print("")
    if os.path.isfile(caminho):
        texto = "Nome do arquivo: {}\n".format(nome)
    else:
        texto = "Nome do diretorio: {}\n".format(nome)   
    texto += "Tamanho: {:0.2f} MB \n".format(tamanho)
    texto += "Tempo de criação {} \n".format(dataCriacao)
    texto += "Tempo de modificação: {}".format(dataModificacao)
    print(texto)
    
def detalheProcesso(pid, processo): #Detalhe de um processo atravém de seu pid (Opção 5)
     
    texto = "Nome do processo: {} \n ".format(processo.name())
    texto += "PID {} | ".format(pid)
    texto += "Nome de usuário do processo {} \n ".format(processo.username())
    texto += "Status do processo: {} \n ".format(processo.status())
    texto += "Tempo de criação {} | ".format(time.ctime(processo.create_time()))
    print(texto)

def infoRedes(rede, interfaces, status): #Informações de rede (Opção 6)
    
    print("Informações da rede")
    for i in interfaces[rede]:
        print("Rede selecionada: {}".format(rede))
        print("Familia: {}".format(str(i[0])))
        print("Endereço: {}".format(str(i[1])))
        print("Mascara de subrede: {}".format(str(i[2])))
        print("Broadcast: {}\n".format(str(i[3])))
   
try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 11037))
    print('Conectado com sucesso')
    msg = ''
    while msg != '0':
        mostraMenu()
        msg = input('Digite o número da opção desejada: ')
	
       
        s.send(msg.encode('ascii'))
        bytes = s.recv(10000000)
        if msg == '1':
            memoria = pickle.loads(bytes)
            tela = pygame.display.set_mode((largura_tela, altura_tela))
            mostra_uso_memoria(memoria)
            fecha_pygame(mostra_uso_memoria, memoria)
        elif msg == '2':
            disco = pickle.loads(bytes)
            tela = pygame.display.set_mode((largura_tela, altura_tela))
            fecha_pygame(mostra_uso_disco, disco)
        elif msg == '3':
            lista = pickle.loads(bytes)
            tela = pygame.display.set_mode((largura_tela, altura_tela))
            fecha_pygame(mostra_uso_cpu, lista)
        elif msg == '4':
            texto = bytes.decode('ascii')
            print(texto)
            msg = input("Caminho: ")
            s.send(msg.encode('ascii'))
            bytes = s.recv(1024)
            texto = bytes.decode('ascii')
            print(texto)
            msg = input("Nome do arquivo/diretório: ")
            s.send(msg.encode('ascii'))
            bytes = s.recv(1024)
            lista = pickle.loads(bytes)
            detalheArquivo(lista[1], lista[0])
        elif msg == '5':
            lista = pickle.loads(bytes)
            print(lista)
            
            pid = int(input("Digite o PID de um processos acima: "))
            byte = pickle.dumps(pid)
            s.send(byte)
            bytes = s.recv(1024)
            processo = pickle.loads(bytes)
            detalheProcesso(pid, processo)
        elif msg == '6':
            lista = pickle.loads(bytes)
            print(lista[0])
            rede = input("Escreva o nome de uma das redes acima para mostrar os respectivos valores: ")
            infoRedes(rede, lista[1], lista[2])
                               
except Exception as erro:
    print(str(erro))

# Fecha o socket
s.close()

input("Pressione qualquer tecla para sair...")


