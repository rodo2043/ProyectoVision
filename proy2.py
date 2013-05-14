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
    x=100
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

def bfs(foto,actual,color,ancho,alto):
    pixeles=foto.load()
    primeros=actual
    con2=0
    con=0
    cola=[]#Se crea la cola
    centro_i=[]
    centro_j=[]
    cola.append(actual)#Se agrega el valor actual a la cola
    partida=pixeles[actual]#punto de partida
    while len(cola)>0:#Mientras existan valores en la cola hacer...
        (x,y)=cola.pop(0)#Removemos el valor de la cola
        actual=pixeles[x,y]#actual toma el valor de la cola
        if actual==partida or actual ==color:#Si el pixel actual es igual al punto de partida o color 
            
            try:
                if (pixeles[x-1,y]):#Revisar vecino izq
                    if (pixeles[x-1,y]==partida):#Si rgb de vecino izq es igual a punto de partida
                        pixeles[x-1,y]=color#Pintar pixel de color
                        cola.append((x-1,y))#Y agregar a cola
                        con+=1
                        centro_i.append((x-1))#Agregar a lista para obtener los centros
                        centro_j.append((y))
            except:
                pass

            try:
                if (pixeles[x+1,y]):#Revisar vecino der                                                
                    if (pixeles[x+1,y]==partida):#Lo mismo vecino der
                        pixeles[x+1,y]=color
                        cola.append((x+1,y))
                        con+=1
                        centro_i.append((x+1))
                        centro_j.append((y))
            except:
                pass
            try:
                if (pixeles[x,y-1]):#Revisar vecino abajo                                              
                    if (pixeles[x,y-1]==partida):#Lo mismo vecino abajo
                        pixeles[x,y-1]=color
                        cola.append((x,y-1))
                        con+=1
                        centro_i.append((x))
                        centro_j.append((y-1))
                                    
            except:
                pass

            try:
                if (pixeles[x,y+1]):#Revisar vecino arriba                                              
                    if (pixeles[x,y+1]==partida):#Lo mismo vecino arriba
                        pixeles[x,y+1]=color
                        cola.append((x,y+1))
                        con+=1
                        con2+=1
                        centro_i.append((x))
                        centro_j.append((y+1))
            except:
                pass
            
    
    return foto,con,color,centro_i,centro_j,primeros

def formas(foto,ancho,alto):
    centro=[]
    centro2=[]
    contador=[]
    colores=[]
    figuras=[]
    pixeles=foto.load()#Cargar imagen
    for i in range(ancho):#Recorrer imagen
        for j in range (alto):
            if pixeles[i,j]==(0,0,0):#Si el pixel actual es negro
                col1=random.randint(0,255)
                col2=random.randint(0,255)#Se genera un color random
                col3=random.randint(0,255)
                r,g,b=(col1,col2,col3)
                foto,cont,color,centro1,centro2,primeros=bfs(foto,(i,j),(r,g,b),ancho,alto)#Se llama al bfs
                contador.append(cont)#Se agrega a la cadena contador el numero de pixeles sumados en el recorrido anterior
                colores.append(color)#Se agrega el color que se uso en el recorrido pasado
                try:
                    centros=((sum(centro1)/float(len(centro1)),sum(centro2)/float(len(centro2))))#Formula para obtener los centros
         
                except:
                    pass                
    maximo=contador.index(max(contador))#Se obtiene el valor mas alto de la cadena contador
    gris=colores[maximo]#Se obtiene el color usado en el valor mas alto del contador
    for i in range(ancho):#Recorrer imagen para repintar el area mas grande por gris
        for j in range(alto):
            if pixeles[i,j]==gris:
                       pixeles[i,j]=(81,81,81)
    draw=ImageDraw.Draw(foto)#Pintamos un circulo en cada uno de los centros que se almacenaron en la lista centro
    for i,recor in enumerate(centro):
        draw.ellipse((recor[0]-2,recor[1]-2,recor[0]+2,recor[1]+2),fill=(0,0,0))
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
    binaria=binarizacion(bordes,ancho,alto)
    binaria.save('Binarizacion.jpg') 
    forma=formas(bordes,ancho,alto)
    forma.save('formas.jpg')
main()
