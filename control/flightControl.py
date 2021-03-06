#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: flightControl
#*
#*  Descricao: this is the actual flight control for SiCAD.
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/fev/12  versão 1.0 started
#*  mlabru   2008/abr/05  versão 2.0 started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versão
#*  -----------------------------------------------------------------------------------------------
#*  start    1997/fev/12  versão inicial
#*  2.0-0.1  2008/jun/20  versão para Linux
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ Python library
#/ ------------------------------------------------------------------------------------------------
import sys
import threading

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca gráfica)
#/ ------------------------------------------------------------------------------------------------
import pygame.mixer

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.glbData as glbData
import model.glbDefs as glbDefs

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  flightControl::flightControl
#*  -----------------------------------------------------------------------------------------------
#*  the flight control class generates new flights and handles their movement. It has a list of
#*  flight objects holding all flights that are currently active. The flights are generated when
#*  activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
#*  been generated it is handed by the flight engine.
#*  -----------------------------------------------------------------------------------------------
#*/
class flightControl ( threading.Thread ):

    #** -------------------------------------------------------------------------------------------
    #*  flightControl::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the app and prepares everything
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_cm - control manager
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightControl::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_cm )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a super classe
        #*/
        threading.Thread.__init__ ( self )

        #** ---------------------------------------------------------------------------------------
        #*  salva o control manager
        #*/
        self._cm = f_cm
        assert ( self._cm )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o modelo
        #*/
        self._mm = f_cm.getMM ()
        assert ( self._mm )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o relógio da simulação
        #*/
        self._st = f_cm.getST ()
        assert ( self._st )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o exercício
        #*/
        self._oExe = self._mm.getExercicio ()
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o tipo de exercício
        #*/
        l_szTExe = self._oExe.getTipoExe ()
        assert ( l_szTExe )

        #** ---------------------------------------------------------------------------------------
        #*  exercício de SiPAR ?
        #*/
        if ( "SiPAR" == l_szTExe ):

            #** -----------------------------------------------------------------------------------
            #*  não há o objeto aeródromo
            #*/
            self._oAer = None
            
        #** ---------------------------------------------------------------------------------------
        #*  senão, exercício de SiCAD
        #*/
        elif ( "SiCAD" == l_szTExe ):

            #** -----------------------------------------------------------------------------------
            #*  obtém o objeto aeródromo
            #*/
            self._oAer = self._mm.getAerodromo ()
            assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  senão, exercício desconhecido
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  não há o objeto aeródromo
            #*/
            self._oAer = None

        #** ---------------------------------------------------------------------------------------
        #*  cria a trava da lista de vôos
        #*/
        glbData.g_lckFlight = threading.Lock ()
        assert ( glbData.g_lckFlight )

        #** ---------------------------------------------------------------------------------------
        #*  import the sound files
        #*/
        self._sndAlert = pygame.mixer.Sound ( glbDefs.xSND_Alert )
        assert ( self._sndAlert )
        
        self._sndExplode = pygame.mixer.Sound ( glbDefs.xSND_Explode )
        assert ( self._sndExplode )

        #** ---------------------------------------------------------------------------------------
        #*  inicia variáveis de instância
        #*/
        self._ns = None

        #** ---------------------------------------------------------------------------------------
        #*  initialize the list for all explosions
        #*/
        self._lstExplode = []

        #** ---------------------------------------------------------------------------------------
        #*  initialize the list for all active flights
        #*/
        self._lstFlight = None

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightControl::run
    #*  -------------------------------------------------------------------------------------------
    #*  checks whether it's time to created another flight
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightControl::run"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return
        
    #** ===========================================================================================
    #*  acesso a área de dados da classe
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  flightControl::getListExplode
    #*  -------------------------------------------------------------------------------------------
    #*  returns the list of active flights
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getListExplode ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "flightControl::getListExplode"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna a lista de explosoes
        #*/
        return ( self._lstExplode )

    #** -------------------------------------------------------------------------------------------
    #*  flightControl::getListFlight
    #*  -------------------------------------------------------------------------------------------
    #*  returns the list of active flights
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getListFlight ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "flightControl::getListFlight"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna a lista de vôos ativos
        #*/
        return ( self._lstFlight )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "flightControl" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
