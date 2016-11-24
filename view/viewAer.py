#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 1997, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: viewAer
#*
#*  Descrição: _
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/jun/20  version started
#*  mlabru   2008/jun/20  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versao
#*  -----------------------------------------------------------------------------------------------
#*  start    1997/jun/20  version started
#*  1.2-0.1  2008/jun/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ math library
#/ ------------------------------------------------------------------------------------------------
import math

#/ log4Py
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca gráfica)
#/ ------------------------------------------------------------------------------------------------
import pygame
from pygame.locals import *

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineCalc as cineCalc
import model.clsCab as clsCab
import model.clsPst as clsPst

import model.glbDefs as glbDefs
import model.locDefs as locDefs

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.viewUtils as viewUtils

#** -----------------------------------------------------------------------------------------------
#*  defines
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  viewAer::viewAer
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class viewAer:

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm  - model manager
    #*  @param  f_tWH - tupla com largura e altura do scope
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_mm, f_tWH ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_mm )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o exercício
        #*/
        self._oExe = f_mm.getExercicio ()
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o aeródromo
        #*/
        self._oAer = f_mm.getAerodromo ()
        assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  cria o canvas de aeródromo
        #*/
        self._srfAer = pygame.Surface ( f_tWH )
        self._srfAer.fill ( locDefs.xCOR_Aer )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaAerodromo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaAerodromo ( self, f_bCircuit ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaAerodromo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._oExe )
        
        #** ---------------------------------------------------------------------------------------
        #*  define a escala do cenario
        #*/
        viewUtils.escalaCenario ( self._oExe, self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  configura a janela de apresentação
        #*/
        viewUtils.setWindow ( self._oAer.getJanelaXInf (),
                              self._oAer.getJanelaXSup (),
                              self._oAer.getJanelaYInf (),
                              self._oAer.getJanelaYSup ())

        #** ---------------------------------------------------------------------------------------
        #*  configura o viewport
        #*/
        viewUtils.setViewport ( locDefs.xVWP_Inf_X,
                                locDefs.xVWP_Sup_X,
                                locDefs.xVWP_Inf_Y,
                                locDefs.xVWP_Sup_Y )

        #** ---------------------------------------------------------------------------------------
        #*  para todas figuras do aeródromo...
        #*/
        for l_Fig in self._oAer.getFiguras ():

            #** -----------------------------------------------------------------------------------
            #*/
            assert ( l_Fig )
            
            #** -----------------------------------------------------------------------------------
            #*  ponto ?
            #*/
            if ( locDefs.xFIG_PONTO == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  ponto
                #*/
                self.desenhaPonto ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  poligono ?
            #*/
            elif ( locDefs.xFIG_POLIGONO == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  poligono
                #*/
                self.desenhaPoligono ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  circunferencia ?
            #*/
            elif ( locDefs.xFIG_CIRCUNFERENCIA == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  circunferencia
                #*/
                if ( 1 == self._oExe.getEscala ()):

                    self.desenhaCirculo ( l_Fig, 0 )

            #** -----------------------------------------------------------------------------------
            #*  circulo ?
            #*/
            elif ( locDefs.xFIG_CIRCULO == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  círculo
                #*/
                if ( 1 == self._oExe.getEscala ()):

                    self.desenhaCirculo ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  linha ?
            #*/
            elif ( locDefs.xFIG_LINHA == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  linha
                #*/
                if ( 1 == self._oExe.getEscala ()):

                    self.desenhaLinha ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  NDB ?
            #*/
            elif ( locDefs.xFIG_NDB == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  NDB ( VOR, NDB e Fixo não devem aparecer na tela do Controlador )
                #*/
                self.desenhaNDB ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  VOR ?
            #*/
            elif ( locDefs.xFIG_VOR == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  VOR ( VOR, NDB e Fixo não devem aparecer na tela do Controlador )
                #*/
                self.desenhaVOR ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  fixo ?
            #*/
            elif ( locDefs.xFIG_FIXO == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  fixo ( VOR, NDB e Fixo não devem aparecer na tela do Controlador )
                #*/
                self.desenhaFixo ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  obstaculo ?
            #*/
            elif ( locDefs.xFIG_OBSTACULO == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  obstaculo
                #*/
                self.desenhaObstaculo ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  linhas de cabeceira ?
            #*/
            elif ( locDefs.xFIG_LINHAS_CABEC == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  linhas de cabeceira
                #*/
                if ( 1 == self._oExe.getEscala ()):

                    self.desenhaLinhasCabec ( l_Fig )

            #** -----------------------------------------------------------------------------------
            #*  linhas de pista ?
            #*/
            elif ( locDefs.xFIG_LINHA_PISTA == l_Fig.getTipo ()):

                #** -------------------------------------------------------------------------------
                #*  linha de pista
                #*/
                if ( 1 == self._oExe.getEscala ()):

                    self.desenhaLinhaPista ( l_Fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica se está na escala 1
        #*/
        if ( 1 == self._oExe.getEscala ()):

            #** -----------------------------------------------------------------------------------
            #*  desenha pontos no solo
            #*/
            self.desenhaPontosNoSolo ()

        #** ---------------------------------------------------------------------------------------
        #*  senão, não esta na escala 1
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  desenha circuitos de trafego ?
            #*/
            if ( f_bCircuit ):

                #** -------------------------------------------------------------------------------
                #*  desenha os circuitos de trafego
                #*/
                self.desenhaCircuitos ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna uma superficie com o aeródromo desenhado
        #*/
        return ( self._srfAer )

    #** -------------------------------------------------------------------------------------------
    #*  desenhaCircuitos
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaCircuitos ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaCircuitos"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  para todoas as pistas do aeródromo...
        #*/
        for l_oPst in self._oAer.getPistas ():

            #** -----------------------------------------------------------------------------------
            #*/
            assert ( l_oPst )
            assert ( isinstance ( l_oPst, clsPst.clsPst ))

            #** -----------------------------------------------------------------------------------
            #*  para todas os circuitos da pista...
            #*/
            for l_oCkt in l_oPst.getPstCkts ():

                #** -------------------------------------------------------------------------------
                #*/
                assert ( l_oCkt )
                assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

                #** -------------------------------------------------------------------------------
                #*  lista de vertices do circuito
                #*/
                l_lstPos = []

                #** -------------------------------------------------------------------------------
                #*  para todos os segmentos deste circuito...
                #*/
                for l_oSeg in l_oCkt.getCktSegs ():
                    
                    #** ---------------------------------------------------------------------------
                    #*/
                    assert ( l_oSeg )
                    assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

                    #** ---------------------------------------------------------------------------
                    #*  obtem a posição inicial do segmento
                    #*/
                    l_tPos = l_oSeg._tSegIni
                    assert ( l_tPos ) 

                    #l_log.info ( "_tSegIni: " + str ( l_oSeg._tSegIni ))

                    #** ---------------------------------------------------------------------------
                    #*  coloca as coordenadas no range (0, 1) (normaliza)
                    #*/
                    l_tPos = viewUtils.normalizeXY ( l_tPos )
                    assert ( l_tPos )

                    #** ---------------------------------------------------------------------------
                    #*  converte para coordenadas de dispositivo
                    #*/
                    l_tPos = viewUtils.scale2Device ( l_tPos )
                    assert ( l_tPos )

                    #** ---------------------------------------------------------------------------
                    #*  acrescenta o ponto ao poligono
                    #*/
                    l_lstPos.append ( l_tPos )
                    #l_log.info ( "l_tPos: " + str ( l_tPos ))

                #** ---------------------------------------------------------------------------
                #*  obtem a cor do circuito
                #*/
                l_tCor = locDefs.xCOR_Circuito

                #** ---------------------------------------------------------------------------
                #*  desenha um linha unindo estes dois pontos
                #*/
                pygame.draw.polygon ( self._srfAer, l_tCor, l_lstPos, 1 )

            #** ----------------------------------------------------------------------------------
            #*  obtem a cabeceira da pista
            #*/
            l_oCab = l_oPst.getPstCab ( 0 )
            assert ( l_oCab )

            #** -----------------------------------------------------------------------------------
            #*  obtem o inicio da final da cabeceira da pista
            #*/
            l_tIni = l_oCab._tFinalIni
            assert ( l_tIni )

            #l_log.info ( "l_tIni(1): " + str ( l_tIni ))

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tIni = viewUtils.normalizeXY ( l_tIni )
            assert ( l_tIni )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tIni = viewUtils.scale2Device ( l_tIni )
            assert ( l_tIni )

            #l_log.info ( "l_tIni(2): " + str ( l_tIni ))

            #** -----------------------------------------------------------------------------------
            #*  obtem a cabeceira oposta da pista
            #*/
            l_oCab = l_oPst.getPstCab ( 1 )
            assert ( l_oCab )

            #** -----------------------------------------------------------------------------------
            #*  obtem o inicio da final da cabeceira oposta da pista
            #*/
            l_tFim = l_oCab._tFinalIni
            assert ( l_tFim )

            #l_log.info ( "l_tFim(1): " + str ( l_tFim ))

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tFim = viewUtils.normalizeXY ( l_tFim )
            assert ( l_tFim )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tFim = viewUtils.scale2Device ( l_tFim )
            assert ( l_tFim )

            #l_log.info ( "l_tFim(2): " + str ( l_tFim ))

            #** -----------------------------------------------------------------------------------
            #*  obtem a cor do circuito
            #*/
            l_tCor = locDefs.xCOR_Circuito

            #** -----------------------------------------------------------------------------------
            #*  desenha um linha unindo estes dois pontos
            #*/
            pygame.draw.line ( self._srfAer, l_tCor, l_tIni, l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaCirculo
    #*  -------------------------------------------------------------------------------------------
    #*  desenha circulo (no fill) ou circunferencia (filled)
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_fill - 0 = com preenchimento (circunferencia)
    #*                   1 = sem preenchimento (circulo)
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaCirculo ( self, f_fig, f_fill = 1 ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaCirculo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto central do circulo
        #*/
        l_tCtr = f_fig.getCtr ()
        assert ( l_tCtr )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto na borda do circulo
        #*/
        l_ptoBdr = ( l_tCtr [ 0 ] + f_fig.getRaio (), l_tCtr [ 1 ] )
        assert ( l_ptoBdr )

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
        l_ptoBdr = viewUtils.normalizeXY ( l_ptoBdr )
        assert ( l_ptoBdr )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_ptoBdr = viewUtils.scale2Device ( l_ptoBdr )
        assert ( l_ptoBdr )

        #** ---------------------------------------------------------------------------------------
        #*  calcula o raio do circulo nas novas coordenadas
        #*/
        l_iRaio = int ( round ( l_ptoBdr [ 0 ] - l_tCtr [ 0 ] ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cor da figura
        #*/
        l_tCor = viewUtils.getCor ( f_fig.getCor ())
        assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o circulo/circunferencia na superficie
        #*/
        pygame.draw.circle ( self._srfAer, l_tCor, l_tCtr, l_iRaio, f_fill )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaFixo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaFixo ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaFixo"

        #/ space to hold datapoints
        #/ ----------------------------------------------------------------------------------------
        l_atPoly = []


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto de inicio do Fixo
        #*/
        l_tIni = f_fig.getIni ()

        #** ---------------------------------------------------------------------------------------
        #*  verifica se esta na area visivel da tela
        #*/
        if ( viewUtils.checkClippingAer ( self._oAer, l_tIni, 40.0 )):

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tIni = viewUtils.normalizeXY ( l_tIni )
            assert ( l_tIni )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tIni = viewUtils.scale2Device ( l_tIni )
            assert ( l_tIni )

            #** -----------------------------------------------------------------------------------
            #*  monta o poligono
            #*/
            l_atPoly.append (( int ( round ( l_tIni [ 0 ] )),     int ( round ( l_tIni [ 1 ] ))))
            l_atPoly.append (( int ( round ( l_tIni [ 0 ] - 6 )), int ( round ( l_tIni [ 1 ] ))))
            l_atPoly.append (( int ( round ( l_tIni [ 0 ] - 3 )), int ( round ( l_tIni [ 1 ] - 6 ))))

            #** -----------------------------------------------------------------------------------
            #*  obtem a cor da figura
            #*/
            l_tCor = viewUtils.getCor ( f_fig.getCor ())
            assert ( l_tCor )

            #** -----------------------------------------------------------------------------------
            #*  desenha o poligono
            #*/
            pygame.draw.polygon ( self._srfAer, l_tCor, l_atPoly )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaLinha
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaLinha ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaLinha"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto de inicio da linha
        #*/
        l_tIni = f_fig.getIni ()
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tIni = viewUtils.normalizeXY ( l_tIni )
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tIni = viewUtils.scale2Device ( l_tIni )
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto final da linha
        #*/
        l_tFim = f_fig.getFim ()
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tFim = viewUtils.normalizeXY ( l_tFim )
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tFim = viewUtils.scale2Device ( l_tFim )
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cor da figura
        #*/
        l_tCor = viewUtils.getCor ( f_fig.getCor ())
        assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  desenha a linha na superficie
        #*/
        pygame.draw.line ( self._srfAer, l_tCor, l_tIni, l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaLinhasCabec
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaLinhasCabec ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaLinhasCabec"

        #/ space to hold datapoints
        #/ ----------------------------------------------------------------------------------------
        l_dXi = range ( 4 )
        l_dXf = range ( 4 )
        l_dYi = range ( 4 )
        l_dYf = range ( 4 )


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto de inicio da linha de cabeceira
        #*/
        l_tIni = f_fig.getIni ()
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto final da linha de cabeceira
        #*/
        l_tFim = f_fig.getFim ()
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_dX = l_tFim [ 0 ] - l_tIni [ 0 ]
        l_dY = l_tFim [ 1 ] - l_tIni [ 1 ]

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( 0.0 != l_dX ):

            l_dTeta = math.atan ( l_dY / l_dX )

        else:

            l_dTeta = math.pi / 2

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( 0.0 != l_dTeta ):

            #** -----------------------------------------------------------------------------------
            #*/
            l_dDist = cineCalc.distanciaEntrePontos ( l_tIni, l_tFim )

            #** -----------------------------------------------------------------------------------
            #*/
            l_dAlfa = math.atan ( 15.0 / l_dDist )
            l_dDAux = math.sqrt ( 225.0 + ( l_dDist * l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*/
            l_dXf [ 0 ] = l_tIni [ 0 ] + ( l_dDAux * math.cos ( l_dTeta + l_dAlfa ))
            l_dYf [ 0 ] = l_tIni [ 1 ] + ( l_dDAux * math.sin ( l_dTeta + l_dAlfa ))
            l_dXf [ 3 ] = l_tIni [ 0 ] + ( l_dDAux * math.cos ( l_dTeta - l_dAlfa ))
            l_dYf [ 3 ] = l_tIni [ 1 ] + ( l_dDAux * math.sin ( l_dTeta - l_dAlfa ))

            #** -----------------------------------------------------------------------------------
            #*/
            l_dXi [ 0 ] = l_dXf [ 0 ] - l_dX
            l_dYi [ 0 ] = l_dYf [ 0 ] - l_dY
            l_dXi [ 3 ] = l_dXf [ 3 ] - l_dX
            l_dYi [ 3 ] = l_dYf [ 3 ] - l_dY

            #** -----------------------------------------------------------------------------------
            #*/
            l_dAlfa = math.atan ( 10.0 / l_dDist )
            l_dDAux = math.sqrt ( 100.0 + ( l_dDist * l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*/
            l_dXf [ 1 ] = l_tIni [ 0 ] + ( l_dDAux * math.cos ( l_dTeta + l_dAlfa ))
            l_dYf [ 1 ] = l_tIni [ 1 ] + ( l_dDAux * math.sin ( l_dTeta + l_dAlfa ))
            l_dXf [ 2 ] = l_tIni [ 0 ] + ( l_dDAux * math.cos ( l_dTeta - l_dAlfa ))
            l_dYf [ 2 ] = l_tIni [ 1 ] + ( l_dDAux * math.sin ( l_dTeta - l_dAlfa ))

            #** -----------------------------------------------------------------------------------
            #*/
            l_dXi [ 1 ] = l_dXf [ 1 ] - l_dX
            l_dYi [ 1 ] = l_dYf [ 1 ] - l_dY
            l_dXi [ 2 ] = l_dXf [ 2 ] - l_dX
            l_dYi [ 2 ] = l_dYf [ 2 ] - l_dY

        #** ---------------------------------------------------------------------------------------
        #*  senão, l_dTeta = 0.0
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            l_dYi [ 0 ] = l_tIni [ 1 ] + 15.0
            l_dYi [ 1 ] = l_tIni [ 1 ] + 10.0
            l_dYi [ 2 ] = l_tIni [ 1 ] - 10.0
            l_dYi [ 3 ] = l_tIni [ 1 ] - 15.0

            #** -----------------------------------------------------------------------------------
            #*/
            for l_iI in xrange ( 4 ):

                #** -------------------------------------------------------------------------------
                #*/
                l_dXi [ l_iI ] = l_tIni [ 0 ]
                l_dXf [ l_iI ] = l_tFim [ 0 ]
                l_dYf [ l_iI ] = l_dYi [ l_iI ]

        #** ---------------------------------------------------------------------------------------
        #*/
        for l_iI in xrange ( 4 ):

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            ( l_dXi [ l_iI ], l_dYi [ l_iI ] ) = viewUtils.normalizeXY (( l_dXi [ l_iI ], l_dYi [ l_iI ] ))

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            ( l_dXi [ l_iI ], l_dYi [ l_iI ] ) = viewUtils.scale2Device (( l_dXi [ l_iI ], l_dYi [ l_iI ] ))

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            ( l_dXf [ l_iI ], l_dYf [ l_iI ] ) = viewUtils.normalizeXY (( l_dXf [ l_iI ], l_dYf [ l_iI ] ))

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            ( l_dXf [ l_iI ], l_dYf [ l_iI ] ) = viewUtils.scale2Device (( l_dXf [ l_iI ], l_dYf [ l_iI ] ))

            #** -----------------------------------------------------------------------------------
            #*/
            pygame.draw.line ( self._srfAer, glbDefs.xCOR_white,
                               ( int ( round ( l_dXi [ l_iI ] )), int ( round ( l_dYi [ l_iI ] ))),
                               ( int ( round ( l_dXf [ l_iI ] )), int ( round ( l_dYf [ l_iI ] ))))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaLinhaPista
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaLinhaPista ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaLinhaPista"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto de inicio da linha de pista
        #*/
        l_tIni = f_fig.getIni ()
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tIni = viewUtils.normalizeXY ( l_tIni )
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tIni = viewUtils.scale2Device ( l_tIni )
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto final da linha de pista
        #*/
        l_tFim = f_fig.getFim ()
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  coloca as coordenadas no range (0, 1) (normaliza)
        #*/
        l_tFim = viewUtils.normalizeXY ( l_tFim )
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  converte para coordenadas de dispositivo
        #*/
        l_tFim = viewUtils.scale2Device ( l_tFim )
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cor da figura
        #*/
        #l_tCor = viewUtils.getCor ( f_fig.getCor ())
        #assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  set um pixel em...
        #*/
        self._srfAer.set_at (( int ( l_tFim [ 0 ] ), int ( l_tFim [ 1 ] )), glbDefs.xCOR_black )

        #** ---------------------------------------------------------------------------------------
        #*  divide-se por 29 para se obter 15 segmentos desenhados e 14 em branco
        #*/
        l_dCompX = ( l_tFim [ 0 ] - l_tIni [ 0 ] ) / 29.0
        l_dCompY = ( l_tFim [ 1 ] - l_tIni [ 1 ] ) / 29.0

        #** ---------------------------------------------------------------------------------------
        #*/
        l_tFim = ( int ( round ( l_tIni [ 0 ] + l_dCompX )),
                   int ( round ( l_tIni [ 1 ] + l_dCompY )))

        #** ---------------------------------------------------------------------------------------
        #*  todos os pontos sao tirados em relação ao ponto inicial, de modo a
        #*  não propagar erro de arredondamento
        #*/
        pygame.draw.line ( self._srfAer, glbDefs.xCOR_white, l_tIni, l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*/
        for l_iI in xrange ( 14 ):

            #** -----------------------------------------------------------------------------------
            #*/
            l_dXi = l_tIni [ 0 ] + ( 2.0 * l_iI * l_dCompX )
            l_dYi = l_tIni [ 1 ] + ( 2.0 * l_iI * l_dCompY )

            #** -----------------------------------------------------------------------------------
            #*/
            l_dXf = l_dXi + l_dCompX
            l_dYf = l_dYi + l_dCompY

            #** -----------------------------------------------------------------------------------
            #*/
            pygame.draw.line ( self._srfAer, glbDefs.xCOR_white,
                               ( int ( round ( l_dXi )), int ( round ( l_dYi ))),
                               ( int ( round ( l_dXf )), int ( round ( l_dYf ))))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaNDB
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaNDB ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaNDB"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto central do NDB
        #*/
        l_tCtr = f_fig.getCtr ()

        #** ---------------------------------------------------------------------------------------
        #*  verifica se esta na area visivel da tela
        #*/
        if ( viewUtils.checkClippingAer ( self._oAer, l_tCtr, 40.0 )):

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tCtr = viewUtils.normalizeXY ( l_tCtr )
            assert ( l_tCtr )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tCtr = viewUtils.scale2Device ( l_tCtr )
            assert ( l_tCtr )

            #** -----------------------------------------------------------------------------------
            #*/
            l_dRaio = 3.0

            #** -----------------------------------------------------------------------------------
            #*/
            l_tCor = viewUtils.getCor ( f_fig.getCor ())
            assert ( l_tCor )

            #** -----------------------------------------------------------------------------------
            #*/
            pygame.draw.circle ( self._srfAer, l_tCor, l_tCtr, int ( round ( l_dRaio )))

            #** -----------------------------------------------------------------------------------
            #*/
            for l_iI in xrange ( 12 ):

                #** -------------------------------------------------------------------------------
                #*/
                for l_iK in xrange ( 3 ):

                    #** ---------------------------------------------------------------------------
                    #*/
                    l_dX2 = l_tCtr [ 0 ] + ( l_dRaio + l_iK ) * math.cos ( l_iI * math.pi / 6.0 )
                    l_dY2 = l_tCtr [ 1 ] + ( l_dRaio + l_iK ) * math.sin ( l_iI * math.pi / 6.0 )

                    #** ---------------------------------------------------------------------------
                    #*/
                    self._srfAer.set_at (( int ( round ( l_dX2 )), int ( round ( l_dY2 ))), l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaObstaculo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaObstaculo ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaObstaculo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto central do obstaculo
        #*/
        l_tCtr = f_fig.getCtr ()
        assert ( l_tCtr )

        #** ---------------------------------------------------------------------------------------
        #*  verifica se esta na area visivel da tela
        #*/
        if ( viewUtils.checkClippingAer ( self._oAer, l_tCtr, 40.0 )):

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tCtr = viewUtils.normalizeXY ( l_tCtr )
            assert ( l_tCtr )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tCtr = viewUtils.scale2Device ( l_tCtr )
            assert ( l_tCtr )

            #** -----------------------------------------------------------------------------------
            #*/
            l_tCor = viewUtils.getCor ( f_fig.getCor ())
            assert ( l_tCtr )

            #** -----------------------------------------------------------------------------------
            #*/
            pygame.draw.line ( self._srfAer, l_tCor, l_tCtr,
                               ( int ( round ( l_tCtr [ 0 ] - 3 )), int ( round ( l_tCtr [ 1 ] + 6 ))))

            pygame.draw.line ( self._srfAer, l_tCor, l_tCtr,
                               ( int ( round ( l_tCtr [ 0 ] + 3 )), int ( round ( l_tCtr [ 1 ] + 6 ))))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaPoligono
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaPoligono ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaPoligono"

        #/ space to hold datapoints
        #/ ----------------------------------------------------------------------------------------
        l_atPoly = []


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*/
        #l_log.info ( "f_fig: " + str ( f_fig ))
        #l_log.info ( "f_fig.getPoligonoVert: [%d]" % f_fig.getPolyNVert ())

        #** ---------------------------------------------------------------------------------------
        #*/
        for l_tVert in f_fig.getPoly ():

            #** -----------------------------------------------------------------------------------
            #*/
            assert ( l_tVert )

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tVert = viewUtils.normalizeXY ( l_tVert )
            assert ( l_tVert )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tVert = viewUtils.scale2Device ( l_tVert )
            assert ( l_tVert )

            #** -----------------------------------------------------------------------------------
            #*/
            l_atPoly.append ( l_tVert )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_tCor = viewUtils.getCor ( f_fig.getCor ())

        #** ---------------------------------------------------------------------------------------
        #*/
        pygame.draw.polygon ( self._srfAer, l_tCor, l_atPoly )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaPonto
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaPonto ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaPonto"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  obtem as coordenadas do ponto
        #*/
        l_tCtr = f_fig.getCtr ()
        assert ( l_tCtr )

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
        #*  obtem a cor da figura
        #*/
        l_tCor = viewUtils.getCor ( f_fig.getCor ())
        assert ( l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  desenha o ponto na superficie
        #*/
        self._srfAer.set_at ( ( int ( l_tCtr [ 0 ] ), int ( l_tCtr [ 1 ] )), l_tCor )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaPontosNoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaPontosNoSolo ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaPontosNoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte
        #*/
        #self._font = pygame.font.Font ( glbDefs.xFNT_None, 10 )
        #assert ( self._font )

        #** ---------------------------------------------------------------------------------------
        #*  plotar todos os pontos de decolagem
        #*/
        for l_oPst in self._oAer.getPistas ():

            #** -----------------------------------------------------------------------------------
            #*/
            assert ( l_oPst )
            assert ( isinstance ( l_oPst, clsPst.clsPst ))

            #** -----------------------------------------------------------------------------------
            #*  para todas as cabeceiras de pista...
            #*/
            for l_oCab in l_oPst.getPstCabs ():

                #** -------------------------------------------------------------------------------
                #*/
                assert ( l_oCab )
                assert ( isinstance ( l_oCab, clsCab.clsCab ))

                #l_iPto = 0
                
                #** -------------------------------------------------------------------------------
                #*  para todos os pontos de decolagem desta cabeceira...
                #*/
                for l_tDec in l_oCab.getCabPontosDep ():
                    
                    #** ---------------------------------------------------------------------------
                    #*/
                    assert ( l_tDec )

                    #** ---------------------------------------------------------------------------
                    #*  coloca as coordenadas no range (0, 1) (normaliza)
                    #*/
                    l_tPto = viewUtils.normalizeXY ( l_tDec )
                    assert ( l_tPto )

                    #** ---------------------------------------------------------------------------
                    #*  converte para coordenadas de dispositivo
                    #*/
                    l_tPto = viewUtils.scale2Device ( l_tPto )
                    assert ( l_tPto )

                    #** ---------------------------------------------------------------------------
                    #*  cores dos pontos = vermelho
                    #*/
                    self._srfAer.set_at (( int ( l_tPto [ 0 ] ), int ( l_tPto [ 1 ] )), glbDefs.xCOR_red )

                    #** ---------------------------------------------------------------------------
                    #*  desenha o circulo/circunferencia na superficie
                    #*/
                    pygame.draw.circle ( self._srfAer, glbDefs.xCOR_red, ( int ( l_tPto [ 0 ] ), int ( l_tPto [ 1 ] )), 2, 0 )

                    #** ---------------------------------------------------------------------------
                    #*  cria o texto do pontos de decolagem
                    #*/
                    #l_szTxt = "D%d" % ( l_iPto )
                    #assert ( l_szTxt )

                    #** ---------------------------------------------------------------------------
                    #*  cria o texto com o pontos de decolagem
                    #*/
                    #l_szTxt = self._font.render ( l_szTxt, 1, glbDefs.xCOR_red )
                    #assert ( l_szTxt )

                    #** ---------------------------------------------------------------------------
                    #*  make the pontos de decolagem id stand under
                    #*/
                    #l_txtPos = l_szTxt.get_rect ()
                    #assert ( l_txtPos )

                    #l_txtPos.center = l_tPto

                    #** ---------------------------------------------------------------------------
                    #*  put the pontos de decolagem id on the screen
                    #*/
                    #self._srfAer.blit ( l_szTxt, l_txtPos )

                    #l_iPto += 1
                    
        #l_iPto = 0 

        #** ---------------------------------------------------------------------------------------
        #*  plotar todos os pontos definidos no solo
        #*/
        for l_oPNS in self._oAer.getPontosNoSolo ():

            #** -----------------------------------------------------------------------------------
            #*  obtem a posição do ponto no solo
            #*/
            l_tPto = l_oPNS.getPos ()
            assert ( l_tPto )

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tPto = viewUtils.normalizeXY ( l_tPto )
            assert ( l_tPto )

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tPto = viewUtils.scale2Device ( l_tPto )
            assert ( l_tPto )

            #** -----------------------------------------------------------------------------------
            #*  cores dos pontos = preto
            #*/
            self._srfAer.set_at (( int ( l_tPto [ 0 ] ), int ( l_tPto [ 1 ] )), glbDefs.xCOR_black )

            #** -----------------------------------------------------------------------------------
            #*  desenha o circulo/circunferencia na superficie
            #*/
            pygame.draw.circle ( self._srfAer, glbDefs.xCOR_black, ( int ( l_tPto [ 0 ] ), int ( l_tPto [ 1 ] )), 2, 0 )

            #** -----------------------------------------------------------------------------------
            #*  cria o texto do ponto no solo
            #*/
            #l_szTxt = "P%d" % ( l_iPto )
            #assert ( l_szTxt )

            #** -----------------------------------------------------------------------------------
            #*  cria o texto com o ponto no solo
            #*/
            #l_szTxt = self._font.render ( l_szTxt, 1, glbDefs.xCOR_darkblue )
            #assert ( l_szTxt )

            #** -----------------------------------------------------------------------------------
            #*  make the ponto no solo id stand under
            #*/
            #l_txtPos = l_szTxt.get_rect ()
            #assert ( l_txtPos )

            #l_txtPos.center = l_tPto

            #** -----------------------------------------------------------------------------------
            #*  put the ponto no solo id on the screen
            #*/
            #self._srfAer.blit ( l_szTxt, l_txtPos )

            #l_iPto += 1
            
        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  viewAer::desenhaVOR
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def desenhaVOR ( self, f_fig ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "viewAer::desenhaVOR"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fig )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._oAer )
        assert ( self._srfAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o ponto central do VOR
        #*/
        l_tCtr = f_fig.getCtr ()
        assert ( l_tCtr ) 
      
        #** ---------------------------------------------------------------------------------------
        #*  verifica se esta na area visivel da tela
        #*/
        if ( viewUtils.checkClippingAer ( self._oAer, l_tCtr, 40.0 )):

            #** -----------------------------------------------------------------------------------
            #*  coloca as coordenadas no range (0, 1) (normaliza)
            #*/
            l_tCtr = viewUtils.normalizeXY ( l_tCtr )
            assert ( l_tCtr )  

            #** -----------------------------------------------------------------------------------
            #*  converte para coordenadas de dispositivo
            #*/
            l_tCtr = viewUtils.scale2Device ( l_tCtr )
            assert ( l_tCtr )  

            #** -----------------------------------------------------------------------------------
            #*/
            l_dRaio = 3.0

            #** -----------------------------------------------------------------------------------
            #*  obtem a cor do VOR
            #*/
            l_tCor = viewUtils.getCor ( f_fig.getCor ())
            assert ( l_tCor )

            #** -----------------------------------------------------------------------------------
            #*  plota um ponto no centro do VOR
            #*/
            self._srfAer.set_at (( int ( l_tCtr [ 0 ] ), int ( l_tCtr [ 1 ] )), l_tCor )

            #** -----------------------------------------------------------------------------------
            #*/
            l_dX2 = l_tCtr [ 0 ] + l_dRaio
            l_dY2 = l_tCtr [ 1 ]

            #** -----------------------------------------------------------------------------------
            #*/
            for l_iI in xrange ( 4 ):

                #** -------------------------------------------------------------------------------
                #*/
                l_dX3 = l_tCtr [ 0 ] + l_dRaio * math.cos ( l_iI * math.pi / 3.0 )
                l_dY3 = l_tCtr [ 1 ] + l_dRaio * math.sin ( l_iI * math.pi / 3.0 )

                #** -------------------------------------------------------------------------------
                #*/
                pygame.draw.line ( self._srfAer, l_tCor,
                                   ( int ( round ( l_dX2 )), int ( round ( l_dY2 ))),
                                   ( int ( round ( l_dX3 )), int ( round ( l_dY3 ))))

                #** -------------------------------------------------------------------------------
                #*/
                l_dX2 = l_dX3
                l_dY2 = l_dY3

            #** -----------------------------------------------------------------------------------
            #*/
            l_dX3 = l_tCtr [ 0 ] + l_dRaio
            l_dY3 = l_tCtr [ 1 ]

            #** -----------------------------------------------------------------------------------
            #*/
            pygame.draw.line ( self._srfAer, l_tCor, ( int ( round ( l_dX2 )), int ( round ( l_dY2 ))),
                                                     ( int ( round ( l_dX3 )), int ( round ( l_dY3 ))))

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
logger = logging.getLogger ( "viewAer" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
