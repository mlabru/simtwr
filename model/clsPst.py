#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SICAD
#*  Classe...: clsPst
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

import model.locDefs as locDefs
import model.glbDefs as glbDefs

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  clsPst::clsSeg
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a Segmento
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class clsSeg:

    #** -------------------------------------------------------------------------------------------
    #*  clsSeg::__init__
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
        #l_szMetodo = "clsSeg::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  proa do segmento
        #*/
        self._dSegProa = 0.0

        #** ---------------------------------------------------------------------------------------
        #*  direcao do segmento
        #*/
        self._dSegDir = 0.0

        #** ---------------------------------------------------------------------------------------
        #*  distancia do segmento
        #*/
        self._dSegDist = 0

        #** ---------------------------------------------------------------------------------------
        #*  numero do segmento
        #*/
        self._iSegNum = 0

        #** =======================================================================================
        #*  posicao
        #*  =======================================================================================
        #*/

        #** ---------------------------------------------------------------------------------------
        #*  ponto inicial do segmento
        #*/
        self._tSegIni = ( 0.0, 0.0 )

        #** ---------------------------------------------------------------------------------------
        #*  ponto final do segmento
        #*/
        self._tSegFim = ( 0.0, 0.0 )

        #** ---------------------------------------------------------------------------------------
        #*  coeficientes da reta que define o segmento ( ax + by + c = 0 )
        #*/
        self._tSegReta = ( 0.0, 0.0, 0.0 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*  clsPst::clsCkt
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a Segmento
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class clsCkt:

    #** -------------------------------------------------------------------------------------------
    #*  clsCkt::__init__
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
        #l_szMetodo = "clsCkt::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  lista de segmentos do circuito
        #*/
        self._lstCktSegs = []

        #** ---------------------------------------------------------------------------------------
        #*  cria todos os segmentos do circuito
        #*/
        for x in xrange ( locDefs.xMAX_Segmentos ):

            #** -----------------------------------------------------------------------------------
            #*  cria um segmento
            #*/
            l_oSeg = clsSeg ()
            assert ( l_oSeg )

            #** -----------------------------------------------------------------------------------
            #*  coloca na lista de segmentos do circuito
            #*/
            self._lstCktSegs.append ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsCkt::getCktSeg
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCktSeg ( self, f_iSeg ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCkt::getCktSeg"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iSeg >= 0 ) or ( f_iSeg < locDefs.xMAX_Segmentos ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstCktSegs [ f_iSeg ] )

    #** -------------------------------------------------------------------------------------------
    #*  clsCkt::getCktSegs
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCktSegs ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsCkt::getCktSeg"


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
        return ( self._lstCktSegs )

#** -----------------------------------------------------------------------------------------------
#*  clsPst::clsPst
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a clsPst
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class clsPst:

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::__init__
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
        #l_szMetodo = "clsPst::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  comprimento da pista
        #*/
        self._uiPstCmp = 0

        #** ---------------------------------------------------------------------------------------
        #*  lista de cabeceiras ( sempre 2 cabeceiras )
        #*/
        self._lstPstCabs = []

        #** ---------------------------------------------------------------------------------------
        #*  cria todos as cabeceiras ( sempre 2 cabeceiras )
        #*/
        for l_iCab in xrange ( locDefs.xMAX_Cabeceiras ):

            #** -----------------------------------------------------------------------------------
            #*  cria uma cabeceira
            #*/
            l_oCab = clsCab.clsCab ()
            assert ( l_oCab )

            #** -----------------------------------------------------------------------------------
            #*  coloca na lista de cabeceira
            #*/
            self._lstPstCabs.append ( l_oCab )

        #** ---------------------------------------------------------------------------------------
        #*  lista de circuitos
        #*/
        self._lstPstCkts = []

        #** ---------------------------------------------------------------------------------------
        #*  cria todos os circuitos
        #*/
        for l_iCkt in xrange ( locDefs.xMAX_Circuitos ):

            #** -----------------------------------------------------------------------------------
            #*  cria um circuito
            #*/
            l_oCkt = clsCkt ()
            assert ( l_oCkt )

            #** -----------------------------------------------------------------------------------
            #*  coloca na lista de circuitos
            #*/
            self._lstPstCkts.append ( l_oCkt )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::loadPista
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def loadPista ( self, f_iI, f_data ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::loadPista"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  comprimento da pista
        #*/
        self._uiPstCmp = int ( f_data [ f_iI ] )
        f_iI += 1

        #l_log.info ( "_uiComp: " + str ( self._uiPstCmp ))

        #** ---------------------------------------------------------------------------------------
        #*  para as duas cabeceiras desta pista...
        #*/
        for l_iC in xrange ( locDefs.xMAX_Cabeceiras ):

            #** -----------------------------------------------------------------------------------
            #*  obtem uma cabeceira
            #*/
            l_oCab = self._lstPstCabs [ l_iC ]
            assert ( l_oCab )
            assert ( isinstance ( l_oCab, clsCab.clsCab ))

            #** -----------------------------------------------------------------------------------
            #*  carrega os dados da cabeceira
            #*/
            f_iI = l_oCab.loadCab ( f_iI, f_data )
            #l_log.info ( "Cab: " + str ( self._lstPstCabs [ l_iC ] ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira 1
        #*/
        l_oCab0 = self._lstPstCabs [ 0 ]
        assert ( l_oCab0 )
        assert ( isinstance ( l_oCab0, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira 2
        #*/
        l_oCab1 = self._lstPstCabs [ 1 ]
        assert ( l_oCab1 )
        assert ( isinstance ( l_oCab1, clsCab.clsCab ))

        #** ----------------------------------------------------------------------------------------
        #*  a direcao da cabeceira deve ser lida em proa...
        #*/
        l_dDir = cineCalc.calcDirecao ( l_oCab0._tCabIni,
                                        l_oCab1._tCabIni )

        #** ----------------------------------------------------------------------------------------
        #*  ...e armazenada em direcao
        #*/
        l_oCab0._dCabDir = l_dDir
        #l_log.info ( "Direcao Cab [ 0 ]: " + str ( l_oCab0._dCabDir ))

        #** ----------------------------------------------------------------------------------------
        #*  calcula a cabeceira oposta
        #*/
        l_dDir += 180.0

        #** ----------------------------------------------------------------------------------------
        #*  normaliza a cabeceira
        #*/
        while ( l_dDir >= 360.0 ):

            l_dDir -= 360.0

        #** ----------------------------------------------------------------------------------------
        #*  armazena a direcao
        #*/
        l_oCab1._dCabDir = l_dDir
        #l_log.info ( "Direcao Cab [ 1 ]: " + str ( l_oCab1._dCabDir ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( f_iI )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::montaDirecaoDistanciaSegmento
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montaDirecaoDistanciaSegmento ( self, f_dDecl ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::montaDirecaoDistanciaSegmento"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  para todos os circuitos da pista...
        #*/
        for l_oCkt in self._lstPstCkts:

            #** -----------------------------------------------------------------------------------
            #*/
            assert ( l_oCkt )
            assert ( isinstance ( l_oCkt, clsCkt ))

            #** -----------------------------------------------------------------------------------
            #*  obtem a lista de segmentos do circuito
            #*/
            l_lstSeg = l_oCkt._lstCktSegs
            assert ( l_lstSeg )

            #** -----------------------------------------------------------------------------------
            #*  segmento 1
            #*/
            assert ( l_lstSeg [ 0 ] )
            assert ( isinstance ( l_lstSeg [ 0 ], clsSeg ))

            l_lstSeg [ 0 ]._dSegDir = self._lstPstCabs [ 1 ]._dCabDir
            #l_log.info ( "l_lstSeg [ 0 ]._dSegDir: " + str ( l_lstSeg [ 0 ]._dSegDir ))

            l_lstSeg [ 0 ]._dSegProa = cineCalc.convProa2Direcao (( l_lstSeg [ 0 ]._dSegDir, f_dDecl ))
            #l_log.info ( "l_lstSeg [ 0 ]._dSegProa: " + str ( l_lstSeg [ 0 ]._dSegProa ))

            l_lstSeg [ 0 ]._iSegNum  = 0
            #l_log.info ( "l_lstSeg [ 0 ]._iSegNum: " + str ( l_lstSeg [ 0 ]._iSegNum ))

            #** ----------------------------------------------------------------------------------------
            #*  segmento 2
            #*/
            assert ( l_lstSeg [ 1 ] )
            assert ( isinstance ( l_lstSeg [ 1 ], clsSeg ))

            l_lstSeg [ 1 ]._dSegDir  = ( self._lstPstCabs [ 1 ]._dCabDir + 90. ) % 360.
            #l_log.info ( "l_lstSeg [ 1 ]._dSegDir: " + str ( l_lstSeg [ 1 ]._dSegDir ))

            l_lstSeg [ 1 ]._dSegProa = cineCalc.convProa2Direcao (( l_lstSeg [ 1 ]._dSegDir, f_dDecl ))
            #l_log.info ( "l_lstSeg [ 1 ]._dSegProa: " + str ( l_lstSeg [ 1 ]._dSegProa ))

            l_lstSeg [ 1 ]._iSegNum  = 1
            #l_log.info ( "l_lstSeg [ 1 ]._iSegNum: " + str ( l_lstSeg [ 1 ]._iSegNum ))

            #** ----------------------------------------------------------------------------------------
            #*  segmento 3
            #*/
            assert ( l_lstSeg [ 2 ] )
            assert ( isinstance ( l_lstSeg [ 2 ], clsSeg ))

            l_lstSeg [ 2 ]._dSegDir  = self._lstPstCabs [ 0 ]._dCabDir
            #l_log.info ( "l_lstSeg [ 2 ]._dSegDir: " + str ( l_lstSeg [ 2 ]._dSegDir ))

            l_lstSeg [ 2 ]._dSegProa = cineCalc.convProa2Direcao (( l_lstSeg [ 2 ]._dSegDir, f_dDecl ))
            #l_log.info ( "l_lstSeg [ 2 ]._dSegProa: " + str ( l_lstSeg [ 2 ]._dSegProa ))

            l_lstSeg [ 2 ]._iSegNum  = 2
            #l_log.info ( "l_lstSeg [ 2 ]._iSegNum: " + str ( l_lstSeg [ 2 ]._iSegNum ))

            #** ----------------------------------------------------------------------------------------
            #*  segmento 4
            #*/
            assert ( l_lstSeg [ 3 ] )
            assert ( isinstance ( l_lstSeg [ 3 ], clsSeg ))

            l_lstSeg [ 3 ]._dSegDir  = ( self._lstPstCabs [ 0 ]._dCabDir + 90. ) % 360.
            #l_log.info ( "l_lstSeg [ 3 ]._dSegDir: " + str ( l_lstSeg [ 3 ]._dSegDir ))

            l_lstSeg [ 3 ]._dSegProa = cineCalc.convProa2Direcao (( l_lstSeg [ 3 ]._dSegDir, f_dDecl ))
            #l_log.info ( "l_lstSeg [ 3 ]._dSegProa: " + str ( l_lstSeg [ 3 ]._dSegProa ))

            l_lstSeg [ 3 ]._iSegNum  = 3
            #l_log.info ( "l_lstSeg [ 3 ]._iSegNum: " + str ( l_lstSeg [ 3 ]._iSegNum ))

            #** ----------------------------------------------------------------------------------------
            #*/
            l_lstSeg [ 0 ]._dSegDist = cineCalc.distanciaEntrePontos ( l_lstSeg [ 0 ]._tSegIni, l_lstSeg [ 1 ]._tSegIni )
            #l_log.info ( "l_lstSeg [ 0 ]._dSegDist: " + str ( l_lstSeg [ 0 ]._dSegDist ))

            l_lstSeg [ 1 ]._dSegDist = cineCalc.distanciaEntrePontos ( l_lstSeg [ 1 ]._tSegIni, l_lstSeg [ 2 ]._tSegIni )
            #l_log.info ( "l_lstSeg [ 1 ]._dSegDist: " + str ( l_lstSeg [ 1 ]._dSegDist ))

            l_lstSeg [ 2 ]._dSegDist = cineCalc.distanciaEntrePontos ( l_lstSeg [ 2 ]._tSegIni, l_lstSeg [ 3 ]._tSegIni )
            #l_log.info ( "l_lstSeg [ 2 ]._dSegDist: " + str ( l_lstSeg [ 2 ]._dSegDist ))

            l_lstSeg [ 3 ]._dSegDist = cineCalc.distanciaEntrePontos ( l_lstSeg [ 3 ]._tSegIni, l_lstSeg [ 0 ]._tSegIni )
            #l_log.info ( "l_lstSeg [ 3 ]._dSegDist: " + str ( l_lstSeg [ 3 ]._dSegDist ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::montaFinal
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montaFinal ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::montaFinal"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira 1
        #*/
        l_oCab0 = self._lstPstCabs [ 0 ]
        assert ( l_oCab0 )
        assert ( isinstance ( l_oCab0, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira 2
        #*/
        l_oCab1 = self._lstPstCabs [ 1 ]
        assert ( l_oCab1 )
        assert ( isinstance ( l_oCab1, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem os pontos iniciais das cabeceiras
        #*/
        l_tPto0 = l_oCab0._tCabIni
        l_tPto1 = l_oCab1._tCabIni

        #** ---------------------------------------------------------------------------------------
        #*  calcula os coeficientes da reta
        #*/
        l_dA = l_tPto1 [ 1 ] - l_tPto0 [ 1 ]
        l_dB = l_tPto0 [ 0 ] - l_tPto1 [ 0 ]

        l_dC = (( l_tPto1 [ 0 ] * l_tPto0 [ 1 ] ) - ( l_tPto0 [ 0 ] * l_tPto1 [ 1 ] ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direcao da cabeceira
        #*/
        l_dDirGr = l_oCab1._dCabDir
        #l_log.info ( "Dir Cab [1]: " + str ( l_dDirGr ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para radianos
        #*/
        l_dDirRd = math.radians ( l_dDirGr )
        #l_log.info ( "l_dDirRd: " + str ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  distancia de 3.5 NM da cabeceira
        #*/
        l_dDist = 3.5 * glbDefs.xCNV_NM2M
        #l_log.info ( "Dist da final em metros: " + str ( l_dDist ))


        #** ---------------------------------------------------------------------------------------
        #*  CALCULO DA FINAL DA CABECEIRA 1
        #*/
        #l_log.info ( "Cabeceira [0] X:[%d] e Y:[%d]" % ( l_oCab0._tCabIni [ 0 ], l_oCab0._tCabIni [ 1 ] ))

        #** ---------------------------------------------------------------------------------------
        #*  decompoem a distancia em X e Y
        #*/
        l_dX = l_dDist * math.cos ( l_dDirRd )
        l_dY = l_dDist * math.sin ( l_dDirRd )
        #l_log.info ( "Final X:[%d] e Y:[%d]" % ( l_dX, l_dY ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o ponto inicial da final
        #*/
        l_dX = l_oCab0._tCabIni [ 0 ] + l_dX
        l_dY = l_oCab0._tCabIni [ 1 ] + l_dY

        l_oCab0._tFinalIni = ( l_dX, l_dY )
        #l_log.info ( "Inicio da Final(0) ( X, Y ):" + str ( l_oCab0._tFinalIni ))

        #** ---------------------------------------------------------------------------------------
        #*  o fim da final eh o ponto de inicio da cabeceira
        #*/
        l_oCab0._tFinalFim = l_oCab0._tCabIni
        #l_log.info ( "Final da Final(0) ( X, Y ):" + str ( l_oCab0._tFinalFim ))

        #** ---------------------------------------------------------------------------------------
        #*  salva os coeficientes da reta
        #*/
        l_oCab0._tFinalReta = ( l_dA, l_dB, l_dC )
        #l_log.info ( "Coeficientes da Final(0) ( A, B, C ):" + str ( l_oCab0._tFinalReta ))


        #** ---------------------------------------------------------------------------------------
        #*  CALCULO DA FINAL DA CABECEIRA OPOSTA
        #*/
        #l_log.info ( "Cabeceira [1] X:[%d] e Y:[%d]" % ( l_oCab1._tCabIni [ 0 ], l_oCab1._tCabIni [ 1 ] ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direcao da cabeceira oposta
        #*/
        l_dDirGr = l_oCab0._dCabDir
        #l_log.info ( "Dir Cab [0]: " + str ( l_dDirGr ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para radianos
        #*/
        l_dDirRd = math.radians ( l_dDirGr )
        #l_log.info ( "l_dDirRd: " + str ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  decompoem a distancia em X e Y
        #*/
        l_dX = l_dDist * math.cos ( l_dDirRd )
        l_dY = l_dDist * math.sin ( l_dDirRd )
        #l_log.info ( "Final X:[%d] e Y:[%d]" % ( l_dX, l_dY ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o ponto inicial da final
        #*/
        l_dX = l_oCab1._tCabIni [ 0 ] + l_dX
        l_dY = l_oCab1._tCabIni [ 1 ] + l_dY

        l_oCab1._tFinalIni = ( l_dX, l_dY )
        #l_log.info ( "Inicio da Final(1) ( X, Y ):" + str ( l_oCab1._tFinalIni ))

        #** ---------------------------------------------------------------------------------------
        #*  o fim da final eh o ponto de inicio da cabeceira
        #*/
        l_oCab1._tFinalFim = l_oCab1._tCabIni
        #l_log.info ( "Final da Final(1) ( X, Y ):" + str ( l_oCab1._tFinalFim ))

        #** ---------------------------------------------------------------------------------------
        #*  salva os coeficientes da reta
        #*/
        l_oCab1._tFinalReta = ( l_dA, l_dB, l_dC )
        #l_log.info ( "Coeficientes da Final(1) ( A, B, C ):" + str ( l_oCab1._tFinalReta ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::montaCircuito
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def montaCircuito ( self, f_iCkt ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::montaCircuito"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iCkt >= 0 ) and ( f_iCkt < locDefs.xMAX_Circuitos ))
        #l_log.info ( "Circuito: " + str ( f_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito 0
        #*/
        if ( 0 == f_iCkt ):

            #** -----------------------------------------------------------------------------------
            #*/
            l_dDist = locDefs.xCKT_Dist11
            l_dTeta = locDefs.xCKT_Teta11

        #** ---------------------------------------------------------------------------------------
        #*  circuito 1
        #*/
        elif ( 1 == f_iCkt ):

            #** -----------------------------------------------------------------------------------
            #*/
            l_dDist = locDefs.xCKT_Dist12
            l_dTeta = locDefs.xCKT_Teta12

        #** ---------------------------------------------------------------------------------------
        #*  circuito 2
        #*/
        elif ( 2 == f_iCkt ):

            #** -----------------------------------------------------------------------------------
            #*/
            l_dDist = locDefs.xCKT_Dist13
            l_dTeta = locDefs.xCKT_Teta13

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira 1
        #*/
        l_oCab0 = self._lstPstCabs [ 0 ]
        assert ( l_oCab0 )
        assert ( isinstance ( l_oCab0, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira 2
        #*/
        l_oCab1 = self._lstPstCabs [ 1 ]
        assert ( l_oCab1 )
        assert ( isinstance ( l_oCab1, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a lista de segmentos do circuito
        #*/
        l_lstSeg = self._lstPstCkts [ f_iCkt ]._lstCktSegs
        assert ( l_lstSeg )

        #l_log.info ( "l_lstSeg: " + str ( l_lstSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direcao da cabeceira
        #*/
        l_dDirGr = l_oCab0._dCabDir
        #l_log.info ( "l_dDirGr: " + str ( l_dDirGr ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para radianos
        #*/
        l_dDirRd = math.radians ( l_dDirGr + l_dTeta )
        #l_log.info ( "l_dDirRd: " + str ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao inicial do segmento
        #*/
        l_tPto1 = l_oCab1._tCabIni
        assert ( l_tPto1 )

        l_dPtoX = l_tPto1 [ 0 ] + ( l_dDist * math.cos ( l_dDirRd ))
        l_dPtoY = l_tPto1 [ 1 ] + ( l_dDist * math.sin ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento 0
        #*/
        l_lstSeg [ 0 ]._tSegIni = ( l_dPtoX, l_dPtoY )
        #l_log.info ( "_tSegIni: " + str ( l_lstSeg [ 0 ]._tSegIni ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para radianos
        #*/
        l_dDirRd = math.radians ( l_dDirGr - l_dTeta )
        #l_log.info ( "l_dDirRd: " + str ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao inicial do segmento
        #*/
        l_tPto4 = l_oCab1._tCabIni
        assert ( l_tPto4 )

        l_dPtoX = l_tPto4 [ 0 ] + ( l_dDist * math.cos ( l_dDirRd ))
        l_dPtoY = l_tPto4 [ 1 ] + ( l_dDist * math.sin ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento 3
        #*/
        l_lstSeg [ 3 ]._tSegIni = ( l_dPtoX, l_dPtoY )
        #l_log.info ( "_tSegIni: " + str ( l_lstSeg [ 3 ]._tSegIni ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direcao da cabeceira oposta
        #*/
        l_dDirGr = l_oCab1._dCabDir
        #l_log.info ( "l_dDirGr: " + str ( l_dDirGr ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para radianos
        #*/
        l_dDirRd = math.radians ( l_dDirGr - l_dTeta )
        #l_log.info ( "l_dDirRd: " + str ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao inicial do segmento
        #*/
        l_tPto2 = l_oCab0._tCabIni
        assert ( l_tPto2 )

        l_dPtoX = l_tPto2 [ 0 ] + ( l_dDist * math.cos ( l_dDirRd ))
        l_dPtoY = l_tPto2 [ 1 ] + ( l_dDist * math.sin ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento 1
        #*/
        l_lstSeg [ 1 ]._tSegIni = ( l_dPtoX, l_dPtoY )
        #l_log.info ( "_tSegIni: " + str ( l_lstSeg [ 1 ]._tSegIni ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para radianos
        #*/
        l_dDirRd = math.radians ( l_dDirGr + l_dTeta )
        #l_log.info ( "l_dDirRd: " + str ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao inicial do segmento
        #*/
        l_tPto3 = l_oCab0._tCabIni
        assert ( l_tPto3 )

        l_dPtoX = l_tPto3 [ 0 ] + ( l_dDist * math.cos ( l_dDirRd ))
        l_dPtoY = l_tPto3 [ 1 ] + ( l_dDist * math.sin ( l_dDirRd ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento 2
        #*/
        l_lstSeg [ 2 ]._tSegIni = ( l_dPtoX, l_dPtoY )
        #l_log.info ( "_tSegIni: " + str ( l_lstSeg [ 2 ]._tSegIni ))

        #** ---------------------------------------------------------------------------------------
        #*  conecta o final dos segmentos ao inicio do segmento seguinte
        #*/
        l_lstSeg [ 0 ]._tSegFim = l_lstSeg [ 1 ]._tSegIni
        #l_log.info ( "_tSegFim: " + str ( l_lstSeg [ 0 ]._tSegFim ))

        l_lstSeg [ 1 ]._tSegFim = l_lstSeg [ 2 ]._tSegIni
        #l_log.info ( "_tSegFim: " + str ( l_lstSeg [ 1 ]._tSegFim ))

        l_lstSeg [ 2 ]._tSegFim = l_lstSeg [ 3 ]._tSegIni
        #l_log.info ( "_tSegFim: " + str ( l_lstSeg [ 2 ]._tSegFim ))

        l_lstSeg [ 3 ]._tSegFim = l_lstSeg [ 0 ]._tSegIni
        #l_log.info ( "_tSegFim: " + str ( l_lstSeg [ 3 ]._tSegFim ))

        #** ---------------------------------------------------------------------------------------
        #*  para todos os segmentos...
        #*/
        for l_iSeg in xrange ( locDefs.xMAX_Segmentos ):

            #** -----------------------------------------------------------------------------------
            #*  obtem as posicoes inicial e final do segmento
            #*/
            l_tPto1 = l_lstSeg [ l_iSeg ]._tSegIni
            l_tPto2 = l_lstSeg [ l_iSeg ]._tSegFim

            #** -----------------------------------------------------------------------------------
            #*  calcula os coeficientes da reta
            #*/
            l_dA = l_tPto2 [ 1 ] - l_tPto1 [ 1 ]
            #l_log.info ( "A: %f - %f = %f" % ( l_tPto2 [ 1 ], l_tPto1 [ 1 ], l_dA ))

            l_dB = l_tPto1 [ 0 ] - l_tPto2 [ 0 ]
            #l_log.info ( "B: %f - %f = %f" % ( l_tPto1 [ 0 ], l_tPto2 [ 0 ], l_dB ))

            l_dC = (( l_tPto2 [ 0 ] * l_tPto1 [ 1 ] ) - ( l_tPto1 [ 0 ] * l_tPto2 [ 1 ] ))
            #l_log.info ( "C: (%f * %f) - (%f * %f) = %f" % ( l_tPto2 [ 0 ], l_tPto1 [ 1 ], l_tPto1 [ 0 ], l_tPto2 [ 1 ], l_dC ))

            #** -----------------------------------------------------------------------------------
            #*  salva a reta
            #*/
            l_lstSeg [ l_iSeg ]._tSegReta = ( l_dA, l_dB, l_dC )
            #l_log.info ( "_tSegReta: " + str ( l_lstSeg [ l_iSeg ]._tSegReta ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  rotinas de acesso a area de dados
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::getPstCab
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPstCab ( self, f_iCab ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::getPstCab"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iCab >= 0 ) or ( f_iCab < locDefs.xMAX_Cabeceiras ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstPstCabs [ f_iCab ] )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::getPstCabs
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPstCabs ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::getPstCabs"


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
        return ( self._lstPstCabs )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::getPstCkt
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPstCkt ( self, f_iCkt ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::getPstCkt"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iCkt >= 0 ) or ( f_iCkt < locDefs.xMAX_Circuitos ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self._lstPstCkts [ f_iCkt ] )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::getPstCkts
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPstCkts ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::getPstCkts"


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
        return ( self._lstPstCkts )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::getPstCmp
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getPstCmp ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::getPstCmp"


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
        return ( self._uiPstCmp )

    #** -------------------------------------------------------------------------------------------
    #*  clsPst::getQtdeCabs
    #*  -------------------------------------------------------------------------------------------
    #*  quantidade de pistas do aerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getQtdeCabs ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "clsPst::getQtdeCabs"


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
        return ( len ( self._lstPstCabs ))

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "clsPst" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** ----------------------------------------------------------------------------------------------- *#
