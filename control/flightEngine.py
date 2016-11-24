#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SICAD
#*  Classe...: flightEngine
#*
#*  Descricao: this file is the flight class of the SiCAD. The flight
#*             class holds information about a flight and holds the
#*             commands the flight has been given.
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
import sys
import threading
import time

#/ pyGame (graphics library)
#/ ------------------------------------------------------------------------------------------------
import pygame.time

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineSolo as cineSolo
import model.cineVoo as cineVoo
import model.clsAtv as clsAtv

import model.glbDefs as glbDefs
import model.glbData as glbData

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  flightEngine::flightEngine
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a flight
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class flightEngine ( threading.Thread ):

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to scope and view
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_oAer, f_oAtv, f_st, f_ns ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_ns )
        assert ( f_st )
        assert ( f_oAer )
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a super classe
        #*/
        threading.Thread.__init__ ( self )

        #** ---------------------------------------------------------------------------------------
        #*  salva os dados do aerodromo
        #*/
        self._oAer = f_oAer

        #** ---------------------------------------------------------------------------------------
        #*  salva os dados da aeronave
        #*/
        self._oAtv = f_oAtv

        #** ---------------------------------------------------------------------------------------
        #*  salva o system time
        #*/
        self._st = f_st

        #** ---------------------------------------------------------------------------------------
        #*  cria a cinematica de solo
        #*/
        self._cineSolo = cineSolo.cineSolo ( self, f_oAer, f_oAtv, f_st, f_ns )
        assert ( self._cineSolo )

        #** ---------------------------------------------------------------------------------------
        #*  cria a cinematica de voo
        #*/
        self._cineVoo = cineVoo.cineVoo ( self, f_oAer, f_oAtv, f_st, f_ns )
        assert ( self._cineVoo )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::movimentaNoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  status da aeronave no solo pode ser:
    #*          A = acidentada
    #*          B = em taxi, porem em pane
    #*          D = deslocando para a posicao de decolagem
    #*          E = congelada durante o taxi para decolagem, isto eh, antes de atingir a cabeceira
    #*              e iniciar a aceleracao para decolar (antes de mudar o StatusSolo para 'Y'
    #*          G = parada e em pane, porem nao necessita de reboque
    #*          P = parada
    #*          R = aguardando ser rebocada
    #*          S = parando, apos o pouso
    #*          T = em taxi
    #*          X = apos colisao no solo ( com outra aeronave )
    #*          Y = decolando. Este Status nao aparece na tela. Serve para impedir que a aeronave
    #*              seja parada durante a decolagem
    #*  -------------------------------------------------------------------------------------------
    #*/
    def moveNoSolo ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::moveNoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes para execucao
        #*/
        assert ( self._oAtv )
        
        if ( not self._oAtv._bActive ):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*  A - acidentada
        #*/
        if ( 'A' == self._oAtv._cStatusSolo ):

            pass
            #** -----------------------------------------------------------------------------------
            #*/
            #if ( '1' == exeCls.getExeEscalaAtual ()): pass

                #** -------------------------------------------------------------------------------
                #*/
                #PasteAviao2 ( AcidentePouso, f_iAnv )

            #else: pass

                #** -------------------------------------------------------------------------------
                #*/
                #PlotAviao2 

        #** ---------------------------------------------------------------------------------------
        #*  B - em taxi, porem em pane
        #*  T - em taxi
        #*/
        elif ( self._oAtv._cStatusSolo in [ 'B', 'T' ] ):

            #** -----------------------------------------------------------------------------------
            #*  movimenta a aeronave no taxi
            #*/
            self._cineSolo.moveNoTaxi ()

            #** -----------------------------------------------------------------------------------
            #*  checa se a aeronave continua ativa
            #*/
            if ( self._oAtv._bActive ):

                #** -------------------------------------------------------------------------------
                #*  B - em taxi, porem em pane
                #*/
                if ( 'B' == self._oAtv._cStatusSolo ):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para G (parada e em pane, porem nao necessita de reboque)
                    #*/
                    self._oAtv._cStatusSolo = 'G'

                #** -------------------------------------------------------------------------------
                #*  T - em taxi
                #*/
                elif ( 'T' == self._oAtv._cStatusSolo ):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para P (parada)
                    #*/
                    self._oAtv._cStatusSolo = 'P'

                #** -------------------------------------------------------------------------------
                #*  avisa que mudou o status
                #*/
                self._oAtv._bAltStatus = True

        #** ---------------------------------------------------------------------------------------
        #*  D - deslocando para a posicao de decolagem
        #*/
        elif ( 'D' == self._oAtv._cStatusSolo ):

            #** -----------------------------------------------------------------------------------
            #*  procedimento de decolagem 
            #*/
            self._cineSolo.procDecolagem ()

        #** ---------------------------------------------------------------------------------------
        #*  G - parada e em pane, porem nao necessita de reboque
        #*  P - parada
        #*  X - apos colisao no solo ( com outra aeronave )
        #*/
        elif ( self._oAtv._cStatusSolo in [ 'G', 'P', 'X' ] ):

            pass
            #** -----------------------------------------------------------------------------------
            #*  escala 1 ?
            #*/
            #if ( '1' == exeCls.getExeEscalaAtual ()):

                #** -------------------------------------------------------------------------------
                #*/
                #PasteAviao2 ( Desenhos.A ( Desenho, Direcao ), f_iAnv )

            #else: pass

                #** -------------------------------------------------------------------------------
                #*/
                #PlotAviao2 

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::moveNoVoo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  C - aeronave dentro do circuito. Os status 'V' e 'K' servem para definir se
    #*              a entrada eh pela perna do vento ou contra vento, e para levar a aeronave
    #*              ate o circuito. Com este status ou status 'N' pode-se solicitar pouso. No
    #*              primeiro caso a aeronave atingira a perna base antes de entrar na final
    #*              No segundo, o status passa a ser 'D' e a aeronave entra direto na final
    #*          D - pouso direto. Com status 'N' (voo normal) pode-se solicitar pouso.
    #*              A aeronave toma a direcao do ponto de encontro da final com a perna base
    #*          F - aeronave na final
    #*          O - peel-off
    #*          P - pousa movendo-se no circuito. Neste, caso, a aeronave ja esta no circuito
    #*          T - toque e arremetida.
    #*          X - arremeter em emergencia
    #*          Y - "toque e arremetida"
    #*          Z - arremeter para a perna do vento
    #*  -------------------------------------------------------------------------------------------
    #*/
    def moveNoVoo ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::moveNoVoo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes para execucao
        #*/
        assert ( self._oAtv )
        
        if ( not self._oAtv._bActive ):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*  N - voo normal ?
        #*/
        if ( 'N' == self._oAtv._cStatusVoo ):

            #** -----------------------------------------------------------------------------------
            #*  procedimento de voo normal
            #*/
            self._cineVoo.procVooNormal ()

        #** ---------------------------------------------------------------------------------------
        #*  O - peel-off ?
        #*/
        elif ( 'O' == self._oAtv._cStatusVoo ):

            #** -----------------------------------------------------------------------------------
            #*  procedimento de peel-off
            #*/
            self._cineVoo.procPeelOff ()

        #** ---------------------------------------------------------------------------------------
        #*  K - circuito, entrada pela perna do contra vento ?
        #*  V - circuito, entrada pela perna do vento ?
        #*/
        elif ( self._oAtv._cStatusVoo in [ 'K', 'V' ] ):

            #** -----------------------------------------------------------------------------------
            #*  procedimento de circuito
            #*/
            self._cineVoo.procCircuito ()

        #** ---------------------------------------------------------------------------------------
        #*  D - pouso direto ?
        #*  P - pousa movendo-se no circuito ?
        #*/
        elif ( self._oAtv._cStatusVoo in [ 'A', 'D', 'P' ] ):

            #** -----------------------------------------------------------------------------------
            #*  procedimento de pouso
            #*/
            self._cineVoo.procPouso ()

        #** ---------------------------------------------------------------------------------------
        #*  X - arremeter em emergencia ?
        #*  Y - "toque e arremetida" ?
        #*  Z - arremeter para a perna do vento ?
        #*/
        elif ( self._oAtv._cStatusVoo in [ 'X', 'Y', 'Z' ] ):

            #** -----------------------------------------------------------------------------------
            #*  procedimento de arremetida
            #*/
            self._cineVoo.procArremeter ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::run
    #*  -------------------------------------------------------------------------------------------
    #*  this function updates the position of all flights in the flight list
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::run"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes para execucao
        #*/
        assert ( self._oAtv )
        assert ( isinstance ( self._oAtv, clsAtv.clsAtv ))

        assert ( self._cineSolo )
        assert ( self._cineVoo )

        #** ---------------------------------------------------------------------------------------
        #*  enquanto nao inicia...
        #*/
        while ( not glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  aguarda 1 seg
            #*/
            time.sleep ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  timestamp of the last turn
        #*/
        self._oAtv._lTempoAnt = self._st.obtemHoraSim ()
        #l_log.info ( "_lTempoAnt: " + str ( self._oAtv._lTempoAnt ))

        #** ---------------------------------------------------------------------------------------
        #*  loop de vida da aeronave
        #*/
        while (( glbData.g_bKeepRun ) and ( self._oAtv._bActive )):

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  a aeronave esta no solo ?
            #*/
            if ( self._oAtv._bSolo ):

                #** -------------------------------------------------------------------------------
                #*  se esta no solo, movimenta no solo
                #*/
                self.moveNoSolo ()

                #** -------------------------------------------------------------------------------
                #*  envia os dados de posicionamento da aeronave
                #*/
                self._cineSolo.sendData ()

            #** -----------------------------------------------------------------------------------
            #*  senao, a aeronave esta em voo
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  se esta em voo, movimenta em voo
                #*/
                self.moveNoVoo ()

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(A): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(A): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(A): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta atrasado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (2/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a area de dados da aeronave
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::getAtv
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getAtv ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::getAtv"


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
        return ( self._oAtv )

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::getCineSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCineSolo ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::getCineSolo"


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
        return ( self._cineSolo )

    #** -------------------------------------------------------------------------------------------
    #*  flightEngine::getCineVoo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getCineVoo ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightEngine::getCineVoo"


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
        return ( self._cineVoo )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "flightEngine" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** ----------------------------------------------------------------------------------------------- *#
