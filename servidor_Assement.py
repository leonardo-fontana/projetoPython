import socket, psutil, pickle, os, cpuinfo

#---------------- Socket-----------------------------------------------
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
host = socket.gethostname()                         
porta = 11037
socket_servidor.bind((host, porta))
socket_servidor.listen()
print("Servidor de nome", host, "esperando conexão na porta", porta)
(socket_cliente,addr) = socket_servidor.accept()
print("Conectado a:", str(addr))
#---------------- Socket-----------------------------------------------

def enviaDados(dados): #Função para evitar repetir código
    info = pickle.dumps(dados)
    socket_cliente.send(info)
    
while True:
    msg = socket_cliente.recv(1000000)
    if msg.decode('ascii') == 'fim':
	    break
    elif msg.decode('ascii') == '1': #Informações da memória
        memory = psutil.virtual_memory()
        enviaDados(memory)
    elif msg.decode('ascii') == '2':
        disco = psutil.disk_usage('.')
        enviaDados(disco)
    elif msg.decode('ascii') == '3':
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        info_cpu = cpuinfo.get_cpu_info()
        cpuFreq = str(round(psutil.cpu_freq().current, 2))
        cpuLog = str(psutil.cpu_count())
        cpuLogFalse = str(psutil.cpu_count(logical=False))
        lista = []
        lista.append(cpu_percent)
        lista.append(info_cpu)
        lista.append(cpuFreq)
        lista.append(cpuLog)
        lista.append(cpuLogFalse)
        enviaDados(lista)
    elif msg.decode('ascii') == '4':
        texto = "Digite o caminho de um arquivo/diretorio(sem o nome do arquivo final)"
        socket_cliente.send(texto.encode('ascii'))
        msg = socket_cliente.recv(1000000)
        path = msg.decode('ascii')
        texto1 = 'Agora digite o nome do arquivo (ou diretorio) que deseje  saber os status'
        socket_cliente.send(texto1.encode('ascii'))
        msg = socket_cliente.recv(1000000)
        nomeArquivo = msg.decode('ascii')
        caminho = path + "\\" + nomeArquivo
        status = os.stat(caminho)
        lista = []
        lista.append(caminho)
        lista.append(status)
        enviaDados(lista)
    elif msg.decode('ascii') == '5':
         lista = []
         for proc in psutil.process_iter():
             pinfo = proc.as_dict(attrs=['pid', 'name'])      
             lista.append(pinfo)
         
         enviaDados(lista)
         msg = socket_cliente.recv(100000000)
         pid = pickle.loads(msg)
         processo = psutil.Process(pid)
         enviaDados(processo)
    elif msg.decode('ascii') == '6':
        interfaces = psutil.net_if_addrs()
        status = psutil.net_if_stats()
        nomes = []
        for i in interfaces:
            nomes.append(str(i))
        texto = "Escreva o nome de uma das redes acima para mostrar os respectivos valores: "
        lista = []
        lista.append(nomes)
        lista.append(interfaces)
        lista.append(status)
        lista.append(texto)
        enviaDados(lista)
        
        
        
    elif msg.decode('ascii') == '0':
        print("Finalizando programa...")
        break
        

# Fecha socket do servidor e cliente
socket_cliente.close()
socket_servidor.close()

