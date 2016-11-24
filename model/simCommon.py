#!/usr/bin/env python2.5
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: simConfig
#*
#*  Descricao: constantes e variaveis validas para todo sistema
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteracao
#*  -----------------------------------------------------------------------------------------------
#*  mlabru   2008/???/??  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versao
#*  -----------------------------------------------------------------------------------------------
#*  start    2008/???/??  version started
#*  1.2-0.1  2008/JUN/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** ===============================================================================================
#*  aeronaves
#*  ===============================================================================================
#*/

RotacaoSolo    = 0.15  #! graus/100th seg
RotacaoSolo8   = 0.45  #! graus/100th seg (familia 8)

VarAngTrafego  = 0.06  #! graus/100th seg
VarAngTrafego8 = 0.15  #! graus/100th seg (familia 8)

VarAngRota     = 0.03  #! graus/100th seg
VarAngRota8    = 0.07  #! graus/100th seg (familia 8)

#** ===============================================================================================
#*  arquivos
#*  ===============================================================================================
#*/

#/ tabela de portas seriais
#/ ------------------------------------------------------------------------------------------------
#xARQ_SERIAL = "COM.TAB"

#/ desenho de aeronaves
#/ ------------------------------------------------------------------------------------------------
#xARQ_DESENHOS = "DESENHOS.TAB"

#/ imagens de aeronaves
#/ ------------------------------------------------------------------------------------------------
#xARQ_IMAGENS = "IMAGENS.TAB"

#/ performance
#/ ------------------------------------------------------------------------------------------------
xARQ_PRF = "PERFORM.TAB"

#/ replay de exercicio
#/ ------------------------------------------------------------------------------------------------
#xARQ_REPLAY = "DADOS.TAB"

#** ===============================================================================================
#*  circuitos
#*  ===============================================================================================
#*/
xCKT_Teta11 = 18.4349  #! graus
xCKT_Teta12 = 16.6992
xCKT_Teta13 = 15.9454

xCKT_Dist11 = 2928.2691  #! metros
xCKT_Dist12 = 4833.8619
xCKT_Dist13 = 6741.3818

#** ===============================================================================================
#*  conversao
#*  ===============================================================================================
#*/
xCNV_ft2M = 0.30480      #! pes -> metro
xCNV_M2ft = 3.28084      #! metro -> pes

xCNV_NM2M = 1852.0       #! milhas nauticas -> metro
xCNV_M2NM = 0.539957E-3  #! metro -> milhas nauticas

xCNV_Knots2Mcs = 0.514444444E-2  #! knots -> m/100th
xCNV_Mcs2Knots = 194.3844492441  #! m/100th -> knots

xCNV_ftMin2Mcs = 0.5080E-4       #! pes/min -> m/100th
xCNV_Mcs2ftMin = 19685.04        #! m/100th -> pes/min

xCNV_KMin2Mcs2 = 0.857407407E-6  #! knots/min -> m/100th^2

#** ===============================================================================================
#*  cores
#*  ===============================================================================================
#*/

#** -----------------------------------------------------------------------------------------------
#*  try to load pyGame (biblioteca grafica)
#*/
try:

    #** -------------------------------------------------------------------------------------------
    #*  import Psyco if available
    #*/
    from pygame.color import THECOLORS

    #/ cores basicas
    #/ --------------------------------------------------------------------------------------------
    xCOR_black     = THECOLORS [ "black" ]
    xCOR_blue      = THECOLORS [ "blue" ]
    xCOR_brown     = THECOLORS [ "brown" ]
    xCOR_cyan      = THECOLORS [ "cyan" ]
    xCOR_darkgreen = THECOLORS [ "darkgreen" ]
    xCOR_darkred   = THECOLORS [ "darkred" ]
    xCOR_gray60    = THECOLORS [ "gray60" ]
    xCOR_green     = THECOLORS [ "green" ]
    xCOR_red       = THECOLORS [ "red" ]
    xCOR_white     = THECOLORS [ "white" ]
    xCOR_yellow    = THECOLORS [ "yellow" ]

    #/ cores proprias
    #/ --------------------------------------------------------------------------------------------
    xCOR_LBrown    = ( 163, 113,  82, 255 )
    xCOR_LYellow1  = ( 255, 255, 120, 255 )
    xCOR_LYellow2  = ( 255, 255, 180, 255 )
    xCOR_SGrey     = ( 210, 210, 210, 255 )

    #/ cores dos elementos de tela
    #/ --------------------------------------------------------------------------------------------
    xCOR_Aer       = xCOR_black
    xCOR_Circuito  = THECOLORS [ "darkorange4" ]
    xCOR_Congelado = xCOR_red
    xCOR_DeclMag   = xCOR_white
    xCOR_FlightNo  = THECOLORS [ "grey98" ]
    xCOR_Header    = THECOLORS [ "grey40" ]
    xCOR_Hora      = THECOLORS [ "grey98" ]
    xCOR_IMet      = xCOR_LYellow1
    xCOR_Messages  = THECOLORS [ "grey98" ]
    xCOR_Percurso  = THECOLORS [ "darkorange4" ]
    xCOR_RangeMark = THECOLORS [ "darkolivegreen4" ]
    xCOR_RoseWind  = THECOLORS [ "grey38" ]
    xCOR_Selected  = xCOR_green
    xCOR_Vers      = THECOLORS [ "grey82" ]

    #/ lista de cores dos status
    #/ --------------------------------------------------------------------------------------------
    xCOR_SA = xCOR_red
    xCOR_SD = THECOLORS [ "salmon" ]
    xCOR_SE = xCOR_LBrown
    xCOR_SP = THECOLORS [ "grey68" ]
    xCOR_ST = THECOLORS [ "lightblue" ]
    xCOR_VC = xCOR_LYellow2
    xCOR_VD = THECOLORS [ "lightsalmon" ]
    xCOR_VN = xCOR_white

#** -----------------------------------------------------------------------------------------------
#*  psyco not found ?
#*/
except ImportError:

    #** -------------------------------------------------------------------------------------------
    #*  get pyGame !
    #*/
    print "get pyGame !"

#** ===============================================================================================
#*  diretorios
#*  ===============================================================================================
#*/

#/ diretorio de aerodromos
#/ ------------------------------------------------------------------------------------------------
xDIR_AER = "aer"

#/ diretorio de exercicios
#/ ------------------------------------------------------------------------------------------------
xDIR_EXE = "exe"

#/ diretorio de exercicios
#/ ------------------------------------------------------------------------------------------------
xDIR_DAT = "data"

#/ diretorio de fontes
#/ ------------------------------------------------------------------------------------------------
xDIR_FNT = "fonts"

#/ diretorio de imagens
#/ ------------------------------------------------------------------------------------------------
xDIR_IMG = "images"

#/ diretorio de PAR's
#/ ------------------------------------------------------------------------------------------------
xDIR_PAR = "par"

#/ diretorio de sons
#/ ------------------------------------------------------------------------------------------------
xDIR_SND = "sounds"

#/ diretorio de tabelas
#/ ------------------------------------------------------------------------------------------------
xDIR_TAB = "tab"

#** ===============================================================================================
#*  figuras
#*  ===============================================================================================
#*/

xFIG_PONTO = 1
xFIG_POLIGONO = 2
xFIG_CIRCUNFERENCIA = 3
xFIG_CIRCULO = 4
xFIG_LINHA = 5
xFIG_NDB = 6
xFIG_VOR = 7
xFIG_FIXO = 8
xFIG_OBSTACULO = 9
xFIG_LINHAS_CABEC = 10
xFIG_LINHA_PISTA = 11

#** ===============================================================================================
#*  fonts
#*  ===============================================================================================
#*/

xFNT_None = "freesansbold.ttf"
xFNT_VARS = None
xFNT_MENU = "vrinda.ttf"
xFNT_MONO = "AurulentSansMono-Regular.otf"
#xFNT_MONO = "verdana.ttf"

#** ===============================================================================================
#*  maximos
#*  ===============================================================================================
#*/

#/ quantidade maxima de cabeceiras
#/ ------------------------------------------------------------------------------------------------
xMAX_Cabeceiras = 2

#/ quantidade maxima de circuitos
#/ ------------------------------------------------------------------------------------------------
xMAX_Circuitos = 3

#/ quantidade de desenhos de aeronaves
#/ ------------------------------------------------------------------------------------------------
xMAX_Desenhos = 5

#/ quantidade maxima de escalas
#/ ------------------------------------------------------------------------------------------------
xMAX_Escalas = 3

#/ quantidade maxima de familias
#/ ------------------------------------------------------------------------------------------------
xMAX_Familias = 8

#/ quantidade maxima de figuras do cenario
#/ ------------------------------------------------------------------------------------------------
xMAX_Figuras = 40

#/ quantidade maxima de gravacoes para replay
#/ ------------------------------------------------------------------------------------------------
#xMAX_Gravacoes = 5000

#/ quantidade maxima de pistas
#/ ------------------------------------------------------------------------------------------------
xMAX_Pistas = 2

#/ quantidade maxima de pontos adjacentes
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosAdjs = 5

#/ quantidade maxima de pontos de saida de pista
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosArr = 6

#/ quantidade maxima de pontos de decolagem
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosDep = 3

#/ quantidade maxima de pontos no solo
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosNoSolo = 45

#/ quantidade maxima de segmentos
#/ ------------------------------------------------------------------------------------------------
xMAX_Segmentos = 4

#/ quantidade maxima de trechos no percurso
#/ ------------------------------------------------------------------------------------------------
xMAX_Trechos = 30

#/ quantidade maxima de vertices de um poligono
#/ ------------------------------------------------------------------------------------------------
xMAX_Vertices = 40

#** ===============================================================================================
#*  mensagens
#*  ===============================================================================================
#*/

#/ codigos das mensagens
#/ ------------------------------------------------------------------------------------------------
xMSG_Acc = 511
xMSG_Ckt = 521
xMSG_CSg = 531
xMSG_Dat = 541
xMSG_Exe = 551
xMSG_Exp = 561
xMSG_Fim = 571
xMSG_Frz = 581
xMSG_Kll = 591
xMSG_RMk = 611
xMSG_Tim = 621
xMSG_Ufz = 631
xMSG_WRs = 641

#/ separador de campos na mensagem
#/ ------------------------------------------------------------------------------------------------
xMSG_Sep = '#'

#/ versao do conjunto de mensagens
#/ ------------------------------------------------------------------------------------------------
xMSG_Vrs = 201

#** ===============================================================================================
#*  quantidades
#*  ===============================================================================================
#*/

#/ quantidade de atributos dos dados de aeronaves
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribAnv = 13

#/ quantidade de atributos dos dados gerais do exercicio
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribExe = 12

#/ quantidade de atributos das aeronaves
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribAer = 9

#/ quantidade de atributos das pistas
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribPista = 17

#/ quantidade de atributos dos dados iniciais do cenario. Os atributos quantidade de Pistas e
#/ quantidade de Pontos no Solo ficam em posicoes dos outros seis atributos diferentes no arquivo
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribIniciais = 8

#/ quantidade de itens da tabela de performace
#/ ------------------------------------------------------------------------------------------------
#xQTD_ItensPerform = 16

#** ===============================================================================================
#*  rede
#*  ===============================================================================================
#*/

#/ endereco multicast de configuracao
#/ ------------------------------------------------------------------------------------------------
xNET_Cnfg = "233.12.2"

#/ endereco multicast de dados
#/ ------------------------------------------------------------------------------------------------
xNET_Data = "235.12.2"

#/ endereco multicast de comunicacao
#/ ------------------------------------------------------------------------------------------------
xNET_VoIP = "237.12.2"

#/ porta de comunicacao
#/ ------------------------------------------------------------------------------------------------
xNET_Port = 1970

#** ===============================================================================================
#*  sets
#*  ===============================================================================================
#*/

xSET_ConfValidas      = [ 'S', 'N' ]
xSET_EscalasValidas   = [ '1', '2', '3' ]
xSET_SentidosGiro     = [ 'A', 'H', 'I' ]
xSET_SentidosValidos  = [ 'D', 'E' ]

xSET_StatusAeronaves  = [ 'A', 'E' ]
xSET_StatusCircuitos  = [ 'C', 'K', 'V' ]
xSET_StatusExercicio  = [ 'D', 'G', 'T' ]
xSET_StatusSolo       = [ 'C', 'D', 'P' ]

#xSET_ProasValidas    = [ x for x in xrange ( 360 ) ]
xSET_DifAngValidas    = [ x for x in xrange ( 160, 200 ) ]
xSET_DifAngAceitaveis = [ x for x in xrange (   0,  20 ) ]

#xSET_AeronavesValidas = [ ( x + 1 ) for x in xrange ( xMAX_Aeronaves ) ]
#xSET_FamiliasValidas  = [ ( x + 1 ) for x in xrange ( xMAX_Familias ) ]
#xSET_CircuitosValidos = [ ( x + 1 ) for x in xrange ( xMAX_Circuitos ) ]

#** ===============================================================================================
#*  tela
#*  ===============================================================================================
#*/

#** ===============================================================================================
#*  sons
#*  ===============================================================================================
#*/

#/ alerta
#/ ------------------------------------------------------------------------------------------------
xSND_Alert = "alert.ogg"

#/ explosao
#/ ------------------------------------------------------------------------------------------------
xSND_Explode = "explosion.wav"

#/ volume de saida (0..1)
#/ ------------------------------------------------------------------------------------------------
xSND_Vol_Out = .5

#/ volume do microfone (0..1)
#/ ------------------------------------------------------------------------------------------------
xSND_Vol_Mic = .5

#** ===============================================================================================
#*  temporizacao
#*  ===============================================================================================
#*/

#/ fast-time simulation acceleration factor
#/ ------------------------------------------------------------------------------------------------
xTIM_Accel = 1

#/ reenvia a configuracao do sistema a cada 5 seg
#/ ------------------------------------------------------------------------------------------------
xTIM_Cnfg = 5

#/ tratador de eventos (100/1000th)
#/ ------------------------------------------------------------------------------------------------
xTIM_Evnt = .1

#/ verifica o tempo de ativacao das aeronaves a cada 30 seg
#/ ------------------------------------------------------------------------------------------------
xTIM_FGen = 30

#/ reenvia a hora do sistema a cada 1 seg
#/ ------------------------------------------------------------------------------------------------
xTIM_Hora = 1

#/ verifica colisao entre aeronaves a cada 1 seg
#/ ------------------------------------------------------------------------------------------------
xTIM_Prox = 1

#/ refresh de tela (100/1000th) (10 fps)
#/ ------------------------------------------------------------------------------------------------
xTIM_Refresh = .1

#/ recalculo da posicao da aeronave (100/1000th) (10 cps)
#/ ------------------------------------------------------------------------------------------------
xTIM_Wait = .1

#/ round robin do sistema (1000/1000th) (1 cps)
#/ ------------------------------------------------------------------------------------------------
xTIM_RRbn = 1.

#** ===============================================================================================
#*  texts
#*  ===============================================================================================
#*/

#** ===============================================================================================
#*  viewport
#*  ===============================================================================================
#*/

#/ viewport
#/ ------------------------------------------------------------------------------------------------
xVWP_Inf_X = 0.0
#xVWP_Inf_X = 0.25

#xVWP_Inf_Y = 0.0
xVWP_Inf_Y = 0.075
#xVWP_Inf_Y = 0.165
#xVWP_Inf_Y = 0.250

#/ viewport superior
#/ ------------------------------------------------------------------------------------------------
xVWP_Sup_X = 1.0
xVWP_Sup_Y = 1.0

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ keep things running
#/ ------------------------------------------------------------------------------------------------
g_bKeepRun = False

#/ trava da lista de voos
#/ ------------------------------------------------------------------------------------------------
g_lckFlight = None

#** ----------------------------------------------------------------------------------------------- *#
