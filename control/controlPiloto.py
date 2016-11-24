#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: controlPiloto
#*
#*  Descrição: DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/fev/12  version started
#*  mlabru   2008/fev/12  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versão
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
import sys
import time

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca gráfica)
#/ ------------------------------------------------------------------------------------------------
import pygame
from pygame.locals import *

#/ SiCAD / control
#/ ------------------------------------------------------------------------------------------------
import control.controlManager as controlManager
import control.flightPiloto as flightPiloto
import control.netManager as netManager
import control.simStats as simStats
import control.simTime as simTime

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.glbData as glbData
import model.glbDefs as glbDefs

import model.modelPiloto as modelPiloto

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.dialog.Tk.configPiloto as configPiloto
import view.dialog.Tk.dlgConfirm as dlgConfirm
import view.viewPiloto as viewPiloto

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  controlPiloto::controlPiloto
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class controlPiloto ( controlManager.controlManager ):

    #** -------------------------------------------------------------------------------------------
    #*  controlPiloto::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the display
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm - model manager
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "controlPiloto::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a super class
        #*/
        controlManager.controlManager.__init__ ( self, "SiCAD.cfg" )

        #** ---------------------------------------------------------------------------------------
        #*  cria a janela de configuração
        #*/
        l_ce = configPiloto.configPiloto ()
        assert ( l_ce )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o numero do exercicio a executar
        #*/
        l_bOk, l_szNExe, l_iCanal = l_ce.startConfigPanel ()

        #** ---------------------------------------------------------------------------------------
        #*  checa se esta tudo bem até agora...
        #*/
        if ( l_bOk and l_szNExe ):

            #** -----------------------------------------------------------------------------------
            #*  instancia o modelo
            #*
            self._mm = modelPiloto.modelPiloto ()
            assert ( self._mm )

            #** -----------------------------------------------------------------------------------
            #*  carrega os arquivos na memória
            #*/
            if ( self._mm.iniciaBaseDados ( l_szNExe )):

                #** -------------------------------------------------------------------------------
                #*  create simulation time engine
                #*/
                self._st = simTime.simTime ()
                assert ( self._st )

                #** -------------------------------------------------------------------------------
                #*  cria o socket de envio
                #*/
                self._ns = netManager.netSender ( l_iCanal )
                assert ( self._ns )

                #** -------------------------------------------------------------------------------
                #*  cria o pier de comunicação
                #*/
                #self._voip.addPier ( l_iCanal )

                #** -------------------------------------------------------------------------------
                #*  create flight control task
                #*/
                self._fc = flightPiloto.flightPiloto ( self )
                assert ( self._fc )

                #** -------------------------------------------------------------------------------
                #*  create view manager task
                #*
                self._vm = viewPiloto.viewPiloto ( self )
                assert ( self._vm )

                #** -------------------------------------------------------------------------------
                #*  create simulation statistics control
                #*/
                self._ss = simStats.simStats ()
                assert ( self._ss )

            #** -----------------------------------------------------------------------------------
            #*  não consegui carregar os arquivos na memoria
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                self._vm = None

        #** ---------------------------------------------------------------------------------------
        #*  algo errado no paraíso...
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            self._mm = None

            #** -----------------------------------------------------------------------------------
            #*/
            self._vm = None

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  controlPiloto::run
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "controlPiloto::run"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução (I)
        #*/
        if (( None == self._mm ) or ( None == self._vm )):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  termina a aplicação
            #*/
            self.cbkTermina ()

        #** ---------------------------------------------------------------------------------------
        #*  ativa o relogio da simulação
        #*/
        self.startTime ()

        #** ---------------------------------------------------------------------------------------
        #*  keep things running
        #*/
        glbData.g_bKeepRun = True

        #** ---------------------------------------------------------------------------------------
        #*  starts flight control
        #*/
        self._fc.start ()

        #** ---------------------------------------------------------------------------------------
        #*  starts view manager (user interface)
        #*/
        self._vm.start ()

        #** ---------------------------------------------------------------------------------------
        #*  obtem o controle do menu
        #*/
        l_guiApp = self._vm.getGuiApp ()
        assert ( l_guiApp )

        #** ---------------------------------------------------------------------------------------
        #*  no flight under control
        #*/
        l_oAtvCntrl = None

        #** ---------------------------------------------------------------------------------------
        #*  application loop
        #*/
        while ( glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  get all events
            #*/
            l_events = pygame.event.get ()

            #** -----------------------------------------------------------------------------------
            #*  trata cada um dos eventos
            #*/
            for l_evt in l_events:

                #** -------------------------------------------------------------------------------
                #*/
                #l_log.info ( "event: " + str ( l_evt ))

                #** -------------------------------------------------------------------------------
                #*  check if user quits
                #*/
                if ( QUIT == l_evt.type ):

                    #** ---------------------------------------------------------------------------
                    #*  termina a aplicação
                    #*/
                    self.cbkTermina ( True )

                #** -------------------------------------------------------------------------------
                #*  this is the keyboard control structure
                #*/
                elif ( KEYDOWN == l_evt.type ):

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to terminate application
                    #*/
                    if ( K_ESCAPE == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  termina a aplicação
                        #*/
                        self.cbkTermina ( True )

                    #** ---------------------------------------------------------------------------
                    #*  toggle controller's circuit exibhition
                    #*/
                    elif ( K_F1 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  envia o aviso de toggle controller's circuit exibhition
                        #*/
                        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                            str ( glbDefs.xMSG_Ckt ))

                        #l_log.info ( "envia o aviso de toggle circuit exibhition" )

                    #** ---------------------------------------------------------------------------
                    #*  toggle controller's call sign exibhition
                    #*/
                    elif ( K_F2 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  envia o aviso de toggle controller's call sign exibhition
                        #*/
                        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                            str ( glbDefs.xMSG_CSg ))
                        #l_log.info ( "envia o aviso de toggle call sign exibhition" )

                    #** ---------------------------------------------------------------------------
                    #*  toggle controller's range mark exibhition
                    #*/
                    elif ( K_F3 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  envia o aviso de toggle controller's range mark exibhition
                        #*/
                        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                            str ( glbDefs.xMSG_RMk ))

                        #l_log.info ( "envia o aviso de toggle range mark exibhition" )

                    #** ---------------------------------------------------------------------------
                    #*  toggle controller's wind rose exibhition
                    #*/
                    elif ( K_F4 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  envia o aviso de toggle controller's wind rose exibhition
                        #*/
                        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                            str ( glbDefs.xMSG_WRs ))

                        #l_log.info ( "envia o aviso de toggle wind rose exibhition" )

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to toggle voip communication
                    #*/
                    elif ( K_SPACE == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle voip communication
                        #*/
                        #self._voip.toggleTalk ()
                        pass

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to desaccelerate simulation
                    #*/
                    elif ( K_KP_DIVIDE == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*/
                        if ( glbDefs.xTIM_Accel > 1 ):

                            #** -------------------------------------------------------------------
                            #*/
                            assert ( self._ns )
                            assert ( self._st )

                            #** -------------------------------------------------------------------
                            #*  ajusta a hora da simulação
                            #*/
                            self._st.ajustaHora ( self._st.obtemHoraSim ())

                            #** -------------------------------------------------------------------
                            #*  desacelera a simulação
                            #*/
                            glbDefs.xTIM_Accel -= 1
                            #l_log.info ( "xTIM_Accel: " + str ( glbDefs.xTIM_Accel ))

                            #** -------------------------------------------------------------------
                            #*  envia o aviso de desaceleração
                            #*/
                            self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                                str ( glbDefs.xMSG_Acc ) + glbDefs.xMSG_Sep +
                                                str ( glbDefs.xTIM_Accel ))
                            
                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to accelerate simulation
                    #*/
                    elif ( K_KP_MULTIPLY == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*/
                        assert ( self._ns )
                        assert ( self._st )

                        #** -----------------------------------------------------------------------
                        #*  ajusta a hora da simulação
                        #*/
                        self._st.ajustaHora ( self._st.obtemHoraSim ())

                        #** -----------------------------------------------------------------------
                        #*  acelera a simulação
                        #*/
                        glbDefs.xTIM_Accel += 1
                        #l_log.info ( "xTIM_Accel: " + str ( glbDefs.xTIM_Accel ))

                        #** -----------------------------------------------------------------------
                        #*  envia o aviso de aceleração
                        #*/
                        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                            str ( glbDefs.xMSG_Acc ) + glbDefs.xMSG_Sep +
                                            str ( glbDefs.xTIM_Accel ))
                        
                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to change scale
                    #*/
                    elif ( K_1 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  muda a escala da aplicação
                        #*/
                        self._vm.cbkExeEscala ( 1 )

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to change scale
                    #*/
                    elif ( K_2 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  muda a escala da aplicação
                        #*/
                        self._vm.cbkExeEscala ( 2 )

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to change scale
                    #*/
                    elif ( K_3 == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  muda a escala da aplicação
                        #*/
                        self._vm.cbkExeEscala ( 3 )

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants <C>ongelar
                    #*/
                    elif ( K_c == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  freeze application
                        #*/
                        self.cbkFreeze ()

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants toggle cir<K>uit
                    #*/
                    elif ( K_k == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle circuito
                        #*/
                        self._vm.cbkToggleCircuit ()

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants toggle range <M>ark
                    #*/
                    elif ( K_m == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle range mark
                        #*/
                        self._vm.cbkToggleRangeMark ()

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants toggle rose <W>ind
                    #*/
                    elif ( K_w == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle rose wind
                        #*/
                        self._vm.cbkToggleRoseWind ()

                #** -------------------------------------------------------------------------------
                #*  this is the mouse control structure
                #*/
                elif ( MOUSEBUTTONDOWN == l_evt.type ):

                    #** ---------------------------------------------------------------------------
                    #*  user pressed right button ?
                    #*/
                    if ( 1 == l_evt.button ):

                        #l_log.info ( "l_evt(A): " + str ( l_evt ))
                        
                        #** -----------------------------------------------------------------------
                        #*  check if mouse position matches any flight positions
                        #*/
                        l_oAtvCntrl = self._vm.cbkSelectFlight ( l_evt.pos, True )

                        #l_log.info ( "l_evt(M): " + str ( l_evt ))

                        #** -----------------------------------------------------------------------
                        #*  none flight selected ?
                        #*/
                        if ( None == l_oAtvCntrl ):

                            #** -------------------------------------------------------------------
                            #*  check if mouse position matches VoIP control
                            #*/
                            self._vm.cbkCheckVoIP ( l_evt.pos )

                        #l_log.info ( "l_evt(D): " + str ( l_evt ))

                    #** ---------------------------------------------------------------------------
                    #*  user pressed left button ?
                    #*/
                    elif ( 3 == l_evt.button ):

                        #** -----------------------------------------------------------------------
                        #*  check if mouse position matches any flight positions
                        #*/
                        l_oAtvCntrl = self._vm.cbkSelectFlight ( l_evt.pos, False )

            #** -----------------------------------------------------------------------------------
            #*  trata os eventos
            #*/
            l_guiApp.run ( l_events )

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow

            #l_log.info ( "l_lDif....(E): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Evnt.(E): " + str ( glbDefs.xTIM_Evnt ))
            #l_log.info ( "Wait/Sleep(E): " + str ( glbDefs.xTIM_Evnt - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta adiantado ?
            #*/
            if ( glbDefs.xTIM_Evnt > l_lDif ):
                                                
                #l_log.info ( "Adiantado em: " + str ( glbDefs.xTIM_Evnt - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Evnt - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*/
        #self._ss.noProcFlights = fe.flightsProcessed

        #** ---------------------------------------------------------------------------------------
        #*/
        #self._ss.printScore ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  controlPiloto::cbkFreeze
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkFreeze ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "controlPiloto::cbkFreeze"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._ns )
        assert ( self._st )
        assert ( self._vm )

        #** ---------------------------------------------------------------------------------------
        #*  envia o aviso de congelamento
        #*/
        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                            str ( glbDefs.xMSG_Frz ))
        
        #** ---------------------------------------------------------------------------------------
        #*  obtem a hora atual
        #*/
        self._st.cbkCongela ()

        #** ---------------------------------------------------------------------------------------
        #*  pause application
        #*/
        self._vm.cbkFreeze ()

        #** ---------------------------------------------------------------------------------------
        #*  pause the app
        #*/
        while ( glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  obtem um unico evento da fila
            #*/
            l_event = pygame.event.wait ()
            #l_log.info ( "event(2): " + str ( l_event ))

            #** -----------------------------------------------------------------------------------
            #*  tecla pressionada ?
            #*/
            if ( KEYDOWN == l_event.type ):

                #** -------------------------------------------------------------------------------
                #*  <D>escongela ?
                #*/
                if ( K_d == l_event.key ):

                    #** ---------------------------------------------------------------------------
                    #*  cai fora...
                    #*/
                    break

        #** ---------------------------------------------------------------------------------------
        #*  envia o aviso de descongelamento
        #*/
        self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                            str ( glbDefs.xMSG_Ufz ))
        
        #** ---------------------------------------------------------------------------------------
        #*  continue application
        #*/
        self._vm.cbkDefreeze ()

        #** ---------------------------------------------------------------------------------------
        #*  restaura a hora
        #*/
        self._st.cbkDescongela ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  controlPiloto::startTime
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def startTime ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "controlPiloto::startTime"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._mm )
        assert ( self._st )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o exercício
        #*/
        l_oExe = self._mm.getExercicio ()
        assert ( l_oExe )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a hora de inicio do exercicio
        #*/
        l_tHora = l_oExe.getHora ()
        #l_log.info ( "l_tHora: " + str ( l_tHora ))

        #** ---------------------------------------------------------------------------------------
        #*  inicia o relógio da simulação
        #*/
        self._st.setaHora ( l_tHora )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a area de dados do objeto
    #*/ ===========================================================================================

    #** -------------------------------------------------------------------------------------------
    #*  controlManager::getNS
    #*  -------------------------------------------------------------------------------------------
    #*  returns the application view
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getNS ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "controlManager::getNS"


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
        #*  returns the application view
        #*/
        return ( self._ns )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "controlPiloto" )

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
    l_cm = controlPiloto ()
    assert ( l_cm )

#** ----------------------------------------------------------------------------------------------- *#
