#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: viewManager
#*
#*  Descrição: this class takes care of all interaction with the user. It has been designed so that
#*             it can be directly linked to an AI.
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
import os
import sys
import threading

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca gráfica)
#/ ------------------------------------------------------------------------------------------------
import pygame

from pygame.locals import *

#/ GooeyPy (gui library)
#/ ------------------------------------------------------------------------------------------------
import gooeypy as gooeypy
from gooeypy.const import *

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.glbDefs as glbDefs
import model.locDefs as locDefs

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.guiInfo as guiInfo
import view.guiScope as guiScope

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
#*  viewManager::viewManager
#*  -----------------------------------------------------------------------------------------------
#*  handles all interaction with user. This class is the interface to SiCAD. It is based on pygame
#*  and SDL packages. It draws the scope on the screen and handles all mouse input.
#*  -----------------------------------------------------------------------------------------------
#*/
class viewManager ( threading.Thread ):

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the display
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm, f_bPil = True ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::__init__"


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
        threading.Thread.__init__ ( self )

        #** ---------------------------------------------------------------------------------------
        #*  salva o control manager
        #*/
        self._cm = f_cm

        #** ---------------------------------------------------------------------------------------
        #*  obtém o flight control
        #*/
        self._fc = f_cm.getFC ()
        assert ( self._fc )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o model manager
        #*/
        l_mm = f_cm.getMM ()
        assert ( l_mm )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o aeródromo
        #*/
        self._oAer = l_mm.getAerodromo ()
        assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o exercício
        #*/
        self._oExe = l_mm.getExercicio ()
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o simulation time engine
        #*/
        self._st = f_cm.getST ()
        assert ( self._st )

        #** ---------------------------------------------------------------------------------------
        #*  test thread locks to escape xlib error
        #*/
        self._screenLock = threading.Lock ()
        assert ( self._screenLock )

        #** ---------------------------------------------------------------------------------------
        #*  flag pause
        #*/
        self._bPause = False

        #** ---------------------------------------------------------------------------------------
        #*  hora da simulação
        #*/
        #self._dHoraSim = 0

        #** ---------------------------------------------------------------------------------------
        #*/
        self.scopeCenterPix = 0

        #** ---------------------------------------------------------------------------------------
        #*  posiciona a tela
        #*/
        os.environ [ "SDL_VIDEO_WINDOW_POS" ] = "-1, -1"

        #** ---------------------------------------------------------------------------------------
        #*  inicia o sistema gráfico
        #*/
        pygame.init ()

        #** ---------------------------------------------------------------------------------------
        #*  uninitialize the mixer
        #*/
        #pygame.mixer.quit ()

        #** ---------------------------------------------------------------------------------------
        #*  modo fullscreen ?
        #*/
        if ( glbDefs.xSCR_Full ):

            #** -----------------------------------------------------------------------------------
            #*  cria a janela em modo fullscreen
            #*/
            self._screen = pygame.display.set_mode ( locDefs.xSCR_Size, FULLSCREEN | DOUBLEBUF | HWSURFACE )
            assert ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  senão, modo janela
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  cria a janela em modo normal
            #*/
            self._screen = pygame.display.set_mode ( locDefs.xSCR_Size, DOUBLEBUF | HWSURFACE )
            assert ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  cria a font padrão
        #*/
        self._font = pygame.font.Font ( glbDefs.xFNT_None, 8 )
        assert ( self._font )

        #** ---------------------------------------------------------------------------------------
        #*  background de congelamento
        #*/
        self._bgFrz = None

        #** ---------------------------------------------------------------------------------------
        #*  initialize background
        #*/
        self._bg = pygame.Surface ( self._screen.get_size ())
        assert ( self._bg )

        #** ---------------------------------------------------------------------------------------
        #*  make background black
        #*/
        self._bg.fill (( 0, 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  initialize scope graphics
        #*/
        self._scope = guiScope.guiScope ( l_mm, self._bg,
                                          glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ],
                                          glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 1 ], f_bPil )
        assert ( self._scope )

        #** ---------------------------------------------------------------------------------------
        #*  initialize info area
        #*/
        self._infoBox = guiInfo.guiInfo ( f_cm, self._bg,
                                          glbDefs.xSCR_POS [ glbDefs.xSCR_Info ][ 0 ],
                                          glbDefs.xSCR_POS [ glbDefs.xSCR_Info ][ 1 ] )
        assert ( self._infoBox )

        #** ---------------------------------------------------------------------------------------
        #*  initialize gui
        #*/
        self._guiApp = None

        #** ---------------------------------------------------------------------------------------
        #*  initialize voip area
        #*/
        self._voipBox = None

        #** ---------------------------------------------------------------------------------------
        #*  load flight icons
        #*/
        self._icnAtvBlue = viewUtils.loadImage ( "blueFlight.bmp", True )
        assert ( self._icnAtvBlue )

        #** ---------------------------------------------------------------------------------------
        #*  load images
        #*/
        self._lstImgExplode = viewUtils.loadImage ( "explosion.png", True, [ ( x, 0, 50, 50 ) for x in xrange ( 0, 400, 50 ) ] )
        assert ( self._lstImgExplode )

        #** ---------------------------------------------------------------------------------------
        #*  import the sound files
        #*/
        self._sndExplode = pygame.mixer.Sound ( os.path.join ( glbDefs.xDIR_SND, "explosion.wav" ))
        assert ( self._sndExplode ) 

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::cbkCheckVoIP
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkCheckVoIP ( self, f_tMouse ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::cbkCheckVoIP"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_tMouse )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._voipBox )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._voipBox.cbkCheckVoIP ( f_tMouse )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::cbkDefreeze
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkDefreeze ( self, f_bPil = True ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::cbkDefreeze"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._bgFrz )
        assert ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  make sure background stays
        #*/
        self._bgFrz.set_colorkey ( self._bgFrz.get_at (( 0, 0 )))
        self._screen.blit ( self._bgFrz, ( 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a tela
        #*/
        self.dispFlip ( f_bPil )

        #** ---------------------------------------------------------------------------------------
        #*  seta o flag de pausa
        #*/
        self._bPause = False

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::cbkFreeze
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkFreeze ( self, f_bPil = True ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::cbkFreeze"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  seta o flag de pausa
        #*/
        self._bPause = True

        #** ---------------------------------------------------------------------------------------
        #*  obtém o background
        #*/
        self._bgFrz = pygame.display.get_surface ()
        assert ( self._bgFrz )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto de aviso
        #*/
        l_font = pygame.font.Font ( glbDefs.xFNT_None, 40 )
        assert ( l_font )
        
        l_szTxt = l_font.render ( "Congelado", 1, locDefs.xCOR_Congelado )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posição do texto na tela 
        #*/
        l_txtPos = l_szTxt.get_rect ()
        assert ( l_txtPos )
        
        l_txtPos.center = self._bgFrz.get_rect ().center

        #** ---------------------------------------------------------------------------------------
        #*  put text on screen
        #*/
        self._screen.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a tela
        #*/
        self.dispFlip ( f_bPil )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::cbkToggleCircuit
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkToggleCircuit ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::cbkToggleCircuit"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  existe o scope ?
        #*/
        if ( None != self._scope ):

            #** -----------------------------------------------------------------------------------
            #*  toggle circuit
            #*/
            self._scope.toggleCircuit ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::cbkToggleRangeMark
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkToggleRangeMark ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::cbkToggleRangeMark"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  existe o scope ?
        #*/
        if ( None != self._scope ):

            #** -----------------------------------------------------------------------------------
            #*  toggle range mark
            #*/
            self._scope.toggleRangeMark ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::cbkToggleRoseWind
    #*  -------------------------------------------------------------------------------------------
    #*  drive application
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkToggleRoseWind ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::cbkToggleRoseWind"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  existe o scope ?
        #*/
        if ( None != self._scope ):

            #** -----------------------------------------------------------------------------------
            #*  toggle rose wind
            #*/
            self._scope.toggleRoseWind ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::dispFlip
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def dispFlip ( self, f_bPil = True ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::dispFlip"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._screenLock )

        #** ---------------------------------------------------------------------------------------
        #*  acquire lock
        #*/
        self._screenLock.acquire ()

        #** ---------------------------------------------------------------------------------------
        #*  tela de piloto ?
        #*/
        if ( f_bPil ):
         
            #** -----------------------------------------------------------------------------------
            #*  gooeypy iniciado ?
            #*/
            if ( None != self._guiApp ):

                #** -------------------------------------------------------------------------------
                #*  atualiza a tela
                #*/
                self._guiApp.dirty = True
                self._guiApp.draw ()

            #** -----------------------------------------------------------------------------------
            #*  atualiza a tela
            #*/
            gooeypy.update_display ()

        #** ---------------------------------------------------------------------------------------
        #*  update display
        #*/
        pygame.display.flip ()

        #** ---------------------------------------------------------------------------------------
        #*  release lock
        #*/
        self._screenLock.release ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::run
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
        #l_szMetodo = "viewManager::run"


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

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::updateImages
    #*  -------------------------------------------------------------------------------------------
    #*  updates the display from the flights in the flightlist
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def updateImages ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::updateImages"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._screen )
               
        #l_log.info ( "lista de explosoes(A): " + str ( self._fc.getListExplode ()))

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de explosões...
        #*/
        for l_tExplode in self._fc.getListExplode ():

            #** -----------------------------------------------------------------------------------
            #*  posição da explosão
            #*/
            l_tAtvPos = l_tExplode [ 0 ]
            assert ( l_tAtvPos )

            #** -----------------------------------------------------------------------------------
            #*  normaliza
            #*/
            l_tAtvPos = viewUtils.normalizeXY ( l_tAtvPos )
            assert ( l_tAtvPos )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de tela
            #*/
            l_tAtvPos = viewUtils.scale2Device ( l_tAtvPos )
            assert ( l_tAtvPos )

            #** -----------------------------------------------------------------------------------
            #*  calculate screen position
            #*/
            l_tScrPos = ( int ( round ( l_tAtvPos [ 0 ] )),
                          int ( round ( l_tAtvPos [ 1 ] )))
            assert ( l_tScrPos )
            #l_log.info ( "Screen.: " + str ( l_tScrPos ))

            #** -----------------------------------------------------------------------------------
            #*  indice da explosao
            #*/
            l_iImg = l_tExplode [ 1 ]

            #** -----------------------------------------------------------------------------------
            #*  imagem da explosão
            #*/
            l_imgExplode = self._lstImgExplode [ l_iImg ]
            assert ( l_imgExplode )

            #** -----------------------------------------------------------------------------------
            #*  incrementa indice da explosão
            #*/
            l_tExplode [ 1 ] += 1

            #** -----------------------------------------------------------------------------------
            #*  calcula a posição da imagem na tela
            #*/
            l_imgPos = l_imgExplode.get_rect ()
            assert ( l_imgPos )

            #** -----------------------------------------------------------------------------------
            #*  verifica se está na porção visivel da tela
            #*/
            if ( viewUtils.checkClippingScr ( l_tScrPos, l_imgPos )):

                #** -------------------------------------------------------------------------------
                #*  ajusta o centro da imagem
                #*/
                l_imgPos.center = l_tScrPos
                #l_log.info ( "Posição na tela: " + str ( l_imgPos ))

                #** -------------------------------------------------------------------------------
                #*  put the image on the screen
                #*/
                #l_bg.set_colorkey ( l_bg.get_at (( 0, 0 )))
                self._screen.blit ( l_imgExplode, l_imgPos )

            #** -----------------------------------------------------------------------------------
            #*  verifica se chegou ao fim da seqüência
            #*/
            if ( l_tExplode [ 1 ] >= len ( self._lstImgExplode )):
            
                #** -------------------------------------------------------------------------------
                #*  retira a seqüência da lista
                #*/
                self._fc.getListExplode ().remove ( l_tExplode )

        #l_log.info ( "lista de explosoes(D): " + str ( self._fc.getListExplode ()))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a área de dados do objeto
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::getScreen
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getScreen ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::getScreen"


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
        return ( self._screen )

    #** -------------------------------------------------------------------------------------------
    #*  viewManager::getViewAer
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getViewAer ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewManager::getViewAer"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._scope )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_viewAer = self._scope.getViewAer ()
        assert ( l_viewAer )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_viewAer )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "viewManager" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
