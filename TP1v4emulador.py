import sys, os
import threading
max_tam=0xffff*2
sync1 = '\xdc'
sync2 = '\xc0'
sync3 = '\x23'
sync4 = '\xc2'
sync_str = 'dcc023c2'
textoescr = ''
#fescr = open(sys.argv[2],'ab');
fler = open(sys.argv[1],'rb');
from struct import *
import socket


def carry_around_add(a, b):
    c = a + b
    return(c &0xffff)+(c>>16)

def checksum(msg):
    s=0
    for i in range(0, (len(msg)-1),2):
        w = ord(msg[i])+(ord(msg[i+1])<<8)
        s = carry_around_add(s, w)
    return~s &0xffff

textoescr=''
def connection_test(str_test):
    global textoescr
    if len(str_test)==0:
        quit();
        #t2.join()

def receber(s):
    global textoescr
    pack_count = 1
    flag_sync=0;
    while True:
        erro = 0
        count_sync = 0
        pt1 = s.recv(1)
        connection_test(pt1);
        pt2 = s.recv(1)
        connection_test(pt2);
        pt3 = s.recv(1)
        connection_test(pt3);
        pt4 = s.recv(1)
        connection_test(pt4);
        while count_sync < 2:
            if(pt1 == sync1):
                if(pt2 == sync2):
                    if(pt3 == sync3):
                        if(pt4 == sync4):
                            #print hex(ord(pt1)), hex(ord(pt2)), hex(ord(pt3)), hex(ord(pt4))
                            count_sync = count_sync + 1
                            if count_sync == 2:
                                flag_sync = 1
                                pack_count=pack_count+1
                                a = ""
                                pack_ok=0
                                #print 'sincronizou'
                            pt1 = b'\x00'
                            pt2 = b'\x00'
                            pt3 = b'\x00'
                            pt4 = b'\x00'
            else:
                pt1 = pt2
                pt2 = pt3
                pt3 = pt4
                pt4 = s.recv(1)
                connection_test(pt4);
        if flag_sync == 1:
            flag_sync = 0
            count_sync=0
            temp_tuple = s.recv(2)
            connection_test(temp_tuple);
            temp_tuple = unpack('!H', temp_tuple)
            checksum_R = temp_tuple[0]
            temp_tuple = s.recv(2)
            connection_test(temp_tuple);
            temp_tuple = unpack('!H',temp_tuple)
            length = temp_tuple[0]
            reserved = s.recv(2)
            connection_test(reserved);
            i=0
            if length>0:
                a=s.recv(length*2)
            frame = sync_str+sync_str+'0000'+("%04x"%length)+("%02x"%ord(reserved[0]))+("%02x"%ord(reserved[1]))+a
            print 'pacote',pack_count-1
            print 'checksum:', checksum(frame), checksum_R
            print 'recebendo'
            if(int(checksum(frame))==checksum_R):
                print 'salvando...'
                fescr = open(sys.argv[2],'ab');
                fescr.write(a)
                fescr.close()
                print 'salvo! :)'
            else:
                print 'PACOTE COM ERRO!! :((((( \n Descartado'

def reserved():
    return b'\xbe\xef';
def enviar(s):
    arq_tam = os.stat(sys.argv[1]).st_size
    nPacotes=0
    if arq_tam <= (max_tam/2):
        nPacotes = 1
    else:
        nPacotes = (arq_tam / (max_tam/2)) + 1
    pack_count = 0
    while (nPacotes-pack_count)>0:
        frame = fler.read(max_tam)
        length = (len(frame)/2)
        frame_h = sync_str+sync_str+'0000'+("%04x"%length)+'beef'+frame
        frame = frame.encode("hex")
        s.send('\x45')
        s.send('\x45')
        s.send('\x45')
        s.send(sync1)
        s.send(sync2)
        s.send(sync3)
        s.send(sync4)
        s.send(sync1)
        s.send(sync2)
        s.send(sync3)
        s.send(sync4)
        s.send(pack('!H',checksum(frame_h)))
        s.send(pack('!H',length))
        s.send(reserved())
        s.send(frame.decode("hex"))
        pack_count+=1
    fler.close;


if sys.argv[5]=='ativo':
    HOST = sys.argv[3]     # Endereco IP do Servidor
elif sys.argv[5]=='passivo':
    HOST = ''

PORT = int(sys.argv[4])
if sys.argv[5]=='passivo':
    anzol = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0) #socket "anzol" (que aceita novas conexoes)
    orig = (HOST, PORT)
    anzol.bind(orig)
    anzol.listen(1)
    new_s, cliente = anzol.accept()
    t1=threading.Thread(target=enviar, args = (new_s,))
    t2=threading.Thread(target=receber, args = (new_s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    new_s.close();
    quit();

elif sys.argv[5]=='ativo':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    dest = (HOST, PORT)
    s.connect(dest)
    t1=threading.Thread(target=enviar, args = (s,))
    t2=threading.Thread(target=receber, args = (s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    s.close()
    quit();
