from PIL import Image, ImageTk
import numpy as np
import math
import random
import ImageDraw


def escala(foto,ancho,alto):#Creacion de imagen con escala de grises
    pixeles=foto.load()#Proceso igual que el del umbral pero sin las comparaciones
    for i in range(ancho):
        for a in range(alto):
            (r,g,b)=foto.getpixel((i,a))
            promedio=int((r+g+b)/3)
            pixeles[i,a]=(promedio,promedio,promedio)
    return foto

def filtro_medio(foto,ancho,alto):
    pixeles=foto.load()#Cargarimagen
    for i in range(ancho):#Se recogrrelaimagen                                                                                               
        for j in range(alto):                                                                                                               
            (r,g,b)=foto.getpixel((i,j))
            cola=[]
            try:
                if(pixeles[i+1,j]):#Vecinos derecho                                                                                           
                    pix=pixeles[i+1,j][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j]):#Vecino izq                                                                                                
                    pix=pixeles[i-1,j][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i,j+1]):#Vecino arriba                                                                                             
                    pix=pixeles[i,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i,j-1]):#Vecino abajo                                                                                              
                    pix=pixeles[i,j-1][0]
                    cola.append((pix))
            except:
                pass                        
            try:
                if(pixeles[i+1,j+1]):#esq derecha
                    pix=pixeles[i+1,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j+1]):#esq izq 
                    pix=pixeles[i-1,j+1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i+1,j-1]):#esq der abajo
                    pix=pixeles[i+1,j-1][0]
                    cola.append((pix))
            except:
                pass
            try:
                if(pixeles[i-1,j-1]):#esq izq abajo
                    pix=pixeles[i-1,j-1][0]
                    cola.append((pix))
            except:
                pass

            

            cola.sort()
            mediano=int(np.median(cola))
            #print mediano
            #print cola
            pixeles[i,j]=(mediano,mediano,mediano)
    return foto

def diferencia(foto,foto2,ancho,alto):
    img=Image.open('escalada.png')
    pixeles=img.load()
    pixeles2=foto2.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            (r,g,b)=foto2.getpixel((i,j))
            nueva=pixeles2[i,j][0]
            original=pixeles[i,j][0]
            dif=(nueva-original)
            pixeles[i,j]=(dif,dif,dif)
    return img
    


def convolucion(foto,ancho,alto):
   # t_in=time()
    gx=[]
    gy=[]
    magnitud=[]
    Gx=([-1,0,1],[-2,0,2],[-1,0,1])#Formulas Convolucion
    Gy=([1,2,1],[0,0,0],[-1,-2,-1])
    pixeles=foto.load()
    for i in range(alto):
        gx.append([])
        gy.append([])
        for j in range(ancho):
            sumx=0
            sumy=0
            for x in range(len(Gx[0])):
                for y in range(len(Gy[0])):
                    try:
                        sumx +=(pixeles[j+y,i+x][0]*Gx[x][y])
                        sumy +=(pixeles[j+y,i+x][0]*Gy[x][y])
                    except:
                        pass
                    Gradiente_Horizontal=pow(sumx,2)#Formulas para obtener el gradiente
                    Gradiente_Vertical=pow(sumy,2)
                    Magnitud=int(math.sqrt(Gradiente_Horizontal+Gradiente_Vertical))
                    gx[i].append(sumx)
                    gy[i].append(sumy)
                    pixeles[j,i]=(Magnitud,Magnitud,Magnitud)
    #t_fi=time()
    #tot=t_fi-t_in
    #print "Tiempo bordes:"+str(tot)+"segundos"
    return foto

def binarizacion(foto,ancho,alto):
    x=150
    #print "Valor maximo binarizacion:"+str(x)
    pixeles=foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            promedio=int((r+g+b)/3)
            if promedio > x:
                pixeles[i,j]=(255,255,255)
            else:
                pixeles[i,j]=(0,0,0)
    return foto



def umbral(foto,ancho,alto):#Funcion para generar la imagen umbral
    minimo=30#valores para usar en el umbral
    maximo=200
    #print "Valor minimo: "+str(minimo)
    #print "Valor maximo: "+str(maximo)
    pixeles=foto.load()#cargar la imagen
    for i in range(ancho):#Se recorre los pixeles de la imagen
        for a in range(alto):
            (r,g,b)=foto.getpixel((i,a))
            promedio=int((r+g+b)/3)#Obtenemos el promedio de cada pixel
            if promedio <= minimo: #Se hace la comparacion con los valores 
                promedio=0
            if promedio >= maximo:
                promedio=255
            pixeles[i,a]=(promedio,promedio,promedio)#Se sustituye el valor de rgb segun sea
    return foto

def bina_invertida(foto,ancho,alto):
    x=10
    #print "Valor maximo binarizacion:"+str(x)
    pixeles=foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            promedio=int((r+g+b)/3)
            if promedio < x:
                pixeles[i,j]=(255,255,255)
            else:
                pixeles[i,j]=(0,0,0)
    return foto

def posibles(foto,ancho,alto):
    cola=[]
    cola2=[]
    pixeles=foto.load()
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)=foto.getpixel((i,j))
            if ((r,g,b)==(255,255,255)):
                cola.append((i,j))
            else:
                cola2.append((i,j))
    
    return cola,cola2

def erocion(foto,ancho,alto,cola2):
    pixeles=foto.load()#Cargarimagen
    #print actual
    x=0
    while x<len(cola2):
        (i,j)=cola2[x]
        (r,g,b)=foto.getpixel((i,j))
        
        try:
            if(pixeles[i+1,j]):#Vecinos derecho                                                                                           
                pixeles[i+1,j]=(0,0,0)
                
        except:
            pass
        try:
            if(pixeles[i-1,j]):#Vecino izq                                                                                                
                pixeles[i-1,j]=(0,0,0)
                
        except:
            pass
        try:
            if(pixeles[i,j+1]):#Vecino arriba                                                                                             
                pixeles[i,j+1]=(0,0,0)
        except:
            pass
        try:
            if(pixeles[i,j-1]):#Vecino abajo                                                                                              
                pixeles[i,j-1]=(0,0,0)
            
        except:
            pass                        
        try:
            if(pixeles[i+1,j+1]):#esq derecha
                pixeles[i+1,j+1]=(0,0,0)
                
        except:
            pass
        try:
            if(pixeles[i-1,j+1]):#esq izq 
                pixeles[i-1,j+1]=(0,0,0)
                
        except:
            pass
        try:
            if(pixeles[i+1,j-1]):#esq der abajo
                pixeles[i+1,j-1]=(0,0,0)    
        except:
            pass
        try:
            if(pixeles[i-1,j-1]):#esq izq abajo
                pixeles[i-1,j-1]=(0,0,0)
        except:
            pass

        x+=1         
        
    return foto

def dilatacion(foto,ancho,alto,cola):
    pixeles=foto.load()#Cargarimagen
    #print actual
    x=0
    while x<len(cola):
        (i,j)=cola[x]
        (r,g,b)=foto.getpixel((i,j))
        
        try:
            if(pixeles[i+1,j]):#Vecinos derecho                                                                                           
                pixeles[i+1,j]=(255,255,255)
                
        except:
            pass
        try:
            if(pixeles[i-1,j]):#Vecino izq                                                                                                
                pixeles[i-1,j]=(255,255,255)
                
        except:
            pass
        try:
            if(pixeles[i,j+1]):#Vecino arriba                                                                                             
                pixeles[i,j+1]=(255,255,255)
        except:
            pass
        try:
            if(pixeles[i,j-1]):#Vecino abajo                                                                                              
                pixeles[i,j-1]=(255,255,255)
            
        except:
            pass                        
        try:
            if(pixeles[i+1,j+1]):#esq derecha
                pixeles[i+1,j+1]=(255,255,255)
                
        except:
            pass
        try:
            if(pixeles[i-1,j+1]):#esq izq 
                pixeles[i-1,j+1]=(255,255,255)
                
        except:
            pass
        try:
            if(pixeles[i+1,j-1]):#esq der abajo
                pixeles[i+1,j-1]=(255,255,255)    
        except:
            pass
        try:
            if(pixeles[i-1,j-1]):#esq izq abajo
                pixeles[i-1,j-1]=(255,255,255)
        except:
            pass

        x+=1         
        
    return foto


def main():
    img= str(raw_input('Nombre de imagen: '))                                                                       
    foto=Image.open(img)#Abrir la imagen   
    ancho,alto=foto.size
    escalada=escala(foto,ancho,alto)
    escalada.save('escalada.png')
    filtromedio=filtro_medio(escalada,ancho,alto)
    filtromedio.save('filtromedio.jpg')
    diferenciada=diferencia(escalada,filtromedio,ancho,alto)
    diferenciada.save('diferencia.jpg')
    bordes=convolucion(diferenciada,ancho,alto)
    bordes.save('convolucion.jpg')
    #binaria=binarizacion(bordes,ancho,alto)
    #binaria.save('Binarizacion.jpg')
    umbrales=umbral(diferenciada,ancho,alto) 
    umbrales.save('umbral.jpg')
    binaria=binarizacion(umbrales,ancho,alto)
    binaria.save('Binarizacion.jpg')
    datos,datos2=posibles(binaria,ancho,alto)
    dila=dilatacion(binaria,ancho,alto,datos)
    dila.save('dilatacion.jpg')
    er=erocion(dila,ancho,alto,datos2)
    er.save('erosion.jpg')
    #bina=bina_invertida(escalada,ancho,alto)
    #bina.save('prueba.jpg')
main()
