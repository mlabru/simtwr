#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: cineSolo
#*
#*  Descrição: this file is the flight class of the SiCAD. The flight class holds information about
#*             a flight and holds the commands the flight has been given.
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
import math
import time

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineCalc as cineCalc
import model.cineClss as cineClss
import model.clsCab as clsCab
import model.clsPst as clsPst
import model.clsTrj as clsTrj
import model.glbDefs as glbDefs

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  cineSolo::cineSolo
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a flight
#*  -----------------------------------------------------------------------------------------------
#*/
class cineSolo ( cineClss.cineClss ):

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  setting the variables pertaining to scope and view
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_fe, f_oAer, f_oAtv, f_st, f_ns ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_fe )
        assert ( f_ns )
        assert ( f_st )
        assert ( f_oAer )
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a superclass
        #*/
        cineClss.cineClss.__init__ ( self, f_fe, f_oAer, f_oAtv, f_st, f_ns )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  CALLBACKS
    #*  ===========================================================================================
    #*/

    #** ===========================================================================================
    #*  PROCEDURES LEVEL 2
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::execCongelaNoSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execCongelaNoSolo ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::execCongelaNoSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
        #*/
        assert ( self._st )
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
        #*  enquanto estiver congelado...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( self._oAtv._cStatusSolo in [ 'C', 'E' ] )):

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  obtem e salva o tempo atual
        #*/
        self._oAtv._lTempoAnt = self._st.obtemHoraSim ()
        #l_log.info ( "_lTempoAnt: " + str ( self._oAtv._lTempoAnt ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::execDecolar
    #*  -------------------------------------------------------------------------------------------
    #*  decola a aeronave
    #*  -------------------------------------------------------------------------------------------
    #*  @param  self - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execDecolar ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::execDecolar"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
        #*/
        assert ( self._oAer )
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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv._tCktAtual [ 0 ]
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira do circuito
        #*/
        l_iCab = self._oAtv._tCktAtual [ 1 ]
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direção da cabeceira da pista
        #*/
        l_dCabDir = l_oCab._dCabDir

        #** ---------------------------------------------------------------------------------------
        #*  muda o status para decolando
        #*/
        self._oAtv.setStatusSolo ( 'Y' )

        #** ---------------------------------------------------------------------------------------
        #*  inicio de rolagem para decolagem
        #*/

        #** ---------------------------------------------------------------------------------------
        #*  direção da aeronave igual a da cabeceira
        #*/
        self._oAtv._dDirAtu = l_dCabDir

        #** ---------------------------------------------------------------------------------------
        #*  verificar se a aeronave atingiu a fim da pista ao decolar (30/03/97)
        #*/
        l_dRun = 0.0

        #** ---------------------------------------------------------------------------------------
        #*  converte a direção da cabeceira para radianos
        #*/
        l_dTeta = math.radians ( l_dCabDir )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a aceleração para decolagem
        #*/
        l_dAcc = self._oAtv.getAceleracaoDep ()

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade de decolagem
        #*/
        self._oAtv._dVelDem = self._oAtv.getVelocidadeDep () * glbDefs.xCNV_Knots2Ms
        #l_log.info ( "velocidade decolagem: " + str ( self._oAtv._dVelDem ))

        #** ---------------------------------------------------------------------------------------
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'A' != self._oAtv.getStatusSolo ()) and
               ( self._oAtv._dVeloc < self._oAtv._dVelDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  obtem a hora atual em segundos
            #*/
            l_lTempoAtu = self._st.obtemHoraSim ()
            #l_log.info ( "_lTempoAtu: " + str ( l_lTempoAtu ))

            #** -----------------------------------------------------------------------------------
            #*  calcula a variação de tempo desde a ultima atualização
            #*/
            l_lDltTempo = l_lTempoAtu - self._oAtv._lTempoAnt
            #l_log.info ( "Delta de tempo: " + str ( l_lDltTempo ))

            #** -----------------------------------------------------------------------------------
            #*  calcula 1/2 at^2
            #*/
            l_at2 = ( l_dAcc * ( l_lDltTempo ** 2 )) / 2.
            #l_log.info ( "l_at2: " + str ( l_at2 ))

            #** -----------------------------------------------------------------------------------
            #*  calcula vot em suas componentes x e y
            #*/
            l_votX = ( self._oAtv._dVeloc * math.cos ( l_dTeta )) * l_lDltTempo
            #l_log.info ( "l_votX: " + str ( l_votX ))

            l_votY = ( self._oAtv._dVeloc * math.sin ( l_dTeta )) * l_lDltTempo
            #l_log.info ( "l_votY: " + str ( l_votY ))

            #** -----------------------------------------------------------------------------------
            #*  salva a posição anterior da aeronave
            #*/
            self._oAtv._tPosicaoAnt = self._oAtv._tPosicao
            assert ( self._oAtv._tPosicaoAnt )

            #** -----------------------------------------------------------------------------------
            #*  calcula a nova posição atual da aeronave (x = xo + vot + 1/2 at^2 )
            #*/
            self._oAtv._tPosicao = (( self._oAtv._tPosicao [ 0 ] + l_votX + l_at2 ),
                                    ( self._oAtv._tPosicao [ 1 ] + l_votY + l_at2 ))
            assert ( self._oAtv._tPosicao )

            #** -----------------------------------------------------------------------------------
            #*  calcula a nova velocidade v = vo + at
            #*/
            self._oAtv._dVeloc += ( l_dAcc * l_lDltTempo )
            #l_log.info ( "nova velocidade: " + str ( self._oAtv._dVeloc ))

            #** -----------------------------------------------------------------------------------
            #*  velocidade ja ultrapassou a demanda ?
            #*/
            if ( self._oAtv._dVeloc > self._oAtv._dVelDem ):

                #** -------------------------------------------------------------------------------
                #*  velocidade é a demanda
                #*/
                self._oAtv._dVeloc = self._oAtv._dVelDem

            #** -----------------------------------------------------------------------------------
            #*  verificar se a aeronave atingiu a fim da pista ao decolar (30/03/97)
            #*/
            l_dRun += math.sqrt (( l_votX ** 2 ) + ( l_votY ** 2 ))
            #l_log.info ( "deslocamento: " + str ( l_dRun ))
            #l_log.info ( "comprimento da pista: " + str ( l_oPst.getPstCmp () ))

            #** -----------------------------------------------------------------------------------
            #*  deslocamento na decolagem maior que o comprimento da pista ?
            #*/
            if ( l_dRun > l_oPst.getPstCmp ()):

                #l_log.info ( "mudou o status para aeronave acidentada !!" )

                #** -------------------------------------------------------------------------------
                #*  muda o status para aeronave acidentada
                #*/
                self._oAtv.setStatusSolo ( 'A' )

            #** -----------------------------------------------------------------------------------
            #*  salva o tempo atual
            #*/
            self._oAtv._lTempoAnt = l_lTempoAtu

            #** -----------------------------------------------------------------------------------
            #*  envia os dados para o controle
            #*/
            self.sendData ()

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave ativa e sem acidentes ?
        #*/
        if (( self._oAtv.isActive ()) and ( 'A' != self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  velocidade da aeronave
            #*/
            self._oAtv._dVeloc = self._oAtv._dVelDem
            self._oAtv.setNavVelDem ( self._oAtv.getVelocidadeSubida () * glbDefs.xCNV_Knots2Ms )

            #** -----------------------------------------------------------------------------------
            #*  proa da aeronave
            #*/
            self._oAtv._dProa = cineCalc.convProa2Direcao (( self._oAtv._dDirAtu, self._oAer.getDifDeclinacao ()))
            self._oAtv.setNavProaDem ( self._oAtv._dProa )

            #** -----------------------------------------------------------------------------------
            #*  altitude da aeronave
            #*/
            self._oAtv._dAltitude = self._oAer.getAltitude () * glbDefs.xCNV_ft2M
            self._oAtv.setNavAltDem (( self._oAer.getAltitude () + 1000. ) * glbDefs.xCNV_ft2M )

            #** -----------------------------------------------------------------------------------
            #*  aeronave em voo
            #*/
            self._oAtv._bSolo = False

            #** -----------------------------------------------------------------------------------
            #*  elimina qualquer outro status
            #*/
            self._oAtv.setStatusSolo ( 'P' )

            #** -----------------------------------------------------------------------------------
            #*  aeronave em voo normal
            #*/
            self._oAtv.setStatusVoo ( 'N' )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::execGiraNoEixo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execGiraNoEixo ( self, f_dDirTax, f_cSent ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::execGiraNoEixo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_cSent in locDefs.xSET_SentidosGiro )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
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
        #*  mantem o sentido de curva ?
        #*/
        if ( 'I' == f_cSent ):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*  obtem a familia da aeronave
        #*/
        l_btFam = self._oAtv._btFamilia
        assert (( l_btFam > 0 ) and ( l_btFam <= locDefs.xMAX_Familias ))

        #** ---------------------------------------------------------------------------------------
        #*  é um jato militar ?
        #*/
        if ( 8 == l_btFam ):

            #** -----------------------------------------------------------------------------------
            #*  obtem a variação angular no solo
            #*/
            l_dVarAng = locDefs.RotacaoSolo8

        #** ---------------------------------------------------------------------------------------
        #*  senão, é uma aeronave normal
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  obtem a variação angular no solo
            #*/
            l_dVarAng = locDefs.RotacaoSolo

        #l_log.info ( "Variação angular: " + str ( l_dVarAng ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direção atual
        #*/
        l_dDirAtu = self._oAtv._dDirAtu
        #l_log.info ( "Direção atual(na entrada)..: " + str ( self._oAtv._dDirAtu ))

        #l_log.info ( "Direção demanda(na entrada): " + str ( f_dDirTax ))
        #l_log.info ( "Proa atual(na entrada).....: " + str ( self._oAtv._dProa ))

        #** ---------------------------------------------------------------------------------------
        #*  converte a direção em proa
        #*/
        l_dProaTax = cineCalc.convProa2Direcao (( f_dDirTax, self._oAer.getDifDeclinacao ()))

        #** ---------------------------------------------------------------------------------------
        #*  proa de demanda
        #*/
        self._oAtv._dProaDem = l_dProaTax
        #l_log.info ( "Proa de demanda: " + str ( self._oAtv._dProaDem ))

        #** ---------------------------------------------------------------------------------------
        #*  curva a esquerda (sentido anti-horario) ?
        #*/
        if ( 'A' == f_cSent ):

            #** -----------------------------------------------------------------------------------
            #*  checa menor angulo de rotação
            #*/
            if ( f_dDirTax < l_dDirAtu ):

                #** -------------------------------------------------------------------------------
                #*  ajusta a direção
                #*/
                f_dDirTax += 360.

            #** -----------------------------------------------------------------------------------
            #*  sentido de curva
            #*/
            self._oAtv._cSentidoCurva = 'E'

            #** -----------------------------------------------------------------------------------
            #*  enquanto estiver curvando...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv._cStatusSolo in [ 'B', 'C', 'D', 'E', 'T' ] ) and
                   ( l_dDirAtu < f_dDirTax )):

                #** -------------------------------------------------------------------------------
                #*  obtem o tempo inicial
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  aeronave foi congelada ?
                #*/
                if ( self._oAtv._cStatusSolo in [ 'C', 'E' ] ):

                    #** ---------------------------------------------------------------------------
                    #*  aguarda descongelar
                    #*/
                    self.execCongelaNoSolo ()

                #** -------------------------------------------------------------------------------
                #*  obtem a hora atual em segundos
                #*/
                l_lTempoAtu = self._st.obtemHoraSim ()
                #l_log.info ( "_lTempoAtu: " + str ( l_lTempoAtu ))

                #** -------------------------------------------------------------------------------
                #*  calcula a variação de tempo desde a ultima atualização
                #*/
                l_lDltTempo = l_lTempoAtu - self._oAtv._lTempoAnt
                #l_log.info ( "Delta de tempo: " + str ( l_lDltTempo ))

                #** -------------------------------------------------------------------------------
                #*  calcula o angulo rodado no tempo
                #*/
                l_dDltAng = l_lDltTempo * l_dVarAng
                #l_log.info ( "Delta de angulo: " + str ( l_dDltAng ))

                #** -------------------------------------------------------------------------------
                #*  gira o angulo calculado
                #*/
                l_dDirAtu += l_dDltAng
                #l_log.info ( "direção atual: " + str ( l_dDirAtu ))

                #** -------------------------------------------------------------------------------
                #*  converte a direção em proa
                #*/
                self._oAtv._dProa = cineCalc.convProa2Direcao (( l_dDirAtu, self._oAer.getDifDeclinacao ()))
                #l_log.info ( "proa atual: " + str ( self._oAtv._dProa ))

                #** -------------------------------------------------------------------------------
                #*  salva o tempo atual
                #*/
                self._oAtv._lTempoAnt = l_lTempoAtu

                #** -------------------------------------------------------------------------------
                #*  envia os dados para o controle
                #*/
                self.sendData ()

                #** -------------------------------------------------------------------------------
                #*  obtem o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  esta adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  senão, curva a direita (sentido horario) ?
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  checa menor angulo de rotação
            #*/
            if ( l_dDirAtu < f_dDirTax ):

                #** -------------------------------------------------------------------------------
                #*  ajusta a direção
                #*/
                l_dDirAtu += 360.

            #** -----------------------------------------------------------------------------------
            #*  sentido de curva
            #*/
            self._oAtv._cSentidoCurva = 'D'

            #** -----------------------------------------------------------------------------------
            #*  enquanto estiver curvando...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv._cStatusSolo in [ 'B', 'C', 'D', 'E', 'T' ] ) and
                   ( l_dDirAtu > f_dDirTax )):

                #** -------------------------------------------------------------------------------
                #*  obtem o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  aeronave foi congelada ?
                #*/
                if ( self._oAtv._cStatusSolo in [ 'C', 'E' ] ):

                    #** ---------------------------------------------------------------------------
                    #*  aguarda descongelar
                    #*/
                    self.execCongelaNoSolo ()

                #** -------------------------------------------------------------------------------
                #*  obtem a hora atual em segundos
                #*/
                l_lTempoAtu = self._st.obtemHoraSim ()
                #l_log.info ( "_lTempoAtu: " + str ( l_lTempoAtu ))

                #** -------------------------------------------------------------------------------
                #*  calcula a variação de tempo desde a ultima atualização
                #*/
                l_lDltTempo = l_lTempoAtu - self._oAtv._lTempoAnt
                #l_log.info ( "Delta de tempo: " + str ( l_lDltTempo ))

                #** -------------------------------------------------------------------------------
                #*  calcula o angulo rodado no tempo
                #*/
                l_dDltAng = l_lDltTempo * l_dVarAng
                #l_log.info ( "Delta de angulo: " + str ( l_dDltAng ))

                #** -------------------------------------------------------------------------------
                #*  gira o angulo calculado
                #*/
                l_dDirAtu -= l_dDltAng
                #l_log.info ( "direção atual: " + str ( l_dDirAtu ))

                #** -------------------------------------------------------------------------------
                #*  converte a direção em proa
                #*/
                self._oAtv._dProa = cineCalc.convProa2Direcao (( l_dDirAtu, self._oAer.getDifDeclinacao ()))
                #l_log.info ( "proa atual: " + str ( self._oAtv._dProa ))

                #** -------------------------------------------------------------------------------
                #*  salva o tempo atual
                #*/
                self._oAtv._lTempoAnt = l_lTempoAtu

                #** -------------------------------------------------------------------------------
                #*  envia os dados para o controle
                #*/
                self.sendData ()

                #** -------------------------------------------------------------------------------
                #*  obtem o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  esta adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  ainda esta no taxi ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( self._oAtv._cStatusSolo in [ 'B', 'C', 'D', 'E', 'T' ] )):

            #** -----------------------------------------------------------------------------------
            #*  ajusta a direção
            #*/
            l_dDir = f_dDirTax

            #** -----------------------------------------------------------------------------------
            #*  converte a proa em direção
            #*/
            self._oAtv._dProa = self._oAtv._dProaDem

        #** ---------------------------------------------------------------------------------------
        #*  senão, não esta mais no taxi
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  salva direção atual
            #*/
            l_dDir = l_dDirAtu

        #** ---------------------------------------------------------------------------------------
        #*  salva a nova direção calculada
        #*/
        self._oAtv._dDirAtu = ( l_dDir % 360. )
        #l_log.info ( "Direção atual (na saida): " + str ( self._oAtv._dDirAtu ))

        #l_log.info ( "Proa atual(na saida)....: " + str ( self._oAtv._dProa ))
        #l_log.info ( "Proa demanda(na saida)..: " + str ( self._oAtv._dProaDem ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  PROCEDURES
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::procArremeter
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def procArremeter ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::procArremeter"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        #assert (( f_iPst >= 0 ) and ( f_iPst < locDefs.xMAX_Pistas ))
        #assert (( f_iCkt >= 0 ) and ( f_iCkt < locDefs.xMAX_Circuitos ))

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
        #*/
        #assert ( self._oAer )
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
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::procDecolagem
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def procDecolagem ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::procDecolagem"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
        #*/
        assert ( self._oAer )
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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv._tCktAtual [ 0 ]
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira do circuito
        #*/
        l_iCab = self._oAtv._tCktAtual [ 1 ]
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a quantidade de pontos do percurso
        #*/
        l_iQPP = len ( self._oAtv._lstEtapa )
        #l_log.info ( "quantidade de pontos do percurso: " + str ( l_iQPP ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a direção da cabeceira
        #*/
        l_dCabDir = l_oCab._dCabDir
        #l_log.info ( "direção da cabeceira: " + str ( l_dCabDir ))

        #** ---------------------------------------------------------------------------------------
        #*  verifica se o ultimo trecho do taxi, antes da decolagem, esta na mesma direção da
        #*  cabeceira. Senão estiver, deve-se girar a aeronave para essa direção
        #*/
        if ( int ( self._oAtv._lstEtapa [ l_iQPP - 1 ]._tTrecho [ 1 ] ) != int ( l_dCabDir )):

            #** -----------------------------------------------------------------------------------
            #*  cria uma etapa
            #*/
            l_oEtapa = clsTrj.Etapa ( 0, self._oAtv.getTaxDestino (), ( 0., l_dCabDir ))
            assert ( l_oEtapa )

            #** -----------------------------------------------------------------------------------
            #*  coloca o destino do taxi como ultimo ponto do percurso
            #*/
            self._oAtv._lstEtapa.append ( l_oEtapa )

        #l_log.info ( "direção do ultimo trecho: " + str ( int ( self._oAtv._lstEtapa [ l_iQPP - 1 ]._tTrecho [ 1 ] )))

        #** ---------------------------------------------------------------------------------------
        #*  movimenta a aeronave no solo
        #*/
        self.moveNoTaxi ()

        #** ---------------------------------------------------------------------------------------
        #*  decolar ?
        #*/
        if ( 'D' == self._oAtv.getStatusSolo ()):

            #** -----------------------------------------------------------------------------------
            #*/
            self.execDecolar ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  MOVES
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::moveProxNo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def moveProxNo ( self, f_iNo, f_dVelTaxi, f_dDirTaxi ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::moveProxNo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
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
        #*  obtem a distancia a ser percorrida neste trecho
        #*/
        l_dDstTaxi = self._oAtv._lstEtapa [ f_iNo ]._tTrecho [ 0 ]
        #l_log.info ( "distancia do trecho: [%f]" % ( l_dDstTaxi ))

        #** ---------------------------------------------------------------------------------------
        #*  converte a direção em radianos
        #*/
        l_dDirTaxi = math.radians ( f_dDirTaxi )
        #l_log.info ( "l_dDirTaxi: %f" % ( l_dDirTaxi ))

        #** ---------------------------------------------------------------------------------------
        #*  distancia percorrida
        #*/
        l_dDstRun = 0.0

        #** ---------------------------------------------------------------------------------------
        #*  enquanto estiver percorrendo o trecho...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( self._oAtv._cStatusSolo in [ 'B', 'C', 'D', 'E', 'T' ] ) and
               ( l_dDstRun < l_dDstTaxi )):

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  aeronave foi congelada ?
            #*/
            if ( self._oAtv._cStatusSolo in [ 'C', 'E' ] ):

                #** -------------------------------------------------------------------------------
                #*  aguarda descongelar
                #*/
                self.execCongelaNoSolo ()

            #** -----------------------------------------------------------------------------------
            #*  obtem a hora atual em segundos
            #*/
            l_lTpoAtu = self._st.obtemHoraSim ()
            #l_log.info ( "l_lTpoAtu: %d" % ( l_lTpoAtu ))

            #** -----------------------------------------------------------------------------------
            #*  calcula a variação de tempo desde a ultima atualização
            #*/
            l_lDltTpo = l_lTpoAtu - self._oAtv._lTempoAnt
            #l_log.info ( "l_lDltTpo: " + str ( l_lDltTpo ))

            #** -----------------------------------------------------------------------------------
            #*  calcula a distancia percorrida neste tempo
            #*/
            l_dDltDst = ( l_lDltTpo * f_dVelTaxi )
            #l_log.info ( "l_dDltDst: %f" % ( l_dDltDst ))

            #** -----------------------------------------------------------------------------------
            #*  decompoem esta distancia em suas partes
            #*/
            l_dDltX = l_dDltDst * math.cos ( l_dDirTaxi )
            #l_log.info ( "l_dDltX: %f" % ( l_dDltX ))

            l_dDltY = l_dDltDst * math.sin ( l_dDirTaxi )
            #l_log.info ( "l_dDltY: %f" % ( l_dDltY ))

            #** -----------------------------------------------------------------------------------
            #*  checa se ainda não chegou ao destino
            #*/
            if (( l_dDstRun + l_dDltDst ) <= l_dDstTaxi ):

                #** -------------------------------------------------------------------------------
                #*  salva a nova posição calculada para a aeronave
                #*/
                self._oAtv._tPosicao = ( self._oAtv._tPosicao [ 0 ] + l_dDltX,
                                         self._oAtv._tPosicao [ 1 ] + l_dDltY )
                assert ( self._oAtv._tPosicao )

                #** -------------------------------------------------------------------------------
                #*  salva o tempo atual
                #*/
                self._oAtv._lTempoAnt = l_lTpoAtu

            #** -----------------------------------------------------------------------------------
            #*  incrementa a distancia percorrida
            #*/
            l_dDstRun += l_dDltDst
            #l_log.info ( "distancia percorrida: [%f]" % ( l_dDstRun ))

            #** -----------------------------------------------------------------------------------
            #*  envia os dados para o controle
            #*/
            self.sendData ()

            #** -----------------------------------------------------------------------------------
            #*  obtem o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  checa se ja chegou ao destino
        #*/
        if ( l_dDstRun >= l_dDstTaxi ):

            #** -----------------------------------------------------------------------------------
            #*  fim de percurso ?
            #*/
            if ( f_iNo == ( len ( self._oAtv._lstEtapa ) - 1 )):

                #** -------------------------------------------------------------------------------
                #*  então, a posição atual será o destino do taxi
                #*/
                self._oAtv._tPosicao = self._oAtv.getTaxDestino ()
                assert ( self._oAtv._tPosicao )

            #** -----------------------------------------------------------------------------------
            #*  senão, não é fim de percurso
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  então, a posição atual sera a posição do próximo no do percurso
                #*/
                self._oAtv._tPosicao = self._oAtv._lstEtapa [ f_iNo + 1 ]._tPos
                assert ( self._oAtv._tPosicao )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineSolo::moveNoTaxi
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  self - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def moveNoTaxi ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineSolo::moveNoTaxi"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições para execução
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

        #l_log.info ( "quantidade de pontos do percurso: [%d]" % ( len ( self._oAtv._lstEtapa )))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade de taxi para esta aeronave
        #*/
        l_dVelTaxi = self._oAtv.getVelocidadeTaxi () * glbDefs.xCNV_Knots2Ms
        #l_log.info ( "velocidade de taxi: [%f]" % ( l_dVelTaxi ))

        #** ---------------------------------------------------------------------------------------
        #*  configura a velocidde atual e a demanda como a de taxi
        #*/
        self._oAtv._dVeloc  = l_dVelTaxi
        self._oAtv._dVelDem = l_dVelTaxi

        #** ---------------------------------------------------------------------------------------
        #*  inicia contador de nos
        #*/
        l_iNo = 0

        #** ---------------------------------------------------------------------------------------
        #*  salva o tempo atual em segundos
        #*/
        self._oAtv._lTempoAnt = self._st.obtemHoraSim ()
        #l_log.info ( "_lTempoAnt: " + str ( self._oAtv._lTempoAnt ))

        #** ---------------------------------------------------------------------------------------
        #*  teste necessario pois uma aeronave pode ser parada ou desativada apos entrar em
        #*  movimento no solo. Caso não fosse feito aqui, tal teste so seria feito no fim do
        #*  percurso, o que daria inconsistencia de dados, pois a aeronave estaria parada e
        #*  o sistema continuaria o calculo de suas novas posições
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( self._oAtv._cStatusSolo in [ 'B', 'C', 'D', 'E', 'T' ] ) and
               ( l_iNo < len ( self._oAtv._lstEtapa ))):

            #** -----------------------------------------------------------------------------------
            #*  aeronave congelada ?
            #*/
            if ( self._oAtv._cStatusSolo in [ 'C', 'E' ] ):

                #** -------------------------------------------------------------------------------
                #*  aguarda descongelar
                #*/
                self.execCongelaNoSolo ()

            #** -----------------------------------------------------------------------------------
            #*  obtem a direção a seguir nesta etapa
            #*/
            l_dDir = self._oAtv._lstEtapa [ l_iNo ]._tTrecho [ 1 ]
            #l_log.info ( "direção do trecho (%d): [%f]" % ( l_iNo, l_dDir ))

            #** -----------------------------------------------------------------------------------
            #*  obtem o sentido de rotação ate a direção a seguir
            #*/
            l_cSent = cineCalc.sentidoRotacao ( self._oAtv._dDirAtu, l_dDir )
            #l_log.info ( "sentido de rotação calculado: [%c]" % ( l_cSent ))

            #** -----------------------------------------------------------------------------------
            #*  gira a aeronave
            #*/
            self.execGiraNoEixo ( l_dDir, l_cSent )
            #l_log.info ( "Apos girar no eixo no move no taxi...." )

            #** -----------------------------------------------------------------------------------
            #*  movimenta a aeronave ate o próximo no
            #*/
            self.moveProxNo ( l_iNo, l_dVelTaxi, l_dDir )

            #** -----------------------------------------------------------------------------------
            #*  incrementa o no
            #*/
            l_iNo += 1

        #l_log.info ( "fim do move no taxi...." )

        #** ---------------------------------------------------------------------------------------
        #*  terminou o percurso ?
        #*/
        if ( l_iNo >= ( len ( self._oAtv._lstEtapa ) - 1 )):

            #** -----------------------------------------------------------------------------------
            #*  para (estanca) a aeronave
            #*/
            self._oAtv._dVeloc  = 0.
            self._oAtv._dVelDem = 0.

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "cineSolo" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
