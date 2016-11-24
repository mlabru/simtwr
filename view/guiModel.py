#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008-2011, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: view
#*  Classe...: guiModel
#*
#*  Descrição: DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versão
#*  -----------------------------------------------------------------------------------------------
#*  mlabru   2010/set  1.0  versão para Linux
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  mlabru   2010/set  1.0  version started
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca gráfica)
#/ ------------------------------------------------------------------------------------------------
import pygame
import pygame.font

from pygame.locals import *

#/ pyACME / model
#/ ------------------------------------------------------------------------------------------------
import model.glbDefs as glbDefs
import model.locDefs as locDefs

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  guiModel::guiModel
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class guiModel:

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm, f_srf, f_tNW, f_tWH, f_szTitle ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_cm )

        #assert ( f_srf )
        #assert ( f_tNW )
        #assert ( f_tWH )

        #assert ( f_szTitle )

        #** ---------------------------------------------------------------------------------------
        #*  salva posição NW da área
        #*/
        self._tNW = f_tNW

        #** ---------------------------------------------------------------------------------------
        #*  salva largura e altura da área
        #*/
        self._tWH = f_tWH

        #** ---------------------------------------------------------------------------------------
        #*  salva o título da área
        #*/
        self._szTitle = f_szTitle

        #** ---------------------------------------------------------------------------------------
        #*  obtém o model manager
        #*/
        self._mm = f_cm.getMM ()
        #assert ( self._mm )

        #** ---------------------------------------------------------------------------------------
        #*  centro da área (só o canvas)
        #*/
        self._tCenter = ( int ( round (  f_tWH [ 0 ] / 2 )),
                          int ( round (( f_tWH [ 1 ] + locDefs.xSCR_HDR_Height ) / 2 )))

        #** ---------------------------------------------------------------------------------------
        #*  cria um background para a área
        #*/
        self._bg = None

        #** ---------------------------------------------------------------------------------------
        #*  cria um canvas para a área
        #*/
        self._canvas = None

        #** ---------------------------------------------------------------------------------------
        #*  cria a área na superfície recebida
        #*/
        self.makeArea ( f_srf, f_tNW, f_tWH, f_szTitle )

        #** ---------------------------------------------------------------------------------------
        #*  força o desenho do canvas
        #*/
        self._bChanged = True

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::doRedraw
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doRedraw ( self, f_srf ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::doRedraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_srf )

        #** ---------------------------------------------------------------------------------------
        #*  copia o background na superfície recebida
        #*/
        f_srf.blit ( self._bg, self._tNW )

        #** ---------------------------------------------------------------------------------------
        #*  força o desenho do canvas
        #*/
        self._bChanged = True

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::drawCanvas
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_srf - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawCanvas ( self, f_srf ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::drawCanvas"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_srf )

        #l_log.info ( "self._tNW...:" + str ( self._tNW ))
        #l_log.info ( "f_srf.......:" + str ( f_srf ))
        #l_log.info ( "self._canvas:" + str ( self._canvas ))

        #** ---------------------------------------------------------------------------------------
        #*  transfere o canvas para a superfície recebida
        #*/
        f_srf.blit ( self._canvas, ( self._tNW [ 0 ], self._tNW [ 1 ] + locDefs.xSCR_HDR_Height ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::drawText
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the info area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawText ( self, f_srf, f_iSize, f_szTxt, f_tCor, f_tPos, f_iPos ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::drawText"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_srf )
        #assert ( f_szTxt )
        #assert ( f_tCor )
        #assert ( f_tPos )

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte
        #*/
        l_font = pygame.font.Font ( glbDefs.xFNT_MONO, f_iSize )
        #assert ( l_font )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto
        #*/
        l_szTxt = l_font.render ( f_szTxt, 1, f_tCor )
        #assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posição do texto
        #*/
        l_txtPos = l_szTxt.get_rect ()
        #assert ( l_txtPos )

        if ( 7 == f_iPos ):

            l_txtPos.topleft = f_tPos

        elif ( 5 == f_iPos ):

            l_txtPos.center = f_tPos

        elif ( 3 == f_iPos ):

            l_txtPos.midright = f_tPos

        #** ---------------------------------------------------------------------------------------
        #*  transfere o texto para a tela
        #*/
        f_srf.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::makeArea
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_srf - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeArea ( self, f_srf, f_tNW, f_tWH, f_szTitle ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::makeArea"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_srf )
        #assert ( f_tNW )
        #assert ( f_tWH )

        #assert ( f_szTitle )

        #** ---------------------------------------------------------------------------------------
        #*  cria um background para a área
        #*/
        self._bg = pygame.Surface ( f_tWH )
        #assert ( self._bg )

        self._bg.set_colorkey ( None )
        #self._bg.set_colorkey ( self._bg.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  cria o header no background
        #*/
        self.makeHeader ( self._bg, f_tWH, f_szTitle )

        #** ---------------------------------------------------------------------------------------
        #*  cria o canvas
        #*/
        self.makeCanvas ( self._bg, f_tWH )

        #** ---------------------------------------------------------------------------------------
        #*  desenha a moldura externa da área
        #*/
        #pygame.draw.rect ( self._bg, glbDefs.xCOR_red, (( 0, 0 ), f_tWH ), 1 )

        #** ---------------------------------------------------------------------------------------
        #*  copia na superfície
        #*/
        f_srf.blit ( self._bg, f_tNW )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::makeCanvas
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_srf - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeCanvas ( self, f_srf, f_tWH ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::makeCanvas"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_srf )
        #assert ( f_tWH )

        #** ---------------------------------------------------------------------------------------
        #*  cria uma superfície para o canvas
        #*/
        self._canvas = pygame.Surface (( f_tWH [ 0 ], f_tWH [ 1 ] - locDefs.xSCR_HDR_Height ))
        #assert ( self._canvas )

        self._canvas.set_colorkey ( None )

        #l_log.info ( "self._canvas: " + str ( self._canvas ))
        #l_log.info ( "f_tH........: " + str ( f_tWH [ 1 ] - locDefs.xSCR_HDR_Height ))
        #l_log.info ( "f_tW........: " + str ( f_tWH [ 0 ] ))

        #** ---------------------------------------------------------------------------------------
        #*  preeche com a cor de fundo
        #*/
        self._canvas.fill ( glbDefs.xCOR_black )
        #self._canvas.set_colorkey ( self._canvas.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  desenha a moldura externa da área
        #*/
        #pygame.draw.rect ( self._canvas, glbDefs.xCOR_yellow,
        #                   (( 0, 0 ), ( f_tWH [ 0 ], f_tWH [ 1 ] - locDefs.xSCR_HDR_Height )), 1 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::makeHeader
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_srf - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeHeader ( self, f_srf, f_tWH, f_szTitle ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::makeHeader"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        #assert ( f_srf )
        #assert ( f_tWH )

        #assert ( f_szTitle )

        #** ---------------------------------------------------------------------------------------
        #*  cria uma superfície para o header
        #*/
        l_srfHdr = pygame.Surface (( f_tWH [ 0 ], locDefs.xSCR_HDR_Height ))
        #assert ( l_srfHdr )

        l_srfHdr.set_colorkey ( None )

        #** ---------------------------------------------------------------------------------------
        #*  preeche com a cor de fundo
        #*/
        l_srfHdr.fill ( locDefs.xCOR_Header )
        #l_srfHdr.set_colorkey ( l_srfHdr.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte (monospaced, 10 pixels)
        #*/
        l_font = pygame.font.Font ( glbDefs.xFNT_MONO, locDefs.xSCR_HDR_FntSiz )
        #assert ( l_font )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto
        #*/
        l_szTxt = l_font.render ( f_szTitle, 1, glbDefs.xCOR_SGrey )
        #assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posição do texto
        #*/
        l_txtPos = l_szTxt.get_rect ()
        #assert ( l_txtPos )

        l_txtPos.center = ( f_tWH [ 0 ] / 2, ( locDefs.xSCR_HDR_Height / 2 ) - 1 )

        #** ---------------------------------------------------------------------------------------
        #*  transfere o texto para o header
        #*/
        l_srfHdr.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  transfere o header para a superfície recebida
        #*/
        f_srf.blit ( l_srfHdr, ( 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a área de dados do objeto
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::getChange
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getChange ( self ):
                                            
        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::getChange"
                                                                    
                                                                    
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
        return ( self._bChanged )

    #** -------------------------------------------------------------------------------------------
    #*  guiModel::setChange
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_bVal - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setChange ( self, f_bVal ):
                                            
        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiModel::setChange"
                                                                    
                                                                    
        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( type ( True ) == type ( f_bVal )):
                                                                                                                                                                    
            #** -----------------------------------------------------------------------------------
            #*/
            self._bChanged = f_bVal
                                                                                                                                                                                                        
        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "guiModel" )

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
    l_gui = guiModel ( f_cm, f_srf, f_tNW, f_tWH )
    #assert ( l_gui )
                            
#** ----------------------------------------------------------------------------------------------- *#