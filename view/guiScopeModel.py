#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2010, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: view
#*  Classe...: guiScopeModel
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
#*  guiScopeModel::guiScopeModel
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class guiScopeModel:

    #** -------------------------------------------------------------------------------------------
    #*  guiScopeModel::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm, f_srf, f_tNW, f_tWH ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScopeModel::__init__"


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

        #** ---------------------------------------------------------------------------------------
        #*  salva posição NW da área
        #*/
        self._tNW = f_tNW

        #** ---------------------------------------------------------------------------------------
        #*  salva largura e altura da área
        #*/
        self._tWH = f_tWH

        #** ---------------------------------------------------------------------------------------
        #*  obtém o model manager
        #*/
        self._mm = f_cm.getMM ()
        #assert ( self._mm )

        #** ---------------------------------------------------------------------------------------
        #*  centro da área (só o canvas)
        #*/
        self._tCenter = ( int ( round ( f_tWH [ 0 ] / 2. )),
                          int ( round ( f_tWH [ 1 ] / 2. )))

        #** ---------------------------------------------------------------------------------------
        #*  cria um background para a área
        #*/
        self._bg = None

        #** ---------------------------------------------------------------------------------------
        #*  cria a área na superfície recebida
        #*/
        self.makeArea ( f_srf, f_tNW, f_tWH )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScopeModel::doRedraw
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doRedraw ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScopeModel::doRedraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  cria um background para a área
        #*/
        self._bg = pygame.Surface ( f_tWH )
        #assert ( self._bg )

        self._bg.set_colorkey ( None )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScopeModel::makeArea
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_srf - DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeArea ( self, f_srf, f_tNW, f_tWH ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScopeModel::makeArea"


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

        #** ---------------------------------------------------------------------------------------
        #*  cria um background para a área
        #*/
        self._bg = pygame.Surface ( f_tWH )
        #assert ( self._bg )

        self._bg.set_colorkey ( None )
        #self._bg.set_colorkey ( self._bg.get_at (( 1, 1 )))

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

    #** ===========================================================================================
    #*  acesso a área de dados do objeto
    #*  ===========================================================================================
    #*/

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "guiScopeModel" )

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
    l_gui = guiScopeModel ( f_cm, f_srf, f_tNW, f_tWH )
    #assert ( l_gui )
                            
#** ----------------------------------------------------------------------------------------------- *#
