#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SICAD
#*  Classe...: clsCab
#*
#*  Descricao: this file is the clsPst class of the SiCAD.
#*             The clsPst class holds information about a exercicio
#*             and holds the commands the exercicio has been given.
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
import model.locDefs as locDefs

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  clsCab::clsCab
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a clsCab
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class clsCab:

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  nome da cabeceira
        #*/
        self._szCabNome = ""

        #** ---------------------------------------------------------------------------------------
        #*  ponto de inicio da cabeceira
        #*/
        self._tCabIni = ( 0., 0. )

        #** ---------------------------------------------------------------------------------------
        #*  a posicao da cabeceira que sera usada para montagem dos circuitos e para pouso
        #*/
        #self._tCabArr = ( 0., 0. )

        #** ---------------------------------------------------------------------------------------
        #*  a direcao da cabeceira deve ser lida em proa e armazenada em direcao
        #*/
        self._dCabDir = 0.

        #** ---------------------------------------------------------------------------------------
        #*  posicao dos pontos de entrada na pista
        #*/
        self._lstCabPontosDep = []

        #** ---------------------------------------------------------------------------------------
        #*  os pontos de saida da pista no pouso ( PosPontosArr ), devem ter a mesma posicao de
        #*  pontos definidos no solo. Assim, basta fornecer o numero dos pontos no solo
        #*/
        self._lstCabPontosArr = []

        #** =======================================================================================
        #*  FINAL
        #*  =======================================================================================
        #*/

        #** ---------------------------------------------------------------------------------------
        #*  ponto de inicio da final
        #*/
        self._tFinalIni = ( 0., 0. )

        #** ---------------------------------------------------------------------------------------
        #*  ponto final da final
        #*/
        self._tFinalFim = ( 0., 0. )

        #** ---------------------------------------------------------------------------------------
        #*  equacao da reta ( ax + by + c = 0 )
        #*/
        self._tFinalReta = ( 0., 0., 0. )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::loadCab
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def loadCab ( self, f_iI, f_data ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::loadCab"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  nome/numero da cabeceira
        #*/
        self._szCabNome = str ( f_data [ f_iI ] ).upper ()
        f_iI += 1

        #l_log.info ( "_szCabNome: " + self._szCabNome )

        #** ---------------------------------------------------------------------------------------
        #*  posicao da cabeceira
        #*/
        l_dX = float ( f_data [ f_iI ] )
        f_iI += 1

        l_dY = float ( f_data [ f_iI ] )
        f_iI += 1

        self._tCabIni = ( l_dX, l_dY )
        #l_log.info ( "_tCabIni: " + str ( self._tCabIni ))

        #** ---------------------------------------------------------------------------------------
        #*  numero de pontos de decolagem (entrada na pista)
        #*/
        l_iNumPontosDep = int ( f_data [ f_iI ] )
        f_iI += 1

        #l_log.info ( "_btNumPontosDep: " + str ( l_iNumPontosDep ))
        assert ( l_iNumPontosDep <= locDefs.xMAX_PontosDep )

        #** ---------------------------------------------------------------------------------------
        #*  para todos os pontos de decolagem...
        #*/
        for l_iD in xrange ( l_iNumPontosDep ):

            #** -----------------------------------------------------------------------------------
            #*  posicao do ponto de decolagem
            #*/
            l_dX = float ( f_data [ f_iI ] )
            f_iI += 1

            l_dY = float ( f_data [ f_iI ] )
            f_iI += 1

            #** -----------------------------------------------------------------------------------
            #*  salva o ponto na lista
            #*/
            self._lstCabPontosDep.append (( l_dX, l_dY ))
            #l_log.info ( "PontosDep: " + str ( self._lstCabPontosDep [ l_iD ] ))

        #l_log.info ( "_lstCabPontosDep: " + str ( self._lstCabPontosDep ))

        #** ---------------------------------------------------------------------------------------
        #*  numero de pontos de pouso (saida da pista)
        #*/
        l_iNumPontosArr = int ( f_data [ f_iI ] )
        f_iI += 1

        #l_log.info ( "_iNumPontosArr: " + str ( l_iNumPontosArr ))
        assert ( l_iNumPontosArr <= locDefs.xMAX_PontosArr )

        #** ---------------------------------------------------------------------------------------
        #*  para cada um dos pontos de pouso...
        #*/
        for l_iP in xrange ( l_iNumPontosArr ):

            #** -----------------------------------------------------------------------------------
            #*  ...obtem a posicao posicao dos pontos de saida da pista
            #*/
            l_iPto = int ( f_data [ f_iI ] ) - 1
            f_iI += 1

            #** -----------------------------------------------------------------------------------
            #*  salva o ponto na lista
            #*/
            self._lstCabPontosArr.append ( l_iPto )
            #l_log.info ( "PontoPouso: " + str ( self._lstCabPontosArr [ l_iP ] ))

        #l_log.info ( "_lstCabPontosArr: " + str ( self._lstCabPontosArr ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( f_iI )

    #** ===========================================================================================
    #*  rotinas de acesso a area de dados
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabDir
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabDir ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabDir"


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
        return ( self._dCabDir )

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabIni
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabIni ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabIni"


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
        return ( self._tCabIni )

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabNome
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabNome ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabNome"


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
        return ( self._szCabNome )

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabQtdePontosArr
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabQtdePontosArr ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabQtdePontosArr"


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
        return ( len ( self._lstCabPontosArr ))

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabQtdePontosDep
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabQtdePontosDep ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabQtdePontosDep"


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
        return ( len ( self._lstCabPontosDep ))

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabPontoArr
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabPontoArr ( self, f_iPto ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabPontoArr"


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
        return ( self._lstCabPontosArr [ f_iPto ] )

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabPontosArr
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabPontosArr ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabPontosArr"


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
        return ( self._lstCabPontosArr )

    #** -------------------------------------------------------------------------------------------
    #*  clsCab::getCabPontosDep
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCabPontosDep ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCab::getCabPontosDep"


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
        return ( self._lstCabPontosDep )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "clsCab" )

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

#** ----------------------------------------------------------------------------------------------- *#
