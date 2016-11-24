#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: locDefs
#*
#*  Descrição: constantes válidas para todo sistema
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  mlabru   2008/jun/20  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versão
#*  -----------------------------------------------------------------------------------------------
#*  start    2008/jun/20  version started
#*  1.2-0.1  2008/jun/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ pyACME / model
#/ ------------------------------------------------------------------------------------------------
import model.glbDefs as glbDefs

#** ===============================================================================================
#*  aeronaves
#*  ===============================================================================================
#*/

RotacaoSolo    = 15.  #! graus/seg
RotacaoSolo8   = 45.  #! graus/seg (família 8)

VarAngTrafego  =  6.  #! graus/seg
VarAngTrafego8 = 15.  #! graus/seg (família 8)

VarAngRota     =  3.  #! graus/seg
VarAngRota8    =  7.  #! graus/seg (família 8)

#** ===============================================================================================
#*  arquivos
#*  ===============================================================================================
#*/

#/ performance
#/ ------------------------------------------------------------------------------------------------
xARQ_PRF = "PERFORM.TAB"

#/ replay de exercício
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
#*  cores
#*  ===============================================================================================
#*/

#** -----------------------------------------------------------------------------------------------
#*  try to load pyGame (biblioteca gráfica)
#*/
try:

    #** -------------------------------------------------------------------------------------------
    #*  import Psyco if available
    #*/
    from pygame.color import THECOLORS

    #/ cores dos elementos de tela
    #/ --------------------------------------------------------------------------------------------
    xCOR_Aer       = glbDefs.xCOR_black
    xCOR_Circuito  = THECOLORS [ "darkorange4" ]
    xCOR_Congelado = glbDefs.xCOR_red
    xCOR_DeclMag   = glbDefs.xCOR_white
    xCOR_FlightNo  = THECOLORS [ "grey98" ]
    xCOR_Header    = THECOLORS [ "grey40" ]
    xCOR_Hora      = THECOLORS [ "grey98" ]
    xCOR_IMet      = glbDefs.xCOR_LYellow1
    xCOR_Messages  = THECOLORS [ "grey98" ]
    xCOR_Percurso  = THECOLORS [ "darkorange4" ]
    xCOR_RangeMark = THECOLORS [ "darkolivegreen4" ]
    xCOR_RoseWind  = THECOLORS [ "grey38" ]
    xCOR_Selected  = glbDefs.xCOR_green
    xCOR_Vers      = THECOLORS [ "grey82" ]

    #/ lista de cores dos status
    #/ --------------------------------------------------------------------------------------------
    xCOR_SA = glbDefs.xCOR_red
    xCOR_SD = THECOLORS [ "salmon" ]
    xCOR_SE = glbDefs.xCOR_LBrown
    xCOR_SP = THECOLORS [ "grey68" ]
    xCOR_ST = THECOLORS [ "lightblue" ]
    xCOR_VC = glbDefs.xCOR_LYellow2
    xCOR_VD = THECOLORS [ "lightsalmon" ]
    xCOR_VN = glbDefs.xCOR_white

#** -----------------------------------------------------------------------------------------------
#*  psyco not found ?
#*/
except ImportError:

    #** -------------------------------------------------------------------------------------------
    #*  get pyGame !
    #*/
    print "get pyGame !"

#** ===============================================================================================
#*  diretórios
#*  ===============================================================================================
#*/

#/ diretório de aeródromos
#/ ------------------------------------------------------------------------------------------------
xDIR_AER = "aer"

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
#*  máximos
#*  ===============================================================================================
#*/

#/ quantidade máxima de aerádromos
#/ ------------------------------------------------------------------------------------------------
xMAX_Aerodromos = 1

#/ quantidade máxima de aeronaves
#/ ------------------------------------------------------------------------------------------------
xMAX_Aeronaves = 50

#/ quantidade máxima de aeronaves ativas
#/ ------------------------------------------------------------------------------------------------
#xMAX_Ativas = 12  # para resolucao de (  800,  600 )
#xMAX_Ativas = 13  # para resolucao de ( 1024,  768 )
#xMAX_Ativas = 17  # para resolucao de ( 1280,  960 )
xMAX_Ativas = 15  # para resolucao de ( 1280,  990 )
#xMAX_Ativas = 19  # para resolucao de ( 1280, 1024 )

#/ quantidade máxima de cabeceiras
#/ ------------------------------------------------------------------------------------------------
xMAX_Cabeceiras = 2

#/ quantidade máxima de circuitos
#/ ------------------------------------------------------------------------------------------------
xMAX_Circuitos = 3

#/ quantidade de desenhos de aeronaves
#/ ------------------------------------------------------------------------------------------------
xMAX_Desenhos = 5

#/ quantidade máxima de escalas
#/ ------------------------------------------------------------------------------------------------
xMAX_Escalas = 3

#/ quantidade máxima de famílias
#/ ------------------------------------------------------------------------------------------------
xMAX_Familias = 8

#/ quantidade máxima de figuras do cenário
#/ ------------------------------------------------------------------------------------------------
xMAX_Figuras = 40

#/ quantidade máxima de gravações para replay
#/ ------------------------------------------------------------------------------------------------
#xMAX_Gravações = 5000

#/ quantidade máxima de pistas
#/ ------------------------------------------------------------------------------------------------
xMAX_Pistas = 2

#/ quantidade máxima de pontos adjacentes
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosAdjs = 5

#/ quantidade máxima de pontos de saída de pista
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosArr = 6

#/ quantidade máxima de pontos de decolagem
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosDep = 3

#/ quantidade máxima de pontos no solo
#/ ------------------------------------------------------------------------------------------------
xMAX_PontosNoSolo = 45

#/ quantidade máxima de segmentos
#/ ------------------------------------------------------------------------------------------------
xMAX_Segmentos = 4

#/ quantidade máxima de trechos no percurso
#/ ------------------------------------------------------------------------------------------------
xMAX_Trechos = 30

#/ quantidade máxima de vértices de um polígono
#/ ------------------------------------------------------------------------------------------------
xMAX_Vertices = 40

#** ===============================================================================================
#*  quantidades
#*  ===============================================================================================
#*/

#/ quantidade de atributos dos dados de aeronaves
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribAnv = 13

#/ quantidade de atributos dos dados gerais do exercício
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribExe = 12

#/ quantidade de atributos das aeronaves
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribAer = 9

#/ quantidade de atributos das pistas
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribPista = 17

#/ quantidade de atributos dos dados iniciais do cenário. Os atributos quantidade de Pistas e
#/ quantidade de Pontos no Solo ficam em posições dos outros seis atributos diferentes no arquivo
#/ ------------------------------------------------------------------------------------------------
#xQTD_AtribIniciais = 8

#/ quantidade de itens da tabela de performace
#/ ------------------------------------------------------------------------------------------------
#xQTD_ItensPerform = 16

#** ===============================================================================================
#*  sets
#*  ===============================================================================================
#*/

xSET_ConfValidas      = [ 'S', 'N' ]
xSET_EscalasValidas   = [ 1, 2, 3 ]
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

#/ altura do header em pixels
#/ ------------------------------------------------------------------------------------------------
xSCR_HDR_Height = 12
xSCR_HDR_FntSiz = 12

#/ altura da strip em pixels
#/ ------------------------------------------------------------------------------------------------
xSCR_STP_Height = 40

#/ tamanho da tela (resolucao de 1024x768)
#/ ------------------------------------------------------------------------------------------------
#xSCR_Size = ( 1024, 768 )

#glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ] = ((   0,   0 ), ( 768, 768 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_Info ]  = (( 768,   0 ), ( 256,  48 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_Strip ] = (( 768,  48 ), ( 256, 520 ))  # 520 / xSCR_STP_Height = 13,...(520)
#glbDefs.xSCR_POS [ glbDefs.xSCR_Menu ]  = (( 768, 568 ), ( 256, 100 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_IMet ]  = (( 768, 638 ), ( 256, 130 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_Msg ]   = (( 768, 668 ), ( 256, 100 ))

#/ distancia entre a aeronave e o 'click' considerada aceitavel
#/ ------------------------------------------------------------------------------------------------
#xSCR_CLK_Dist = 10

#/ tamanho da tela (resolucao de 1280x960)
#/ ------------------------------------------------------------------------------------------------
#xSCR_Size = ( 1280, 960 )

#glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ] = ((    0,   0 ), ( 960, 960 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_Info ]  = (( 1024,   0 ), ( 256,  50 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_Strip ] = (( 1024,  50 ), ( 256, 710 ))  # 710 / xSCR_STP_Height = 17,..(680)
#glbDefs.xSCR_POS [ glbDefs.xSCR_Menu ]  = (( 1024, 760 ), ( 256, 100 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_IMet ]  = (( 1024, 840 ), ( 256, 130 ))
#glbDefs.xSCR_POS [ glbDefs.xSCR_Msg ]   = (( 1024, 860 ), ( 256, 100 ))

#/ distancia entre a aeronave e o 'click' considerada aceitavel
#/ ------------------------------------------------------------------------------------------------
#xSCR_CLK_Dist = 11

#/ tamanho da tela (resolucao de 1280x960)
#/ ------------------------------------------------------------------------------------------------
xSCR_Size = ( 1280, 990 )

glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ] = ((    0,   0 ), ( 990, 990 ))
glbDefs.xSCR_POS [ glbDefs.xSCR_Info ]  = (( 1024,   0 ), ( 256,  54 ))

glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ] = (( 1024,  54 ), ( 256, 635 ))  # (635 - 12) / xSCR_STP_Height = 15,..(640)
glbDefs.xSCR_PIL [ glbDefs.xSCR_VoIP ]  = (( 1024, 689 ), ( 256, 100 ))
glbDefs.xSCR_PIL [ glbDefs.xSCR_Menu ]  = (( 1024, 789 ), ( 256, 101 ))
glbDefs.xSCR_PIL [ glbDefs.xSCR_Msg ]   = (( 1024, 890 ), ( 256, 100 ))

glbDefs.xSCR_CTR [ glbDefs.xSCR_Strip ] = (( 1024,  54 ), ( 256, 706 ))  # (706 - 12) / xSCR_STP_Height = 17,..(680)
glbDefs.xSCR_CTR [ glbDefs.xSCR_VoIP ]  = (( 1024, 760 ), ( 256, 100 ))
glbDefs.xSCR_CTR [ glbDefs.xSCR_IMet ]  = (( 1024, 860 ), ( 256, 130 ))

#/ distancia entre a aeronave e o 'click' considerada aceitavel
#/ ------------------------------------------------------------------------------------------------
xSCR_CLK_Dist = 12

#/ tamanho da tela (resolucao de 1280x1024)
#/ ------------------------------------------------------------------------------------------------
#xSCR_Size = ( 1280, 1024 )

#xSCR_POS [ xSCR_Scope ] = ((    0,   0 ), ( 1024, 1024 ))
#xSCR_POS [ xSCR_Info ]  = (( 1024,   0 ), (  256,   50 ))
#xSCR_POS [ xSCR_Strip ] = (( 1024,  50 ), (  256,  774 ))  # 774 / xSCR_STP_Height = 19,..(760)
#xSCR_POS [ xSCR_Menu ]  = (( 1024, 824 ), (  256,  100 ))
#xSCR_POS [ xSCR_IMet ]  = (( 1024, 894 ), (  256,  130 ))
#xSCR_POS [ xSCR_Msg ]   = (( 1024, 924 ), (  256,  100 ))

#/ distancia entre a aeronave e o 'click' considerada aceitavel
#/ ------------------------------------------------------------------------------------------------
#xSCR_CLK_Dist = 12

#** ===============================================================================================
#*  texts
#*  ===============================================================================================
#*/

#/ versao
#/ ------------------------------------------------------------------------------------------------
xTXT_Mjr = "2"
xTXT_Mnr = "09"
xTXT_Rls = "6.03p"
xTXT_Vrs = xTXT_Mjr + "." + xTXT_Mnr
xTXT_Bld = xTXT_Vrs + "-" + xTXT_Rls

#/ programa
#/ ------------------------------------------------------------------------------------------------
xTXT_Prg = "SiCAD"
xTXT_Tit = xTXT_Prg + " " + xTXT_Vrs
xTXT_Hdr = xTXT_Prg + " " + xTXT_Bld

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

#** ----------------------------------------------------------------------------------------------- *#
