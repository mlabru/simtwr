#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: guiInfo
#*
#*  Descricao: this class takes care of all interaction with the user
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

#/ pyGame (biblioteca grafica)
#/ ------------------------------------------------------------------------------------------------
import pygame
import pygame.font

from pygame.locals import *

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.glbDefs as glbDefs
import model.locDefs as locDefs

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  guiInfo::guiInfo
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class guiInfo:

    #** -------------------------------------------------------------------------------------------
    #*  guiInfo::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the info area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm, f_bg, f_tNW, f_tWH ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiInfo::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_cm )
        assert ( f_bg )

        assert ( f_tNW )
        assert ( f_tWH )

        #** ---------------------------------------------------------------------------------------
        #*  posicao da area de informacoes
        #*/
        self._tNW = f_tNW

        #** ---------------------------------------------------------------------------------------
        #*  largura e altura da caixa
        #*/
        self._tWH = f_tWH

        #** ---------------------------------------------------------------------------------------
        #*  obtem o model manager
        #*/
        l_mm = f_cm.getMM ()
        assert ( l_mm )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o aerodromo
        #*/
        self._oAer = l_mm.getAerodromo ()
        assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o exercicio
        #*/
        self._oExe = l_mm.getExercicio ()
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o simulation time engine
        #*/
        self._st = f_cm.getST ()
        assert ( self._st )

        #** ---------------------------------------------------------------------------------------
        #*  fonte monospaced
        #*/
        self._szFont = glbDefs.xFNT_MONO

        #** ---------------------------------------------------------------------------------------
        #*  centro da area de informacoes
        #*/
        self._tInfoCtr = ( int ( round ( f_tNW [ 0 ] + (  f_tWH [ 0 ] / 2 ))),
                           int ( round ( f_tNW [ 1 ] + (( f_tWH [ 1 ] + locDefs.xSCR_HDR_Height ) / 2 ))))

        #** ---------------------------------------------------------------------------------------
        #*  cria a area de informacoes
        #*/
        l_srfInfo = pygame.Surface ( f_tWH )
        assert ( l_srfInfo )

        l_srfInfo.set_colorkey ( l_srfInfo.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        self.makeHeader ( l_srfInfo )

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        f_bg.blit ( l_srfInfo, f_tNW )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiInfo::doDraw
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the info area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doDraw ( self, f_screen ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiInfo::doDraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_screen )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._st )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao do texto (hora)
        #*/
        l_txtPos = ( self._tInfoCtr [ 0 ],
                     self._tInfoCtr [ 1 ] - 7 )
        assert ( l_txtPos ) 

        #** ---------------------------------------------------------------------------------------
        #*  obtem a hora formatada
        #*/
        l_szHora = self._st.getHoraFormat ()
        assert ( l_szHora )

        #** ---------------------------------------------------------------------------------------
        #*  escreve a hora
        #*/
        self.drawText ( f_screen, 24, l_szHora, locDefs.xCOR_Hora, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao do texto (versao)
        #*/
        l_txtPos = ( self._tInfoCtr [ 0 ],
                     self._tInfoCtr [ 1 ] + 12 )
        assert ( l_txtPos ) 

        #** ---------------------------------------------------------------------------------------
        #*  monta exercicio e aerodromo
        #*/
        l_szTxt = "%s(x%01d) - %s" % ( self._oExe.getFName (),
                                       glbDefs.xTIM_Accel,
                                       self._oExe.getIndicativo ())
        assert ( l_szTxt )  

        #** ---------------------------------------------------------------------------------------
        #*  escreve exercicio e aerodromo
        #*/
        self.drawText ( f_screen, 12, l_szTxt, locDefs.xCOR_Vers, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiInfo::doRedraw
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the info area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doRedraw ( self, f_bg ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiInfo::doRedraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_bg )

        #** ---------------------------------------------------------------------------------------
        #*  cria a area de informacoes
        #*/
        l_srfInfo = pygame.Surface ( self._tWH )
        assert ( l_srfInfo )

        l_srfInfo.set_colorkey ( l_srfInfo.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        self.makeHeader ( l_srfInfo )

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        f_bg.blit ( l_srfInfo, self._tNW )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiInfo::drawText
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the info area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawText ( self, f_screen, f_iSize, f_szTxt, f_tCor, f_tPos ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiInfo::drawText"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_screen )
        assert ( f_szTxt )
        assert ( f_tCor )
        assert ( f_tPos )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._szFont )

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte
        #*/
        l_font = pygame.font.Font ( self._szFont, f_iSize )
        assert ( l_font )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto
        #*/
        l_szTxt = l_font.render ( f_szTxt, 1, f_tCor )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao do texto
        #*/
        l_txtPos = l_szTxt.get_rect ()
        assert ( l_txtPos )

        l_txtPos.center = f_tPos

        #** ---------------------------------------------------------------------------------------
        #*  transfere o texto para a tela
        #*/
        f_screen.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiInfo::makeHeader
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeHeader ( self, f_screen ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiInfo::makeHeader"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_screen )

        #** ---------------------------------------------------------------------------------------
        #*  retangulo que define a area de strips
        #*/
        #l_retArea = ( 0, 0 ), self._tWH

        #** ---------------------------------------------------------------------------------------
        #*  desenha a moldura externa da area de strips
        #*/
        #pygame.draw.rect ( f_screen, locDefs.xCOR_Header, l_retArea, 1 )

        #** ---------------------------------------------------------------------------------------
        #*  cria o header da lista de strips
        #*/
        l_srfHdr = pygame.Surface (( self._tWH [ 0 ], locDefs.xSCR_HDR_Height ))
        assert ( l_srfHdr )

        #** ---------------------------------------------------------------------------------------
        #*  preeche com a cor de fundo
        #*/
        l_srfHdr.fill ( locDefs.xCOR_Header )
        #l_srfHdr.set_colorkey ( l_srfHdr.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte (monospaced, 10 pixels)
        #*/
        l_font = pygame.font.Font ( glbDefs.xFNT_MONO, locDefs.xSCR_HDR_FntSiz )
        assert ( l_font )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto
        #*/
        l_szTxt = l_font.render ( locDefs.xTXT_Hdr, 1, glbDefs.xCOR_SGrey )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posicao do texto
        #*/
        l_txtPos = l_szTxt.get_rect ()
        assert ( l_txtPos )

        l_txtPos.center = ( self._tWH [ 0 ] / 2, ( locDefs.xSCR_HDR_Height / 2 ) - 1 )

        #** ---------------------------------------------------------------------------------------
        #*  transfere o texto para o header
        #*/
        l_srfHdr.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  transfere o header para a tela
        #*/
        f_screen.blit ( l_srfHdr, ( 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a area de dados do objeto
    #*  ===========================================================================================
    #*/

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "guiInfo" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** ----------------------------------------------------------------------------------------------- *#
