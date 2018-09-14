from time import sleep
from sys import exit
import os

class Item(object):
    def __init__(self, nome, descr, pegav, chave, atualiz1, atualiz2):
        self.nome = nome
        self.descr = descr
        self.pegav = pegav
        self.chave = chave
        self.atualiz1 = atualiz1
        self.atualiz2 = atualiz2
 
    def descrever(self):  ## Descreve o item ##
        for linha in self.descr:
            print(linha)

    def atualizar(self):  ## Atualiza a descriçao ##
        if len(self.atualiz1) > 0:
            itenslis = []
            for item in self.itens:
                itenslis.append(item)
            for n in range(1,len(self.atualiz1)+1):
                if self.atualiz1[n] == itenslis:
                    self.descr = self.atualiz2[n]
                else:
                    pass

class Porta(Item):
    def __init__(self, nome, descr, pegav, chave, atualiz1, atualiz2, itens, id_porta, bools, caminho, some):
        super(Porta, self).__init__(nome, descr, pegav, chave, atualiz1, atualiz2)
        
        self.itens = itens
        self.id_porta = id_porta
        self.bools = bools
        self.caminho = caminho
        self.some = some

    def dar_caminho(self): ## Abre um caminho especificado para outra sala ##
        itenslis = []
        for item in self.itens:
            itenslis.append(item)
        for n in range(1,len(self.atualiz1)+1):
            if self.atualiz1[n] == itenslis:
                if self.bools[n] == True:
                    mundo[local].saidas.update(self.caminho)
                    self.narraçao_caminho()
                if self.some == True:
                        nome = (self.nome).lower()
                        del mundo[local].itens[nome]

    def narraçao_caminho(self):
        for chave in self.caminho:
            mundo[local].descrever()
            print("\n\n    ---------------- Você liberou o caminho para o %s ! ----------------\n" % chave)


class Recipiente(Porta):
    def __init__(self, nome, descr, pegav, chave, atualiz1, atualiz2, itens, id_porta, bools, caminho, some, recip):
        super(Recipiente, self).__init__(nome, descr, pegav, chave, atualiz1, atualiz2, itens, id_porta, bools, caminho, some)

        self.recip = recip  ## Identifica o item como recipiente ##
    ## (Obs: pseudo recipiente, somente aponta, em sua descrição, a presença de um item na sala)##

                
class Chave(Item):
    def __init__(self, nome, descr, pegav, chave, atualiz1, atualiz2, id_porta, nome_porta, abertura):
        super(Chave, self).__init__(nome, descr, pegav, chave, atualiz1, atualiz2)
        
        self.id_porta = id_porta
        self.nome_porta = nome_porta
        self.abertura = abertura

    def narraçao(self):  ## Descreve o uso do item ##
        for linha in self.abertura:
            print(linha)
            
    def usar(self):  ## Remove item do inventário para abrir porta correspondente ##
        if self.nome_porta in mundo[local].itens:
            if mundo[local].itens[self.nome_porta].id_porta == self.id_porta:
                nome = (self.nome).lower()
                mundo[local].itens[self.nome_porta].itens.update({nome:self})
                mundo[local].itens[self.nome_porta].atualizar()
                del inventario[nome]
                self.narraçao()
                mundo[local].itens[self.nome_porta].dar_caminho()
            else:
                print("\n    Isso não pode ser usado aqui")
        else:
            print("\n    Isso não pode ser usado aqui")
        
        
            
class Sala(object):
    def __init__(self, nome, descr, itens, atualiz1, atualiz2, saidas, sentido):
        self.nome = nome
        self.descr = descr
        self.itens = itens
        self.atualiz1 = atualiz1
        self.atualiz2 = atualiz2
        self.saidas = saidas
        self.sentido = sentido

    def descrever(self):  ## Descreve a sala ##
        print("\n\n")
        print("=" * 80)
        print(self.nome)
        for linha in self.descr:
            print(linha)
        print()
        print(self.sentido[0])
        print(self.sentido[1])
        print(self.sentido[2],end="   ")
        print("Caminhos livres:", end="  ")
        for caminho in self.saidas:
            print(caminho, end="   ")
        print()
        print(self.sentido[3])
        print(self.sentido[4])
        print(self.sentido[5])
        print("=" * 80)
        print()

    def entregar(self, item):  ## Adiciona item ao inventário, caso esteja na sala ## 
        if item in self.itens:
            inventario.update({item : self.itens[item]})
            for x in self.itens:
                try:
                    self.itens[x].recip
                except AttributeError:
                    break
                self.itens[x].itens.update({item : self.itens[item]})
                self.itens[x].atualizar()
            del self.itens[item]

    def atualizar(self): ## Atualiza a descriçao da Sala ##
        if len(self.atualiz1) > 0:
            itenslis = []
            for item in self.itens:
                itenslis.append(item)
            for n in range(1,len(self.atualiz1)+1):
                if self.atualiz1[n] == itenslis:
                    self.descr = self.atualiz2[n]
                else:
                    pass


################################################# ESTRUTURA DE DADOS #################################################


#------------------------------------------------ OBJETOS - USO GERAL -----------------------------------------------#
                    
bussola = Item(
    #------ NOME ------#
    "Bússola",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma bússola comum, referência para a localização,",
     "    estava no seu bolso por algum motivo."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

balde = Item(
    #------ NOME ------#
    "Balde",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um balde de madeira, nada de especial."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

barril = Item(
    #------ NOME ------#
    "Barril",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um barril de madeira, está vazio."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

destroços = Item(
    #------ NOME ------#
    "Destroços",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Destroços da estrutura da masmorra, não parece ser possível movê-los."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

porta_geral = Item(
    #------ NOME ------#
    "Porta",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma porta de madeira, está destrancada."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

pedra_geral = Item(
    #------ NOME ------#
    "Pedra",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É uma grande rocha, não está mais bloqueando o caminho."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

papeis = Item(
    #------ NOME ------#
    "Papéis",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    São papéis deteriorados pelo tempo, não há nada legível."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

mesa = Item(
    #------ NOME ------#
    "Mesa",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma mesa de madeira, nada de espcial."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

cadeiras = Item(
    #------ NOME ------#
    "Cadeiras",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um conjunto de cadeiras de madeira."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

#----------------------------------------- OBJETOS DA SALA 1 (CELA - INÍCIO) ----------------------------------------#

chave1 = Chave(
    #------ NOME ------#
    "Chave",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma chave enferrujada, nada de especial."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    1,"porta",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você destranca a porta da cela, revelando o sombrio corredor a frente."]
    
)

porta1 = Porta(
    #------ NOME ------#
    "Porta",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma porta de ferro gradeada, trancada."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["chave"]}, #>>>>> atualiz1 <<<<<#
    {1:["\n    Uma porta de ferro gradeada, está aberta"]},
    #------- INVENTÁRIO DO ITEM -------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    1,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {1:True}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {"NORTE":2},
    #----- "PORTA" SOME QUANDO ABERTA? -----#
    False
)

#--------------------------------------- OBJETOS DA SALA 2 (CORREDOR PRINCIPAL) -------------------------------------#

pedra1 = Porta(
    #------ NOME ------#
    "Pedra",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É uma grande rocha, bloquando o seu caminho.",
     "    Parece pesada demais para ser empurrada com as mãos."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["bastão"]}, #>>>>> atualiz1 <<<<<#
    {1:[" "]}, #>>>>> atualiz2 <<<<<#
    #------------ INVENTÁRIO DO ITEM ------------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    2,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {1:True}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {"OESTE":7},
    #----- "PORTA" "SOME" QUANDO ABERTA? -----#
    True
)

porta9 = Porta(
    #------ NOME ------#
    "Porta",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    uma cúbica e outra, triangular.",],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#

    #------------------------ MELHORAR!!!!!!!!!!!!!!! ------------------------#
    #------------------------ MELHORAR!!!!!!!!!!!!!!! ------------------------#
    #------------------------ MELHORAR!!!!!!!!!!!!!!! ------------------------#
    #------------------------ MELHORAR!!!!!!!!!!!!!!! ------------------------#
    #------------------------ MELHORAR!!!!!!!!!!!!!!! ------------------------#
    #------------------------ MELHORAR!!!!!!!!!!!!!!! ------------------------#
    {1:["maçã"], 2:["cubo"], 3:["maçã","cubo"], 4:["cubo","maçã"],5:["pirâmide"],
     6:["maçã","pirâmide"],7:["pirâmide","maçã"],8:["pirâmide","cubo"],9:["cubo","pirâmide"],
     10:["maçã","cubo","pirâmide"],11:["maçã","pirâmide","cubo"],12:["cubo","maçã","pirâmide"],
     13:["cubo","pirâmide","maçã"],14:["pirâmide","maçã","cubo"],15:["pirâmide","cubo","maçã"]},
    
    {1:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    preenchida pela maçã de pedra, uma cúbica e outra, triangular."],
     2:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    uma cúbica, preenchida pelo cubo dourado, e outra, triangular."],
     3:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    preenchida pela maçã de pedra, uma cúbica, preenchida pelo cubo dourado,",
     "    e outra, triangular."],
     4:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    preenchida pela maçã de pedra, uma cúbica, preenchida pelo cubo dourado,",
     "    e outra, triangular."],
     5:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    uma cúbica e outra, triangular, preenchida pela pirâmide em miniatura.",],
     6:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    preenchida pela maçã de pedra, uma cúbica e outra, triangular, preenchida",
     "    pela pirâmide em miniatura."],
     7:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    preenchida pela maçã de pedra, uma cúbica e outra, triangular, preenchida",
     "    pela pirâmide em miniatura."],
     8:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    uma cúbica, preenchida pelo cubo dourado, e outra, triangular, preenchida",
     "    pela pirâmide em miniatura."],
     9:["\n    Uma grande porta de ferro sem nenhuma tranca aparente, ao invés disso,",
     "    você nota a presença de 3 concavidades em sua superfície: uma arredondada,",
     "    uma cúbica, preenchida pelo cubo dourado, e outra, triangular, preenchida",
     "    pela pirâmide em miniatura."],
     10:["\n Uma grande porta de ferro com os três itens encaixados, está aberta."],
     11:["\n Uma grande porta de ferro com os três itens encaixados, está aberta."],
     12:["\n Uma grande porta de ferro com os três itens encaixados, está aberta."],
     13:["\n Uma grande porta de ferro com os três itens encaixados, está aberta."],
     14:["\n Uma grande porta de ferro com os três itens encaixados, está aberta."],
     15:["\n Uma grande porta de ferro com os três itens encaixados, está aberta."]},
    #------- INVENTÁRIO DO ITEM -------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    9,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False,
     10:True, 11:True, 12:True, 13:True, 14:True, 15:True}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {"NORTE":9},
    #----- "PORTA" SOME QUANDO ABERTA? -----#
    False
)

#--------------------------------------- OBJETOS DA SALA 3 (CORREDOR PRINCIPAL) -------------------------------------#

#--------------------------------------- OBJETOS DA SALA 4 (CORREDOR PRINCIPAL) -------------------------------------#

bastao = Chave(
    #------ NOME ------#
    "Bastão",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um rígido bastão de madeira, parece ter sido uma lança no pasado",
     "    (ou, quem sabe, apenas um cabo de vassoura)."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    2,"pedra",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você usa o bastão como alavanca, empurrando a pedra e, assim, liberando",
     "    a passagem. O bastão quebra no processo."]
    
)

#--------------------------------------- OBJETOS DA SALA 5 (CORREDOR PRINCIPAL) -------------------------------------#

maçã = Chave(
    #------ NOME ------#
    "Maçã",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma maçã de pedra"],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    9,"porta",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você encaixa a maçã na fenda arredondada da porta, ouvem-se os cliques de",
     "    um mecanismo interno."]
    
)

estatua = Recipiente(
    #------ NOME ------#
    "Estátua",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É uma estátua de pedra de um guerreiro erguendo uma maçã ao alto."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["maçã"]}, #>>>>> atualiz1 <<<<<#
    {1:["\n    Uma estátua de pedra de um guerreiro, você levou a maçã que ela segurava."]}, #>>>>> atualiz2 <<<<<#
    #------------ INVENTÁRIO DO ITEM ------------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    0,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {},
    #----- "PORTA" "SOME" QUANDO ABERTA? -----#
    False,
    #----- É (OU NÃO) RECIPIENTE -----#
    True
    
)

porta2 = Porta(
    #------ NOME ------#
    "Porta",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma porta de madeira, trancada."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["chave"]}, #>>>>> atualiz1 <<<<<#
    {1:["\n    Uma porta de madeira, destrancada."]},
    #------- INVENTÁRIO DO ITEM -------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    5,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {1:True}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {"LESTE":6},
    #----- "PORTA" SOME QUANDO ABERTA? -----#
    False
)

#--------------------------------------- OBJETOS DA SALA 6 (CORREDOR PRINCIPAL) -------------------------------------#

cubo = Chave(
    #------ NOME ------#
    "Cubo",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um cubo dourado, coberto de inscrições incompreensíveis."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    9,"porta",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você encaixa o cubo na fenda cúbica da porta, ouvem-se os cliques de",
     "    um mecanismo interno."]
    
)

chave3 = Chave(
    #------ NOME ------#
    "Chave",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É uma simples chave de metal."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    7,"porta",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você abre a porta."]
    
)

tabua = Item(
    #------ NOME ------#
    "Tábua",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Qktk fkbjt y fkqhyezv, uzcz rzt szjvy y rzwojbvz:"
    "- zrqkuk",
    "- stkrgy",
    "- CÁ ZEFYTK FYUZ ZBYTEZ!"],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

#--------------------------------------- OBJETOS DA SALA 7 (CORREDOR PRINCIPAL) -------------------------------------#

bau = Recipiente(
    #------ NOME ------#
    "Baú",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É um baú de madeira, no seu interior você vê muitos papéis, um",
     "    frasco de vidro e uma chave."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["frasco"],2:["chave"],3:["frasco","chave"],4:["chave","frasco"]}, #>>>>> atualiz1 <<<<<#
    {1:["\n    É um baú de madeira, no seu interior você vê muitos papéis e uma chave."], #>>>>> atualiz2 <<<<<#
     2:["\n    É um baú de madeira, no seu interior você vê muitos papéis e um frasco de vidro."],
     3:["\n    É um baú de madeira, no seu interior você vê muitos papéis."],
     4:["\n    É um baú de madeira, no seu interior você vê muitos papéis."]},
    #------------ INVENTÁRIO DO ITEM ------------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    0,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {},
    #----- "PORTA" "SOME" QUANDO ABERTA? -----#
    False,
    #----- É (OU NÃO) RECIPIENTE -----#
    True
)

frasco = Chave(
    #------ NOME ------#
    "Frasco",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É um frasco de vidro preenchido de um líquido azul e tampado com uma rolha.",
     "    Há um rótulo com a imagem de um crânio e ossos cruzados."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    666,"monstro",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    ."]
    
)

chave2 = Chave(
    #------ NOME ------#
    "Chave",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma pequena chave."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    5,"porta",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você destranca a porta."]
    
)

porta3 = Porta(
    #------ NOME ------#
    "Porta",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma porta de metal, está trancada."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["chave"]}, #>>>>> atualiz1 <<<<<#
    {1:["\n    Uma porta de metal, está destrancada."]},
    #------- INVENTÁRIO DO ITEM -------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    7,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {1:True}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {"SUL":8},
    #----- "PORTA" SOME QUANDO ABERTA? -----#
    False
)

#--------------------------------------- OBJETOS DA SALA 8 (CORREDOR PRINCIPAL) -------------------------------------#

pintura = Recipiente(
    #------ NOME ------#
    "Pintura",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É uma pintura a óleo da pirâmide de Gizé em meio ao deserto",
     "    (\"Cairo - 1824, óleo sobre tela\")"],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DO ITEM ------------#
    {1:["pirâmide"]}, #>>>>> atualiz1 <<<<<#
    {1:["\n    É uma pintura a óleo de um deserto no Egito",
     "    (\"                            \")"]},
    #------------ INVENTÁRIO DO ITEM ------------#
    {},
    #------- IDENTIFICADOR DA PORTA -------#
    0,
    #------- ABERTURA DA PORTA POR INVENTÁRIO DO ITEM -------#
    {}, #>>>>> bools <<<<<#
    #----- CAMINHO QUE ABRE NA SALA -----#
    {},
    #----- "PORTA" "SOME" QUANDO ABERTA? -----#
    False,
    #----- É (OU NÃO) RECIPIENTE -----#
    True
)

piramide = Chave(
    #------ NOME ------#
    "Pirâmide",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É a pirâmide de Gizé."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    9,"porta",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    Você encaixa a pirâmide na fenda triangular da porta, ouvem-se os cliques de",
     "    um mecanismo interno."]
    
)

espada = Chave(
    #------ NOME ------#
    "Espada",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    É uma espada de aço, está afiada."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    True,
    {},{},
    #------- IDENTIFICADOR E NOME DA PORTA QUE ABRE-------#
    666,"monstro",
    #--------------- TEXTO DE USO DA CHAVE --------------#
    ["\n    ."]
    
)

pergaminho = Item(
    #------ NOME ------#
    "Pergaminho",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    kfguzswhjnpaebyqltrvocimxd"],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    True,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

esqueleto = Item(
    #------ NOME ------#
    "Esqueleto",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um esqueleto trajando trapos de roupa, está sentado encarando",
     "    uma pintura na parede em sua frente."],
    #------ PODE (OU NÃO) SER OBTIDO ------#
    False,
    #------ É (OU NÃO) CHAVE ------#
    False,
    {},{}
)

#--------------------------------------- OBJETOS DA SALA 9 () -------------------------------------#




######################################################   SALAS   ######################################################

quarto1 = Sala(
    #------ NOME ------#
    "    -Cela-",
    #------ DESCRIÇÃO ORIGINAL ------#fffffffffffffffffffffffffffffffffffffffffffff
    ["\n    Você se encontra em um calabouço úmido com paredes de pedra e uma porta",
     "    de ferro gradeada. No chão, há uma chave enferrujada."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"chave":chave1, "porta":porta1},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {1:["porta"]},
    {1:["\n    Você se encontra em um calabouço úmido com paredes de pedra e uma porta",
     "    de ferro gradeada."]},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {},
    #"NORTE":2
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌ N ────┐"," │       │"," │       │"," └───────┘","         ","         "]
)

corredor2 = Sala(
    #------ NOME ------#
    "    -Corredor Principal-",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Um corredor estreito parte da sua cela e continua a direita.",
     "    O caminho a oeste está bloqueado por uma pedra, aparentemente,",
     "    fruto de um desmoronamento da estrutura precária.",
     "    Ao norte, chama a atenção uma grandiosa porta de ferro."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"pedra":pedra1, "porta":porta9},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {1:[]},
    {1:["\n    Um corredor estreito parte da sua cela e continua a direita,",
     "    nota-se ainda uma entrada a esquerda, não mais obstruída."
     "    Ao norte, chama a atenção uma grandiosa porta de ferro."]},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"SUL":1, "LESTE":3},
    #,"OESTE":7
    #,"NORTE":9
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌ N ────┐"," O       L"," │   ┌───┘"," │   │    "," │   │    "," └ S ┘    "]
)

corredor_LESTE3 = Sala(
    #------ NOME ------#
    "    -Corredor - Continuação-",
    ["\n    O corredor segue a direita e termina com uma porta de madeira, a direita",
     "    da mesma, você nota uma passagem aberta para outra cela."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"porta":porta_geral},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {},{},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"SUL":4, "LESTE":5, "OESTE":2},
    #------------------------ DESENHO DO MAPA ------------------------#
    [" "," ┌──────────┐"," O          L"," └─────── S ┘"," "," "]
)

quarto4 = Sala(
    #------ NOME ------#
    "    -Cela-",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Uma cela como a qual onde você despertou, está, contudo, sem porta e",
     "    cheia de destroços, aparentemente resultado de um desmoronamento.",
     "    Entre esses destroços você distingue objetos como um bastão de madeira,",
     "    um balde e um barril."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"bastão":bastao,"balde":balde,"barril":barril,"destroços":destroços},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {1:["balde","barril","destroços"]},
    {1:["    Uma cela como a qual onde você despertou, está, contudo, sem porta e",
     "    cheia de destroços, aparentemente resultado de um desmoronamento.",
     "    Entre esses destroços você distingue objetos como um balde e um barril."]},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"NORTE":3},
    #------------------------ DESENHO DO MAPA ------------------------#
    ["         ","   ┌───── N ┐","   │        │","   │        │","   └────────┘","         "]
)

quarto5 = Sala(
    #------ NOME ------#
    "    -Câmara Oeste-",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Essa sala está repleta de restos de vasos e estátuas quebradas, salvo por",
     "    uma, em meio a uns poucos destroços. Há ainda, uma porta a Leste."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"estátua":estatua,"maçã":maçã,"destroços":destroços, "porta":porta2},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {},{},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"OESTE":3},
    #,"LESTE":6
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌────────┐"," O        │"," │        │"," │        L"," └────────┘","         "]
)

quarto6 = Sala(
    #------ NOME ------#
    "    -Altar-",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    Nessa câmara há um improvisado, porém sultuoso altar.",
     "    Sob ele, você observa um cubo dourado, além de uma chave de metal.",
     "    Há ainda, uma tábua de pedra com inscrições em baixo relevo."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"cubo":cubo, "chave":chave3, "tábua":tabua},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {1:["chave","tábua"],2:["cubo","tábua"],3:["tábua"]},
    {1:["\n    Nessa câmara há um improvisado, porém sultuoso altar.",
     "    Sob ele, você encontra somente uma chave de metal.",
     "    Há ainda, uma tábua de pedra com inscrições em baixo relevo."],
    2:["\n    Nessa câmara há um improvisado, porém sultuoso altar.",
     "    Sob ele, você vê um cubo dourado, coberto de incrições.",
     "    Há ainda, uma tábua de pedra com inscrições em baixo relevo."],
    3:["\n    Nessa câmara há um improvisado, porém sultuoso altar.",
     "    Há uma tábua de pedra com inscrições em baixo relevo."]},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"OESTE":5},
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌────────┐"," │        │"," │        │"," O        │"," └────────┘","         "]
)

quarto7 = Sala(
    #------ NOME ------#
    "    -Câmara Oeste-",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    O teto dessa sala está desmoronado. Em meio a muitos destroços, você vê",
     "    a pedra que antes bloqueava a entrada, além de um baú, que parece intacto.",
     "    Ao Sul, nota-se uma porta de ferro comum; os destroços estão obstruindo uma",
     "    saída a Oeste."],
    #------------ INVENTÁRIO DA SALA ------------#
    {"baú":bau, "pedra":pedra_geral, "destroços":destroços, "papéis":papeis, "chave":chave2, "frasco":frasco, "porta":porta3},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {},{},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"LESTE":2},
    #,"SUL":8
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌────────┐"," │        L"," │        │"," │        │"," │        │"," └── S ───┘"]
)

quarto8 = Sala(
    #------ NOME ------#
    "    -Câmara Sul-",
    #------ DESCRIÇÃO ORIGINAL ------#
    ["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto. De suas mãos pendem",
     "    uma espada e um pergaminho"],
    #------------ INVENTÁRIO DA SALA ------------#
    {"pintura":pintura,"esqueleto":esqueleto,"mesa":mesa,"cadeiras":cadeiras,"pirâmide":piramide,"espada":espada,"pergaminho":pergaminho},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {1:["pintura","esqueleto","mesa","cadeiras","pirâmide","pergaminho"],
     2:["pintura","esqueleto","mesa","cadeiras","pirâmide","espada"],
     3:["pintura","esqueleto","mesa","cadeiras","pirâmide"],
     4:["pintura","esqueleto","mesa","cadeiras","pergaminho"],
     5:["pintura","esqueleto","mesa","cadeiras","espada"],
     6:["pintura","esqueleto","mesa","cadeiras"]},
    
    {1:["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto. De uma de suas mãos,",
     "    pende um pergaminho"],
     2:["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto. De uma de suas mãos,",
     "    pende uma espada"],
     3:["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto."],
     4:["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto. De uma de suas mãos,",
     "    pende um pergaminho"],
     5:["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto. De uma de suas mãos,",
     "    pende uma espada"],
     6:["\n    A sala está livre de destroços, há uma mesa com cadeiras,",
     "    em uma das quais, senta-se um esqueleto."]},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"NORTE":7},
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌── N ───┐"," │        │"," │        │"," │        │"," └────────┘","         "]
)

quarto9 = Sala(
    #------ NOME ------#
    "    ",
    #------ DESCRIÇÃO ORIGINAL ------#
    [" "],
    #------------ INVENTÁRIO DA SALA ------------#
    {},
    #------------ ATUALIZAÇÃO DA DESCRIÇÃO POR INVENTÁRIO DA SALA ------------#
    {},{},
    #------ CAMINHOS ORIGINALMENTE ABERTOS ------#
    {"NORTE":10, "SUL":2},
    #------------------------ DESENHO DO MAPA ------------------------#
    [" ┌─────────┐"," │         │"," │         │"," │         │"," │         │"," └─── S ───┘"]
)


local = 1 ###### Identificador da sala atual ######
anterior = 1 ###### Identificador da sala anterior ######

#------------------ RELAÇÃO PARA CONEXÃO ENTRE AS SALAS ------------------#
mundo = {1:quarto1, 2:corredor2, 3:corredor_LESTE3, 4:quarto4, 5:quarto5,
         6:quarto6, 7:quarto7, 8:quarto8, 9:quarto9 }


inventario = {"bússola":bussola} ###### INVENTÁRIO - ITEMS SÃO GUARDADOS AQUI ######

def ver_inventario():
    print("\n Inventário:", end=" ")
    for item in inventario:
        print(inventario[item].nome, end="   ")
    print()


def cls():
    os.system('cls' if os.name=='nt' else 'clear')




def inicio():
    print("=" * 80)
    print("\n      No jogo a seguir você irá explorar um labirinto de salas interligadas")
    print("   nas quais você poderá interagir com os objetos do cenário ao observá-los,")
    print("   coletá-los e utilizá-los com o fim de fugir do labirinto.")
    print("\n       Para realizar essa interação, você deverá digitar comandos tais como:")
    print("   ver x, Pegar x, Utilizar X, ir NORTE, andar para sul, ver inventário, I,")
    print("   N, s, Leste, OESTE, ajuda, ver, inveNtário, e assim em diante, note que a")
    print("   distinção entre letras maiúsculas e minúsculas não é necessária, enquanto")
    print("   acentuação o é.")
    print("\n   Para uma experiência ideal, ajuste a janela para enquadrar a barra acima.")
    nada = input("\n                      - Pressione ENTER para começar -")
    sleep(1)
    print("\n                                    .")
    sleep(1)
    print("\n                                    .")
    sleep(1)
    print("\n                                    .")
    sleep(1)
    print("\n                                    .")
    sleep(1)
    print("\n                                    .")
    sleep(1)
    cls()
    print("=" * 80)
    print("     _______  _______  _______  _______  _______  _______  _______  _______ ")
    print("    (       )(  ___  )(  ____ \(       )(  ___  )(  ____ )(  ____ )(  ___  )")
    print("    | () () || (   ) || (    \/| () () || (   ) || (    )|| (    )|| (   ) |")
    print("    | || || || (___) || (_____ | || || || |   | || (____)|| (____)|| (___) |")
    print("    | |(_)| ||  ___  |(_____  )| |(_)| || |   | ||     __)|     __)|  ___  |")
    print("    | |   | || (   ) |      ) || |   | || |   | || (\ (   | (\ (   | (   ) |")
    print("    | )   ( || )   ( |/\____) || )   ( || (___) || ) \ \__| ) \ \__| )   ( |")
    print("    |/     \||/     \|\_______)|/     \|(_______)|/   \__/|/   \__/|/     \|")
    print()
    print("=" * 80)
    print("\n\n")
    print("\n   Como um sonho distante, o som de um desabamento, um terremoto, a escuridão.")
    nada = input("\n                             - Pressione ENTER -")
    print("\n Você acorda em uma cela subterrânea ao som de um objeto metálico jogado no chão")
    nada = input("\n                             - Pressione ENTER -")
    print("\n\n                               \"TENTE ESCAPAR\" ")
    sleep(2)

    
############################################# FIM DA ESTRUTURA DE DADOS #############################################


verl = ["ver", "olhar", "v", "ler", "abrir", "mostrar", "inspecionar"]
pegarl = ["pegar", "p", "levar", "adquirir"]
usarl = ["usar", "u", "utilizar","acender"]
moverl = ["ir", "i", "andar", "mover", "movimento"]
salal = ["sala", "cômodo", "espaço", "ambiente", "calabouço", "corredor", "lugar", "cela", "altar","masmorra"]
direçoes = ["norte", "sul", "leste", "oeste"]
abrev = {"n":"norte", "s":"sul", "l":"leste", "o":"oeste"}


    

inicio()

while True:
    if local == 9:
        print("\n    Você escuta ruídos monstruosos a frente")
        print("    Deseja proceguir ? (S/N)")
        sn = input("\n> ")
        sn = sn.lower()
        if sn == "sim" or sn == "s":
            break
        else:
            local = 2
            pass
    #------ Descrição da sala ao entrar ------#
    mundo[local].descrever()
    while True:
        comandos = []
        for x in input("\n> ").split():
            comandos.append(x)

        ######## COMANDOS DE UMA PALAVRA ########
        if len(comandos) == 1:
            palavra = comandos[0].lower()
            #------ Ver descrição da sala ------#
            if palavra in verl:
                mundo[local].descrever()
            #------ Mover-se para direção ------#
            elif palavra in abrev:
                palavra = abrev[palavra]
                if palavra.upper() in mundo[local].saidas:
                    anterior = local
                    local = mundo[local].saidas[palavra.upper()]
                    break
                else:
                    print("\n    Você não consegue ir nessa direção")
                
            elif palavra in direçoes:
                if palavra.upper() in mundo[local].saidas:
                    anterior = local
                    local = mundo[local].saidas[palavra.upper()]
                    break
                else:
                    print("\n    Você não consegue ir nessa direção")
            #------ Ver descrição de item da sala ------#
            elif palavra in mundo[local].itens:
                mundo[local].itens[palavra].descrever()
            #------ Ver descrição de item do inventário ------#
            elif palavra in inventario:
                inventario[palavra].descrever()
            #------ Ver inventário ------#
            elif palavra == "inventário" or palavra == "i" or palavra == "itens":
                    ver_inventario()
            #------ Ver descrição da sala (de novo) ------#
            elif palavra in salal:
                mundo[local].descrever()
            #------ Ver ajuda ------#        
            elif palavra == "ajuda" or palavra == "a" or palavra == "help":
                print("\n    Ajuda:")
                print("\n        Para realizar uma interação, você deverá digitar comandos tais como:")
                print("    ver x, Pegar x, Utilizar X, ir NORTE, andar para sul, ver inventário, I,")
                print("    N, s, Leste, OESTE, ajuda, ver, inveNtário, e assim em diante, note que a")
                print("    distinção entre letras maiúsculas e minúsculas não é necessária, enquanto")
                print("    acentuação o é.")
                print("\n        Procure inspecionar tudo que estiver na sala, ás vezes você só irá")
                print("    notar um objeto ao inspecionar outro.")
            else:
                print("\n    Comando Inválido")
            

        ######## COMANDOS DE DUAS OU MAIS PALAVRAS ########   
        elif len(comandos) > 1:
            verbo, substantivo = comandos[0].lower(), comandos[-1].lower()
            
            if verbo in verl:
                #------ Ver descrição da sala ------#
                if substantivo in salal:   
                    mundo[local].descrever()
                #------ Ver descrição de item da sala ------#
                elif substantivo in mundo[local].itens:
                    mundo[local].itens[substantivo].descrever()
                #------ Ver descrição de item do inventário ------#
                elif substantivo in inventario:
                    inventario[substantivo].descrever()
                #------ Ver inventário ------#
                elif substantivo == "inventário" or substantivo == "i" or substantivo == "itens":
                    ver_inventario()
                #------ Ver ajuda ------#
                elif substantivo == "ajuda":
                    print("\n    Ajuda:")
                    print("\n        Para realizar uma interação, você deverá digitar comandos tais como:")
                    print("    ver x, Pegar x, Utilizar X, ir NORTE, andar para sul, ver inventário, I,")
                    print("    N, s, Leste, OESTE, ajuda, ver, inveNtário, e assim em diante, note que a")
                    print("    distinção entre letras maiúsculas e minúsculas não é necessária, enquanto")
                    print("    acentuação o é.")
                    print("\n        Procure inspecionar tudo que estiver na sala, ás vezes você só irá")
                    print("    notar um objeto ao inspecionar outro.")
                else:
                    print("\n    Você não vê isso.")
                    
            elif verbo in pegarl:
                #------ Pegar item da sala ------# 
                if substantivo in mundo[local].itens and mundo[local].itens[substantivo].pegav == True:
                    mundo[local].entregar(substantivo)
                    print("\n    -- %s adicionado(a) ao inventário --" % inventario[substantivo].nome)
                    mundo[local].atualizar()
                elif substantivo in inventario:
                    print("\n    Você já possui esse item.")
                else:
                    print("\n    Você não pode pegar isso.")

            elif verbo in moverl:
                #------ Mover-se para direção ------#
                if substantivo.upper() in mundo[local].saidas:
                    anterior = local
                    local = mundo[local].saidas[substantivo.upper()]
                    break
                
                elif substantivo in abrev:
                    substantivo = abrev[substantivo]
                    if substantivo.upper() in mundo[local].saidas:
                        anterior = local
                        local = mundo[local].saidas[substantivo.upper()]
                        break
                    else:
                        print("\n    Você não consegue ir nessa direção.")
                    
                else:
                    print("\n    Você não consegue ir nessa direção.")

            elif verbo in usarl:
                if substantivo in inventario:
                    if inventario[substantivo].chave == True:
                        inventario[substantivo].usar()
                    else:
                        print("\n    Você não consegue usar isso")
                else:
                    print("\n    Você não possui isso.")
            
            else:
                print("\n    Você não consegue fazer isso. (tente: ver ajuda)")

        else:
            print("\n    Você não consegue fazer isso. (tente: ver ajuda)")


cls()
print("=" * 80)
print("\n   Você segue por um corredor estreito em meio a grunidos cada vez mais altos.  ")
nada = input("\n                             - Pressione ENTER -")
print("\n             O corredor termina subitamente em uma câmara gigantesca.")
nada = input("\n                             - Pressione ENTER -")
sleep(1)
print("\n                                      .")
sleep(1)
print("\n                                      .")
sleep(1)
print("\n                                      .")
sleep(1)
print("\n                                      .")
sleep(1)
print("\n                                      .")
sleep(1)
cls()
print("=" * 80)       
print("                                      <`--._<`--.____________________________") 
print("                                       ) ,..-) ,..------------------------,-'") 
print("                                     ,','  >','  \\                  ,       ")
print("                                   ,','  ,','     \\            ,            ")
print("                                 ,','  ,','        \\       ,                ")
print("                               ,' /  ,' /           \\  ,                    ")
print("                              /  /  /  /             \`<                     ")
print("                             /  /,-/  /,--------------\/                     ")
print("                            /__'--/  (/--.                                   ") 
print("            .-.     ____, '<.  / '   '   '----.                              ") 
print("           ( . `. ,'    \  '     .-------.  ` '--,                           ")
print("            \_) ,'  (_.  \      /         `-----<\                           ") 
print("            \'   ,'', `.  \   ,'   ,  '          `\                          ") 
print("           _/ _/',O)>   )  )_            ,'        >                         ")
print("       \  (o /o) \` )  /  /'\`   `------<___   ,   )                         ") 
print("       \`-)| (/`,)\`-'  /   `.          /   >-'    \                         ")
print("         `-VvvV ,/( `---'\     `       ,'   /`.      )                       ") 
print("             / ,/\    \   `.    `          ' ,'`.   '\                       ") 
print("          (^^(/`      \    `--<, ` --------' ,' `.   )                       ")
print("            ``` ________>  ,'   `-')  `      /     \  |                      ") 
print("       ,-------'        `  )   .--'     ,   /       \  |_                    ")
print("     ,'/ _,--,--,,,-,______>   )     \,    (_.-.     \   ),---.              ") 
print("    / ,\ )                   ,'     ,'          \ .--.\,  .__, \-.           ") 
print("   /_/ /\)                  /      /             / )-.    /--`--) \          ") 
print("  ( )\ ) `                 .      /             (-'   `--'      `--)         ") 
print("   \' \'                  ,      .                 )                         ")
print("                          ,     ,                ,'                          ") 
print("                           `.  .               ,'`.                          ") 
print("                          ,',` |              /-.  `.                        ") 
print("                         ( (   |              \  \   `._                     ") 
print("                          \ \  /             \    \     \.                   ") 
print("                           \ \  /          ,\`-.   \  ,'  )                  ") 
print("                            \ \  /`--,--,-')   /    \'   /                   ")
print("                             \ `---------,'   /-.    \\,'                    ") 
print("                              `--------,'    /-. \                           ") 
print("                                      /     /   ) )                          ")
print("                                     (      > ,/ (_                          ") 
print("                                    /`-,---'\ |, ,'                          ") 
print("                                    `-^-----' |,'                            ")   

print("\n               VOCÊ SE DEPARA COM O ENORME BAPHOMET!")
nada = input("\n               - Pressione ENTER -")
print("\n               ELE PREPARA-SE PARA LHE PISOTEAR!")
print("               O QUE VOCÊ IRÁ FAZER ?")

def morte():
    print("               VOCÊ MORREU")
    sleep(1)
    print("\n                    .")
    sleep(1)
    print("\n                    .")
    sleep(1)
    print("\n                    .")
    sleep(1)
    nada = input("\n               - Pressione ENTER para sair-")
    exit()
    
comandos = []
for x in input("\n> ").split():
    comandos.append(x)
if len(comandos) > 1:
    x, y = comandos[0].lower(), comandos[-1].lower()
    if x in usarl:
        if y == "espada":
            if "espada" in inventario:
                print("\n               VOCÊ CORTA A PATA DA CRIATURA COM UM SÓ GOLPE!")
            else:
                morte()
        else:
            morte()
    else:
        morte()
else:
    morte()


nada = input("\n               - Pressione ENTER -")
print("\n               ELE CAI NO CHÃO MAS TENTA TE ABOCANHAR LOGO EM SEGUIDA!")
print("\n               O QUE VOCÊ IRÁ FAZER ?")


comandos = []
for x in input("\n> ").split():
    comandos.append(x)
if len(comandos) > 1:
    x, y = comandos[0].lower(), comandos[-1].lower()
    if x in usarl:
        if y == "frasco":
            if "frasco" in inventario:
                print("\n               VOCÊ ARREMESSA O FRASCO, QUE EXPLODE NA BOCA DO MONSTRO!")
            else:
                morte()
        else:
            morte()
    else:
        morte()
else:
    morte()
    
nada = input("\n               - Pressione ENTER -")
print("\n               Atordoado, o Baphomet cai de costas no chão")
nada = input("\n               - Pressione ENTER -")
print("               REPENTINAMENTE, SE LEVANTA COM UM PULO")
print("               E COSPE UMA COLOSSAL BOLA DE FOGO EM SUA DIREÇÃO")
print("\n               O QUE VOCÊ IRÁ FAZER ?")

s = input("\n> ")

if s == "VÁ EMBORA BODE ENORME!":
    cls()
    sleep(2)
    print("=" * 80)
    print("       Antes que possa lhe atingir, a labareda dissipa-se em fumaça, assim")
    print("   como o monstro que a proferiu.")
    nada = input("\n                             - Pressione ENTER -")
    print("            Você se dirige para o portão no fundo da sala, e o abre")
    nada = input("\n                             - Pressione ENTER -")
    print("           O ar puro enche os seus pulmões, e a luz do sol te ofusca")
    nada = input("\n                             - Pressione ENTER -")
    print("\n\n                               \"VOCE ESCAPOU\" ")
    sleep(2)
    nada = input("\n                           - Pressione ENTER para sair-")
    print("      nas quais você poderá interagir com os objetos do cenário ao observá-los,")    
else:
    morte()
