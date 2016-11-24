#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: viewConsole
#*
#*  Descrição: this class takes care of all interaction with the user. It has been designed so that
#*             it can be directly linked to an AI.
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/jun/20  version started
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

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.glbData as glbData

import model.glbDefs as glbDefs
import model.locDefs as locDefs

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.guiIMet as guiIMet
import view.guiVoIP as guiVoIP

import view.stripConsole as stripConsole

import view.viewManager as viewManager
import view.viewUtils as viewUtils

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  viewConsole::viewConsole
#*  -----------------------------------------------------------------------------------------------
#*  handles all interaction with user. This class is the interface to SiCAD. It is based on pygame
#*  and SDL packages. It draws the scope on the screen and handles all mouse input.
#*  -----------------------------------------------------------------------------------------------
#*/
class viewConsole ( viewManager.viewManager ):

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the display
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::__init__"


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
        #*  initialize super class
        #*/
        viewManager.viewManager.__init__ ( self, f_cm, False )

        #** ---------------------------------------------------------------------------------------
        #*  define o titulo da janela
        #*/
        pygame.display.set_caption ( locDefs.xTXT_Tit + " [Console/" + self._oExe.getFName () + "]" )

        #** ---------------------------------------------------------------------------------------
        #*  initialize strip list
        #*/
        self._stripList = stripConsole.stripConsole ( f_cm, self._bg, 
                                                      glbDefs.xSCR_CTR [ glbDefs.xSCR_Strip ][ 0 ],
                                                      glbDefs.xSCR_CTR [ glbDefs.xSCR_Strip ][ 1 ] )
        assert ( self._stripList )

        #** ---------------------------------------------------------------------------------------
        #*  initialize VoIP box
        #*/
        self._voipBox = guiVoIP.guiVoIP ( self._bg, f_cm,
                                          glbDefs.xSCR_CTR [ glbDefs.xSCR_VoIP ][ 0 ],
                                          glbDefs.xSCR_CTR [ glbDefs.xSCR_VoIP ][ 1 ] )
        assert ( self._voipBox )

        #** ---------------------------------------------------------------------------------------
        #*  initialize info area
        #*/
        self._imetBox = guiIMet.guiIMet ( f_cm, self._bg,
                                          glbDefs.xSCR_CTR [ glbDefs.xSCR_IMet ][ 0 ],
                                          glbDefs.xSCR_CTR [ glbDefs.xSCR_IMet ][ 1 ] )
        assert ( self._imetBox )

        #** ---------------------------------------------------------------------------------------
        #*  rodando no windows ?
        #*/
        #if (( "win32" == sys.platform ) or ( "win64" == sys.platform )):

            #** -----------------------------------------------------------------------------------
            #*  cria a tela em modo janela
            #*/
            #self._screen = pygame.display.set_mode ( locDefs.xSCR_Size, DOUBLEBUF | HWSURFACE )

        #** ---------------------------------------------------------------------------------------
        #*  senão, provavel linux ou outro unix
        #*/
        #else:

            #** -----------------------------------------------------------------------------------
            #*  cria a tela em modo fullscreen
            #*/
            #self._screen = pygame.display.set_mode ( locDefs.xSCR_Size, FULLSCREEN | DOUBLEBUF | HWSURFACE )

        #assert ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  set permanent background
        #*/
        self._screen.blit ( self._bg, ( 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  flight call sign
        #*/
        self._bCallSign = False

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a tela
        #*/
        self.dispFlip ( False )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::cbkElimina
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkElimina ( self, f_oAtv ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::cbkElimina"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._fc )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o flight engine da aeronave
        #*/
        l_fe = f_oAtv.getFE ()
        assert ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  retira a aeronave da lista de aeronaves ativas
        #*/
        self._fc.cbkElimina ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::cbkExeEscala
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkExeEscala ( self, f_iEsc ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::cbkExeEscala"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_iEsc in locDefs.xSET_EscalasValidas )
        
        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oExe )
        
        #** ---------------------------------------------------------------------------------------
        #*  verifica se mudou a escala
        #*/
        if ( self._oExe.getEscala () != f_iEsc ):

            #** -----------------------------------------------------------------------------------
            #*  configura a nova escala
            #*/
            self._oExe.setEscala ( f_iEsc )

            #** -----------------------------------------------------------------------------------
            #*  avisa que houve mudança de escala
            #*/
            self._oExe.setMudouEscala ( True )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::cbkToggleCallSign
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkToggleCallSign ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::cbkToggleCallSign"
            

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #l_log.info ( "self._scope: " + str ( self._scope ))

        #** ---------------------------------------------------------------------------------------
        #*  existe o scope ?
        #*/
        if ( None != self._scope ):

            #** -----------------------------------------------------------------------------------
            #*  toggle call sign flag 
            #*/
            self._bCallSign = not self._bCallSign
            #l_log.info ( "CallSign: " + str ( self._bCallSign ))

            #** -----------------------------------------------------------------------------------
            #*  redraws entire scope
            #*/
            self._scope.doRedraw ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::run
    #*  -------------------------------------------------------------------------------------------
    #*  routine that runs the application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::run"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._bg )
        assert ( self._imetBox )
        assert ( self._infoBox )
        assert ( self._scope )
        assert ( self._oExe )
        assert ( self._stripList )
        assert ( self._voipBox )
        
        #** ---------------------------------------------------------------------------------------
        #*  enquanto nao inicia...
        #*/
        while ( not glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  aguarda 1 seg
            #*/
            time.sleep ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  inicia hora da simulação
        #*/
        #self._dHoraSim = self._st.obtemHoraSim ()

        #** ---------------------------------------------------------------------------------------
        #*  eternal loop
        #*/
        while ( glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  se mudou a escala atualiza o scope
            #*/
            if ( self._oExe.getMudouEscala ()):

                #** -------------------------------------------------------------------------------
                #*  clear background
                #*/
                self._bg.fill (( 0, 0, 0 ))

                #** -------------------------------------------------------------------------------
                #*  new scope graphics
                #*/
                self._scope.doRedraw ()

                #** -------------------------------------------------------------------------------
                #*  new info box
                #*/
                self._infoBox.doRedraw ( self._bg )

                #** -------------------------------------------------------------------------------
                #*  new strip box
                #*/
                self._stripList.doRedraw ( self._bg )

                #** -------------------------------------------------------------------------------
                #*  new voip box
                #*/
                self._voipBox.doRedraw ( self._bg )

                #** -------------------------------------------------------------------------------
                #*  new imet box
                #*/
                self._imetBox.doRedraw ( self._bg )

                #** -------------------------------------------------------------------------------
                #*  reseta o flag de mudanca de escala
                #*/
                self._oExe.setMudouEscala ( False )

            #** -----------------------------------------------------------------------------------
            #*  enquanto estiver congelado...
            #*/
            while (( glbData.g_bKeepRun ) and ( self._bPause )):

                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait )

            #** -----------------------------------------------------------------------------------
            #*  make sure background stays
            #*/
            #l_bg.set_colorkey ( l_bg.get_at (( 0, 0 )))
            self._screen.blit ( self._bg, ( 0, 0 ))

            #** -----------------------------------------------------------------------------------
            #*  atualiza os vôos
            #*/
            self.updateFlights ()

            #** -----------------------------------------------------------------------------------
            #*  atualiza as imagens
            #*/
            self.updateImages ()

            #** -----------------------------------------------------------------------------------
            #*  atualiza a tela
            #*/
            self.dispFlip ( False )

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif......(V): " + str ( l_lDif ))
            #l_log.info ( "xTIM_Refresh(V): " + str ( glbDefs.xTIM_Refresh ))
            #l_log.info ( "Wait/Sleep..(V): " + str ( glbDefs.xTIM_Refresh - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta atrasado ?
            #*/
            if ( glbDefs.xTIM_Refresh > l_lDif ):

                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Refresh - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::updateAnv
    #*  -------------------------------------------------------------------------------------------
    #*  updates the display from the flights in the flightlist
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_oAtv - DOCUMENT ME!
    #*  @param  f_iI   - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def updateAnv ( self, f_oAtv, f_iI ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::updateAnv"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._font )
        assert ( self._oAer )
        assert ( self._screen )
        assert ( self._stripList )
        
        #** ---------------------------------------------------------------------------------------
        #*  obtem a posição do vôo
        #*/
        l_tAnvPos = f_oAtv.getPosicao ()
        assert ( l_tAnvPos )
        #l_log.info ( "Posição............: " + str ( l_tAnvPos ))

        #** ---------------------------------------------------------------------------------------
        #*  normaliza
        #*/
        l_tAnvPos = viewUtils.normalizeXY ( l_tAnvPos )
        assert ( l_tAnvPos )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de tela
        #*/
        l_tAnvPos = viewUtils.scale2Device ( l_tAnvPos )
        assert ( l_tAnvPos )

        #** ---------------------------------------------------------------------------------------
        #*  calculate screen position
        #*/
        l_tScrPos = ( int ( round ( l_tAnvPos [ 0 ] )),
                      int ( round ( l_tAnvPos [ 1 ] )))
        assert ( l_tScrPos )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a proa
        #*/
        l_dAnvProa = f_oAtv.getNavProa ()
        #l_log.info ( "Proa: " + str ( l_dAnvProa ))

        #** ---------------------------------------------------------------------------------------
        #*  calculate heading transformation
        #*/
        l_dRotate = 360. - l_dAnvProa - self._oAer.getDifDeclinacao ()

        #** ---------------------------------------------------------------------------------------
        #*  normal flight, use blue icon
        #*/
        l_icnAtv = pygame.transform.rotate ( self._icnAtvBlue, l_dRotate )
        assert ( l_icnAtv )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posição do icone na tela
        #*/
        l_icnPos = l_icnAtv.get_rect ()
        assert ( l_icnPos )

        #** ---------------------------------------------------------------------------------------
        #*  verifica se esta na porção visivel da tela
        #*/
        if ( viewUtils.checkClippingScr ( l_tScrPos, l_icnPos )):

            #** -----------------------------------------------------------------------------------
            #*  ajusta o centro do icone
            #*/
            #l_icnPos = l_icnAtv.get_rect ()
            #assert ( l_icnPos )

            l_icnPos.center = l_tScrPos
            #l_log.info ( "Posição na tela: " + str ( l_icnPos ))

            #** -----------------------------------------------------------------------------------
            #*  put the icon on the screen
            #*/
            #l_bg.set_colorkey ( l_bg.get_at (( 0, 0 )))
            self._screen.blit ( l_icnAtv, l_icnPos )

            #** -----------------------------------------------------------------------------------
            #*  verifica se o flag de exibição de call sign esta ativo
            #*/
            if ( self._bCallSign ):

                #** -------------------------------------------------------------------------------
                #*  obtem a identificação do vôo
                #*/
                l_szTxt = f_oAtv.getIdent () #+ "/" + f_oAtv.getTipo ()
                assert ( l_szTxt )

                #** -------------------------------------------------------------------------------
                #*  cria o texto com Id e tipo na cor desejada
                #*/
                l_szTxt = self._font.render ( l_szTxt, 1, locDefs.xCOR_FlightNo )
                assert ( l_szTxt )

                #** -------------------------------------------------------------------------------
                #*  make the flight no stand under the icon
                #*/
                l_txtPos = l_szTxt.get_rect ()
                assert ( l_txtPos )
                
                l_txtPos.center = ( l_tScrPos [ 0 ],
                                    l_tScrPos [ 1 ] + 11 + l_txtPos.center [ 1 ] )

                #** -------------------------------------------------------------------------------
                #*  put the flight no. on the screen
                #*/
                #l_bg.set_colorkey ( l_bg.get_at (( 0, 0 )))
                self._screen.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a strip da aeronave
        #*/
        self._stripList.doUpdate ( self._screen, f_iI, f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewConsole::updateFlights
    #*  -------------------------------------------------------------------------------------------
    #*  updates the display from the flights in the flightlist
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def updateFlights ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewConsole::updateFlights"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._fc )
        assert ( self._infoBox )
        assert ( self._imetBox )
        assert ( self._screen )
        assert ( self._voipBox )
               
        #** ---------------------------------------------------------------------------------------
        #*  trava a lista de vôos
        #*/
        glbData.g_lckFlight.acquire ()

        #** ---------------------------------------------------------------------------------------
        #*/
        try:

            #** -----------------------------------------------------------------------------------
            #*  inicia o contador de strips
            #*/
            l_iI = 0

            #** -----------------------------------------------------------------------------------
            #*  obtem a lista de vôos
            #*/
            l_lstFlight = self._fc.getListFlight ()

            #** -----------------------------------------------------------------------------------
            #*  percorre a lista de vôos ativos
            #*/
            for l_key, l_oAtv in l_lstFlight.iteritems ():

                #** -------------------------------------------------------------------------------
                #*  atualiza a posição da aeronave
                #*/
                self.updateAnv ( l_oAtv, l_iI )

                #** -------------------------------------------------------------------------------
                #*  incrementa o contador de strips
                #*/
                l_iI += 1

        #** ---------------------------------------------------------------------------------------
        #*/
        finally:

            #** -----------------------------------------------------------------------------------
            #*  libera a lista de vôos
            #*/
            glbData.g_lckFlight.release ()

        #** ---------------------------------------------------------------------------------------
        #*  exibe relogio e versão
        #*/
        self._infoBox.doDraw ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  exibe parametros de comunicação
        #*/
        self._voipBox.doDraw ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  exibe informações meteorologicas
        #*/
        self._imetBox.doDraw ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "viewConsole" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
