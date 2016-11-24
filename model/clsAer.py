#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SICAD
#*  Classe...: clsAer
#*
#*  Descricao: implementacao das classes PtoSolo e clsAer do SiCAD.
#*             A classe clsAer mantem as informacoes sobre exercicio e os metodos que um objeto
#*             exercicio pode responder
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteracao
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/fev/12  version started
#*  mlabru   2008/fev/12  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versao
#*  -----------------------------------------------------------------------------------------------
#*  start    2008/fev/12  version started
#*  1.2-0.1  2008/jun/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ Python library
#/ ------------------------------------------------------------------------------------------------
import math

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineCalc as cineCalc
import model.clsCab as clsCab
import model.clsFig as clsFig
import model.clsPst as clsPst
import model.clsTrj as clsTrj
import model.shortestPath as shortestPath
import model.locDefs as locDefs
import model.glbDefs as glbDefs

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  clsAer::PtoSolo
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a PtoSolo
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class PtoSolo:

    #** -------------------------------------------------------------------------------------------
    #*  PtoSolo::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to PtoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_tPos ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "PtoSolo::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_tPos )

        #** ---------------------------------------------------------------------------------------
        #*  posicao do ponto
        #*/
        self._tPos = f_tPos
        assert ( self._tPos )

        #** ---------------------------------------------------------------------------------------
        #*  lista de pontos adjacentes
        #*/
        self._lstAdjacentes = []

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  PtoSolo::getPos
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to PtoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPos ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "PtoSolo::getPos"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._tPos )

#** -----------------------------------------------------------------------------------------------
#*  clsAer::clsAer
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a clsAer
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class clsAer:

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to scope and view
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_szAer ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_szAer )
        #l_log.info ( "Arquivo de aerodromo a carregar: " + f_szAer )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dComp = None
        self._dicG = None
        self._dLarg = None
        self._dXInf = None
        self._dXSup = None
        self._dYInf = None
        self._dYSup = None

        self._iDifDeclinacao = None

        self._lstFig = None
        self._lstPontosNoSolo = None
        self._lstPst = None

        self._oTrj = None

        self._tCentro = None

        self._uiAltitude = None

        #** ---------------------------------------------------------------------------------------
        #*  abre o arquivo de aerodromo
        #*/
        l_FAer = open ( f_szAer, "r" )
        assert ( l_FAer )

        #** ---------------------------------------------------------------------------------------
        #*  cria a area de dados
        #*/
        l_data = []

        #** ---------------------------------------------------------------------------------------
        #*  percorre todas as linhas do arquivo de exercicio
        #*/
        for l_line in l_FAer.readlines ():

            #** -----------------------------------------------------------------------------------
            #*  checa se eh uma linha de comentario ou vazia
            #*/
            if (( not l_line.startswith ( "#" )) and
                ( not l_line.startswith ( "\n" ))):

                #** -------------------------------------------------------------------------------
                #*  checa end-of-line
                #*/
                if ( l_line.endswith ( "\n" ) or l_line.endswith ( "\x1a" )):

                    #** ---------------------------------------------------------------------------
                    #*  aceita o valor sem o end-of-line
                    #*/
                    l_data.extend ( l_line [ :-1 ].split ())

                #** -------------------------------------------------------------------------------
                #*  senao, nao eh fim de linha
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  aceita o valor
                    #*/
                    l_data.extend ( l_line.split ())

        #** ---------------------------------------------------------------------------------------
        #*  fecha o arquivo
        #*/
        l_FAer.close ()

        #** ---------------------------------------------------------------------------------------
        #*  carrega o exercicio
        #*/
        self.loadAerodromo ( l_data )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::loadAerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  carrega os dados do exercicio
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_data - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def loadAerodromo ( self, f_data ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::loadAerodromo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  carrega o comprimento e a largura
        #*/
        self._dComp = float ( f_data [ 0 ] )
        #l_log.info ( "_dComp: " + str ( self._dComp ))

        self._dLarg = float ( f_data [ 1 ] )
        #l_log.info ( "_dLarg: " + str ( self._dLarg ))

        #** ---------------------------------------------------------------------------------------
        #*  define a janela do aerodromo
        #*/
        self._dXInf = 0.0
        self._dYInf = 0.0

        self._dXSup = self._dComp
        self._dYSup = self._dLarg

        #** ---------------------------------------------------------------------------------------
        #*  carrega a altitue do aerodromo
        #*/
        self._uiAltitude = int ( f_data [ 2 ] )
        #l_log.info ( "_uiAltitude: " + str ( self._uiAltitude ))

        #** ---------------------------------------------------------------------------------------
        #*  carrega o centro (x, y) do aerodromo
        #*/
        self._tCentro = ( float ( f_data [ 3 ] ), float ( f_data [ 4 ] ))
        #l_log.info ( "_tCentro: " + str ( self._tCentro ))

        #** ---------------------------------------------------------------------------------------
        #*  carrega a declinacao magnetica do aerodromo
        #*/
        self._iDifDeclinacao = int ( f_data [ 5 ] )
        #l_log.info ( "_iDifDeclinacao: " + str ( self._iDifDeclinacao ))

        #** ---------------------------------------------------------------------------------------
        #*  carrega as figuras do aerodromo
        #*/
        l_iD = self.loadFiguras ( f_data )

        #** ---------------------------------------------------------------------------------------
        #*  carrega os pontos no solo
        #*/
        l_iD = self.loadPontosNoSolo ( l_iD, f_data )

        #** ---------------------------------------------------------------------------------------
        #*  carrega as pistas do aerodromo
        #*/
        l_iD = self.loadPistas ( l_iD, f_data )

        #** ---------------------------------------------------------------------------------------
        #*  para todas as pistas do aerodromo...
        #*/
        for l_oPst in self._lstPst:

            #** -----------------------------------------------------------------------------------
            #*/
            assert ( l_oPst )
            assert ( isinstance ( l_oPst, clsPst.clsPst ))

            #** -----------------------------------------------------------------------------------
            #*  para todos os circuitos definidos...
            #*/
            for l_iCkt in xrange ( locDefs.xMAX_Circuitos ):

                #** -------------------------------------------------------------------------------
                #*  monta os circuitos
                #*/
                l_oPst.montaCircuito ( l_iCkt )

            #** -----------------------------------------------------------------------------------
            #*  monta a final da pista
            #*/
            l_oPst.montaFinal ()

            #** -----------------------------------------------------------------------------------
            #*/
            l_oPst.montaDirecaoDistanciaSegmento ( self._iDifDeclinacao )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::loadFiguras
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def loadFiguras ( self, f_data ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::loadFiguras"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a lista de figuras
        #*/
        self._lstFig = []

        #** ---------------------------------------------------------------------------------------
        #*  carrega o nome da figura
        #*/
        l_szNomeFigura = str ( f_data [ 6 ] ).upper ()
        #l_log.info ( "l_szNomeFigura: " + l_szNomeFigura )

        #** ---------------------------------------------------------------------------------------
        #*  inicia pointer de dados
        #*/
        l_iD = 7

        #** ---------------------------------------------------------------------------------------
        #*  trata todas as figuras do arquivo
        #*/
        while ( "FIMIMAGEM" != l_szNomeFigura ):

            #** -----------------------------------------------------------------------------------
            #*  cria o objeto figura
            #*/
            l_Fig = clsFig.clsFig ()
            assert ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  ponto ?
            #*/
            if ( "PONTO" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do ponto
                #*/
                l_iD = l_Fig.loadPonto ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  poligono ?
            #*/
            elif ( "POLIGONO" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do poligono
                #*/
                l_iD = l_Fig.loadPoligono ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  circunferencia ?
            #*/
            elif ( "CIRCUNFERENCIA" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do ponto
                #*/
                l_iD = l_Fig.loadCircunferencia ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  circulo ?
            #*/
            elif ( "CIRCULO" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do circulo
                #*/
                l_iD = l_Fig.loadCirculo ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  linha ?
            #*/
            elif ( "LINHA" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados da linha
                #*/
                l_iD = l_Fig.loadLinha ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  NDB ?
            #*/
            elif ( "NDB" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do NDB
                #*/
                l_iD = l_Fig.loadNDB ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  VOR ?
            #*/
            elif ( "VOR" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do VOR
                #*/
                l_iD = l_Fig.loadVOR ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  fixo ?
            #*/
            elif ( "FIXO" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do fixo
                #*/
                l_iD = l_Fig.loadFixo ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  obstaculo ?
            #*/
            elif ( "OBSTACULO" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados do obstaculo
                #*/
                l_iD = l_Fig.loadObstaculo ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  linhas de cabeceira ?
            #*/
            elif ( "LINHASCABEC" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados das linhas de cabeceira
                #*/
                l_iD = l_Fig.loadLinhasCabec ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  linha de pista ?
            #*/
            elif ( "LINHASPISTA" == l_szNomeFigura ):

                #** -------------------------------------------------------------------------------
                #*  carrega os dados das linhas de pista
                #*/
                l_iD = l_Fig.loadLinhaPista ( l_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  salva a figura na lista
            #*/
            self._lstFig.append ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  carrega o nome da figura
            #*/
            l_szNomeFigura = str ( f_data [ l_iD ] ).upper ()
            l_iD += 1

            #l_log.info ( "l_szNomeFigura: " + l_szNomeFigura )

        #** ---------------------------------------------------------------------------------------
        #*/
        #l_log.info ( "Qtde de Figuras: " + str ( len ( self._lstFig )))
        assert ( len ( self._lstFig ) <= locDefs.xMAX_Figuras )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_iD )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::loadPistas
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def loadPistas ( self, f_iD, f_data ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::loadPistas"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a lista de pistas
        #*/
        self._lstPst = []

        #** ---------------------------------------------------------------------------------------
        #*  quantidade de pistas do aerodromo
        #*/
        l_iQtdePistas = int ( f_data [ f_iD ] )
        f_iD += 1

        #l_log.info ( "l_iQtdePistas: " + str ( l_iQtdePistas ))
        assert ( l_iQtdePistas <= locDefs.xMAX_Pistas )

        #** ---------------------------------------------------------------------------------------
        #*  para todas as pistas deste aerodromo...
        #*/
        for l_iP in xrange ( l_iQtdePistas ):

            #** -----------------------------------------------------------------------------------
            #*  cria o objeto pista
            #*/
            l_Pst = clsPst.clsPst ()
            assert ( l_Pst )

            #** -----------------------------------------------------------------------------------
            #*  carrega os dados da pista
            #*/
            f_iD = l_Pst.loadPista ( f_iD, f_data )

            #** -----------------------------------------------------------------------------------
            #*  salva a figura na lista
            #*/
            self._lstPst.append ( l_Pst )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( f_iD )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::loadPontosNoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  uma tabela de pontos no solo para cada aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*/
    def loadPontosNoSolo ( self, f_iD, f_data ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::loadPontosNoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  quantidade de pontos no solo
        #*/
        l_iQtdePtos = int ( f_data [ f_iD ] )
        f_iD += 1

        #l_log.info ( "l_iQtdePtos: " + str ( l_iQtdePtos ))
        assert ( l_iQtdePtos <= locDefs.xMAX_PontosNoSolo )

        #** ---------------------------------------------------------------------------------------
        #*  cria a lista que ira conter os pontos no solo
        #*/
        self._lstPontosNoSolo = []

        #** ---------------------------------------------------------------------------------------
        #*  cria o dicionario que ira conter os pontos no solo
        #*/
        self._dicG = {}

        #** ---------------------------------------------------------------------------------------
        #*  para cada um dos pontos no solo...
        #*/
        for l_iP in xrange ( l_iQtdePtos ):

            #** -----------------------------------------------------------------------------------
            #*/
            #l_log.info ( "Ponto: " + str ( l_iP ))

            #** -----------------------------------------------------------------------------------
            #*  obtem a posicao X do ponto
            #*/
            l_dX = float ( f_data [ f_iD ] )
            f_iD += 1

            #** -----------------------------------------------------------------------------------
            #*  obtem a posicao Y do ponto
            #*/
            l_dY = float ( f_data [ f_iD ] )
            f_iD += 1

            #l_log.info ( "Pos: " + str (( l_dX, l_dY )))

            #** -----------------------------------------------------------------------------------
            #*  quantidade de pontos adjacentes
            #*/
            l_iQtdeAdjs = int ( f_data [ f_iD ] )
            f_iD += 1

            #l_log.info ( "l_iQtdeAdjs: " + str ( l_iQtdeAdjs ))

            #** -----------------------------------------------------------------------------------
            #*  cria o ponto no solo com a posicao
            #*/
            l_oPtoSolo = PtoSolo (( l_dX, l_dY ))
            assert ( l_oPtoSolo )

            #** -----------------------------------------------------------------------------------
            #*/
            l_Dict = {}

            #** -----------------------------------------------------------------------------------
            #*  para todos os pontos adjacentes...
            #*/
            for l_iA in xrange ( l_iQtdeAdjs ):

                #** -------------------------------------------------------------------------------
                #*  obtem o ponto adjacente
                #*/
                l_iPto = int ( f_data [ f_iD ] )
                f_iD += 1

                #** -------------------------------------------------------------------------------
                #*  ajusta para inicio de array em 0 (zero) e salva
                #*/
                l_oPtoSolo._lstAdjacentes.append ( l_iPto - 1 )

                #** -------------------------------------------------------------------------------
                #*  ajusta para inicio de array em 0 (zero) e coloca no dicionario
                #*/
                l_Dict [ l_iPto - 1 ] = 0.0

            #l_log.info ( "_lstAdjacentes: " + str ( l_oPtoSolo._lstAdjacentes ))
            #l_log.info ( "Dic.Adjacentes: " + str ( l_Dict ))

            #** -----------------------------------------------------------------------------------
            #*  salva o ponto
            #*/
            self._lstPontosNoSolo.append ( l_oPtoSolo )
            assert ( self._lstPontosNoSolo [ l_iP ] )

            #** -----------------------------------------------------------------------------------
            #*  salva o ponto no dicionario
            #*/
            self._dicG [ l_iP ] = l_Dict

            #** -----------------------------------------------------------------------------------
            #*/
            #for x in self._dicG:

                #l_log.info ( "key: " + str ( x ) + " value: " + str ( self._dicG [ x ] ))

                #for y in self._dicG [ x ]:

                    #l_log.info ( "key: " + str ( y ) + " value: " + str ( self._dicG [ x ][ y ] ))
                    #l_log.info ( "distancia de: " + str ( x ) + " ate: " + str ( y ) + " = " + str ( self._dicG [ x ][ y ] ))

        #** ---------------------------------------------------------------------------------------
        #*  monta as trajetorias e caminhos
        #*/
        self._oTrj = clsTrj.clsTrj ( self._lstPontosNoSolo, self._dicG )
        assert ( self._oTrj )

        #** ---------------------------------------------------------------------------------------
        #*/
        #for x in self._dicG:

            #l_log.info ( "key: " + str ( x ) + " value: " + str ( self._dicG [ x ] ))

            #for y in self._dicG [ x ]:

                #l_log.info ( "key: " + str ( y ) + " value: " + str ( self._dicG [ x ][ y ] ))
                #l_log.info ( "distancia de: " + str ( x ) + " ate: " + str ( y ) + " = " + str ( self._dicG [ x ][ y ] ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( f_iD )

    #** ===========================================================================================
    #*  rotinas de tratamento de percursos e trajetorias
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::calculaPontoParadaPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def calculaPontoParadaPouso ( self, f_oAtv, f_dCabDir ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::calculaPontoParadaPouso"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a desaceleracao no pouso
        #*/
        l_dAcc = f_oAtv.getDesaceleracaoArr ()
        #l_log.info ( "desaceleracao no pouso: " + str ( l_dAcc ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade atual da aeronave
        #*/
        l_dV0 = f_oAtv.getNavVel ()
        #l_log.info ( "velocidade atual: " + str ( l_dV0 ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade de taxi desta aeronave. Esta sera a velocidade de referencia para
        #*  que uma aeronave saia do status 'S' (parando apos o pouso) para o status 'T' ou 'B'
        #*/
        l_dVTax = f_oAtv.getVelocidadeTaxi () * glbDefs.xCNV_Knots2Ms
        #l_log.info ( "velocidade de taxi: " + str ( l_dVTax ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o tempo necessario para parar
        #*/
        l_dDltT = ( l_dV0 - l_dVTax ) / l_dAcc
        #l_log.info ( "tempo para parar: " + str ( l_dDltT ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distancia percorrida nestas condicoes x = vot - 1/2 at^2
        #*/
        l_dDst = ( l_dV0 * l_dDltT ) - (( l_dAcc * ( l_dDltT ** 2 )) / 2.0 )
        #l_log.info ( "distancia ate parar: " + str ( l_dDst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direcao da pista
        #*/
        l_dDir = math.radians ( f_dCabDir )
        #l_log.info ( "direcao da pista: " + str ( l_dDir ))

        #** ---------------------------------------------------------------------------------------
        #*  decompoem o deslocamento em X e Y na direcao da pista
        #*/
        l_dDstX = l_dDst * math.cos ( l_dDir )
        l_dDstY = l_dDst * math.sin ( l_dDir )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a posicao atual da aeronave
        #*/
        l_tAnv = f_oAtv.getPosicao ()
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return (( l_tAnv [ 0 ] + l_dDstX, l_tAnv [ 1 ] + l_dDstY ))

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::menorDistancia
    #*  -------------------------------------------------------------------------------------------
    #*  encontra a menor distancia entre um ponto dado e os pontos no solo pre-definidos
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def menorDistancia ( self, f_tPto, f_bSinal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::menorDistancia"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #l_log.info ( "Ponto inicial: " + str ( f_tPto ))

        #** ---------------------------------------------------------------------------------------
        #*  inicia menor distancia encontrada (oo)
        #*/
        l_dMinDst = 999999999.

        #** ---------------------------------------------------------------------------------------
        #*  para todos os pontos no solo...
        #*/
        for l_iPNS in xrange ( len ( self._lstPontosNoSolo )):

            #l_log.info ( "Numero do ponto no solo: " + str ( l_iPNS ))

            #** -----------------------------------------------------------------------------------
            #*  obtem o ponto
            #*/
            l_oPNS = self._lstPontosNoSolo [ l_iPNS ]
            assert ( l_oPNS )

            #l_log.info ( "Ponto no solo: " + str ( l_oPNS._tPos  ))

            #** -----------------------------------------------------------------------------------
            #*/
            if ( f_bSinal ):

                #** -------------------------------------------------------------------------------
                #*  obtem a distancia euclidiana e o angulo entre os pontos
                #*/
                l_dDist, l_dDir = cineCalc.distanciaDirecao ( l_oPNS._tPos, f_tPto )

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtem a distancia euclidiana e o angulo entre os pontos
                #*/
                l_dDist, l_dDir = cineCalc.distanciaDirecao ( f_tPto, l_oPNS._tPos )

            #l_log.info ( "Distancia: " + str ( l_dDist ))
            #l_log.info ( "Direcao..: " + str ( l_dDir ))

            #** -----------------------------------------------------------------------------------
            #*  testa se a distancia eh maior que zero, pois a posicao atual pode estar localizada
            #*  em um ponto pre-definido no solo (o que pode ocorrer quando uma aeronave eh parada
            #*  durante um taxi, no ponto em que esta girando). Neste caso tal ponto nao deve ser
            #*  incluido no percurso
            #*/
            if (( l_dDist < l_dMinDst ) and ( l_dDist > 0. )):

                #** -------------------------------------------------------------------------------
                #*  salva a distancia calculada como a menor ate agora
                #*/
                l_dMinDst = l_dDist
                #l_log.info ( "achou menor distancia: " + str ( l_dMinDst ))

                #** -------------------------------------------------------------------------------
                #*  salva a direcao calculada
                #*/
                l_dMinDir = l_dDir
                #l_log.info ( "direcao..............: " + str ( l_dMinDir ))

                #** -------------------------------------------------------------------------------
                #*  salva a referencia ao ponto mais proximo
                #*/
                l_iMinPto = l_iPNS
                #l_log.info ( "numero do ponto......: " + str ( l_iMinPto ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna o segmento e o ponto mais perto
        #*/
        return (( l_dMinDst, l_dMinDir ), l_iMinPto )

    #** -------------------------------------------------------------------------------------------
    #*  menorDistanciaPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  1 - calcular o ponto previsto para parada, apos o pouso
    #*          2 - verificar qual dos pontos previstos para saida da pista esta mais perto do
    #*              ponto mencionado em (1)
    #*          3 - do item (2) conclui-se, tambem, qual o ponto no solo esta mais perto do ponto
    #*              mencionado em (1), uma vez que os pontos de saida da pista, no pouso, estao
    #*              sobre os pontos ja definidos no solo.
    #*          4 - o percurso inicial sera do ponto de parada da aeronave (1) ate o ponto no solo
    #*              mencionado em (3)
    #*  -------------------------------------------------------------------------------------------
    #*/
    def menorDistanciaPouso ( self, f_oAtv ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::menorDistanciaPouso"

        #/ distancia calculada
        #/ ----------------------------------------------------------------------------------------
        l_dMDst = 999999999.

        #/ direcao calculada
        #/ ----------------------------------------------------------------------------------------
        l_dMDir = 0.

        #/ indice do ponto
        #/ ----------------------------------------------------------------------------------------
        l_iMPto = 0

        #/ distancia calculada
        #/ ----------------------------------------------------------------------------------------
        l_dMinDst = 999999999.

        #/ direcao calculada
        #/ ----------------------------------------------------------------------------------------
        l_dMinDir = 0.


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = f_oAtv._tCktAtual [ 0 ]
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a pista
        #*/
        l_oPst = self._lstPst [ l_iPst ]
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira da pista
        #*/
        l_iCab = f_oAtv._tCktAtual [ 1 ]
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto de inicio da cabeceira da pista
        #*/
        l_tCabIni = l_oCab._tCabIni
        assert ( l_tCabIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direcao da cabeceira da pista
        #*/
        l_dCabDir = l_oCab._dCabDir

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto de parada apos o pouso da aeronave
        #*/
        l_tPto = self.calculaPontoParadaPouso ( f_oAtv, l_dCabDir )
        assert ( l_tPto )

        #** ---------------------------------------------------------------------------------------
        #*  salva o ponto de parada apos o pouso da aeronave
        #*/
        f_oAtv.setParadaPouso ( l_tPto )

        #** ---------------------------------------------------------------------------------------
        #*  inicia menor distancia encontrada (oo)
        #*/
        l_dMinDst = 999999999.

        #** ---------------------------------------------------------------------------------------
        #*  para todos os pontos de pouso...
        #*/
        for l_iI in xrange ( l_oCab.getCabQtdePontosArr ()):

            #** -----------------------------------------------------------------------------------
            #*  obtem o numero do ponto de pouso
            #*/
            l_iArr = l_oCab.getCabPontoArr ( l_iI )

            #** -----------------------------------------------------------------------------------
            #*  obtem o ponto no solo correspondente
            #*/
            l_tArr = self._lstPontosNoSolo [ l_iArr ]._tPos
            assert ( l_tArr )

            #** -----------------------------------------------------------------------------------
            #*  calcula a distancia e o angulo entre eles
            #*/
            l_dDist, l_dAng = cineCalc.distanciaDirecao ( l_tPto, l_tArr )

            #** -----------------------------------------------------------------------------------
            #*  checa se a distancia eh maior que zero, pois a posicao de parada de uma aeronave,
            #*  no pouso, pode estar localizada em um ponto pre-definido de saida de pista. Neste
            #*  caso tal ponto nao deve ser incluido no percurso
            #*/
            if (( l_dDist < l_dMinDst ) and ( l_dDist > 0. )):

                #** -------------------------------------------------------------------------------
                #*  calcula a distancia entre o ponto de parada e a cabeceira da pista
                #*/
                l_dCabDst = cineCalc.distanciaEntrePontos ( l_tPto, l_tCabIni )

                #** -------------------------------------------------------------------------------
                #*  garante que a aeronave retorne a um ponto de saida apenas quando passar pelo
                #*  ultimo ponto, isto e quando a aeronave para entre o ultimo ponto de saida de
                #*  pista e o inicio da cabeceira seguinte
                #*/
                if ( l_dCabDst <= l_oPst.getPstCmp ()):

                    #** ---------------------------------------------------------------------------
                    #*  salva a distancia calculada como a menor ate agora
                    #*/
                    l_dMDst = l_dDist

                    #** ---------------------------------------------------------------------------
                    #*  salva a direcao calculada
                    #*/
                    l_dMDir = l_dAng

                    #** ---------------------------------------------------------------------------
                    #*  salva a referencia ao ponto mais proximo
                    #*/
                    l_iMPto = l_iArr

                #** -------------------------------------------------------------------------------
                #*  evita pontos ja passados pela aeronave
                #*/
                if (( abs ( l_dAng - l_dCabDir ) < 10. ) or ( abs ( l_dAng - l_dCabDir ) > 350. )):

                    #** ---------------------------------------------------------------------------
                    #*  salva a distancia calculada como a menor ate agora
                    #*/
                    l_dMinDst = l_dDist

                    #** ---------------------------------------------------------------------------
                    #*  salva a direcao calculada
                    #*/
                    l_dMinDir = l_dAng

                    #** ---------------------------------------------------------------------------
                    #*  salva a referencia ao ponto mais proximo
                    #*/
                    l_iMinPto = l_iArr

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( 999999999. == l_dMinDst ):

            #** -----------------------------------------------------------------------------------
            #*  cria um trecho com a menor distancia e a direcao entre os pontos
            #*/
            l_tTrecho = ( l_dMDst, l_dMDir )
            assert ( l_tTrecho )

            #** -----------------------------------------------------------------------------------
            #*/
            l_iMinPto = l_iMPto

        #** ---------------------------------------------------------------------------------------
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  cria um trecho com a menor distancia e a direcao entre os pontos
            #*/
            l_tTrecho = ( l_dMinDst, l_dMinDir )
            assert ( l_tTrecho )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_tTrecho, l_iMinPto )

    #** -------------------------------------------------------------------------------------------
    #*  montaPercurso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montaPercurso ( self, f_iI, f_iJ ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::montaPercurso"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iI >= 0 ) and ( f_iI < locDefs.xMAX_PontosNoSolo ))
        assert (( f_iJ >= 0 ) and ( f_iJ < locDefs.xMAX_PontosNoSolo ))

        #l_log.info ( "monta percurso de [%d] ate [%d] iniciando em (%d)" % ( f_iI, f_iJ, f_iCont ))

        #** ---------------------------------------------------------------------------------------
        #*  cria um percurso
        #*/
        l_lstEtapa = []
        #assert ( l_lstEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  cria a primeira etapa do percurso
        #*/
        l_oEtapa = clsTrj.Etapa ( 0, ( 0., 0. ), ( 0., 0. ))
        assert ( l_oEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  insere no percurso
        #*/
        l_lstEtapa.append ( l_oEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  descobre o menor caminho entre os pontos
        #*/
        l_Path = shortestPath.shortestPath ( self._dicG, f_iI, f_iJ )

        #l_log.info ( "caminho de [%d] ate [%d]: [%s]" % ( f_iI, f_iJ, str ( l_Path )))

        #** ---------------------------------------------------------------------------------------
        #*  para cada um dos pontos do caminho descoberto...
        #*/
        for l_iP in l_Path:

            #** -----------------------------------------------------------------------------------
            #*  cria uma nova etapa no percurso
            #*/
            l_oEtapa = clsTrj.Etapa ( l_iP, ( 0., 0. ), ( 0., 0. ))
            assert ( l_oEtapa )

            #** -----------------------------------------------------------------------------------
            #*  transfere o menor caminho para o percurso
            #*/
            l_lstEtapa.append ( l_oEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_lstEtapa, len ( l_Path ))

    #** -------------------------------------------------------------------------------------------
    #*  montarPercurso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  o ponto de destino do taxi ja deve estar definido
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montarPercurso ( self, f_oAtv ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::montarPercurso"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave parada em pane ou parada ?
        #*/
        if ( f_oAtv.getStatusSolo () in [ 'G', 'P' ] ):

            #** -----------------------------------------------------------------------------------
            #*  obtem a posicao atual da aeronave
            #*/
            l_tAnv = f_oAtv.getPosicao ()
            assert ( l_tAnv )

            #** -----------------------------------------------------------------------------------
            #*  obtem a menor distancia entre a aeronave e qualquer ponto no solo pre-definido
            #*/
            l_tIni, l_iPart = self.menorDistancia ( l_tAnv, False )
            assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave em pouso
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  obtem a menor distancia entre a aeronave e qualquer ponto de saida
            #*/
            l_tIni, l_iPart = self.menorDistanciaPouso ( f_oAtv )
            assert ( l_tIni )

            #** -----------------------------------------------------------------------------------
            #*  obtem o ponto de parada apos o pouso
            #*/
            l_tAnv = f_oAtv.getParadaPouso ()
            assert ( l_tAnv )

        #l_log.info ( "Trecho de partida (Cmp): " + str ( l_tIni [ 0 ] ))
        #l_log.info ( "Trecho de partida (Dir): " + str ( l_tIni [ 1 ] ))
        #l_log.info ( "Trecho de partida (Pto): " + str ( l_iPart ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a menor distancia entre o ponto final do taxi desta aeronave e qualquer ponto no
        #*  solo pre-definido
        #*/
        l_tFim, l_iDest = self.menorDistancia ( f_oAtv.getTaxDestino (), True )
        assert ( l_tFim )

        #l_log.info ( "Trecho de destino(Cmp): " + str ( l_tFim [ 0 ] ))
        #l_log.info ( "Trecho de destino(Dir): " + str ( l_tFim [ 1 ] ))
        #l_log.info ( "Trecho de destino(Pto): " + str ( l_iDest ))

        #** -----------------------------------------------------------------------------------
        #*  monta o percurso entre o ponto de partida e o destino
        #*/
        l_lstEtapa, l_iCont = self.montaPercurso ( l_iPart, l_iDest )
        assert ( l_lstEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  salva a posicao da aeronave no primero ponto do percurso
        #*/
        l_lstEtapa [ 0 ]._tPos = l_tAnv
        assert ( l_lstEtapa [ 0 ]._tPos )

        #** ---------------------------------------------------------------------------------------
        #*  salva o trecho da aeronave ao primero ponto do percurso
        #*/
        l_lstEtapa [ 0 ]._tTrecho = l_tIni
        assert ( l_lstEtapa [ 0 ]._tTrecho )

        #** ---------------------------------------------------------------------------------------
        #*  salva o trecho do ultimo ponto do percurso ao ponto de destino do taxi
        #*/
        l_lstEtapa [ l_iCont ]._tTrecho = l_tFim
        assert ( l_lstEtapa [ l_iCont ]._tTrecho )

        #** ---------------------------------------------------------------------------------------
        #*  monta os dados do percurso obtido na estrutura
        #*/
        for l_iI in xrange ( 1, l_iCont ):

            #** -----------------------------------------------------------------------------------
            #*  obtem o numero do ponto
            #*/
            l_iP = l_lstEtapa [ l_iI ]._iPto
            #l_log.info ( "Numero do ponto.: " + str ( l_iP ))

            #** -----------------------------------------------------------------------------------
            #*  obtem o trecho
            #*/
            l_lstEtapa [ l_iI ]._tTrecho = self._oTrj.getTrecho ( l_iP, l_lstEtapa [ l_iI + 1 ]._iPto )
            assert ( l_lstEtapa [ l_iI ]._tTrecho )

            #l_log.info ( "Trecho (Cmp)....: " + str ( l_lstEtapa [ l_iI ]._tTrecho [ 0 ] ))
            #l_log.info ( "Trecho (Dir)....: " + str ( l_lstEtapa [ l_iI ]._tTrecho [ 1 ] ))

            #** -----------------------------------------------------------------------------------
            #*  posicao do ponto
            #*/
            l_lstEtapa [ l_iI ]._tPos = self._lstPontosNoSolo [ l_iP ]._tPos
            assert ( l_lstEtapa [ l_iI ]._tPos )

            #l_log.info ( "Posicao do ponto: " + str ( l_lstEtapa._tPos [ l_iI ] ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem o numero do ultimo ponto
        #*/
        l_iP = l_lstEtapa [ l_iCont ]._iPto
        #l_log.info ( "Numero do ultimo ponto.: " + str ( l_iP ))

        #** ---------------------------------------------------------------------------------------
        #*  posicao do ultimo ponto
        #*/
        l_lstEtapa [ l_iCont ]._tPos = self._lstPontosNoSolo [ l_iP ]._tPos
        assert ( l_lstEtapa [ l_iCont ]._tPos )

        #l_log.info ( "Posicao do ultimo ponto: " + str ( l_lstEtapa [ l_iCont ]._tPos ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem o numero do penultimo ponto do percurso
        #*/
        l_iAux = l_lstEtapa [ l_iCont - 1 ]._iPto
        #l_log.info ( "Numero do penultimo ponto.: " + str ( l_iAux ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a posicao do penultimo ponto
        #*/
        l_tAux = self._lstPontosNoSolo [ l_iAux ]._tPos
        assert ( l_tAux )

        #l_log.info ( "Posicao do penultimo ponto: " + str ( l_tAux ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distancia e o angulo ate o destino da aeronave
        #*/
        l_dDst, l_dDir = cineCalc.distanciaDirecao ( l_tAux, f_oAtv.getTaxDestino ())

        #** ---------------------------------------------------------------------------------------
        #*  verifica se o ultimo ponto deve ser eliminado do percurso, caso esteja entre o
        #*  penultimo ponto e o de destino
        #*/
        if (( l_dDst <= l_lstEtapa [ l_iCont - 1 ]._tTrecho [ 0 ] ) and
            ( abs ( int ( l_dDir - l_lstEtapa [ l_iCont ]._tTrecho [ 1 ] )) in locDefs.xSET_DifAngAceitaveis )):

            #** -----------------------------------------------------------------------------------
            #*  remove o ultimo ponto do percurso
            #*/
            del l_lstEtapa [ l_iCont ]
            
            #** -----------------------------------------------------------------------------------
            #*  decrementa contador de trechos
            #*/
            l_iCont -= 1

            #** -----------------------------------------------------------------------------------
            #*  segmento de trecho
            #*/
            l_lstEtapa [ l_iCont ]._tTrecho = ( l_dDst, l_dDir )
            assert ( l_lstEtapa [ l_iCont ]._tTrecho )

        #** ---------------------------------------------------------------------------------------
        #*  existem 1 ou mais trechos no percurso ?
        #*/
        if ( l_iCont >= 1 ):

            #** -----------------------------------------------------------------------------------
            #*  existem mais que 1 trecho no percurso ?
            #*/
            if ( l_iCont > 1 ):

                #** -------------------------------------------------------------------------------
                #*  obtem o numero do segundo ponto do percurso
                #*/
                l_iAux = l_lstEtapa [ 2 ]._iPto

                #** -------------------------------------------------------------------------------
                #*  obtem a posicao do ponto
                #*/
                l_tAux = self._lstPontosNoSolo [ l_iAux ]._tPos
                assert ( l_tAux )

                #** -------------------------------------------------------------------------------
                #*  calcula a distancia e o angulo da aeronave ate o 2* ponto
                #*/
                l_dDst, l_dDir = cineCalc.distanciaDirecao ( l_tAnv, l_tAux )

            #** -----------------------------------------------------------------------------------
            #*  senao, so existe 1 trecho no percurso
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtem a posicao de destino do taxi
                #*/
                l_tTax = f_oAtv.getTaxDestino ()
                assert ( l_tTax )

                #** -------------------------------------------------------------------------------
                #*  calcula a distancia e o angulo da aeronave ate o ponto de destino
                #*/
                l_dDst, l_dDir = cineCalc.distanciaDirecao ( l_tAnv, l_tTax )

            #** -----------------------------------------------------------------------------------
            #*  verifica se o primeiro ponto deve ser eliminado do percurso, caso esteja entre o
            #*  segundo ponto e o de partida
            #*/
            if (( l_dDst <= l_lstEtapa [ 1 ]._tTrecho [ 0 ] ) and
                ( abs ( int ( l_dDir - l_lstEtapa [ 0 ]._tTrecho [ 1 ] )) in locDefs.xSET_DifAngAceitaveis )):

                #** -------------------------------------------------------------------------------
                #*  remove a etapa do percurso
                #*/
                del l_lstEtapa [ 1 ]
                
                #** -------------------------------------------------------------------------------
                #*/
                l_lstEtapa [ 0 ]._tTrecho = ( l_dDst, l_dDir )
                assert ( l_lstEtapa [ 0 ]._tTrecho )

        #** ---------------------------------------------------------------------------------------
        #*  salva o percurso da aeronave
        #*/
        f_oAtv.setPercurso ( l_lstEtapa )

        #** ---------------------------------------------------------------------------------------
        #*/
        #for l_oEtapa in l_lstEtapa :

            #l_log.info ( "--------------" )
            #l_log.info ( "Percurso(Pto): " + str ( l_oEtapa._iPto ))
            #l_log.info ( "Percurso(Pos): " + str ( l_oEtapa._tPos ))
            #l_log.info ( "Percurso(Cmp): " + str ( l_oEtapa._tTrecho [ 0 ] ))
            #l_log.info ( "Percurso(Dir): " + str ( l_oEtapa._tTrecho [ 1 ] ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -----------------------------------------------------------------------------------------------
    #*  clsAer::montarPercursoAteCabeceira
    #*  -----------------------------------------------------------------------------------------------
    #*  define qual ponto de decolagem, referente a cabeceira em questao, esta mais perto da posicao
    #*  atual da aeronave. Tal ponto sera considerado como destino do taxi
    #*  -----------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -----------------------------------------------------------------------------------------------
    #*/
    def montarPercursoAteCabeceira ( self, f_oAtv, f_iPst, f_iCab ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::montarPercursoAteCabeceira"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oAtv )
        assert (( f_iPst >= 0 ) and ( f_iPst < locDefs.xMAX_Pistas ))
        assert (( f_iCab >= 0 ) and ( f_iCab < locDefs.xMAX_Cabeceiras ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a pista
        #*/
        l_oPst = self._lstPst [ f_iPst ]
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( f_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  inicia o ponto mais proximo (destino do taxi)
        #*/
        l_tTaxDst = None

        #** ---------------------------------------------------------------------------------------
        #*  inicia a menor distancia
        #*/
        l_dMinDst = 999999999.

        #** ---------------------------------------------------------------------------------------
        #*  obtem a posicao atual da aeronave
        #*/
        l_tAtv = f_oAtv.getPosicao ()
        assert ( l_tAtv )

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de pontos de decolagem da cabeceira
        #*/
        for l_tDep in l_oCab.getCabPontosDep ():

            #** ---------------------------------------------------------------------------------------
            #*  calcula a distancia e a direcao da aeronave ao ponto de decolagem
            #*/
            l_dDst = cineCalc.distanciaEntrePontos ( l_tDep, l_tAtv )

            #** ---------------------------------------------------------------------------------------
            #*  esta mais proximo que o anterior ?
            #*/
            if ( l_dDst < l_dMinDst ):

                #** ---------------------------------------------------------------------------------------
                #*  salva a distancia como a menor ate agora
                #*/
                l_dMinDst = l_dDst

                #** ---------------------------------------------------------------------------------------
                #*  salva o ponto como o ponto mais proximo
                #*/
                l_tTaxDst = l_tDep

        #** ---------------------------------------------------------------------------------------
        #*  salva o ponto mais proximo como destino do taxi
        #*/
        f_oAtv.setTaxDestino ( l_tTaxDst )

        #** ---------------------------------------------------------------------------------------
        #*  monta um percurso ate la
        #*/
        self.montarPercurso ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  rotinas de leitura da janela do aerodromo
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getJanelaComp
    #*  -------------------------------------------------------------------------------------------
    #*  comprimento do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getJanelaComp ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getJanelaComp"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._dComp )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getJanelaLarg
    #*  -------------------------------------------------------------------------------------------
    #*  largura do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getJanelaLarg ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getJanelaLarg"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._dLarg )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getJanelaXInf
    #*  -------------------------------------------------------------------------------------------
    #*  X da coordenada inferior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getJanelaXInf ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getJanelaXInf"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ----------------------------------------------------------------------------------------
        #*/
        return ( self._dXInf )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getJanelaYInf
    #*  -------------------------------------------------------------------------------------------
    #*  Y da coordenada inferior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getJanelaYInf ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getJanelaYInf"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._dYInf )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getJanelaXSup
    #*  -------------------------------------------------------------------------------------------
    #*  X da coordenada superior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getJanelaXSup ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getJanelaXSup"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._dXSup )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getJanelaYSup
    #*  -------------------------------------------------------------------------------------------
    #*  Y da coordenada superior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getJanelaYSup ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getJanelaYSup"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._dYSup )

    #** ===========================================================================================
    #*  rotinas de leitura dos parametros do aerodromo
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getAltitude
    #*  -------------------------------------------------------------------------------------------
    #*  altitude do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getAltitude ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getAltitude"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._uiAltitude )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getCentro
    #*  -------------------------------------------------------------------------------------------
    #*  o ponto central do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCentro ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getCentro"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._tCentro )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getDifDeclinacao
    #*  -------------------------------------------------------------------------------------------
    #*  diferenca da declinacao magnetica
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getDifDeclinacao ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getDifDeclinacao"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._iDifDeclinacao )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getFiguras
    #*  -------------------------------------------------------------------------------------------
    #*  as figuras do desenho
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getFiguras ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getFiguras"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstFig )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getPista
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPista ( self, f_iPst ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getPista"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstPst [ f_iPst ] )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getPistas
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPistas ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getPistas"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstPst )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getPontosNoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPontosNoSolo ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getPontosNoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstPontosNoSolo )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getQtdeFiguras
    #*  -------------------------------------------------------------------------------------------
    #*  quantidade de figuras no desenho
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getQtdeFiguras ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getQtdeFiguras"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( len ( self._lstFig ))

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getQtdePistas
    #*  -------------------------------------------------------------------------------------------
    #*  quantidade de pistas do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getQtdePistas ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getQtdePistas"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( len ( self._lstPst ))

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getQtdePontosNoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  quantidade de pistas do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getQtdePontosNoSolo ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getQtdePontosNoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( len ( self._lstPontosNoSolo ))

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::getTrj
    #*  -------------------------------------------------------------------------------------------
    #*  quantidade de pistas do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getTrj ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::getTrj"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._oTrj )

    #** ===========================================================================================
    #*  rotinas de configuracao da janela do aerodromo
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::setJanelaComp
    #*  -------------------------------------------------------------------------------------------
    #*  comprimento do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setJanelaComp ( self, f_dVal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::setJanelaComp"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dComp = f_dVal

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::setJanelaLarg
    #*  -------------------------------------------------------------------------------------------
    #*  largura do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setJanelaLarg ( self, f_dVal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::setJanelaLarg"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dLarg = f_dVal

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::setJanelaXInf
    #*  -------------------------------------------------------------------------------------------
    #*  X da coordenada inferior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setJanelaXInf ( self, f_dVal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::setJanelaXInf"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dXInf = f_dVal

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::setJanelaYInf
    #*  -------------------------------------------------------------------------------------------
    #*  Y da coordenada inferior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setJanelaYInf ( self, f_dVal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::setJanelaYInf"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dYInf = f_dVal

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::setJanelaXSup
    #*  -------------------------------------------------------------------------------------------
    #*  X da coordenada superior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setJanelaXSup ( self, f_dVal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::setJanelaXSup"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dXSup = f_dVal

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsAer::setJanelaYSup
    #*  -------------------------------------------------------------------------------------------
    #*  Y da coordenada superior do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setJanelaYSup ( self, f_dVal ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsAer::setJanelaYSup"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._dYSup = f_dVal

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "clsAer" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** -----------------------------------------------------------------------------------------------
#*  this is the bootstrap process
#*/
#if ( '__main__' == __name__ ):

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #logging.basicConfig ()

    #** -------------------------------------------------------------------------------------------
    #*
    #l_aer = clsAer ( "aer/SBBR" )
    #assert ( l_aer )

    #** -------------------------------------------------------------------------------------------
    #*
    #print "QtdeFiguras.....: [%d]" % ( l_aer.getQtdeFiguras ())
    #print "QtdePistas......: [%d]" % ( l_aer.getQtdePistas ())
    #print "QtdePontosNoSolo: [%d]" % ( l_aer.getQtdePontosNoSolo ())

#** ----------------------------------------------------------------------------------------------- *#
