#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SICAD
#*  Classe...: guiScope
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

#/ Python library
#/ ------------------------------------------------------------------------------------------------
import math

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca grafica)
#/ ------------------------------------------------------------------------------------------------
import pygame
import pygame.font
import pygame.image

from pygame.locals import *

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineCalc as cineCalc

import model.glbDefs as glbDefs
import model.locDefs as locDefs

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.viewAer as viewAer
import view.viewUtils as viewUtils

#** -----------------------------------------------------------------------------------------------
#*  defines
#*  -----------------------------------------------------------------------------------------------
#*/

#/ raio da seta de horizontalizacao
#/ ------------------------------------------------------------------------------------------------
w_xRaio     = 35
w_xRaioSeta = 30

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  guiScope::guiScope
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class guiScope:

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the scope area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm  - model manager
    #*  @param  f_bg  - background surface
    #*  @param  f_tNW - ponto ( X, Y ) do canto superior direito (NW)
    #*  @param  f_tWH - tupla com largura e altura
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_mm, f_bg, f_tNW, f_tWH, f_bPil = True ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_mm )
        assert ( f_bg )

        assert ( f_tNW )
        assert ( f_tWH )

        #** ---------------------------------------------------------------------------------------
        #*  salva o model manager localmente
        #*/
        self._mm = f_mm

        #** ---------------------------------------------------------------------------------------
        #*  salva o background localmente
        #*/
        self._bg = f_bg

        #** ---------------------------------------------------------------------------------------
        #*  obtem o exercicio
        #*/
        self._oExe = f_mm.getExercicio ()
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o aerodromo
        #*/
        self._oAer = f_mm.getAerodromo ()
        assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte
        #*/
        self._font = pygame.font.Font ( glbDefs.xFNT_None, 8 )
        assert ( self._font )

        #** ---------------------------------------------------------------------------------------
        #*  posicao do scope
        #*/
        self._tNW = f_tNW

        #** ---------------------------------------------------------------------------------------
        #*  largura e altura da caixa
        #*/
        self._tWH = f_tWH

        #** ---------------------------------------------------------------------------------------
        #*  centro do scope
        #*/
        self._tScopeCtr = (( self._tWH [ 0 ] / 2.0 ), ( self._tWH [ 1 ] / 2.0 ))
        assert ( self._tScopeCtr )

        #** ---------------------------------------------------------------------------------------
        #*  posicao da base da seta do indicativo de horizontalizacao
        #*/
        self._xSetaX = self._tWH [ 0 ] - 16
        self._xSetaY = 40

        #** ---------------------------------------------------------------------------------------
        #*  desenha o circuito ?
        #*/
        self._bCircuit = f_bPil

        #** ---------------------------------------------------------------------------------------
        #*  desenha o indicativo de horizontalizacao ?
        #*/
        self._bIndH14O = True

        #** ---------------------------------------------------------------------------------------
        #*  desenha range mark ?
        #*/
        self._bRangeMark = f_bPil

        #** ---------------------------------------------------------------------------------------
        #*  desenha a rosa-dos-ventos ?
        #*/
        self._bRoseWind = f_bPil

        #** ---------------------------------------------------------------------------------------
        #*  aerodromo
        #*/
        self._viewAer = None

        #** ---------------------------------------------------------------------------------------
        #*  setup the pontos cardeais
        #*/
        self._lstPtosCardeais = self.genPontosCardeais ()
        assert ( self._lstPtosCardeais )

        #** ---------------------------------------------------------------------------------------
        #*  superficie de desenho do aerodromo
        #*/
        self._srfAer = None

        #** ---------------------------------------------------------------------------------------
        #*  cria a area de scope
        #*/
        self._srfScope = pygame.Surface ( self._tWH )
        assert ( self._srfScope )
        
        self._srfScope.set_colorkey ( self._srfScope.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  desenha as camadas com os elementos do scope
        #*/
        self.doDraw ()

        #** ---------------------------------------------------------------------------------------
        #*  copia o scope no background na posicao 'self._tNW'
        #*/
        self._bg.blit ( self._srfScope, self._tNW )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::desenhaRangeMark
    #*  -------------------------------------------------------------------------------------------
    #*  draws the range mark
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_srfRM - superficie onde desenhar o range mark
    #*  @param  f_dRaio - raio do range mark
    #*  @param  f_tCor  - cor do range mark
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaRangeMark ( self, f_srfRM, f_dRaio, f_tCor ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::desenhaRangeMark"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_srfRM )
        assert ( f_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  raio de milhas nauticas para metros
        #*/
        l_dRaio = f_dRaio * glbDefs.xCNV_NM2M

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto central do aerodromo
        #*/
        l_tCtr = self._oAer.getCentro ()
        assert ( l_tCtr )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto na borda do circulo
        #*/
        l_tBdr = ( l_tCtr [ 0 ] + l_dRaio, l_tCtr [ 1 ] )
        assert ( l_tBdr )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto na borda do circulo
        #*/
        l_tTxt = ( l_tCtr [ 0 ], l_tCtr [ 1 ] - l_dRaio )
        assert ( l_tTxt )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tCtr = viewUtils.normalizeXY ( l_tCtr )
        assert ( l_tCtr )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tCtr = viewUtils.scale2Device ( l_tCtr )
        assert ( l_tCtr )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tBdr = viewUtils.normalizeXY ( l_tBdr )
        assert ( l_tBdr )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tBdr = viewUtils.scale2Device ( l_tBdr )
        assert ( l_tBdr )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tTxt = viewUtils.normalizeXY ( l_tTxt )
        assert ( l_tTxt )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tTxt = viewUtils.scale2Device ( l_tTxt )
        assert ( l_tTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula o raio do circulo nas novas coordenadas
        #*/
        l_dRaio = abs ( l_tBdr [ 0 ] - l_tCtr [ 0 ] )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o circulo/circunferencia na superficie
        #*/
        pygame.draw.circle ( f_srfRM, f_tCor, ( int ( l_tCtr [ 0 ] ), int ( l_tCtr [ 1 ] )), int ( l_dRaio ), 1 )

        #** ---------------------------------------------------------------------------------------
        #*  cria a identificacao do range mark
        #*/
        l_szTxt = "%.1f NM" % ( f_dRaio )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto com a identificacao do range mark
        #*/
        l_szTxt = self._font.render ( l_szTxt, 1, f_tCor )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  make the range id stand under the line
        #*/
        l_txtPos = l_szTxt.get_rect ()
        assert ( l_txtPos )

        l_txtPos.center = ( l_tCtr [ 0 ],
                            l_tCtr [ 1 ] + l_dRaio + l_txtPos.center [ 1 ] + 2. )

        #** ---------------------------------------------------------------------------------------
        #*  put the range id on the screen
        #*/
        f_srfRM.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::doDraw
    #*  -------------------------------------------------------------------------------------------
    #*  desenha os elementos do scope
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doDraw ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::doDraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  camada 0. Desenha o aerodromo
        #*/
        self.drawAirport ()

        #** ---------------------------------------------------------------------------------------
        #*  indicativo de horizontalizacao ?
        #*/
        if ( self._bIndH14O ):

            #** -----------------------------------------------------------------------------------
            #*  camada 1. Desenha o indicativo de horizontalizacao
            #*/
            self.drawIndH14O ()

        #** ---------------------------------------------------------------------------------------
        #*  range mark ?
        #*/
        if ( self._bRangeMark ):

            #** -----------------------------------------------------------------------------------
            #*  camada 2. Desenha o range mark
            #*/
            self.drawRangeMark ()

        #** ---------------------------------------------------------------------------------------
        #*  rosa-dos-ventos ?
        #*/
        if ( self._bRoseWind ):

            #** -----------------------------------------------------------------------------------
            #*  camada 3. Desenha a rosa-dos-ventos
            #*/
            self.drawRoseWind ()

        #** ---------------------------------------------------------------------------------------
        #*  camada 4. Desenha a moldura externa da area de scope
        #*/
        #pygame.draw.rect ( self._srfScope, "darkolivegreen", self._rtScope, 1 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::doRedraw
    #*  -------------------------------------------------------------------------------------------
    #*  desenha os elementos do scope
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm - model manager
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doRedraw ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::doRedraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._bg )
        assert ( self._srfScope )
        
        #** ---------------------------------------------------------------------------------------
        #*  cria a area de scope
        #*/
        #self._srfScope = pygame.Surface ( self._tWH )
        #assert ( self._srfScope )
        
        #self._srfScope.set_colorkey ( self._srfScope.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  limpa o scope
        #*/
        self._srfScope.fill ( locDefs.xCOR_Aer )

        #l_log.info ( "self._srfScope(A): " + str ( self._srfScope ))
        #l_log.info ( "self._srfScope.id(A): " + str ( id ( self._srfScope )))

        #** ---------------------------------------------------------------------------------------
        #*  desenha o scope
        #*/
        self.doDraw ()

        #** ---------------------------------------------------------------------------------------
        #*  limpa o background
        #*/
        self._bg.fill (( 0, 0, 0 ), self._srfScope.get_rect ())

        #** ---------------------------------------------------------------------------------------
        #*  copia o scope no background na posicao 'self._tNW'
        #*/
        self._bg.blit ( self._srfScope, self._tNW )

        #l_log.info ( "self._bg: " + str ( self._bg ))
        #l_log.info ( "self._bg.id: " + str ( id ( self._bg )))
        #l_log.info ( "self._srfScope(D): " + str ( self._srfScope ))
        #l_log.info ( "self._srfScope.id(D): " + str ( id ( self._srfScope )))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::drawAirport
    #*  -------------------------------------------------------------------------------------------
    #*  draws the airport
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm - model manager
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawAirport ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::drawAirport"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._mm )
        assert ( self._srfScope )

        #** ---------------------------------------------------------------------------------------
        #*  cria o objeto viewAer
        #*/
        self._viewAer = viewAer.viewAer ( self._mm, self._tWH )
        assert ( self._viewAer )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o aerodromo em uma superficie
        #*/
        self._srfAer = self._viewAer.desenhaAerodromo ( self._bCircuit )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  posiciona o centro do aerodromo no centro do scope
        #*/
        l_tAerPos = self._srfAer.get_rect ()
        assert ( l_tAerPos )

        l_tAerPos.center = self._tScopeCtr

        #** ---------------------------------------------------------------------------------------
        #*  transfere o desenho do aerodromo para o scope
        #*/
        self._srfScope.blit ( self._srfAer, l_tAerPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::drawIndH14O
    #*  -------------------------------------------------------------------------------------------
    #*  desenha o indicativo de horizontalizacao (h14o)
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawIndH14O ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::drawIndH14O"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._srfScope )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cor de desenho do indicativo de horizontalizacao
        #*/
        l_tCor = locDefs.xCOR_RangeMark
        assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o indicativo de horizontalizacao em uma superficie
        #*/
        l_srfH14O = pygame.Surface ( self._tWH )
        assert ( l_srfH14O )

        l_srfH14O.set_colorkey ( l_srfH14O.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  desenha a lamina esquerda
        #*/
        l_tSeta = ( self._xSetaX, self._xSetaY - w_xRaio )

        #** ---------------------------------------------------------------------------------------
        #*  desenha a lamina esquerda
        #*/
        pygame.draw.line ( l_srfH14O, l_tCor, l_tSeta, ( self._xSetaX - 2, self._xSetaY - w_xRaioSeta ))

        #** ---------------------------------------------------------------------------------------
        #*  desenha o corpo da seta
        #*/
        pygame.draw.line ( l_srfH14O, l_tCor, l_tSeta, ( self._xSetaX, self._xSetaY ))

        #** ---------------------------------------------------------------------------------------
        #*  desenha a lamina direita
        #*/
        pygame.draw.line ( l_srfH14O, l_tCor, l_tSeta, ( self._xSetaX + 2, self._xSetaY - w_xRaioSeta ))

        #** ---------------------------------------------------------------------------------------
        #*  proa e horizontalizacao
        #*/
        l_tProa = ( 0.0, self._oAer.getDifDeclinacao ())
        assert ( l_tProa )

        #** ---------------------------------------------------------------------------------------
        #*  converte a proa em direcao (rad)
        #*/
        l_dRad = math.radians ( cineCalc.convProa2Direcao ( l_tProa ))

        #** ---------------------------------------------------------------------------------------
        #*/
        l_dCos = math.cos ( l_dRad )
        l_dSin = math.sin ( l_dRad )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_tSeta = ( self._xSetaX + ( w_xRaio * l_dCos ),
                    self._xSetaY - ( w_xRaio * l_dSin ))

        #** ---------------------------------------------------------------------------------------
        #*/
        l_iXSeta = self._xSetaX + ( w_xRaioSeta * l_dCos )
        l_iYSeta = self._xSetaY - ( w_xRaioSeta * l_dSin )

        #** ---------------------------------------------------------------------------------------
        #*  desenha a lamina esquerda
        #*/
        pygame.draw.line ( l_srfH14O, l_tCor, l_tSeta, ( l_iXSeta, l_iYSeta + 2 ))

        #** ---------------------------------------------------------------------------------------
        #*  desenha o corpo da seta
        #*/
        pygame.draw.line ( l_srfH14O, l_tCor, l_tSeta, ( self._xSetaX, self._xSetaY ))

        #** ---------------------------------------------------------------------------------------
        #*  desenha a lamina direita
        #*/
        pygame.draw.line ( l_srfH14O, l_tCor, l_tSeta, ( l_iXSeta, l_iYSeta - 2 ))

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto do indicativo
        #*/
        l_szTxt = "%.1f" % ( self._oAer.getDifDeclinacao ())
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte
        #*/
        l_font = pygame.font.Font ( glbDefs.xFNT_None, 12 )
        assert ( l_font )

        #** ---------------------------------------------------------------------------------------
        #*  cria o texto com o indicativo
        #*/
        l_szTxt = l_font.render ( l_szTxt, 1, l_tCor )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  make the horizontalization id stand under the arrows
        #*/
        l_txtPos = l_szTxt.get_rect ()
        assert ( l_txtPos )

        l_txtPos.center = ( self._xSetaX, self._xSetaY + l_txtPos.center [ 1 ] + 2 )

        #** ---------------------------------------------------------------------------------------
        #*  put the horizontalization id on the screen
        #*/
        l_srfH14O.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  posiciona o centro do indicativo de horizontalizacao no centro do scope
        #*/
        l_tHOPos = l_srfH14O.get_rect ()
        assert ( l_tHOPos )

        l_tHOPos.center = self._tScopeCtr

        #** ---------------------------------------------------------------------------------------
        #*  transfere o desenho do indicativo de horizontalizacao para o scope
        #*/
        self._srfScope.blit ( l_srfH14O, l_tHOPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::drawRangeMark
    #*  -------------------------------------------------------------------------------------------
    #*  draws the range mark
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawRangeMark ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::drawRangeMark"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._srfScope )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o range mark em uma superficie
        #*/
        l_srfRM = pygame.Surface ( self._tWH )
        assert ( l_srfRM )

        l_srfRM.set_colorkey ( l_srfRM.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  escala 1 ?
        #*/
        if ( 1 == self._oExe.getEscala ()):

            #** -----------------------------------------------------------------------------------
            #*  range marks a desenhar (em NM)
            #*/
            l_lstRM = [ 0.75, 1.0 ]

        #** ---------------------------------------------------------------------------------------
        #*  escala 2 ?
        #*/
        elif ( 2 == self._oExe.getEscala ()):

            #** -----------------------------------------------------------------------------------
            #*  range marks a desenhar (em NM)
            #*/
            l_lstRM = [ 1.0, 2.0, 3.0, 4.0 ]

        #** ---------------------------------------------------------------------------------------
        #*  escala 3 ?
        #*/
        elif ( 3 == self._oExe.getEscala ()):

            #** -----------------------------------------------------------------------------------
            #*  range marks a desenhar (em NM)
            #*/
            l_lstRM = [ 5.0, 7.5, 10.0, 12.5 ]

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cor de desenho do range mark
        #*/
        l_tCor = locDefs.xCOR_RangeMark
        assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  desenha os range marks
        #*/
        for l_iRM in xrange ( len ( l_lstRM )):

            #** -----------------------------------------------------------------------------------
            #*  raio de 'l_iRM' milhas nauticas
            #*/
            self.desenhaRangeMark ( l_srfRM, l_lstRM [ l_iRM ], l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  posiciona o centro do range mark no centro do scope
        #*/
        l_tRmkPos = l_srfRM.get_rect ()
        assert ( l_tRmkPos )

        l_tRmkPos.center = self._tScopeCtr

        #** ---------------------------------------------------------------------------------------
        #*  transfere o desenho do range mark para o scope
        #*/
        self._srfScope.blit ( l_srfRM, l_tRmkPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::drawRoseWind
    #*  -------------------------------------------------------------------------------------------
    #*  draws the range mark
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def drawRoseWind ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::drawRoseWind"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._srfScope )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o rose wind em uma superficie
        #*/
        l_srfRW = pygame.Surface ( self._tWH )
        assert ( l_srfRW )

        l_srfRW.set_colorkey ( l_srfRW.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cor de desenho do rose wind
        #*/
        l_tCor = locDefs.xCOR_RoseWind
        assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  calcula o raio do circulo
        #*/
        l_dRaio = self._tScopeCtr [ 0 ] - 10.

        #** ---------------------------------------------------------------------------------------
        #*  desenha o circulo/circunferencia na superficie
        #*/
        pygame.draw.circle ( l_srfRW, l_tCor, ( int ( self._tScopeCtr [ 0 ] ), int ( self._tScopeCtr [ 1 ] )), int ( l_dRaio ), 1 )

        #** ----------------------------------------------------------------------------------------
        #*  first set the 8 pontos cardeais
        #*/
        for l_iI in xrange ( 8 ):

           #** ------------------------------------------------------------------------------------
           #*  obtem a identificacao do rose wind
           #*/
           ( l_szName, l_crdPos ) = self._lstPtosCardeais [ l_iI ]

           #** ------------------------------------------------------------------------------------
           #*  calculate the screen pos
           #*/
           l_scrPos = (  l_crdPos [ 0 ] + self._tScopeCtr [ 0 ],
                        -l_crdPos [ 1 ] + self._tScopeCtr [ 1 ] )
           assert ( l_scrPos )

           #** ------------------------------------------------------------------------------------
           #*  cria o texto com a identificacao do rose wind
           #*/
           l_szTxt = self._font.render ( l_szName, 1, l_tCor )
           assert ( l_szTxt )

           #** ------------------------------------------------------------------------------------
           #*  make the text stand under the line
           #*/
           l_txtPos = l_szTxt.get_rect ()
           assert ( l_txtPos )

           l_txtPos.center = l_scrPos

           #** ------------------------------------------------------------------------------------
           #*  put the text on the screen
           #*/
           l_srfRW.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  posiciona o centro do rose wind no centro do scope
        #*/
        l_tRWPos = l_srfRW.get_rect ()
        assert ( l_tRWPos )

        l_tRWPos.center = self._tScopeCtr

        #** ---------------------------------------------------------------------------------------
        #*  transfere o desenho do rose wind para o scope
        #*/
        self._srfScope.blit ( l_srfRW, l_tRWPos )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::genPontosCardeais
    #*  -------------------------------------------------------------------------------------------
    #*  gera a lista de pontos cardeais
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def genPontosCardeais ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::genPontosCardeais"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execucao
        #*/
        assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  set the alphabet to create points
        #*/
        l_lstPCardsName = ( 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW' )

        #** ---------------------------------------------------------------------------------------
        #*  lista de pontos cardeais
        #*/
        l_lstPCards = []

        #** ---------------------------------------------------------------------------------------
        #*  calcula o raio
        #*/
        l_dRaio = self._tScopeCtr [ 0 ] - 5.

        #** ---------------------------------------------------------------------------------------
        #*  insert the eight out-zone points
        #*/
        for l_iI in xrange ( 8 ):

            #** -----------------------------------------------------------------------------------
            #*  calcula o angulo dos pontos cardeais
            #*/
            l_dAng = math.radians (( l_iI * 45. ) + self._oAer.getDifDeclinacao ())

            #** -----------------------------------------------------------------------------------
            #*  calcula a posicao dos pontos cardeais
            #*/
            l_crdPos = ( l_dRaio * math.sin ( l_dAng ), l_dRaio * math.cos ( l_dAng ))
            assert ( l_crdPos )

            #** -----------------------------------------------------------------------------------
            #*  coloca na lista de pontos cardeais
            #*/
            l_lstPCards.append (( l_lstPCardsName [ l_iI ], l_crdPos ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna a lista de pontos cardeais
        #*/
        return ( l_lstPCards )

    #** ===========================================================================================
    #*  acesso a area de dados do objeto
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::getSrfAer
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getSrfAer ( self ):

        #// nome do metodo (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::getSrfAer"


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
        #*/
        return ( self._srfAer )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::getViewAer
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getViewAer ( self ):

        #// nome do metodo (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::getViewAer"


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
        #*/
        return ( self._viewAer )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::toggleCircuit
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def toggleCircuit ( self ):

        #// nome do metodo (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::toggleCircuit"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        #assert ( type ( True ) == type ( f_bVal ))

        #** ---------------------------------------------------------------------------------------
        #*  toggle range mark flag 
        #*/
        self._bCircuit = not self._bCircuit
        #l_log.info ( "Circuit: " + str ( self._bCircuit ))

        #** ---------------------------------------------------------------------------------------
        #*  redraws entire scope
        #*/
        self.doRedraw ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::toggleRangeMark
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def toggleRangeMark ( self ):

        #// nome do metodo (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::toggleRangeMark"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        #assert ( type ( True ) == type ( f_bVal ))

        #** ---------------------------------------------------------------------------------------
        #*  toggle range mark flag 
        #*/
        self._bRangeMark = not self._bRangeMark
        #l_log.info ( "RangeMark: " + str ( self._bRangeMark ))

        #** ---------------------------------------------------------------------------------------
        #*  redraws entire scope
        #*/
        self.doRedraw ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiScope::toggleRoseWind
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def toggleRoseWind ( self ):

        #// nome do metodo (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiScope::toggleRoseWind"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        #assert ( type ( True ) == type ( f_bVal ))

        #** ---------------------------------------------------------------------------------------
        #*  toggle rose wind flag 
        #*/
        self._bRoseWind = not self._bRoseWind
        #l_log.info ( "RoseWind: " + str ( self._bRoseWind ))

        #** ---------------------------------------------------------------------------------------
        #*  redraws entire scope
        #*/
        self.doRedraw ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "guiScope" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** ----------------------------------------------------------------------------------------------- *#
