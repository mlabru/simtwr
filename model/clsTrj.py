#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: clsTrj
#*
#*  Descricao: this file is the clsTrj class of the SiCAD. The clsTrj class holds information about
#*             a trajetoria and holds the commands the exercicio has been given.
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

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineCalc as cineCalc
import model.locDefs as locDefs

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  clsTrj::Etapa
#*  -----------------------------------------------------------------------------------------------
#*  define Etapa como um ponto e um trecho em um percurso
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class Etapa:

    #** -------------------------------------------------------------------------------------------
    #*  Etapa::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to Etapa
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_iPto, f_tPos, f_tTrecho ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "Etapa::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  numero do ponto no solo
        #*/
        self._iPto = f_iPto

        #** ---------------------------------------------------------------------------------------
        #*  posicao x, y do ponto
        #*/
        self._tPos = f_tPos
        #assert ( self._tPos )

        #** ---------------------------------------------------------------------------------------
        #*  comprimento e direcao da etapa
        #*/
        self._tTrecho = f_tTrecho
        #assert ( self._tTrecho )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*  clsTrj::Caminho
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a Caminho
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class Caminho:

    #** -------------------------------------------------------------------------------------------
    #*  Caminho::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to Caminho
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "Caminho::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  menor distancia entre quaisquer dois pontos definidos no solo
        #*/
        self._dA = [[ x for x in xrange ( locDefs.xMAX_PontosNoSolo ) ] for x in xrange ( locDefs.xMAX_PontosNoSolo ) ]
        assert ( self._dA )

        #** ---------------------------------------------------------------------------------------
        #*  primeiro ponto a ser atingido no percurso i, j
        #*/
        self._iP = [[ x for x in xrange ( locDefs.xMAX_PontosNoSolo ) ] for x in xrange ( locDefs.xMAX_PontosNoSolo ) ]
        assert ( self._iP )

        #** ---------------------------------------------------------------------------------------
        #*  distancia e direcao entre todos os pontos adjacentes
        #*/
        self._oC = [[ x for x in xrange ( locDefs.xMAX_PontosNoSolo ) ] for x in xrange ( locDefs.xMAX_PontosNoSolo ) ]
        assert ( self._oC )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*  clsTrj::clsTrj
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a clsTrj
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class clsTrj:

    #** -------------------------------------------------------------------------------------------
    #*  clsTrj::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to scope and view
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_lstPontosNoSolo, f_dicG ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsTrj::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_lstPontosNoSolo )

        #** ---------------------------------------------------------------------------------------
        #*  define o caminho
        #*/
        self._oCaminho = None

        #** ---------------------------------------------------------------------------------------
        #*  zera as matrizes
        #*/
        self.iniciaMatrizes ()

        #** ---------------------------------------------------------------------------------------
        #*  monta a matriz de adjacencias
        #*/
        self.montaMatrizAdjacencias ( f_lstPontosNoSolo, f_dicG )

        #** ---------------------------------------------------------------------------------------
        #*  calcula o caminho mais curto entre dois pontos
        #*/
        self.montaMaisCurto ( len ( f_lstPontosNoSolo ))

        #** ---------------------------------------------------------------------------------------
        #*/
        #for x in f_dicG:

            #l_log.info ( "key: " + str ( x ) + " value: " + str ( f_dicG [ x ] ))

            #for y in f_dicG [ x ]:

                #l_log.info ( "distancia de: " + str ( x ) + " ate: " + str ( y ) + " = " + str ( f_dicG [ x ][ y ] ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsTrj::iniciaMatrizes
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def iniciaMatrizes ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsTrj::iniciaMatrizes"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  cria a estrutura de dados
        #*/
        self._oCaminho = Caminho ()
        assert ( self._oCaminho )

        #** ---------------------------------------------------------------------------------------
        #*  para todos os pontos no solo...
        #*/
        for l_iI in xrange ( locDefs.xMAX_PontosNoSolo ):

            #** -----------------------------------------------------------------------------------
            #*  para todos os pontos no solo...
            #*/
            for l_iJ in xrange ( locDefs.xMAX_PontosNoSolo ):

                #** -------------------------------------------------------------------------------
                #*  inicia a menor distancia entre dois pontos definidos no solo ( i, j )
                #*/
                self._oCaminho._dA [ l_iI ][ l_iJ ] = 0.

                #** -------------------------------------------------------------------------------
                #*  inicia primeiro ponto a ser atingido no percurso i, j
                #*/
                self._oCaminho._iP [ l_iI ][ l_iJ ] = 0

                #** -------------------------------------------------------------------------------
                #*  inicia distancia e direcao entre os pontos adjacentes
                #*/
                self._oCaminho._oC [ l_iI ][ l_iJ ] = ( 0., 0. )
                assert ( self._oCaminho._oC [ l_iI ][ l_iJ ] )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsTrj::montaMaisCurto
    #*  -------------------------------------------------------------------------------------------
    #*  monta a matriz A (contendo a menor distancia entre quaisquer dois pontos definidos no solo)
    #*  e a matriz P (contendo o primeiro ponto a ser atingido no percurso i, j )
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iLen - tamanho da lista de pontos no solo
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montaMaisCurto ( self, f_iLen ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsTrj::montaMaisCurto"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  percorre todos os pontos no solo
        #*/
        for l_iP in xrange ( f_iLen ):

            #** -----------------------------------------------------------------------------------
            #*  a distancia entre um ponto e ele mesmo eh zero
            #*/
            self._oCaminho._dA [ l_iP ][ l_iP ] = 0.

        #** ---------------------------------------------------------------------------------------
        #*  percorre todos os pontos no solo...
        #*/
        for l_iP in xrange ( f_iLen ):

            #** -----------------------------------------------------------------------------------
            #*  percorre todos os pontos no solo...
            #*/
            for l_iK in xrange ( f_iLen ):

                #** -------------------------------------------------------------------------------
                #*  percorre todos os pontos no solo...
                #*/
                for l_iJ in xrange ( f_iLen ):

                    #** ---------------------------------------------------------------------------
                    #*  calcula a soma dos caminhos
                    #*/
                    l_dN = self._oCaminho._dA [ l_iP ][ l_iK ] + self._oCaminho._dA [ l_iK ][ l_iJ ]

                    #** ---------------------------------------------------------------------------
                    #*  normaliza a soma dos caminhos
                    #*/
                    if ( l_dN > 999999999. ):

                        l_dN = 999999999.

                    #l_log.info ( "Caminho de [%d] ate [%d] e de [%d] ate [%d]: [%d]" % ( l_iP, l_iK, l_iK, l_iJ, l_lN ))

                    #** ---------------------------------------------------------------------------
                    #*  verifica se achou um caminho mais curto...
                    #*/
                    if ( l_dN < self._oCaminho._dA [ l_iP ][ l_iJ ] ):

                        #l_log.info ( "Achou mais curto entre [%d] e [%d]. Era %5.2f agora: %5.2f" % ( l_iP, l_iJ, self._oCaminho._dA [ l_iP ][ l_iJ ], l_dN ))

                        #** -----------------------------------------------------------------------
                        #*  salva a soma dos caminhos
                        #*/
                        self._oCaminho._dA [ l_iP ][ l_iJ ] = l_dN

                        #** -----------------------------------------------------------------------
                        #*  salva a posicao inicial do caminho
                        #*/
                        self._oCaminho._iP [ l_iP ][ l_iJ ] = l_iK
                        #l_log.info ( "self._oCaminho._iP: " + str ( l_iK ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsTrj::montaMatrizAdjacencias
    #*  -------------------------------------------------------------------------------------------
    #*  monta a matriz C, que contem a distancia e direcao entre todos os
    #*  pontos adjacentes.
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montaMatrizAdjacencias ( self, f_lstPontosNoSolo, f_dicG ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsTrj::montaMatrizAdjacencias"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  percorre todos os pontos no solo...
        #*/
        for l_iP in xrange ( len ( f_lstPontosNoSolo )):

            #** -----------------------------------------------------------------------------------
            #*  obtem um ponto no solo
            #*/
            l_oPtoSolo = f_lstPontosNoSolo [ l_iP ]
            assert ( l_oPtoSolo )
            #assert ( isinstance ( l_oPtoSolo, clsAer.PtoSolo ))

            #** -----------------------------------------------------------------------------------
            #*  percorre todos os pontos adjacentes ao ponto no solo
            #*/
            for l_iA in xrange ( len ( l_oPtoSolo._lstAdjacentes )):

                #** -------------------------------------------------------------------------------
                #*  obtem o ponto adjacente
                #*/
                l_iAdj = l_oPtoSolo._lstAdjacentes [ l_iA ]
                #l_log.info ( "Entre pontos [%d] e [%d]: " % ( l_iP, l_iAdj ))

                #** -------------------------------------------------------------------------------
                #*  obtem as coordenadas do ponto no solo
                #*/
                l_tPto = l_oPtoSolo._tPos
                assert ( l_tPto )

                #** -------------------------------------------------------------------------------
                #*  obtem as coordenadas do ponto adjacente
                #*/
                l_tAdj = f_lstPontosNoSolo [ l_iAdj ]._tPos
                assert ( l_tAdj )

                #** -------------------------------------------------------------------------------
                #*  calcula a distancia e o angulo entre eles
                #*/
                l_dDst, l_dDir = cineCalc.distanciaDirecao ( l_tPto, l_tAdj )

                #** -------------------------------------------------------------------------------
                #*  salva a distancia e direcao entre o ponto no solo e seu adjacente
                #*/
                self._oCaminho._oC [ l_iP ][ l_iAdj ] = ( l_dDst, l_dDir )
                #l_log.info ( "Distancia: " + str ( self._oCaminho._oC [ l_iP ][ l_iAdj ][ 0 ] ))
                #l_log.info ( "Direcao..: " + str ( self._oCaminho._oC [ l_iP ][ l_iAdj ][ 1 ] ))

                #** -------------------------------------------------------------------------------
                #*  salva a distancia entre o ponto no solo e seu adjacente
                #*/
                self._oCaminho._dA [ l_iP ][ l_iAdj ] = self._oCaminho._oC [ l_iP ][ l_iAdj ][ 0 ]

            #** -----------------------------------------------------------------------------------
            #*  percorre todos os pontos no solo...
            #*/
            for l_iK in xrange ( len ( f_lstPontosNoSolo )):

                #** -------------------------------------------------------------------------------
                #*  checa se nao existe conexao entre os pontos p, k
                #*/
                if ( 0. == self._oCaminho._oC [ l_iP ][ l_iK ][ 0 ] ):

                    #** ---------------------------------------------------------------------------
                    #*  caminho de comprimento infinito
                    #*/
                    self._oCaminho._oC [ l_iP ][ l_iK ] = ( 999999999., 999. ) # oo

                    #** ---------------------------------------------------------------------------
                    #*  caminho de comprimento infinito
                    #*/
                    self._oCaminho._dA [ l_iP ][ l_iK ] = 999999999. # oo

            #** -----------------------------------------------------------------------------------
            #*  distancia entre o ponto e ele mesmo
            #*/
            self._oCaminho._oC [ l_iP ][ l_iP ] = ( 0., 0. )

            #** -----------------------------------------------------------------------------------
            #*  distancia entre o ponto e ele mesmo
            #*/
            self._oCaminho._dA [ l_iP ][ l_iP ] = 0.

        #** ---------------------------------------------------------------------------------------
        #*  para todos os pontos no solo...
        #*/
        for l_keyX in f_dicG:

            #** -----------------------------------------------------------------------------------
            #*  para todos os ponto adjacentes a este ponto no solo...
            #*/
            for l_keyY in f_dicG [ l_keyX ]:

                #** -------------------------------------------------------------------------------
                #*  obtem as coordenadas do ponto no solo
                #*/
                l_tPto = f_lstPontosNoSolo [ l_keyX ]._tPos
                assert ( l_tPto )

                #l_log.info ( "Pto: " + str ( l_keyX ) + " pos: " + str ( l_tPto ))

                #** -------------------------------------------------------------------------------
                #*  obtem as coordenadas do ponto adjacente
                #*/
                l_tAdj = f_lstPontosNoSolo [ l_keyY ]._tPos
                assert ( l_tAdj )

                #l_log.info ( "Adj: " + str ( l_keyY ) + " pos: " + str ( l_tAdj ))

                #** -------------------------------------------------------------------------------
                #*  calcula a distancia entre eles
                #*/
                f_dicG [ l_keyX ][ l_keyY ] = cineCalc.distanciaEntrePontos ( l_tPto, l_tAdj )

                #** -------------------------------------------------------------------------------
                #*/
                #l_log.info ( "distancia de: " + str ( l_keyX ) +
                #                      " ate: " + str ( l_keyY ) +
                #                         " = " + str ( f_dicG [ l_keyX ][ l_keyY ] ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  rotinas de leitura da janela do aerodromo
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsTrj::getAtalho
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getAtalho ( self, f_iI, f_iJ ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsTrj::getAtalho"


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

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._oCaminho._iP [ f_iI ][ f_iJ ] )

    #** -------------------------------------------------------------------------------------------
    #*  clsTrj::getTrecho
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getTrecho ( self, f_iI, f_iJ ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsTrj::getTrecho"


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

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._oCaminho._oC [ f_iI ][ f_iJ ] )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "clsTrj" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** -----------------------------------------------------------------------------------------------
#*  this is the bootstrap process
#*/
if ( '__main__' == __name__ ):

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    logging.basicConfig ()

    #** -------------------------------------------------------------------------------------------
    #*
    #l_aer = clsTrj ( "aer/SBBR" )
    #assert ( l_aer )

#** ----------------------------------------------------------------------------------------------- *#
