#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# pSiPAR
# Copyright (c) 2008-2011, Milton Abrunhosa
# -------------------------------------------------------------------------------------------------
# Package..: control
# Classe...: controlManager
#
# Descrição: this class is the interface to SiCAD. It is based on pygame and SDL packages.
#            It draws the scope on the screen and handles all interaction with user.
# -------------------------------------------------------------------------------------------------
# Detalhes de Versão
# -------------------------------------------------------------------------------------------------
# mlabru   2008/fev  2.0  versão para Linux (2D)
# mlabru   2011/fev  3.0  versão para Linux (3D)
# -------------------------------------------------------------------------------------------------
# Detalhes de Alteração
# -------------------------------------------------------------------------------------------------
# mlabru   2008/jun  2.0  version started
# mlabru   2009/jun  2.09 release 09
# mlabru   2011/jan  2.11 release 11
# mlabru   2011/fev  3.0  version started
# -------------------------------------------------------------------------------------------------

# < imports >--------------------------------------------------------------------------------------

# python library
import sys
import threading
import time

# log4Py (logger)
import logging

# pyGame (biblioteca gráfica)
# from pygame.locals import *

# pSiPAR / control
import control.configManager as configManager

# pSiPAR / model
import model.glbDefs as glbDefs
import model.glbData as glbData

import model.locDefs as locDefs

# pSiPAR / view
import view.dialog.Tk.dlgConfirm as dlgConfirm

# pSiPAR / voip
# import voip.voipTalk as voipTalk

# < variáveis globais >----------------------------------------------------------------------------

# logging level
w_logLvl = logging.ERROR

# < class controlManager >-------------------------------------------------------------------------

class controlManager ( threading.Thread ):

    # ---------------------------------------------------------------------------------------------
    # controlManager::__init__
    # ---------------------------------------------------------------------------------------------
    def __init__ ( self, f_szCnfg = None ):

        """
        inicia o controle.

        @param  f_szCnfg : nome do arquivo de configuração.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::__init__" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # initialize super class
        threading.Thread.__init__ ( self )

        # verifica parâmetros de entrada
        if ( f_szCnfg is None ):

            # arquivo de configuração padrão
            f_szCnfg = "xACME.cfg"

        # carrega as opções de configuração
        l_cm = configManager.configManager ( f_szCnfg )
        # assert ( l_cm )

        # inicia a biblioteca de VoIP
        self._voip = None # voipTalk.voipTalk ()
        #assert ( self._voip )

        # cria os atributos de instância
        self._fc = None
        self._mm = None
        self._ns = None
        self._st = None
        self._vm = None

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # controlManager::cbkAcelera
    # ---------------------------------------------------------------------------------------------
    def cbkAcelera ( self, f_dFator ):

        """
        drive application.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::cbkAcelera" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # salva o fator de multiplicação da aceleração
        glbDefs.xTIM_Accel = f_dFator

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # controlManager::cbkTermina
    # ---------------------------------------------------------------------------------------------
    def cbkTermina ( self, f_bAsk = False, f_bPil = True ):

        """
        terminate application.

        @param  f_bAsk : DOCUMENT ME!
        @param  f_bPil : DOCUMENT ME!

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::cbkTermina" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # se estiver em modo full screen, não pergunta
        f_bAsk = f_bAsk and ( not glbDefs.xSCR_Full )

        # exibe dialogo de confirmação ?
        if ( f_bAsk ):

            # exibe dialogo de confirmação ?
            if ( not dlgConfirm.askConfirm ( locDefs.xTXT_Tit, " Termina ? " )):

                # m.poirot logger
                #l_log.debug ( "<<" )

                return

        # terminal de piloto ?
        if ( f_bPil ):

            # envia o aviso de fim de execução
            self._ns.sendCnfg ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                                str ( glbDefs.xMSG_Fim ))

        # termina a comunicação voip
        # self._voip.termTalk ()

        # termina a aplicação
        glbData.g_bKeepRun = False

        # aguarda as tasks terminarem
        time.sleep ( 2 )

        # cai fora
        sys.exit ()

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # controlManager::run
    # ---------------------------------------------------------------------------------------------
    def run ( self ):

        """
        drive application.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::run" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        return

    # ---------------------------------------------------------------------------------------------
    # controlManager::startTime
    # ---------------------------------------------------------------------------------------------
    def startTime ( self ):

        """
        drive application.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::startTime" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        return

    # =============================================================================================
    # acesso a área de dados do objeto
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    # controlManager::getFC
    # ---------------------------------------------------------------------------------------------
    def getFC ( self ):

        """
        returns the application model.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::getFC" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        # returns the application model
        return ( self._fc )

    # ---------------------------------------------------------------------------------------------
    # controlManager::getMM
    # ---------------------------------------------------------------------------------------------
    def getMM ( self ):

        """
        returns the application model.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::getMM" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        # returns the application model
        return ( self._mm )

    # ---------------------------------------------------------------------------------------------
    # controlManager::getNS
    # ---------------------------------------------------------------------------------------------
    def getNS ( self ):

        """
        returns the application view.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::getNS" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        # returns the application view
        return ( self._ns )

    # ---------------------------------------------------------------------------------------------
    # controlManager::getST
    # ---------------------------------------------------------------------------------------------
    def getST ( self ):

        """
        returns the application view.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::getST" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        # returns the application view
        return ( self._st )

    # ---------------------------------------------------------------------------------------------
    # controlManager::getVM
    # ---------------------------------------------------------------------------------------------
    def getVM ( self ):

        """
        returns the application view.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::getVM" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        # returns the application view
        return ( self._vm )

    # ---------------------------------------------------------------------------------------------
    # controlManager::getVoIP
    # ---------------------------------------------------------------------------------------------
    def getVoIP ( self ):

        """
        returns the application view.
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "controlManager::getVoIP" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( "><" )

        # returns the application voip
        return ( self._voip )

# < the end >-------------------------------------------------------------------------------------- #
