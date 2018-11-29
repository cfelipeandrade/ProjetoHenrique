import heapq
import os
import pickle
import timeit


def criarFrequencia(codigoArquivo):
    '''
    :param Arquivo em hexadecial
    :return Lista com a frequencia de 4 bits
    '''
    frequencia = {}
    inicio = 0
    fim = 4
    frase = codigoArquivo[inicio:fim]

    for i in range(int(len(codigoArquivo)/4)):
        if frase in frequencia:
            frequencia[frase] += 1
        else:
            frequencia[frase] = 1
        inicio += 4
        fim += 4
        frase = codigoArquivo[inicio:fim]
    lista = []
    for i in frequencia:
        dado = (frequencia[i], i)
        lista.append(dado)
    return lista

def criarArvore(frequencias):
        '''
        :param Lista de frequencia de bits:
        :return Arvore de Huffman criada a partir das frequencias , em uma lista:
        '''
        arvore = []
        for i in frequencias:
            heapq.heappush(arvore, [i])
        while (len(arvore) > 1):
            filho_esquerda = heapq.heappop(arvore)
            filho_direita = heapq.heappop(arvore)
            frequenciaEsquerda, letraEsquerda = filho_esquerda[0]
            frequenciaDireita, letraDireita = filho_direita[0]
            frequencia = frequenciaEsquerda + frequenciaDireita
            letras = ''.join(sorted(letraEsquerda + letraDireita))
            no = [(frequencia, letras), filho_esquerda, filho_direita]
            heapq.heappush(arvore, no)

        return arvore.pop()

def criarCodMapa(arvore):
        '''
        :param Arvore de Huffman:
        :return Codigo em binario representando cada elemento da arvore de Huffman:
        '''
        codeMap = {}
        percorrerArvore(arvore, codeMap, '')
        return codeMap

def percorrerArvore(arvore, codeMap, codigo):
        if (len(arvore) == 1):
            frequencia, letras = arvore[0]
            codeMap[letras] = codigo
        else:
            no, filho_esquerda, filho_direita = arvore
            percorrerArvore(filho_esquerda, codeMap, codigo + '0')
            percorrerArvore(filho_direita, codeMap, codigo + '1')

def codificar(mapCode, mensagem):
        '''
        :param Dicionario com cada elemento da arvore com seu respectivo codigo em binario:
        :param ccodigo do aruivo em hexadecimal:
        :return uma string com codigo do arquivo em hex, reescrito em binario a partir do dicinario:
        '''
        codeMap = mapCode
        string = ''
        inicio = 0
        fim = 4
        frase = mensagem[inicio:fim]
        for i in range(int(len(mensagem)/4)):
            if frase in mensagem:
                string += codeMap[frase]
            inicio += 4
            fim += 4
            frase = mensagem[inicio:fim]
        return string

def padTextoCodificar(textoCodificado):
        extra_padding = 8 - len(textoCodificado) % 8
        for i in range(extra_padding):
            textoCodificado += "0"
        padded_info = "{0:08b}".format(extra_padding)
        textoCodificado = padded_info + textoCodificado
        return textoCodificado

def obterArrayByte(padded_text):
        '''
        :param Arquivo em binario:
        :return Arquivo em bits:
        '''
        b = bytearray()
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

def removerPadding(padded_encoded_text):

    '''
    :param remove o padding (8 carateres na frente e no final do arquivo codificado:
    :return Arquivo codificado em binario:
    '''

    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]
    return encoded_text


def decodificar(mensagemCodificada, arvoreFrequencias):
    '''

    :param Codigo do arquivo codificado em binario:
    :param Arvore com as frequencias dos bits do arquivo:
    :return string do codigo do arquivo decodificado:
    '''
    codeTree = arvoreCompleta = arvoreFrequencias
    letrasDecodidicada = []

    for digito in mensagemCodificada:
        if (digito == '0'):
            codeTree = codeTree[1]
        else:
            codeTree = codeTree[2]
        if len(codeTree) == 1:
            frequencia, letras = codeTree[0]
            letrasDecodidicada.append(letras)
            codeTree = arvoreCompleta
    return ''.join(letrasDecodidicada)




exec = True
while True:

    #DIREITORIO DE ONDE LOCALIZA-SE OS ARQUIVOS PARA COMPACTAÇÃO, E ONDE SERA SALVO OS ARQUIVOS COMPACTADOS OU DESCOMPACTADOS
    diretorio = "C:\projeto/"
    if exec == False:
        break

    print('ESCOLHA UMA OPÇÃO: ')
    print('1 - COMPACTAR UM ARQUIVO ')
    print('2 - DESCOMPACTAR UM ARQUIVO ')
    print('3 - ENCERRAR PROGRAMA')
    escolha = input()
    if escolha == '1':
            while True:
                print('DIGITE NOME DO ARQUIVO QUE DESEJA COMPACTAR (EX: paisagem.bmp / livro.txt):')
                nomeArquivo = input()
                arquivo = diretorio + nomeArquivo
                if os.path.isfile(arquivo):
                    break
                else:
                    print('ERRO!!!, VERIFIQUE SE O ARQUIVO É EXISTENTE NO DIRETORIO E SE A DIGITAÇÃO ESTA CORRETA!')

            filename, file_extension = os.path.splitext(arquivo)
            EX = file_extension
            ArquivoSaida = filename + ".pequeninitoPT1"
            ArquivoSaida2 = filename + ".pequeninitoPT2"
            inicio = timeit.default_timer()
            # A linha a seguir podera ser impressa com  probelma dependendo do diretorio do arquivo, observar index de filename
            print('COMPACTANDO O ARQUIVO ({})...'.format(filename[11:]))
            with open(arquivo, 'rb') as file, open(ArquivoSaida, 'wb') as output1, open(ArquivoSaida2, 'wb') as fp:
                codigoArquivo = file.read().hex()
                frequencia = criarFrequencia(codigoArquivo)
                arvoreFrequencias = criarArvore(frequencia)
                pickle.dump(arvoreFrequencias, fp,protocol=4)          
                codigoMapa = criarCodMapa(arvoreFrequencias)
                codigoArquivoCodificado = codificar(codigoMapa, codigoArquivo)
                padded_codigoArquivo = padTextoCodificar(codigoArquivoCodificado)
                b = obterArrayByte(padded_codigoArquivo)
                output1.write(bytes(b))              

                print("\nARQUIVO COMPACTADO COM SUCESSO!")
                fim = timeit.default_timer()
            print('Tempo de execução da compactação: {:.2f} segundos'.format(fim - inicio))
            print('DIGITE QUALQUER TECLA PARA UTILIZAR PROGRAMA NOVAMENTE, OU DIGITE "SAIR" PARA ENCERRAR!!!')
            esc = input()
            if esc == 'SAIR' or esc == 'sair':
                break


    elif(escolha == '2'):

        while True:
            print('DIGITE NOME DO ARQUIVO QUE DESEJA DESCOMPACTAR: ')
            nomeArquivo = input()
            arqCompact1 = diretorio + nomeArquivo + '.pequeninitoPT1'
            arqCompact2 = diretorio + nomeArquivo + '.pequeninitoPT2'
            if os.path.isfile(arqCompact1) and os.path.isfile(arqCompact2):
                break
            else:
                print('ERRO!!!, VERIFIQUE SE OS ARQUIVOS COMPACTADOS É EXISTENTE NO DIRETORIO E SE A DIGITAÇÃO ESTA CORRETA!')

        print('DIGITE A EXTENSAO ORIGINAL DO ARQUIVO: ')
        ext = input()
        filename,file_extension = os.path.splitext(arqCompact1)
        output_path = filename + "_descompactado." + ext
        inicio = timeit.default_timer()

        #A linha a seguir podera ser impressa com  probelma dependendo do diretorio do arquivo, observar index de filename
        print('DESCOMPACTANDO O ARQUIVO ({})....'.format(filename[11:]))
        with open(arqCompact1, 'rb') as file, open(output_path, 'wb') as output, open(arqCompact2, 'rb') as fp:
            bit_string = ""
            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            codigoArquivoCodificado = removerPadding(bit_string)
            frequencias = pickle.load(fp)
            codigoArquivoDescompactado = decodificar(codigoArquivoCodificado, frequencias)

            #recebe o codigo do arquivo decodificado e hexadecinal e converte novamente para dentro do arquivo e bits
            b = bytearray.fromhex(codigoArquivoDescompactado)
            output.write(b)  

            print("\nARQUIVO DESCOMPACTADO COM SUCESSO!!!")
            fim = timeit.default_timer()
            print('Tempo de execução da descompactação : {:.2f} segundos'.format(fim - inicio))
            print('DIGITE QUALQUER TECLA PARA UTILIZAR PROGRAMA NOVAMENTE, OU DIGITE "SAIR" PARA ENCERRAR!!!')
            esc = input()
            if esc == 'SAIR' or esc == 'sair':
                break

    elif(escolha == '3'):
        exec = False
    else:
        print('ESCOLHA UMA OPÇÃO VALIDA!')