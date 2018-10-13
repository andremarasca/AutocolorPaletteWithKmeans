import matplotlib.image as mpimg
from os import listdir
from os.path import isfile, join
import os as osfnc
import numpy as np

#%% Descobrir o nome de todas as imagens da base

# Para isso é necessário descobrir o diretório atual
# Em seguida apontar a pasta da base de imagens
# Descobrir o nome de todos os arquivos da pasta
# Filtrar apenas aqueles que são imagens e adicionar
# Na lista de imagens

# Descobrir o diretório atual
mypath = osfnc.getcwd()
# apontar a pasta que as minhas imagens estão
dirEntrada = mypath + '\\Entrada'
dirSaida = mypath + '\\Saida'
# Criar uma lista de imagens
soimagens = []
# Iterar cada um dos arquivos dentro de mypath
for f in listdir(dirEntrada):
    #Calcular o diretório completo do arquivo
    aa = join(dirEntrada, f)
    # verificar se é um arquivo ou não
    if isfile(aa):
        # Se for arquivo verificar se é .png
        if f.endswith(".png"):
            # Se for .png então adiciona na lista de imagens
            soimagens.append(f)


#%%

from sklearn.cluster import KMeans

# número de cores de cada imagem
numero_cores = [3, 3, 4]



for u, nome_das_imagens in enumerate(soimagens):
    # Abrir a imagem
    imagem = mpimg.imread(join(dirEntrada, nome_das_imagens))
    # Descobrir dimensões da imagem
    forma = imagem.shape
    # A Entrada ta no intervalo [0,1]
    # Para trabalhar com histograma deve ser [0, 255]
    imagem = imagem * 255
    # Converter a imagem em uint8

    lista = []
    for i in range(forma[0]):
            for j in range(forma[1]):
                mini_lista = []
                for k in range(forma[2]):
                    mini_lista.append(imagem[i][j][k])
                lista.append(mini_lista)

    lista = np.array(lista)

    kmeans = KMeans(n_clusters=numero_cores[u], random_state=0).fit(lista)

    cores = kmeans.cluster_centers_.tolist()

    print(nome_das_imagens)
    # calcular o histograma consiste em contar o número
    # de pixels de cada cor [0, 255]...
    # Para isso deve iterar os pixels da imagem contando
    for i in range(forma[0]):
        for j in range(forma[1]):
            val_min = 1000000000
            cor_min = cores[0]
            for cor in cores:
                dist = 0
                for k in range(forma[2]):
                    dist += (cor[k] - imagem[i][j][k])**2
                if val_min > dist:
                    val_min = dist
                    cor_min = cor
            for k in range(forma[2]):
                imagem[i][j][k] = cor_min[k]

    imagem = imagem.astype(np.uint8)
    mpimg.imsave(join(dirSaida, nome_das_imagens), imagem)