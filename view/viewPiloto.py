#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: viewPiloto
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
import sys
import time

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
import model.cineCalc as cineCalc

import model.glbData as glbData
import model.glbDefs as glbDefs
import model.locDefs as locDefs

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.guiMenu as guiMenu
import view.guiMessage as guiMessage
import view.guiVoIP as guiVoIP
import view.stripPiloto as stripPiloto

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
#*  viewPiloto::viewPiloto
#*  -----------------------------------------------------------------------------------------------
#*  handles all interaction with user. This class is the interface to SiCAD. It is based on pygame
#*  and SDL packages. It draws the scope on the screen and handles all mouse input.
#*  -----------------------------------------------------------------------------------------------
#*/
class viewPiloto ( viewManager.viewManager ):

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::__init__
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
        #l_szMetodo = "viewPiloto::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_cm )

        #** ---------------------------------------------------------------------------------------
        #*  initialize super class
        #*/
        viewManager.viewManager.__init__ ( self, f_cm, True )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o netSender
        #*/
        self._ns = f_cm.getNS ()
        assert ( self._ns )

        #** ---------------------------------------------------------------------------------------
        #*  define o título da janela
        #*/
        pygame.display.set_caption ( locDefs.xTXT_Tit + " [Piloto/" + self._oExe.getFName () + "]" )

        #** ---------------------------------------------------------------------------------------
        #*  initialize strip list
        #*/
        self._stripList = stripPiloto.stripPiloto ( f_cm, self._bg, 
                                                    glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ],
                                                    glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 1 ] )
        assert ( self._stripList )

        #* ----------------------------------------------------------------------------------------
        #* inicia a gui
        #*
        gooeypy.init ( myscreen = self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a app da gui
        #*/
        self._guiApp = gooeypy.App ( width  = locDefs.xSCR_Size [ 0 ],
                                     height = locDefs.xSCR_Size [ 1 ],
                                     theme  = "SiCAD" )
        assert ( self._guiApp )

        #** ---------------------------------------------------------------------------------------
        #*  initialize VoIP box
        #*/
        self._voipBox = guiVoIP.guiVoIP ( self._bg, f_cm,
                                          glbDefs.xSCR_PIL [ glbDefs.xSCR_VoIP ][ 0 ],
                                          glbDefs.xSCR_PIL [ glbDefs.xSCR_VoIP ][ 1 ] )
        assert ( self._voipBox )

        #** ---------------------------------------------------------------------------------------
        #*  initialize menu list
        #*/
        self._menuBox = guiMenu.guiMenu ( f_cm, self._bg, self._guiApp,
                                          glbDefs.xSCR_PIL [ glbDefs.xSCR_Menu ][ 0 ],
                                          glbDefs.xSCR_PIL [ glbDefs.xSCR_Menu ][ 1 ] )
        assert ( self._menuBox )

        #** ---------------------------------------------------------------------------------------
        #*  initialize message box
        #*/
        self._msgBox = guiMessage.guiMessage ( self._bg,
                                               glbDefs.xSCR_PIL [ glbDefs.xSCR_Msg ][ 0 ],
                                               glbDefs.xSCR_PIL [ glbDefs.xSCR_Msg ][ 1 ] )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  inicia área de mensagens de erro e de alerta
        #*/
        self._msgBox.addTxt ( locDefs.xTXT_Tit + " (C) ICEA 2008-09", locDefs.xCOR_Messages )

        #** ---------------------------------------------------------------------------------------
        #*  avisa ao menu sobre a lista de mensagens
        #*/
        self._menuBox.setMsgBox ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  load flight icons
        #*/
        self._icnAtvGreen = viewUtils.loadImage ( "greenFlight.bmp", True )
        assert ( self._icnAtvGreen )

        self._icnAtvRed = viewUtils.loadImage ( "redFlight.bmp", True )
        assert ( self._icnAtvRed )

        self._icnAtvYellow = viewUtils.loadImage ( "yellowFlight.bmp", True )
        assert ( self._icnAtvYellow )

        self._icnAtvTarget = viewUtils.loadImage ( "navTarget.bmp", True )
        assert ( self._icnAtvTarget )

        #** ---------------------------------------------------------------------------------------
        #*  set permanent background
        #*/
        self._screen.blit ( self._bg, ( 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a tela
        #*/
        self.dispFlip ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::cbkElimina
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
        #l_szMetodo = "viewPiloto::cbkElimina"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._fc )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o flight engine da aeronave
        #*/
        l_fe = f_oAtv.getFE ()
        assert ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  o vôo esta selecionado ?
        #*/
        if ( f_oAtv.getSelected ()):
        
            #** -----------------------------------------------------------------------------------
            #*  deseleciona a aeronave
            #*/
            self._menuBox.deselectFlight ()

        #** ---------------------------------------------------------------------------------------
        #*  retira a aeronave da lista de aeronaves ativas
        #*/
        self._fc.cbkElimina ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::cbkExeEscala
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
        #l_szMetodo = "viewPiloto::cbkExeEscala"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o menu box
        #*/
        if ( None != self._menuBox ):

            #** -----------------------------------------------------------------------------------
            #*  muda a escala
            #*/
            self._menuBox.cbkExeEscala ( f_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::cbkSelectFlight
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkSelectFlight ( self, f_tMouse, f_bNav ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::cbkSelectFlight"

        #/ aeronave selecionada
        #/ ----------------------------------------------------------------------------------------
        l_oAnvSel = None


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #l_log.info ( "f_tMouse: " + str ( f_tMouse ))
        assert ( f_tMouse )

        #** ---------------------------------------------------------------------------------------
        #*  checks selection via flight icon
        #*/
        if (( f_tMouse [ 0 ] >=   glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ][ 0 ] ) and
            ( f_tMouse [ 0 ] <= ( glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ][ 0 ] +
                                  glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 1 ][ 0 ] ))):

            #l_log.info ( "glbDefs.xSCR_POS: " + str ( glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ] ))

            #** -----------------------------------------------------------------------------------
            #*  checks whether mouse position is close to any flights
            #*/
            l_oAnvSel = self.selectAnvIcon ( f_tMouse, f_bNav )

        #** ---------------------------------------------------------------------------------------
        #*  checks selection via flight strip
        #*/
        elif (( f_tMouse [ 0 ] >=   glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ][ 0 ] ) and
              ( f_tMouse [ 0 ] <= ( glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ][ 0 ] +
                                    glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 1 ][ 0 ] ))):

            #l_log.info ( "glbDefs.xSCR_PIL: " + str ( glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ] ))

            #** -----------------------------------------------------------------------------------
            #*  checks whether mouse position is inside strip flights
            #*/
            l_oAnvSel = self.selectAnvStrip ( f_tMouse, f_bNav )

        #** ---------------------------------------------------------------------------------------
        #*  senão, não clicou na area de scope
        #*/
        else:
        
            pass
            
        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave para seleção
        #*/
        return ( l_oAnvSel )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::geraColisaoAr
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def geraColisaoAr ( self, f_oAtvN1, f_oAtvN2 ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::GeraColisaoAr"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_oAtvN1 )
        assert ( f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição da aeronave 1
        #*/
        l_tAnv1Pos = f_oAtvN1.getPosicao ()
        assert ( l_tAnv1Pos )
        #l_log.info ( "Posição: " + str ( l_tAnv1Pos ))

        #** ---------------------------------------------------------------------------------------
        #*  elimina as aeronaves envolvidas
        #*/
        self.cbkElimina ( f_oAtvN1 )
        self.cbkElimina ( f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  envia os dados para o controle
        #*/
        self._ns.sendData ( str ( glbDefs.xNET_Vers ) + glbDefs.xMSG_Sep +
                            str ( glbDefs.xMSG_Exp )  + glbDefs.xMSG_Sep +
                            str ( l_tAnv1Pos [ 0 ] )    + glbDefs.xMSG_Sep +
                            str ( l_tAnv1Pos [ 1 ] )    + glbDefs.xMSG_Sep +
                            str ( 0 )                   + glbDefs.xMSG_Sep + str ( 1 )) 

        #** ---------------------------------------------------------------------------------------
        #*  coloca a explosão na lista de sequencias a exibir
        #*  tupla formada por: posição, indice da imagem, tipo de explosão
        #*/
        l_lstExplode = self._fc.getListExplode ()
        #l_log.info ( "lista de explosoes(P): " + str ( l_lstExplode ))

        #** ---------------------------------------------------------------------------------------
        #*  coloca a explosão na lista de sequencias a exibir
        #*  tupla formada por: posição, indice da imagem, tipo de explosão
        #*/
        l_lstExplode.append ( [ l_tAnv1Pos, 0, 1 ] )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::geraColisaoArSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def geraColisaoArSolo ( self, f_oAtvN1, f_oAtvN2 ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::GeraColisaoArSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_oAtvN1 )
        assert ( f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oExe )
        assert ( self._menuBox )

        #** ---------------------------------------------------------------------------------------
        #*/
        #CASE Exercicio.EscalaAtual OF
        #    '1' : Off := 100.0
        #|  '2' : Off := 600.0
        #|  '3' : Off := 1200.0

        #X := f_oAtvN1._tPosicao.X
        #Y := f_oAtvN1._tPosicao.Y

        #if (X > (Aerodromo.Window.XSuperior - Off)) OR
        #   (X < (Aerodromo.Window.XInferior + Off)) OR
        #   (Y > (Aerodromo.Window.YSuperior - Off)) OR
        #   (Y < (Aerodromo.Window.YInferior + Off))
        
        #** ---------------------------------------------------------------------------------------
        #*  salva a escala atual
        #*/
        l_iEsc = self._oExe.getEscala ()
        assert ( l_iEsc in locDefs.xSET_EscalasValidas )

        #** ---------------------------------------------------------------------------------------
        #*  vai para a escala 1
        #*/
        self._menuBox.cbkExeEscala ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave 1 no solo ?
        #*/
        if ( f_oAtvN1.getSolo ()):

            #** -----------------------------------------------------------------------------------
            #*  modifica o status das aeronaves envolvidas
            #*/
            f_oAtvN1.setStatusSolo ( 'X' )

            #** -----------------------------------------------------------------------------------
            #*  elimina a aeronave que esta no ar
            #*/
            self.cbkElimina ( f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  senão, aeronave 2 no solo
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  modifica o status das aeronaves envolvidas
            #*/
            f_oAtvN2.setStatusSolo ( 'X' )

            #** -----------------------------------------------------------------------------------
            #*  elimina a aeronave que esta no ar
            #*/
            self.cbkElimina ( f_oAtvN1 )

        #** ---------------------------------------------------------------------------------------
        #*/
        #DesenhaColisaoSolo ( f_oAtvN1, f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  volta a escala anterior
        #*/
        self._menuBox.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::geraColisaoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def geraColisaoSolo ( self, f_oAtvN1, f_oAtvN2 ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::GeraColisaoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_oAtvN1 )
        assert ( f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oExe )
        assert ( self._menuBox )

        #** ---------------------------------------------------------------------------------------
        #*  salva a escala atual
        #*/
        l_iEsc = self._oExe.getEscala ()
        assert ( l_iEsc in locDefs.xSET_EscalasValidas )

        #** ---------------------------------------------------------------------------------------
        #*  vai para a escala 1
        #*/
        self._menuBox.cbkExeEscala ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  modifica o status das aeronaves envolvidas
        #*/
        f_oAtvN1.setStatusSolo ( 'X' )
        f_oAtvN2.setStatusSolo ( 'X' )

        #** ---------------------------------------------------------------------------------------
        #*  desenha a colisão
        #*/
        #DesenhaColisaoSolo ( f_oAtvN1, f_oAtvN2 )

        #** ---------------------------------------------------------------------------------------
        #*  volta a escala anterior
        #*/
        self._menuBox.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::run
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
        #l_szMetodo = "viewPiloto::run"


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
        assert ( self._infoBox )
        assert ( self._menuBox )
        assert ( self._msgBox )
        assert ( self._scope )
        assert ( self._oExe )
        assert ( self._stripList )
        assert ( self._voipBox )
        
        #** ---------------------------------------------------------------------------------------
        #*  enquanto não inicia...
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
            #*  obtém o tempo inicial em segundos
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
                #l_log.info ( "self._bg(P): " + str ( self._bg ))
                #l_log.info ( "self._bg.id: " + str ( id ( self._bg )))

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
                #*  new strip box
                #*/
                self._menuBox.doRedraw ( self._bg )

                #** -------------------------------------------------------------------------------
                #*  new message box
                #*/
                self._msgBox.doRedraw ( self._bg )

                #** -------------------------------------------------------------------------------
                #*  reseta o flag de mudanca de escala
                #*/
                self._oExe.setMudouEscala ( False )

            #** -----------------------------------------------------------------------------------
            #*  enquanto estiver congelado...
            #*/
            while (( glbData.g_bKeepRun ) and ( self._bPause )):

                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (200/1000th)
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
            self.dispFlip ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
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
    #*  viewPiloto::showPercurso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def showPercurso ( self, f_screen, f_oAtv ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::showPercurso"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_screen )
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  lista de vértices do percurso
        #*/
        l_lstPos = []

        #** ---------------------------------------------------------------------------------------
        #*  percorre os pontos do percurso...
        #*/
        for l_oEtapa in f_oAtv.getPercurso ():

            #l_log.info ( "ponto: " + str ( l_iI ))

            #** -----------------------------------------------------------------------------------
            #*  obtém um ponto do percurso
            #*/
            l_tPos = l_oEtapa._tPos
            assert ( l_tPos )

            #l_log.info ( "ponto do percurso: " + str ( l_tPos ))

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tPos = viewUtils.normalizeXY ( l_tPos )
            assert ( l_tPos )

            #l_log.info ( "coordenadas normalizadas: " + str ( l_tPos ))

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tPos = viewUtils.scale2Device ( l_tPos )
            assert ( l_tPos )

            #l_log.info ( "coordenadas de dispositivo: " + str ( l_tPos ))

            #** -----------------------------------------------------------------------------------
            #*  acrescenta o ponto ao polígono
            #*/
            l_lstPos.append ( l_tPos )
            #l_log.info ( "l_tPos (%d): [%s]" % ( l_iI, str ( l_tPos )))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o destino do taxi
        #*/
        l_tPos = f_oAtv.getTaxDestino ()
        assert ( l_tPos )

        #l_log.info ( "destino do taxi: " + str ( l_tPos ))

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tPos = viewUtils.normalizeXY ( l_tPos )
        assert ( l_tPos )

        #l_log.info ( "coordenadas normalizadas: " + str ( l_tPos ))

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tPos = viewUtils.scale2Device ( l_tPos )
        assert ( l_tPos )

        #l_log.info ( "coordenadas de dispositivo: " + str ( l_tPos ))

        #** ---------------------------------------------------------------------------------------
        #*  acrescenta o ponto ao poligono (scr.coord)
        #*/
        l_lstPos.append ( l_tPos )
        #l_log.info ( "l_tPos(D): " + str ( l_tPos ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cor do percurso
        #*/
        l_tCor = locDefs.xCOR_Percurso

        #** ---------------------------------------------------------------------------------------
        #*  desenha um linha unindo estes pontos
        #*/
        #l_log.info ( "l_lstPos........: " + str ( l_lstPos ))
        #l_log.info ( "len ( l_lstPos ): " + str ( len ( l_lstPos )))

        #** ---------------------------------------------------------------------------------------
        #*  tem pontos suficientes para uma linha ?
        #*/
        if ( len ( l_lstPos ) > 1 ):

            #** -----------------------------------------------------------------------------------
            #*  desenha um linha unindo estes pontos
            #*/
            pygame.draw.lines ( f_screen, l_tCor, False, l_lstPos, 1 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::selectAnvIcon
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def selectAnvIcon ( self, f_tMouse, f_bNav ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::selectAnvIcon"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #l_log.info ( "f_tMouse: " + str ( f_tMouse ))
        assert ( f_tMouse )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._fc )
        assert ( self._menuBox )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a lista de vôos ativos
        #*/
        l_lstFlight = self._fc.getListFlight ()

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de vôos ativos
        #*/
        for l_iI in xrange ( len ( l_lstFlight )):

            #** -----------------------------------------------------------------------------------
            #*  obtém um flight engine
            #*/
            l_fe = l_lstFlight [ l_iI ]
            assert ( l_fe )

            #** -----------------------------------------------------------------------------------
            #*  obtém a area de dados da aeronave
            #*/
            l_oAtv = l_fe.getAtv ()
            assert ( l_oAtv )

            #** -----------------------------------------------------------------------------------
            #*  obtém a posição do vôo
            #*/
            l_tAnvPos = l_oAtv.getPosicao ()
            assert ( l_tAnvPos )

            #** -----------------------------------------------------------------------------------
            #*  normaliza
            #*/
            l_tAnvPos = viewUtils.normalizeXY ( l_tAnvPos )
            assert ( l_tAnvPos )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de tela
            #*/
            l_tAnvPos = viewUtils.scale2Device ( l_tAnvPos )
            assert ( l_tAnvPos )

            #** -----------------------------------------------------------------------------------
            #*  calcula distancia entre o 'click' e a aeronave
            #*/
            l_dDist = cineCalc.distanciaEntrePontos ( f_tMouse, l_tAnvPos )
            #l_log.info ( "l_dDist: " + str ( l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*  distancia aceitavel ? 
            #*/
            if ( l_dDist <= locDefs.xSCR_CLK_Dist ):

                #** -------------------------------------------------------------------------------
                #*  deseleciona as outras aeronaves
                #*/
                self._fc.deselectFlights ()

                #** -------------------------------------------------------------------------------
                #*  also update the color of the menu item...
                #*/
                self._menuBox.deselectFlight ()

                #** -------------------------------------------------------------------------------
                #*  seleciona esta aeronave
                #*/
                l_oAtv.setSelected ( True, f_bNav )

                #** -------------------------------------------------------------------------------
                #*  also update the color of the menu item...
                #*/
                self._menuBox.selectFlight ( l_oAtv )

                #** -------------------------------------------------------------------------------
                #*  retorna a aeronave selecionada
                #*/
                return ( l_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  deseleciona todas as aeronaves
        #*/
        self._fc.deselectFlights ()

        #** ---------------------------------------------------------------------------------------
        #*  also update the color of the menu item...
        #*/
        self._menuBox.deselectFlight ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  não achou nenhuma aeronave para seleção
        #*/
        return ( None )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::selectAnvStrip
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def selectAnvStrip ( self, f_tMouse, f_bNav ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::selectAnvStrip"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #l_log.info ( "f_tMouse: " + str ( f_tMouse ))
        #l_log.info ( "glbDefs.xSCR_PIL: " + str ( glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ] ))
        assert ( f_tMouse )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._fc )
        assert ( self._menuBox )

        #** -----------------------------------------------------------------------------------
        #*  calcula a posição do click dentro da strip
        #*/
        l_tClick = (( f_tMouse [ 0 ] - glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ][ 0 ] ), 
                    ( f_tMouse [ 1 ] - glbDefs.xSCR_PIL [ glbDefs.xSCR_Strip ][ 0 ][ 1 ] ))
        #l_log.info ( "l_tClick: " + str ( l_tClick ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a lista de vôos ativos
        #*/
        l_lstFlight = self._fc.getListFlight ()

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de vôos ativos
        #*/
        for l_iI in xrange ( len ( l_lstFlight )):

            #** -----------------------------------------------------------------------------------
            #*  obtém um flight engine
            #*/
            l_fe = l_lstFlight [ l_iI ]
            assert ( l_fe )

            #** -----------------------------------------------------------------------------------
            #*  obtém a area de dados da aeronave
            #*/
            l_oAtv = l_fe.getAtv ()
            assert ( l_oAtv )

            #** -----------------------------------------------------------------------------------
            #*  obtém a posição da strip
            #*/
            l_tPosStrip = l_oAtv.getStrip ()
            assert ( l_tPosStrip )

            #** -----------------------------------------------------------------------------------
            #*  cria um retângulo
            #*/
            l_rtStrip = pygame.Rect ( l_tPosStrip )
            assert ( l_rtStrip )

            #l_log.info ( "l_rtStrip: " + str ( l_rtStrip ))

            #** -----------------------------------------------------------------------------------
            #*  'click' dentro da 'strip' ? 
            #*/
            if ( l_rtStrip.collidepoint ( l_tClick )):

                #** -------------------------------------------------------------------------------
                #*  deseleciona as outras aeronaves
                #*/
                self._fc.deselectFlights ()

                #** -------------------------------------------------------------------------------
                #*  also update the color of the menu item...
                #*/
                self._menuBox.deselectFlight ()

                #** -------------------------------------------------------------------------------
                #*  seleciona esta aeronave
                #*/
                l_oAtv.setSelected ( True, f_bNav )

                #** -------------------------------------------------------------------------------
                #*  also update the color of the menu item...
                #*/
                self._menuBox.selectFlight ( l_oAtv )

                #** -------------------------------------------------------------------------------
                #*  retorna a aeronave selecionada
                #*/
                return ( l_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  não achou nenhuma aeronave para seleção
        #*/
        return ( None )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::updateAnv
    #*  -------------------------------------------------------------------------------------------
    #*  updates the display from the flights in the flightlist
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def updateAnv ( self, f_oAtv, f_iI ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::updateAnv"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
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
        #*  obtém a posição do vôo
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
        #*  obtém a proa
        #*/
        l_dAnvProa = f_oAtv.getNavProa ()
        #l_log.info ( "Proa: " + str ( l_dAnvProa ))

        #** ---------------------------------------------------------------------------------------
        #*  calculate heading transformation
        #*/
        l_dRotate = 360. - l_dAnvProa - self._oAer.getDifDeclinacao ()

        #** ---------------------------------------------------------------------------------------
        #*  aeronave selecionada ?
        #*/
        if ( f_oAtv.getSelected ()):

            #** -----------------------------------------------------------------------------------
            #*  user has selected this flight, use green icon
            #*/
            l_icnAtv = pygame.transform.rotate ( self._icnAtvGreen, l_dRotate )
            assert ( l_icnAtv )

        #** ---------------------------------------------------------------------------------------
        #*  existem alertas para esta aeronave ?
        #*/
        elif ( f_oAtv.getAlert ()):

            #** -----------------------------------------------------------------------------------
            #*  this flight has alerts, use red icons
            #*/
            l_icnAtv = pygame.transform.rotate ( self._icnAtvRed, l_dRotate )
            assert ( l_icnAtv )

            #** -----------------------------------------------------------------------------------
            #*  existe aviso de alerta
            #*/
            #if ( None != self._sndAlert ):

                #** -------------------------------------------------------------------------------
                #*  calcula o tempo desde o ultimo aviso
                #*/
                #l_dDlt = self._st.obtemHoraSim () - self._dHoraSim

                #** -------------------------------------------------------------------------------
                #*  ja passou mais de 1s ?
                #*/
                #if ( l_dDlt >= 1000. ):

                    #** ---------------------------------------------------------------------------
                    #*  emite o aviso sonoro
                    #*/
                    #self._sndAlert.play ()

                    #** ---------------------------------------------------------------------------
                    #*  salva a hora
                    #*/
                    #self._dHoraSim = self._st.obtemHoraSim ()

        #** ---------------------------------------------------------------------------------------
        #*  senão, normal flight
        #*/
        else:

            #** -----------------------------------------------------------------------------------
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
            #*  obtém a identificação do vôo
            #*/
            l_szTxt = f_oAtv.getIdent () #+ "/" + f_oAtv.getTipo ()
            assert ( l_szTxt )

            #** -----------------------------------------------------------------------------------
            #*  cria o texto com Id e tipo na cor desejada
            #*/
            l_szTxt = self._font.render ( l_szTxt, 1, locDefs.xCOR_FlightNo )
            assert ( l_szTxt )

            #** -----------------------------------------------------------------------------------
            #*  make the flight no stand under the icon
            #*/
            l_txtPos = l_szTxt.get_rect ()
            assert ( l_txtPos )
            
            l_txtPos.center = ( l_tScrPos [ 0 ],
                                l_tScrPos [ 1 ] + 11 + l_txtPos.center [ 1 ] )

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
            #*  put the flight no. on the screen
            #*/
            #l_bg.set_colorkey ( l_bg.get_at (( 0, 0 )))
            self._screen.blit ( l_szTxt, l_txtPos )

            #** -----------------------------------------------------------------------------------
            #*  should the nav target be displayed ?
            #*/
            if ( f_oAtv.getNav ()):

                #** -------------------------------------------------------------------------------
                #*  this is a nav select - draw target
                #*/
                l_navPos = self._icnAtvTarget.get_rect ()
                assert ( l_navPos )

                l_navPos.center = l_tScrPos

                #** -------------------------------------------------------------------------------
                #*  transfere para a tela
                #*/
                #l_bg.set_colorkey ( l_bg.get_at (( 0, 0 )))
                self._screen.blit ( self._icnAtvTarget, l_navPos )

            #** -----------------------------------------------------------------------------------
            #*  exibe o percurso ?
            #*/
            if (( None != f_oAtv.getPercurso ()) and ( f_oAtv.getShowPercurso ())):

                #** -------------------------------------------------------------------------------
                #*  exibe o percurso da aeronave
                #*/
                self.showPercurso ( self._screen, f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a strip da aeronave
        #*/
        self._stripList.doUpdate ( self._screen, f_iI, f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::updateFlights
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
        #l_szMetodo = "viewPiloto::updateFlights"


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
        assert ( self._msgBox )
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
            #*  obtém a lista de vôos
            #*/
            l_lstFlight = self._fc.getListFlight ()

            #** -----------------------------------------------------------------------------------
            #*  percorre a lista de vôos ativos
            #*/
            for l_iI in xrange ( len ( l_lstFlight )):

                #** -------------------------------------------------------------------------------
                #*  obtém um flight engine
                #*/
                l_fe = l_lstFlight [ l_iI ]
                assert ( l_fe )

                #** -------------------------------------------------------------------------------
                #*  obtém a area de dados da aeronave
                #*/
                l_oAtv = l_fe.getAtv ()
                assert ( l_oAtv )

                #** -------------------------------------------------------------------------------
                #*  atualiza a posição da aeronave
                #*/
                self.updateAnv ( l_oAtv, l_iI )

        #** ---------------------------------------------------------------------------------------
        #*/
        finally:

            #** -----------------------------------------------------------------------------------
            #*  libera a lista de vôos
            #*/
            glbData.g_lckFlight.release ()

        #** ---------------------------------------------------------------------------------------
        #*  exibe relógio e versão
        #*/
        self._infoBox.doDraw ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  exibe parâmetros de comunicação
        #*/
        self._voipBox.doDraw ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  redraw all the messages in the msgBox
        #*/
        self._msgBox.doRedrawMsgs ( self._screen )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a área de dados do objeto
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::getGuiApp
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getGuiApp ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::getGuiApp"


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
        return ( self._guiApp )

    #** -------------------------------------------------------------------------------------------
    #*  viewPiloto::getMenuBox
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getMenuBox ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewPiloto::getMenuBox"


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
        return ( self._menuBox )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "viewPiloto" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
