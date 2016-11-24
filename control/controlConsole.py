#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: controlConsole
#*
#*  Descrição: DOCUMENT ME!
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
import os
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
import control.flightConsole as flightConsole
import control.netManager as netManager
import control.simStats as simStats
import control.simTime as simTime

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.data as data
import model.modelConsole as modelConsole
import model.glbDefs as glbDefs
import model.glbData as glbData

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.dialog.Tk.configConsole as configConsole
import view.dialog.Tk.dlgConfirm as dlgConfirm
import view.viewConsole as viewConsole

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  controlConsole::controlConsole
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class controlConsole ( controlManager.controlManager ):

    #** -------------------------------------------------------------------------------------------
    #*  controlConsole::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the display
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "controlConsole::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a supercalss
        #*/
        controlManager.controlManager.__init__ ( self, "SiCAD.cfg" )

        #** ---------------------------------------------------------------------------------------
        #*  cria a janela de configuração
        #*/
        l_ce = configConsole.configConsole ()
        assert ( l_ce )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o canal de comunicação
        #*/
        l_bOk, l_iCanal = l_ce.startConfigPanel ()
        #l_log.info ( "l_iCanal: " + str ( l_iCanal ))

        #** ---------------------------------------------------------------------------------------
        #*  checa se está tudo bem ate agora...
        #*/
        if ( l_bOk ):

            #** -----------------------------------------------------------------------------------
            #*  cria o socket de recebimento de configuração
            #*/
            self._cl = netManager.netListener ( l_iCanal, True )
            assert ( self._cl )

            #** -----------------------------------------------------------------------------------
            #*  aguarda receber o nome do exercício
            #*/
            l_szNExe = self._cl.getExe ()
            assert ( l_szNExe )

            #l_log.info ( "l_szNExe: " + str ( l_szNExe ))

            #** -----------------------------------------------------------------------------------
            #*  monta o filepath do arquivo
            #*/
            l_szNExe = data.filepath ( os.path.join ( glbDefs.xDIR_EXE, l_szNExe [ 0 ] ))
            #l_log.info ( "l_szNExe: " + str ( l_szNExe ))

            #** -----------------------------------------------------------------------------------
            #*  instancia o modelo
            #*
            self._mm = modelConsole.modelConsole ()
            assert ( self._mm )

            #** -----------------------------------------------------------------------------------
            #*  carregou os arquivos na memória ?
            #*/
            if ( self._mm.iniciaBaseDados ( l_szNExe )):

                #** -------------------------------------------------------------------------------
                #*  cria o socket de recebimento de dados
                #*/
                self._dl = netManager.netListener ( l_iCanal )
                assert ( self._dl )

                #** -------------------------------------------------------------------------------
                #*  cria o pier de comunicação
                #*/
                #self._voip.addPier ( l_iCanal )

                #** -------------------------------------------------------------------------------
                #*  create simulation time engine
                #*/
                self._st = simTime.simTime ()
                assert ( self._st )

                #** -------------------------------------------------------------------------------
                #*  create flight control task
                #*/
                self._fc = flightConsole.flightConsole ( self )
                assert ( self._fc )

                #** -------------------------------------------------------------------------------
                #*  create view manager task
                #*
                self._vm = viewConsole.viewConsole ( self )
                assert ( self._vm )

                #** -------------------------------------------------------------------------------
                #*  create simulation statistics control
                #*/
                self._ss = simStats.simStats ()
                assert ( self._ss )

            #** -----------------------------------------------------------------------------------
            #*  senão, não conseguiu carregar os arquivos na memoria...
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                self._vm = None

        #** ---------------------------------------------------------------------------------------
        #*  senão, algo errado no paraíso...
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
    #*  controlConsole::run
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "controlConsole::run"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução (I)
        #*/
        if (( None == self._mm ) or ( None == self._vm )):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  termina a aplicação sem confirmação e sem envio de fim
            #*/
            self.cbkTermina ( False, False )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução (I)
        #*/
        assert ( self._cl )
        assert ( self._fc )
        assert ( self._mm )
        assert ( self._vm )

        #** ---------------------------------------------------------------------------------------
        #*  keep things running
        #*/
        glbData.g_bKeepRun = True

        #** ---------------------------------------------------------------------------------------
        #*  inicia o recebimento de mensagens de configuração
        #*/
        self._cl.start ()

        #** ---------------------------------------------------------------------------------------
        #*  starts flight control
        #*/
        self._fc.start ()

        #** ---------------------------------------------------------------------------------------
        #*  starts view manager (user interface)
        #*/
        self._vm.start ()

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
                    #*  termina a aplicação sem confirmação e sem envio de fim
                    #*/
                    self.cbkTermina ( False, False )

                #** -------------------------------------------------------------------------------
                #*  this is the keyboard control structure
                #*/
                elif ( KEYDOWN == l_evt.type ):

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants to terminate application
                    #*/
                    if ( K_ESCAPE == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  termina a aplicação sem confirmação e sem envio de fim
                        #*/
                        self.cbkTermina ( False, False )

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
                    #*  check if user wants toggle <C>ircuit
                    #*/
                    #elif ( K_c == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle circuito
                        #*/
                        #self._vm.cbkToggleCircuit ()

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants toggle range <M>ark
                    #*/
                    #elif ( K_m == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle range mark
                        #*/
                        #self._vm.cbkToggleRangeMark ()

                    #** ---------------------------------------------------------------------------
                    #*  check if user wants toggle rose <W>ind
                    #*/
                    #elif ( K_w == l_evt.key ):

                        #** -----------------------------------------------------------------------
                        #*  toggle rose wind
                        #*/
                        #self._vm.cbkToggleRoseWind ()

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

                #** -------------------------------------------------------------------------------
                #*  this is the mouse control structure
                #*/
                elif ( MOUSEBUTTONDOWN == l_evt.type ):

                    #** ---------------------------------------------------------------------------
                    #*  user pressed right button ?
                    #*/
                    if ( 1 == l_evt.button ):

                        #** -----------------------------------------------------------------------
                        #*  check if mouse position matches VoIP control
                        #*/
                        self._vm.cbkCheckVoIP ( l_evt.pos )

            #** -----------------------------------------------------------------------------------
            #*  obtem um item da queue de entrada
            #*/
            l_lstData = self._cl.getData ()
            #l_log.info ( "l_lstData: (%s)" % str ( l_lstData ))

            #** -----------------------------------------------------------------------------------
            #*  queue tem dados ?
            #*/
            if ( l_lstData ):

                #l_log.info ( "l_lstData [ 0 ]: (%s)" % str ( l_lstData [ 0 ] ))
  
                #** -------------------------------------------------------------------------------
                #*  mensagem de aceleração ?
                #*/
                if ( glbDefs.xMSG_Acc == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  acelera/desacelera a aplicação
                    #*/
                    self.cbkAcelera ( float ( l_lstData [ 1 ] ))

                #** -------------------------------------------------------------------------------
                #*  mensagem toggle circuit ?
                #*/
                elif ( glbDefs.xMSG_Ckt == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  liga/desliga circuito
                    #*/
                    self._vm.cbkToggleCircuit ()

                    #l_log.info ( "liga/desliga circuito" )

                #** -------------------------------------------------------------------------------
                #*  mensagem toggle call sign ?
                #*/
                elif ( glbDefs.xMSG_CSg == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  liga/desliga call-sign
                    #*/
                    self._vm.cbkToggleCallSign ()

                    #l_log.info ( "liga/desliga call-sign" )

                #** -------------------------------------------------------------------------------
                #*  mensagem de fim de execução ?
                #*/
                elif ( glbDefs.xMSG_Fim == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  termina a aplicação sem confirmação e sem envio de fim
                    #*/
                    self.cbkTermina ( False, False )

                #** -------------------------------------------------------------------------------
                #*  mensagem de congelamento ?
                #*/
                elif ( glbDefs.xMSG_Frz == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  freeze application
                    #*/
                    self._vm.cbkFreeze ( False )

                #** -------------------------------------------------------------------------------
                #*  mensagem toggle range mark ?
                #*/
                elif ( glbDefs.xMSG_RMk == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  liga/desliga range mark
                    #*/
                    self._vm.cbkToggleRangeMark ()

                    #l_log.info ( "liga/desliga range mark" )

                #** -------------------------------------------------------------------------------
                #*  mensagem de hora ?
                #*/
                elif ( glbDefs.xMSG_Tim == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  coloca a mensagem na queue
                    #*/
                    l_tHora = tuple ( int ( s ) for s in l_lstData [ 1 ][ 1 : -1 ].split ( ',' ))

                    #** ---------------------------------------------------------------------------
                    #*  coloca a mensagem na queue
                    #*/
                    self._st.setaHora ( l_tHora )

                #** -------------------------------------------------------------------------------
                #*  mensagem de descongelamento ?
                #*/
                elif ( glbDefs.xMSG_Ufz == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  defreeze application
                    #*/
                    self._vm.cbkDefreeze ( False )

                #** -------------------------------------------------------------------------------
                #*  mensagem toggle wind rose ?
                #*/
                elif ( glbDefs.xMSG_WRs == int ( l_lstData [ 0 ] )):

                    #** ---------------------------------------------------------------------------
                    #*  liga/desliga wind rose
                    #*/
                    self._vm.cbkToggleRoseWind ()

                    #l_log.info ( "liga/desliga wind rose" )

                #** -------------------------------------------------------------------------------
                #*  senão, mensagem não reconhecida ou não tratavél
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  pr[oxima mensagem
                    #*/
                    pass
                                        
            #** -----------------------------------------------------------------------------------
            #*  senão, aguarda um instante...
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtem o tempo final em segundos e calcula o tempo decorrido
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

    #** ===========================================================================================
    #*  acesso a area de dados do objeto
    #*/ ===========================================================================================

    #** -------------------------------------------------------------------------------------------
    #*  controlManager::getCL
    #*  -------------------------------------------------------------------------------------------
    #*  returns the configuration listener
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCL ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "controlManager::getCL"


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
        return ( self._cl )

    #** -------------------------------------------------------------------------------------------
    #*  controlManager::getDL
    #*  -------------------------------------------------------------------------------------------
    #*  returns the data listener
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getDL ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        l_szMetodo = "controlManager::getDL"


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
        return ( self._dl )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "controlConsole" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

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
    l_cc = controlConsole ()
    assert ( l_cc )

#** ----------------------------------------------------------------------------------------------- *#
