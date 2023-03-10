import json
import os 
import requests

import pathlib            
import time
class existZip:
    #constructor:
    def __init__(self):
        try:
            with open('/var/www/html/XtamLite-UI/configuration.json') as file:
                data = json.load(file)
                #esta es la ip detectada por ethernet
                self.ipXtam = data['ipXtamRemoto']
                #poner la ip del central
                self.ipCentral = data['ipXtamCentral']
        except Exception as e:
            print("Exepcion en el constructor ", e)
    
    #cuantos archivos existen
    def howFiles(self):
        try:
            #directorio actual
            #self.cwd = os.getcwd()
            self.cwd  = "/home/pi/XtamLite/Streaming"
            self.initial_count = 0
            for path in os.listdir(self.cwd):
                if os.path.isfile(os.path.join(self.cwd, path)):
                    self.initial_count += 1
            self. cameras = self.initial_count-1
            return self. cameras
        except Exception as e:
            print("Se ha presentado una exepcion en la funcion : howFiles",e)
        
    #calculo la posicion de las comillas del comando
    def characters(self,content):
        try:
            self.content = content
            #logica
            self.positions  = []
            self.textt      = []
            for index in range ( len ( self.content ) ):
                if self.content[index] == '"':
                    self.positions.append(index )
            self.subcadena = self.content[self.positions[0]:self.positions[1]+1]
            return self.subcadena
        except Exception as e:
            print("Se ha presentado una exepcion en la funcion : characters",e)
        
    #funcion que extrae la camara o el rtsp del final del comando.
    def finalCharacters(self,numberr):
        try:
            
            #directorio actual
            #cwd = os.getcwd()
            cwd = "/home/pi/XtamLite/Streaming"
            test = '{base}/camara{number}.sh'.format(base=cwd,number=numberr)
            myfile = open(test,'r')
            ult_line = ""
            for num, name in enumerate(myfile, start=1):
                if(num == 3):
                    ult_line = name 
            subcadena = ult_line[-7:]
            return subcadena
        except Exception as e:
            print("Se ha presentado una exepcion en la funcion : finalCharacters",e)
        
    # Core del programa: abre compara y escribe en la carpeta streaming
    def openFile(self,uptText):
        try:
            #self.lii = []
            i=1
            cameras = self.howFiles()+1
            #directorio actual
            cwd = "/home/pi/XtamLite/Streaming"
            while i <= cameras:
                #importar modulo peticion 
                test = '{base}/camara{number}.sh'.format(base=cwd,number=i)
                co = open(test,'r')
                self.characte = co.read()
                #Logica:
                self.characters(self.characte)
                self.finalCharacters(i)

                self.before = self.characters(self.characte)
                self.camera = self.finalCharacters(i)
                updatee = uptText
                #Nuevo Comando
                self.pathNewComand = updatee
                with open(self.pathNewComand) as f:
                    self.act = f.readlines()[0]
                    self.spltNewComand = (self.act.split('""'))
                    
                self.comandUpt = '{ini} {ip} {rtsp}{camm}'.format(ini=self.spltNewComand[0],ip= self.before ,rtsp=self.spltNewComand[1],camm=self.camera )
    
                self.oldComand = "/home/pi/XtamLite/Streaming/{camm}.sh".format(camm=self.camera)
                with open(self.oldComand) as v:
                    self.coa = v.readlines()[2]
                
                if self.coa ==  self.comandUpt:
                    print('Son iguales, no aplica para actualizacion!')
                    self.falgUpt = False
                else:
                    print("Distintos , aplico el nuevo comando o actualizacion!")
                    self.line1 ="#!/bin/bash\n"
                    self.line2 ="#script streaming\n"
                    self.filee = open(self.oldComand ,'w')
                    self.filee.write(self.line1+self.line2+self.comandUpt)
                    self.filee.close()
                    self.falgUpt = 'reboot'
                self.lii.append(self.falgUpt)
                i+=1
        except Exception as e:
            print("Se ha presentado una exepcion en la funcion : openFile",e)

    #descomprimir el zip que viene de la peticion
    def execUpt(self):
        try:
            self.lii = []
            #directorio actual
            self.cwd =  "/home/pi/Videos" #os.getcwd()
            #las versiones del zip solo soporten un decimal (IMPORTANTE)
            self.listZip = []
            self.listVersions = []
            #print(self.cwd)
            for path in os.listdir(self.cwd):
                x=pathlib.Path('{ruta}{slash}{path}'.format(slash='/',path=path,ruta=self.cwd))
                #print('Extension:', x.suffix)
                if x.suffix == '.zip':
                    self.listZip.append(x)
                    self.listVersions.append(x.stem.split("_")[1])
            #RETORNAR EL MAXIMO     
            self.numb = [ float(x) for x in self.listVersions]
            self.fileBigg = "Update_{v}.zip".format(v=max(self.numb))
            
            for path2 in os.listdir(self.cwd):
                if path2 == "Update_{v}.zip".format(v=max(self.numb)):
                    self.whatFile(path2)
                     
        except Exception as e:
            print("Exepcion en la funcion :: execUpt",e)
        
    #funcion que valida si existen actualizaciones?
    def dataRequest(self):
        try:
            # api-endpoint
            self.url = "http://{central}:3000/api/sendUpdate".format(central = self.ipCentral)
            # defining a params dict for the parameters to be sent to the API
            self.params = {'ip':self.ipXtam }#produccion cambia por ipXtam
            # sending get request and saving the response as response object
            self.r = requests.post(url = self.url, json = self.params)
            # extracting data in json format
            self.data = self.r.json()
            #print("data de la peticion ::  ", self.data)
            if self.data["status"] == True :
                #ejecute la descompresion
                #print (self.data)
                 
                 self.execUpt()
                 self.flagUpt = True
            else: 
                print("No tiene actualizaciones disponibles!")
                self.flagUpt = False
        except Exception :
            print ("Excepcion:: En peticion de la datarequest " ,Exception )
         
    def whatFile(self,patth):
        #path2 == "Update_{v}.zip".format(v=max(self.numb))
        print ("path:: " ,patth)
        fileFolder = patth.split(".zip")
        print("Que ve " , fileFolder[0])
        self.route_scripts = "/home/pi/Videos/uptfin"
     
        txt ="{pat}/{folder}/Update_{v}.txt".format(v=max(self.numb), pat = self.route_scripts,folder=fileFolder[0])
        py  ="{pat}/{folder}/Update_{v}.py".format(v=max(self.numb), pat  = self.route_scripts , folder=fileFolder[0])
        sh  ="{pat}/{folder}/Update_{v}.sh".format(v=max(self.numb), pat  = self.route_scripts, folder=fileFolder[0])
        #print(txt)
        if os.path.exists(txt) :
            #print("Existe el .txt")
            self.openFile(txt)
        if os.path.exists(py) :
            #print("Nada py")
            self.execPy(py)
        if os.path.exists(sh) :
            #print("Nada.sh")
            self.execSh(sh)
        else:
            print("Descomprima y ejecute txt")
            fileZip = 'unzip {filee}'.format(filee=patth)
            os.system(fileZip)
            if os.path.exists(py) :
                #print("Existe el .py")
                self.execPy(py)
            elif os.path.exists(sh) :
                #print("Existe el .sh")
                self.execSh(sh)
            elif os.path.exists(txt) :
                #print("Existe el .txt")
                self.openFile(txt)
                    
    #Ejecutar scripts .py
    def execPy (self,scripy):
        try:
            if os.path.exists(scripy) :
                cmd = 'python3 {vers}'.format(vers= scripy)
                os.system(cmd)
                self.lii.append(True)
            else :
                print("No existe el path   ")
        except Exception as e:
            print ("Excepcion:: En la funcion execPy" ,e )
            
    #Ejecutar scripts .sh
    def execSh(self,scriptsh):
        try:
           import os
           if os.path.exists(scriptsh) :
                cm1 = 'sh {vers}'.format(vers= scriptsh)
                os.system(cm1)
                self.lii.append(True)
           else :
                print("No existe el path   ") 
        except Exception as e:
            print ("Excepcion:: En la funcion execSh" ,e )
            
    #funcion para Actualizar BD 
    def UpdateDb(self):
        #print (" que ve : ",self.lii )
        #print("DATA:: ", self.data)
        try:
            for valuee in self.lii:
                print(self.lii)
                if valuee == True:
                    print("Logica actualizacion::  ",self.data['ip'])
                    # api-endpoint
                    self.url = "http://{central}:3000/api/uptStateXyams".format(central=self.ipCentral  )
                    # defining a params dict for the parameters to be sent to the API
                    self.params = {'ip': self.data['ip'] ,'actualizacion': self.data['vsion']}
                    # sending get request and saving the response as response object
                    self.r = requests.post(url = self.url, json = self.params)
                    # extracting data in json format
                    self.data = self.r.json()
                    if self.r.status_code == 200:
                        print ( "Remoto Actualizado")
                    else :
                        err = "remoto No Actualizado,{ipp} ".format (ipp = self.data['ip'])
                        print( err)
                    break
                elif valuee == 'reboot':
                    print("Acutializacion y Reinicio")
                   
                    # api-endpoint
                    self.url = "http://{central}:3000/api/uptStateXyams".format(central=self.ipCentral)
                    # defining a params dict for the parameters to be sent to the API
                    self.params = {'ip': self.data['ip'] ,'actualizacion': self.data['vsion']}
                    # sending get request and saving the response as response object
                    self.r = requests.post(url = self.url, json = self.params)
                    # extracting data in json format
                    self.data = self.r.json()
                    if self.r.status_code == 200:
                        print ( "Remoto Actualizado")
                        print("En 20 segundos se reiniciara el sistema")
                        time.sleep(8)
                        print("Reiniciar")
                        os.system("sudo python3 /home/pi/XtamLite/Watchdog-Service/restart-all-services.py")
                    else :
                        err = "remoto No Actualizado,{ipp} ".format (ipp = self.data['ip'])
                        print( err)
                    break
        except Exception as e:
            print ("Excepcion:: en la funcion  UpdateDb ",e)     
  
    ################################## Fin Actualizar BD ##############################

#Desencadenar la logica
try:
    watuptxtam = existZip()
    watuptxtam.dataRequest()
    if ( watuptxtam.flagUpt) :
        watuptxtam.UpdateDb()
except Exception as e:
    print ("Excepcion:: En donde desencadena toda la logica ",e)     


