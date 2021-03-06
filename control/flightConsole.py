#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: flightConsole
#*
#*  Descrição: this is the actual flight control for SiCAD.
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/jun/20  version started
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

#/ Python library
#/ ------------------------------------------------------------------------------------------------
import sys
import time

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ SiCAD / control
#/ ------------------------------------------------------------------------------------------------
import control.flightControl as flightControl

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.clsFlt as clsFlt
import model.glbData as glbData
import model.glbDefs as glbDefs

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  flightConsole::flightConsole
#*  -----------------------------------------------------------------------------------------------
#*  the flight control class generates new flights and handles their movement. It has a list of
#*  flight objects holding all flights that are currently active. The flights are generated when
#*  activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
#*  been generated it is handed by the flight engine.
#*  -----------------------------------------------------------------------------------------------
#*/
class flightConsole ( flightControl.flightControl ):

    #** -------------------------------------------------------------------------------------------
    #*  flightConsole::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the app and prepares everything
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm - model manager
    #*  @param  f_st - simulation time
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "flightConsole::__init__"


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
        flightControl.flightControl.__init__ ( self, f_cm )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o configuration listener
        #*/
        self._cl = f_cm.getCL ()
        assert ( self._cl )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o data listener
        #*/
        self._dl = f_cm.getDL ()
        assert ( self._dl )

        #** ---------------------------------------------------------------------------------------
        #*  initialize the list for all active flights
        #*/
        self._lstFlight = {}

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightConsole::run
    #*  -------------------------------------------------------------------------------------------
    #*  checks whether it's time to created another flight
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "flightConsole::run"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  enquanto não inicia...
        #*/
        while ( not glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  aguarda 1 seg
            #*/
            time.sleep ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  inicia o recebimento de mensagens de dados
        #*/
        self._dl.start ()

        #** ---------------------------------------------------------------------------------------
        #*  loop
        #*/
        while ( glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  obtém um item da queue de entrada
            #*/
            l_lstData = self._dl.getData ()
            #l_log.info ( "l_lstData: (%s)" % str ( l_lstData ))

            #** -----------------------------------------------------------------------------------
            #*  queue tem dados ?
            #*/
            if ( l_lstData ):

                #** -------------------------------------------------------------------------------
                #*  mensagem de status de aeronave ?
                #*/
                if ( glbDefs.xMSG_Dat == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  coloca a mensagem na queue
                    #*/
                    #l_log.info ( "Callsign: (%s)" % str ( l_lstData [ 1 ] ))

                    #** ---------------------------------------------------------------------------
                    #*  trava a lista de vôos
                    #*/
                    glbData.g_lckFlight.acquire ()

                    #** ---------------------------------------------------------------------------
                    #*/
                    try:

                        #** -----------------------------------------------------------------------
                        #*  atualiza os dados da aeronave
                        #*/
                        self._lstFlight [ l_lstData [ 1 ] ] = clsFlt.clsFlt ( l_lstData [ 1: ] )
                        assert ( self._lstFlight [ l_lstData [ 1 ] ] )

                    #** ---------------------------------------------------------------------------
                    #*/
                    finally:

                        #** -----------------------------------------------------------------------
                        #*  libera a lista de vôos
                        #*/
                        glbData.g_lckFlight.release ()

                #** -------------------------------------------------------------------------------
                #*  mensagem de explosão de aeronave ?
                #*/
                elif ( glbDefs.xMSG_Exp == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  obtém os dados da explosão
                    #*/
                    l_tExplode = [ ( float ( l_lstData [ 1 ] ), float ( l_lstData [ 2 ] )),
                                       int ( l_lstData [ 3 ] ),   int ( l_lstData [ 4 ] ) ]
                    assert ( l_tExplode )

                    #l_log.info ( "Explode: (%s)" % str ( l_tExplode ))
                    
                    #** ---------------------------------------------------------------------------
                    #*  coloca na lista de explosoes
                    #*/
                    self._lstExplode.append ( l_tExplode )
                    
                #** -------------------------------------------------------------------------------
                #*  mensagem de eliminação de aeronave ?
                #*/
                elif ( glbDefs.xMSG_Kll == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  coloca a mensagem na queue
                    #*/
                    #l_log.info ( "Elimina: (%s)" % str ( l_lstData [ 1 ] ))

                    #** ---------------------------------------------------------------------------
                    #*  trava a lista de vôos
                    #*/
                    glbData.g_lckFlight.acquire ()

                    #** ---------------------------------------------------------------------------
                    #*/
                    try:

                        #** -----------------------------------------------------------------------
                        #*  aeronave está na lista ?
                        #*/
                        if ( self._lstFlight [ l_lstData [ 1 ] ] ):

                            #** -------------------------------------------------------------------
                            #*  retira a aeronave da lista
                            #*/
                            del self._lstFlight [ l_lstData [ 1 ] ]

                    #** ---------------------------------------------------------------------------
                    #*/
                    finally:

                        #** -----------------------------------------------------------------------
                        #*  libera a lista de vôos
                        #*/
                        glbData.g_lckFlight.release ()

                #** -------------------------------------------------------------------------------
                #*  senão, mensagem não reconhecida ou não tratada
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  próxima mensagem
                    #*/
                    pass
                                        
            #** -----------------------------------------------------------------------------------
            #*  senão, aguarda um instante...
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow

                #l_log.info ( "l_lDif....(E): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Evnt.(E): " + str ( glbDefs.xTIM_Evnt ))
                #l_log.info ( "Wait/Sleep(E): " + str ( glbDefs.xTIM_Evnt - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  esta adiantado ?
                #*/
                if ( glbDefs.xTIM_Evnt > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Evnt - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "flightConsole" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
