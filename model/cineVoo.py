#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: cineVoo
#*
#*  Descrição: this file is the flight class of the SiCAD. The flight class holds information about
#*             a flight and holds the commands the flight has been given.
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
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
import random
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

import model.glbData as glbData
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
#*  cineVoo::cineVoo
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a flight
#*  -----------------------------------------------------------------------------------------------
#*/
class cineVoo ( cineClss.cineClss ):

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::__init__
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
        #l_szMetodo = "cineVoo::__init__"


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

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::ajustaNaFinal
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def ajustaNaFinal ( self, f_iPst, f_iCab ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::ajustaNaFinal"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iPst >= 0 ) and ( f_iPst < locDefs.xMAX_Pistas ))
        assert (( f_iCab >= 0 ) and ( f_iCab < locDefs.xMAX_Cabeceiras ))

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
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( f_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira 0 da pista (é ZERO mesmo...)
        #*/
        l_oCab = l_oPst.getPstCab ( 0 )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a direção da cabeceira em radianos
        #*/
        l_dCabDir = math.radians ( l_oCab._dCabDir )
        #l_log.info ( "[%s] l_dCabDir: [%f]" % ( self._oAtv.getIdent (), l_dCabDir ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a final
        #*/
        l_tFinal = l_oCab._tFinalReta
        assert ( l_tFinal )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre eles
        #*/
        l_dDAF = cineCalc.distanciaPontoReta ( l_tAnv, l_tFinal )
        #l_log.info ( "[%s] l_dDAF: [%f]" % ( self._oAtv.getIdent (), l_dDAF ))

        #** ---------------------------------------------------------------------------------------
        #*  a distância entre a aeronave e a final e maior que 1m ?
        #*/
        if ( abs ( l_dDAF ) > 1. ):

            #** -----------------------------------------------------------------------------------
            #*  permite que aeronaves no setor 4, com proa ate 3 graus de diferença em relação a
            #*  cabeceira, possam ser consideradas na Final.
            #*/
            l_dX = abs ( l_dDAF ) * math.sin ( l_dCabDir )
            l_dY = abs ( l_dDAF ) * math.cos ( l_dCabDir )

            #** -----------------------------------------------------------------------------------
            #*  obtém a cabeceira da pista
            #*/
            l_oCab = l_oPst.getPstCab ( f_iCab )
            assert ( l_oCab )
            assert ( isinstance ( l_oCab, clsCab.clsCab ))

            #** -----------------------------------------------------------------------------------
            #*  obtém a direção da cabeceira da pista
            #*/
            l_dCabDir = l_oCab._dCabDir
            #l_log.info ( "[%s] l_dCabDir: [%f]" % ( self._oAtv.getIdent (), l_dCabDir ))

            #** -----------------------------------------------------------------------------------
            #*  converte a direção em proa
            #*/
            l_dCabProa = cineCalc.convProa2Direcao (( l_dCabDir, self._oAer.getDifDeclinacao ()))
            #l_log.info ( "[%s] l_dCabProa: [%f]" % ( self._oAtv.getIdent (), l_dCabProa ))

            #** -----------------------------------------------------------------------------------
            #*  proa para cabeceira da pista
            #*/
            self._oAtv._dProa = l_dCabProa
            self._oAtv._dProaDem = l_dCabProa

            #** -----------------------------------------------------------------------------------
            #*  direção da cabeceira da pista
            #*/
            self._oAtv._dDir = l_dCabDir

            #** -----------------------------------------------------------------------------------
            #*  aeronave acima da final ?
            #*/
            if ( l_dDAF < 0. ):

                #** -------------------------------------------------------------------------------
                #*  calcula a nova posição da aeronave
                #*/
                self._oAtv._tPosicao = ( self._oAtv._tPosicao [ 0 ] + l_dX,
                                         self._oAtv._tPosicao [ 1 ] - l_dY )

            #** -----------------------------------------------------------------------------------
            #*  senão, aeronave abaixo da final
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  calcula a nova posição da aeronave
                #*/
                self._oAtv._tPosicao = ( self._oAtv._tPosicao [ 0 ] - l_dX,
                                         self._oAtv._tPosicao [ 1 ] + l_dY )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::aproaFinal
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_lDeltaT - delta de tempo desde a ultima atualização
    #*  @param  f_dVelMed - velocidade media
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  esta rotina deve receber a distância ate a Final > raio de curva.
    #*  -------------------------------------------------------------------------------------------
    #*/
    def aproaFinal ( self, f_iPst, f_iCab ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::aproaFinal"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iPst >= 0 ) and ( f_iPst < locDefs.xMAX_Pistas ))
        assert (( f_iCab >= 0 ) and ( f_iCab < locDefs.xMAX_Cabeceiras ))

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
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( f_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( f_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a reta da final
        #*/
        l_tReta = l_oCab._tFinalReta
        assert ( l_tReta )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posico atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre eles
        #*/
        l_dDist = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tReta )
        #l_log.info ( "[%s] l_dDist: [%f]" % ( self._oAtv.getIdent (), l_dDist ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o raio de curvatura da aeronave
        #*/
        l_dRaio = self._oAtv.getRaioCurva ()
        #l_log.info ( "[%s] l_dRaio: [%f]" % ( self._oAtv.getIdent (), l_dRaio ))

        #** ---------------------------------------------------------------------------------------
        #*  enquanto não chegar o ponto de curva...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'P' == self._oAtv.getStatusVoo ()) and
               ( l_dDist >= l_dRaio )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém a posico atual da aeronave
            #*/
            l_tAnv = self._oAtv._tPosicao
            assert ( l_tAnv )

            #** -----------------------------------------------------------------------------------
            #*  calcula a distância entre eles
            #*/
            l_dDist = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tReta )
            #l_log.info ( "[%s] l_dDist: [%f]" % ( self._oAtv.getIdent (), l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o raio de curvatura da aeronave #!X! REVER (raio so depende da vel.)
            #*/
            l_dRaio = self._oAtv.getRaioCurva ()
            #l_log.info ( "[%s] l_dRaio(variou ?): [%f]" % ( self._oAtv.getIdent (), l_dRaio ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  keep going ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'P' == self._oAtv.getStatusVoo ())):

            #** -----------------------------------------------------------------------------------
            #*  obtém a direção da cabeceira
            #*/
            l_dCabDir = l_oCab._dCabDir
            #l_log.info ( "[%s] l_dCabDir: [%f]" % ( self._oAtv.getIdent (), l_dCabDir ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o sentido de menor rotação
            #*/
            l_cSent = cineCalc.sentidoRotacao ( self._oAtv._dDirAtu, l_dCabDir )
            #l_log.info ( "[%s] l_cSent: [%c]" % ( self._oAtv.getIdent (), l_cSent ))

            #** -----------------------------------------------------------------------------------
            #*  sentido de rotação diferente do atual ?
            #*/
            if ( 'I' != l_cSent ):

                #** -------------------------------------------------------------------------------
                #*  sentido anti-horario ?
                #*/
                if ( 'A' == l_cSent ):

                    #** ---------------------------------------------------------------------------
                    #*  curva a esquerda
                    #*/
                    l_cSent = 'E'

                #** -------------------------------------------------------------------------------
                #*  sentido horario ?
                #*/
                elif ( 'H' == l_cSent ):

                    #** ---------------------------------------------------------------------------
                    #*  curva a direita
                    #*/
                    l_cSent = 'D'

            #** -----------------------------------------------------------------------------------
            #*  converte a direção em proa
            #*/
            l_dCabProa = cineCalc.convProa2Direcao (( l_dCabDir, self._oAer.getDifDeclinacao ()))
            #l_log.info ( "[%s] l_dCabProa: [%f]" % ( self._oAtv.getIdent (), l_dCabProa ))

            #** -----------------------------------------------------------------------------------
            #*  altera navegação
            #*/
            self._oAtv._cSentidoCurva = l_cSent

            #** -----------------------------------------------------------------------------------
            #*  altitude do circuito
            #*/
            self._oAtv._dAltDem = self._oAer.getAltitude () * glbDefs.xCNV_ft2M

            #** -----------------------------------------------------------------------------------
            #*  proa para cabeceira da pista
            #*/
            self._oAtv._dProaDem = l_dCabProa

            #** -----------------------------------------------------------------------------------
            #*  enquanto está curvando...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'P' == self._oAtv.getStatusVoo ()) and
                   ( self._oAtv._dProa != self._oAtv._dProaDem )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  keep going ?
            #*/
            if (( glbData.g_bKeepRun ) and
                ( self._oAtv._bActive ) and
                ( 'P' == self._oAtv.getStatusVoo ())):

                #** -------------------------------------------------------------------------------
                #*/
                self.ajustaNaFinal ( f_iPst, f_iCab )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::atualizaAltitude
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_lDeltaT - delta de tempo desde a ultima atualização
    #*  @param  f_dVelMed - velocidade media
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def atualizaAltitude ( self, f_lDeltaT, f_dVelMed ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::atualizaAltitude"


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
            return ( 0, False )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a altitude atual
        #*/
        l_dAltAtu = self._oAtv._dAltitude
        #l_log.info ( "Alt Atual..: " + str ( l_dAltAtu ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a altitude de demanda
        #*/
        l_dAltDem = self._oAtv._dAltDem
        #l_log.info ( "Alt Demanda: " + str ( l_dAltDem ))

        #** ---------------------------------------------------------------------------------------
        #*  está variando a altitude ?
        #*/
        if ( l_dAltAtu != l_dAltDem ):

            #** -----------------------------------------------------------------------------------
            #*  na final (F), acidente (A) ou toque (T) ?
            #*/
            if ( self._oAtv.getStatusVoo () in [ 'A', 'F', 'T' ] ):

                #** -------------------------------------------------------------------------------
                #*  obtém a razao de descida atual
                #*/
                l_dVelZ = self._oAtv._dRazaoDescida

            #** -----------------------------------------------------------------------------------
            #*  está subindo ?
            #*/
            elif ( l_dAltAtu < l_dAltDem ):

                #** -------------------------------------------------------------------------------
                #*  obtém a razao de subida
                #*/
                l_dVelZ = self._oAtv.getRazaoSubida ()

            #** -----------------------------------------------------------------------------------
            #*  senão, está descendo
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtém a razao de descida
                #*/
                l_dVelZ = self._oAtv.getRazaoDescida ()

            #** -----------------------------------------------------------------------------------
            #*  está subindo ?
            #*/
            if ( l_dAltAtu < l_dAltDem ):

                #** -------------------------------------------------------------------------------
                #*  calcula a nova altitude ( z = zo + vt )
                #*/
                l_dAltNew = l_dAltAtu + ( l_dVelZ * f_lDeltaT )

                #** -------------------------------------------------------------------------------
                #*  a altitude calculada ultrapassou a demanda ?
                #*/
                if ( l_dAltNew > l_dAltDem ):

                    #** ---------------------------------------------------------------------------
                    #*  ajusta a altitude pela demanda
                    #*/
                    l_dAltNew = l_dAltDem

            #** -----------------------------------------------------------------------------------
            #*  senão, está descendo
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  calcula a nova altitude ( z = zo - vt )
                #*/
                l_dAltNew = l_dAltAtu - ( l_dVelZ * f_lDeltaT )

                #** -------------------------------------------------------------------------------
                #*  a altitude calculada ultrapassou a demanda ?
                #*/
                if ( l_dAltNew < l_dAltDem ):

                    #** ---------------------------------------------------------------------------
                    #*  ajusta a altitude pela demanda
                    #*/
                    l_dAltNew = l_dAltDem

            #** -----------------------------------------------------------------------------------
            #*  salva a nova altitude calculada
            #*/
            self._oAtv._dAltitude = l_dAltNew
            #l_log.info ( "Nova Alt Atual: " + str ( l_dAltNew ))

            #** -----------------------------------------------------------------------------------
            #*  calcula ?
            #*/
            l_dAlfa = math.asin ( l_dVelZ / f_dVelMed )

            #** -----------------------------------------------------------------------------------
            #*  seta flag 'on demand'
            #*/
            l_bFlag = True

        else:

            #** -----------------------------------------------------------------------------------
            #*/
            l_dAlfa = 0.

            #** -----------------------------------------------------------------------------------
            #*  seta flag 'on demand'
            #*/
            l_bFlag = False

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna a ? calculada e o flag 'on demand'
        #*/
        return ( l_dAlfa, l_bFlag )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::atualizaPosicao
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_lDeltaT - delta de tempo desde a ultima atualização
    #*  @param  f_dVelMed - velocidade media
    #*  @param  f_dAlfa   - ?
    #*  @param  f_dDirAtu - direção atual
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def atualizaPosicao ( self, f_lDeltaT, f_dVelMed, f_dAlfa, f_dDirAtu ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::atualizaPosicao"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        #l_log.info ( "f_lDeltaT: " + str ( f_lDeltaT ))
        #l_log.info ( "f_dVelMed: " + str ( f_dVelMed ))
        #l_log.info ( "f_dAlfa..: " + str ( f_dAlfa ))
        #l_log.info ( "f_dDirAtu: " + str ( f_dDirAtu ))

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
        #*  converte a direção atual para radianos
        #*/
        l_dDirAtu = math.radians ( f_dDirAtu )

        #** ---------------------------------------------------------------------------------------
        #*  decompõem a velocidade em seus componentes x e y
        #*/
        l_dVx = f_dVelMed * math.cos ( f_dAlfa ) * math.cos ( l_dDirAtu )
        #l_log.info ( "Velocidade em X: " + str ( l_dVx ))

        l_dVy = f_dVelMed * math.cos ( f_dAlfa ) * math.sin ( l_dDirAtu )
        #l_log.info ( "Velocidade em Y: " + str ( l_dVy ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula os componentes x e y da posição atual ( x = xo + vt )
        #*/
        l_dAtuX = self._oAtv._tPosicao [ 0 ] + ( l_dVx * f_lDeltaT )
        l_dAtuY = self._oAtv._tPosicao [ 1 ] + ( l_dVy * f_lDeltaT )

        #** ---------------------------------------------------------------------------------------
        #*  salva a posição atual calculada
        #*/
        self._oAtv._tPosicao = ( l_dAtuX, l_dAtuY )
        #l_log.info ( "PosicaoAtu: " + str ( self._oAtv._tPosicao ))

        #** ---------------------------------------------------------------------------------------
        #*  o teste a seguir é necessario para que aeronaves que estão pousando sejam desenhadas
        #*  apenas na escala 1 nas demais é apenas plotado um ponto.
        #*/
        #if (( '1' != self._oAtv._oExe.getEscala ()) and ( self._oAtv._bSolo ())):

            #** -----------------------------------------------------------------------------------
            #*/
            # PlotAviao ( f_iAtv )

        #else:

            #** -----------------------------------------------------------------------------------
            #*/
            # CarimbaAviao ( f_iAtv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::atualizaProa
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_lDeltaT - delta de tempo desde a ultima atualização
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def atualizaProa ( self, f_lDeltaT ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::atualizaProa"


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
            return ( False )

        #** ---------------------------------------------------------------------------------------
        #*  obtém as proas atual e demanda
        #*/
        l_dProaAtu = self._oAtv._dProa
        #l_log.info ( "Proa Atual..: " + str ( l_dProaAtu ))

        l_dProaDem = self._oAtv._dProaDem
        #l_log.info ( "Proa Demanda: " + str ( l_dProaDem ))

        #** ---------------------------------------------------------------------------------------
        #*  está curvando ?
        #*/
        if ( l_dProaAtu != l_dProaDem ):

            #** -----------------------------------------------------------------------------------
            #*  obtém o sentido de curva
            #*/
            l_cSent = self._oAtv._cSentidoCurva
            assert ( l_cSent in locDefs.xSET_SentidosValidos )

            #** -----------------------------------------------------------------------------------
            #*  obtém a familia da aeronave
            #*/
            l_btFam = self._oAtv._btFamilia
            assert (( l_btFam > 0 ) and ( l_btFam <= locDefs.xMAX_Familias ))

            #** -----------------------------------------------------------------------------------
            #*  está em vôo normal ?
            #*/
            if ( 'N' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  é um caça ?
                #*/
                if ( 8 == l_btFam ):

                    #** ---------------------------------------------------------------------------
                    #*  calcula o angulo de rotação
                    #*/
                    l_dDeltaP = locDefs.VarAngRota8 * f_lDeltaT

                #** -------------------------------------------------------------------------------
                #*  senão, é uma aeronave comum
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  calcula o angulo de rotação
                    #*/
                    l_dDeltaP = locDefs.VarAngRota * f_lDeltaT

            #** -----------------------------------------------------------------------------------
            #*  senão, está em vôo...
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  é um caça ?
                #*/
                if ( 8 == l_btFam ):

                    #** ---------------------------------------------------------------------------
                    #*  calcula o angulo de rotação
                    #*/
                    l_dDeltaP = locDefs.VarAngTrafego8 * f_lDeltaT

                #** -------------------------------------------------------------------------------
                #*  senão, é uma aeronave comum
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  calcula o angulo de rotação
                    #*/
                    l_dDeltaP = locDefs.VarAngTrafego * f_lDeltaT

            #** -----------------------------------------------------------------------------------
            #*  curva a direita ?
            #*/
            if (( 'D' == l_cSent ) or ( 'd' == l_cSent )):

                #** -------------------------------------------------------------------------------
                #*/
                if ( l_dProaDem < l_dProaAtu ):

                    #** ---------------------------------------------------------------------------
                    #*/
                    l_dProaDem += 360.

                #** -------------------------------------------------------------------------------
                #*  incrementa a proa atual do angulo de rotação calculado
                #*/
                l_dProaAtu += l_dDeltaP

                #** -------------------------------------------------------------------------------
                #*  ja curvou ?
                #*/
                if ( l_dProaAtu > l_dProaDem ):

                    #** ---------------------------------------------------------------------------
                    #*  ajusta proa
                    #*/
                    l_dProaAtu = self._oAtv._dProaDem

            #** -----------------------------------------------------------------------------------
            #*  senão, curva a esquerda
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                if ( l_dProaAtu < l_dProaDem ):

                    #** ---------------------------------------------------------------------------
                    #*/
                    l_dProaAtu += 360.

                #** -------------------------------------------------------------------------------
                #*  decrementa a proa atual do angulo de rotação calculado
                #*/
                l_dProaAtu -= l_dDeltaP

                #** -------------------------------------------------------------------------------
                #*  ja curvou ?
                #*/
                if ( l_dProaAtu < l_dProaDem ):

                    #** ---------------------------------------------------------------------------
                    #*  ajusta a proa
                    #*/
                    l_dProaAtu = self._oAtv._dProaDem

            #** -----------------------------------------------------------------------------------
            #*  salva a proa atual
            #*/
            self._oAtv._dProa = l_dProaAtu
            #l_log.info ( "Nova Proa Atual: " + str ( l_dProaAtu ))

            #** -----------------------------------------------------------------------------------
            #*  converte a proa atual em direção
            #*/
            l_dDir = cineCalc.convProa2Direcao (( l_dProaAtu, self._oAer.getDifDeclinacao ()))

            #** -----------------------------------------------------------------------------------
            #*  salva a nova direção calculada
            #*/
            self._oAtv._dDirAtu = l_dDir
            #l_log.info ( "Nova Direção Atual: " + str ( l_dDir ))

            #** -----------------------------------------------------------------------------------
            #*  seta flag 'on demand'
            #*/
            l_bFlag = True

        #** ---------------------------------------------------------------------------------------
        #*  senão, não está curvando
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  seta flag 'on demand'
            #*/
            l_bFlag = False

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna flag 'on demand'
        #*/
        return ( l_bFlag )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::atualizaVelocidade
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_lDeltaT - delta de tempo desde a ultima atualização
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def atualizaVelocidade ( self, f_lDeltaT ):

        #/ nome do método (logger)
        #/ -----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::atualizaVelocidade"


        #** ----------------------------------------------------------------------------------------
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
            return ( 0.0001, False )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a velocidade atual
        #*/
        l_dVelAtu = self._oAtv._dVeloc
        #l_log.info ( "Vel Atual..: " + str ( l_dVelAtu ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a velocidade de demanda
        #*/
        l_dVelDem = self._oAtv._dVelDem
        #l_log.info ( "Vel Demanda: " + str ( l_dVelDem ))

        #** ---------------------------------------------------------------------------------------
        #*  está variando a velocidade ?
        #*/
        if ( l_dVelAtu != l_dVelDem ):

            #** -----------------------------------------------------------------------------------
            #*  parando apos pouso (S) ou toque e arremetida (T)
            #*/
            if (( 'S' == self._oAtv.getStatusSolo ()) or ( 'T' == self._oAtv.getStatusVoo ())):

                #** -------------------------------------------------------------------------------
                #*  obtém a aceleração
                #*/
                l_dAcc = self._oAtv.getDesaceleracaoArr ()
                #l_log.info ( "Desaceleracao Pouso: " + str ( l_dAcc ))

            #** -----------------------------------------------------------------------------------
            #*  está acelerando ?
            #*/
            elif ( l_dVelAtu < l_dVelDem ):

                #** -------------------------------------------------------------------------------
                #*  obtém a aceleração
                #*/
                l_dAcc = self._oAtv.getAceleracaoVoo ()
                #l_log.info ( "Aceleracao Voo: " + str ( l_dAcc ))

            #** -----------------------------------------------------------------------------------
            #*  senão, está freando
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtém a aceleração
                #*/
                l_dAcc = self._oAtv.getDesaceleracaoVoo ()
                #l_log.info ( "Desaceleração Voo: " + str ( l_dAcc ))

            #** -----------------------------------------------------------------------------------
            #*  está acelerando ?
            #*/
            if ( l_dVelAtu < l_dVelDem ):

                #** -------------------------------------------------------------------------------
                #*  calcula a nova velocidade ( v = vo + at )
                #*/
                l_dVelNew = l_dVelAtu + ( l_dAcc * f_lDeltaT )
                #l_log.info ( "Nova Velocidade (A): " + str ( l_dVelNew ))

                #** -------------------------------------------------------------------------------
                #*  velocidade calculada ultrapassou a demanda ?
                #*/
                if ( l_dVelNew > l_dVelDem ):

                    #** ---------------------------------------------------------------------------
                    #*  ajusta a velocidade calculada pela demanda
                    #*/
                    l_dVelNew = l_dVelDem

            #** -----------------------------------------------------------------------------------
            #*  senão, está freando
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  calcula a nova velocidade ( v = vo - at )
                #*/
                l_dVelNew = l_dVelAtu - ( l_dAcc * f_lDeltaT )
                #l_log.info ( "Nova Velocidade (D): " + str ( l_dVelNew ))

                #** -------------------------------------------------------------------------------
                #*  velocidade calculada ultrapassou a demanda ?
                #*/
                if ( l_dVelNew < l_dVelDem ):

                    #** ---------------------------------------------------------------------------
                    #*  ajusta a velocidade calculada pela demanda
                    #*/
                    l_dVelNew = l_dVelDem

            #** -----------------------------------------------------------------------------------
            #*  salva a velocidade atual
            #*/
            self._oAtv._dVeloc = l_dVelNew
            #l_log.info ( "Nova Vel. Atual: " + str ( l_dVelNew ))

            #** -----------------------------------------------------------------------------------
            #*  calcula a velocidade media do percurso
            #*/
            l_dVelMed = ( l_dVelNew + l_dVelAtu ) / 2.
            #l_log.info ( "Vel. Media.....: " + str ( l_dVelMed ))

            #** -----------------------------------------------------------------------------------
            #*  seta flag 'on demand'
            #*/
            l_bFlag = True

        #** ---------------------------------------------------------------------------------------
        #*  senão, velocidade constante
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  calcula a velocidade media do percurso
            #*/
            l_dVelMed = l_dVelAtu

            #** -----------------------------------------------------------------------------------
            #*  seta flag 'on demand'
            #*/
            l_bFlag = False

        #** ---------------------------------------------------------------------------------------
        #*  velocidade media = 0 ?
        #*/
        if ( 0. == l_dVelMed ):

            #** -----------------------------------------------------------------------------------
            #*  evita divisao por zero
            #*/
            l_dVelMed = 0.0001

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  retorna a velocidade media calculada e o flag 'on demand'
        #*/
        return ( l_dVelMed, l_bFlag )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::calcRazaoPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iFator - define se o ponto de pouso obedecera a uma distribuição normal ou
    #*                     constante, sendo que na ultima, é aumentada a chance de ocorrer
    #*                     um acidente.
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def calcRazaoPouso ( self, f_iFator ):

        #/ nome do método (logger)
        #/ -----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::calcRazaoPouso"


        #** ----------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ----------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iFator >= 0 ) and ( f_iFator <= 100 ))

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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o comprimento da pista
        #*/
        l_uiPstCmp = l_oPst.getPstCmp ()

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição de pouso
        #*/
        l_tPosArr = l_oCab._tCabIni
        assert ( l_tPosArr )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a direção da cabeceira em radianos
        #*/
        l_dDirRad = math.radians ( l_oCab._dCabDir )

        #** ---------------------------------------------------------------------------------------
        #*  distribuição constante ?
        #*/
        if ( 0 != f_iFator ):

            #** -----------------------------------------------------------------------------------
            #*/
            f_iFator = 101 - f_iFator

            #** -----------------------------------------------------------------------------------
            #*  0 = numero aleatorio
            #*/
            if ( 0 == random.randrange ( f_iFator )):

                #** -------------------------------------------------------------------------------
                #*  distância de 100m antes do inicio da cabeceira
                #*/
                l_dDst = -100.

                #** -------------------------------------------------------------------------------
                #*  obtém a taxa de acidentes
                #*/
                l_iAcidente = self._oExe.getAcidente ()

                #** -------------------------------------------------------------------------------
                #*/
                if ( l_iAcidente > 10 ):

                    self._oExe.setAcidente ( l_iAcidente - 10 )

                #** -------------------------------------------------------------------------------
                #*  muda o status para 'Acidente Pouso'
                #*/
                self._oAtv.setStatusVoo ( 'A' )

            #** -----------------------------------------------------------------------------------
            #*  senão, numero aleatorio != 0
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  gera uma distância aleatoria para o pouso
                #*/
                l_dDst = cineCalc.distanciaAleatoriaPouso ( l_uiPstCmp )

                #** -------------------------------------------------------------------------------
                #*  pouso antes do inicio da pista (distância negativa) ?
                #*/
                if ( l_dDst < 0. ):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para 'Acidente Pouso'
                    #*/
                    self._oAtv.setStatusVoo ( 'A' )

        #** ---------------------------------------------------------------------------------------
        #*  senão, distribuição normal
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  gera uma distância aleatoria para o pouso
            #*/
            l_dDst = abs ( cineCalc.distanciaAleatoriaPouso ( l_uiPstCmp ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a nova posição de pouso
        #*/
        l_tPosArr = ( l_tPosArr [ 0 ] + ( l_dDst * math.cos ( l_dDirRad )),
                      l_tPosArr [ 1 ] + ( l_dDst * math.sin ( l_dDirRad )))

        #** ---------------------------------------------------------------------------------------
        #*  calcula distância horizontal da posição atual da aeronave ate a posição da cabeceira
        #*/
        l_dDstAnvCab = cineCalc.distanciaEntrePontos ( self._oAtv._tPosicao, l_tPosArr )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a ALTURA da aeronave
        #*/
        l_dAlt = self._oAtv._dAltitude - ( self._oAer.getAltitude () * glbDefs.xCNV_ft2M )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a velocidade atual
        #*/
        l_dVelAtu = self._oAtv._dVeloc

        #** ---------------------------------------------------------------------------------------
        #*  obtém o angulo de inclinação da altura da aeronave
        #*/
        l_dAlfa = math.atan ( l_dAlt / l_dDstAnvCab )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância inclinada
        #*/
        l_dDist = l_dDstAnvCab / math.cos ( l_dAlfa )

        #** ---------------------------------------------------------------------------------------
        #*  calcula o tempo de descida da aeronave
        #*/
        l_dTpoDsc = l_dDist / l_dVelAtu

        #** ---------------------------------------------------------------------------------------
        #*  salva a razao de descida atual da aeronave
        #*/
        self._oAtv._dRazaoDescida = l_dAlt / l_dTpoDsc
        #l_log.info ( "RazaoDescida: " + str ( self._oAtv._dRazaoDescida ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ------------------------------------------------------------------------------------------
    #*  cineVoo::checkRampaVelocidade
    #*  ------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  ------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def checkRampaVelocidade ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::checkRampaVelocidade"


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
            return ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "[%s] l_iPst: [%d]" % ( self._oAtv.getIdent (), l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "[%s] l_iCab: [%d]" % ( self._oAtv.getIdent (), l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o ponto de inicio da cabeceira do circuito
        #*/
        l_tCabIni = l_oCab._tCabIni
        assert ( l_tCabIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre a aeronave e a final
        #*/
        l_dDAF = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_oCab._tFinalReta )
        #l_log.info ( "[%s] l_dDAF: [%f]" % ( self._oAtv.getIdent (), l_dDAF ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre a aeronave e a cabeceira
        #*/
        l_dDAC = cineCalc.distanciaEntrePontos ( l_tAnv, l_tCabIni )
        #l_log.info ( "[%s] l_dDAC: [%f]" % ( self._oAtv.getIdent (), l_dDAC ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância euclidiana entre a final e cabeceira
        #*/
        l_dDFC = math.sqrt (( l_dDAC ** 2 ) - ( l_dDAF ** 2 ))
        #l_log.info ( "[%s] l_dDFC: [%f]" % ( self._oAtv.getIdent (), l_dDFC ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância, em planta, a ser percorrida pela aeronave ate atingir a cabeceira
        #*/
        l_dDist = l_dDAF + l_dDFC
        #l_log.info ( "[%s] l_dDist: [%f]" % ( self._oAtv.getIdent (), l_dDist ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a desaceleração da aeronave em vôo (m/cs^2)
        #*/
        l_dAcc = self._oAtv.getDesaceleracaoVoo ()
        #l_log.info ( "[%s] l_dAcc: [%f]" % ( self._oAtv.getIdent (), l_dAcc ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a ALTURA da aeronave
        #*/
        l_dAlt = self._oAtv._dAltitude - ( self._oAer.getAltitude () * glbDefs.xCNV_ft2M )
        #l_log.info ( "[%s] l_dAlt: [%f]" % ( self._oAtv.getIdent (), l_dAlt ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância real ate a cabeceira
        #*/
        l_dDstCab = math.sqrt (( l_dDist ** 2 ) + ( l_dAlt ** 2 ))
        #l_log.info ( "[%s] l_dDstCab: [%f]" % ( self._oAtv.getIdent (), l_dDstCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a velocidade de pouso em m/cs
        #*/
        l_dVelArr = self._oAtv.getVelocidadeArr () * glbDefs.xCNV_Knots2Ms
        #l_log.info ( "[%s] l_dVelArr: [%f]" % ( self._oAtv.getIdent (), l_dVelArr ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o tempo (em cs) necessario para atingir a velocidade de pouso (t = v/a)
        #*/
        l_dTpoVArr = abs ( self._oAtv._dVeloc - l_dVelArr ) / l_dAcc
        #l_log.info ( "[%s] l_dTpoVArr: [%f]" % ( self._oAtv.getIdent (), l_dTpoVArr ))

        #** ---------------------------------------------------------------------------------------
        #*  distância (m) a ser percorrida com velocidade acima da velocidade de pouso (vot + (at^2/2))
        #*/
        l_dDstVArr = ( self._oAtv._dVeloc * l_dTpoVArr ) - ( l_dAcc * ( l_dTpoVArr ** 2 ) / 2. )
        #l_log.info ( "[%s] l_dDstVArr: [%f]" % ( self._oAtv.getIdent (), l_dDstVArr ))

        #** ---------------------------------------------------------------------------------------
        #*  a distância percorrida com velocidade acima da velocidade de pouso é maior que
        #*  a distância real ate a cabeceira ?
        #*/
        if ( l_dDstVArr > l_dDstCab ):

            #** -----------------------------------------------------------------------------------
            #*  erro, velocidade muito alta
            #*/
            l_iErr = 1
            #l_log.info ( "[%s] velocidade muito alta" % self._oAtv.getIdent ())

        #** ---------------------------------------------------------------------------------------
        #*  senão, distância Ok
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  distância (m) que falta para atigir a cabeceira, a ser feito com a velocidade de pouso
            #*/
            l_dDstVApx = l_dDstCab - l_dDstVArr
            #l_log.info ( "[%s] l_dDstVApx: [%f]" % ( self._oAtv.getIdent (), l_dDstVApx ))

            #** -----------------------------------------------------------------------------------
            #*  calcula o tempo (em cs) ate atigir a cabeceira (t = e/v)
            #*/
            l_dTpoApx = l_dDstVApx / l_dVelArr
            #l_log.info ( "[%s] l_dTpoApx: [%f]" % ( self._oAtv.getIdent (), l_dTpoApx ))

            #** -----------------------------------------------------------------------------------
            #*  calcula o tempo total ate o pouso
            #*/
            l_dTpoTot = l_dTpoVArr + l_dTpoApx
            #l_log.info ( "[%s] l_dTpoTot: [%f]" % ( self._oAtv.getIdent (), l_dTpoTot ))

            #** -----------------------------------------------------------------------------------
            #*  calcula razao de descida, em pes/min
            #*/
            l_dRaz = ( l_dAlt * glbDefs.xCNV_M2ft ) / ( l_dTpoTot / 6000. )
            #l_log.info ( "[%s] l_dRaz: [%f]" % ( self._oAtv.getIdent (), l_dRaz ))

            #** -----------------------------------------------------------------------------------
            #*  razao calculada é maior que a razao maxima de descida da aeronave ?
            #*/
            if ( l_dRaz > self._oAtv.getRazaoDescidaMax ()):

                #** -------------------------------------------------------------------------------
                #*  erro, rampa maior que a permitida
                #*/
                l_iErr = 2
                #l_log.info ( "[%s] rampa maior que a permitida" % self._oAtv.getIdent ())

            #** -----------------------------------------------------------------------------------
            #*  senão, rampa Ok
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  Ok
                #*/
                l_iErr = 0
                #l_log.info ( "[%s] Ok" % self._oAtv.getIdent ())

        #l_log.info ( "[%s] l_iErr: [%d]" % ( self._oAtv.getIdent (), l_iErr ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_iErr )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::obtemSetor
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  ja foi determinado antes, que a aeronave ou encontra-se no setor 0 ou no setor 1.
    #*          Aqui, o setor 0 é dividido em 0 e 2 ( 0 acima da Final e 2 abaixo ), e o setor 1
    #*          é dividido em 1 e 3.
    #*  ------------------------------------------------------------------------------------------
    #*/
    def obtemSetor ( self, f_iCkt ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::obtemSetor"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iCkt >= 0 ) and ( f_iCkt < locDefs.xMAX_Circuitos ))

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
            return ( 0 )

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        logger.info ( "[%s] l_iPst: [%d]" % ( self._oAtv.getIdent (), l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( f_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 0 (perna do vento)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 0 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a perna do vento
        #*/
        l_tVnto = l_oSeg._tSegReta
        assert ( l_tVnto )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 1 (perna base)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 1 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a perna base
        #*/
        l_tBase = l_oSeg._tSegReta
        assert ( l_tBase )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 2 (perna do contra-vento)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 2 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a reta da perna do contra-vento
        #*/
        l_tCVto = l_oSeg._tSegReta
        assert ( l_tCVto )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 3 (perna de travez)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 3 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a reta da perna de travez
        #*/
        l_tTrvz = l_oSeg._tSegReta
        assert ( l_tTrvz )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distãncia entre a aeronave e os vários segmentos
        #*/
        l_dDVnto = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_tVnto )
        l_dDBase = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_tBase )
        l_dDCVto = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_tCVto )
        l_dDTrvz = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_tTrvz )

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        logger.info ( "[%s] l_iCab: [%d]" % ( self._oAtv.getIdent (), l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a direção da cabeceira da pista
        #*/
        l_dCabDir = l_oCab._dCabDir
        logger.info ( "[%s] l_dCabDir: [%f]" % ( self._oAtv.getIdent (), l_dCabDir ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o angulo entre a aeronave e a cabeceira da pista
        #*/
        l_dAng = math.fabs ( self._oAtv._dDirAtu - l_dCabDir )
        logger.info ( "[%s] l_dAng: [%f]" % ( self._oAtv.getIdent (), l_dAng ))

        #** ---------------------------------------------------------------------------------------
        #*/
        if (( abs ( l_dDVnto - l_dDCVto ) < 200. ) and (( l_dAng < 3. ) or ( 180 == int ( round ( l_dAng ))))):

            #** -----------------------------------------------------------------------------------
            #*  está na final
            #*/
            l_iSetor = 4

        #** ---------------------------------------------------------------------------------------
        #*  senão, 
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  distância ate a perna de travez maior que a distância ate a perna base ?
            #*/
            if ( l_dDTrvz > l_dDBase ):

                #** -------------------------------------------------------------------------------
                #*  distância ate a perna do vento menor que a distância ate a perna do contra-vento ?
                #*/
                if ( l_dDVnto < l_dDCVto ):

                    #** ---------------------------------------------------------------------------
                    #*  aeronave no setor 0, acima da final
                    #*/
                    l_iSetor = 0

                else:

                    #** ---------------------------------------------------------------------------
                    #*  aeronave no setor 2, abaixo da final
                    #*/
                    l_iSetor = 2

            #** -----------------------------------------------------------------------------------
            #*  senão, distância ate a perna de travez menor ou igual a distância ate a perna base
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  distância ate a perna do vento menor que a distância ate a perna do contra-vento ?
                #*/
                if ( l_dDVnto < l_dDCVto ):

                    #** ---------------------------------------------------------------------------
                    #*  aeronave no setor 1, acima da final
                    #*/
                    l_iSetor = 1

                #** -------------------------------------------------------------------------------
                #*  senão, distância ate a perna do vento maior ou igual a distância ate a perna do
                #*  contra-vento
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  aeronave no setor 3, abaixo da final
                    #*/
                    l_iSetor = 3

        logger.info ( "[%s] setor: [%d]" % ( self._oAtv.getIdent (), l_iSetor ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_iSetor )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::obtemSetorPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemSetorPouso ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::obtemSetorPouso"


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
            return ( 0 )

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "[%s] l_iPst: [%d]" % ( self._oAtv.getIdent (), l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "[%s] l_iCkt: [%d]" % ( self._oAtv.getIdent (), l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( l_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 2 (perna base)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 1 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a perna base
        #*/
        l_tBase = l_oSeg._tSegReta
        assert ( l_tBase )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 4 (perna do travez)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 3 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a perna de travez
        #*/
        l_tTrvz = l_oSeg._tSegReta
        assert ( l_tTrvz )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 1 (perna do vento)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 0 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #l_log.info ( "[%s] self._oAtv._tPosicao: [%f]" % ( self._oAtv.getIdent (), str ( self._oAtv._tPosicao ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a distância entre a perna base e o travez
        #*/
        l_dDBT = l_oSeg._dSegDist
        #l_log.info ( "[%s] l_dDBT: [%f]" % ( self._oAtv.getIdent (), l_dDBT ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a distância entre a aeronave e a perna base    
        #*/
        l_dDAB = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_tBase )
        #l_log.info ( "[%s] l_dDAB: [%f]" % ( self._oAtv.getIdent (), l_dDAB ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a distância entre a aeronave e a perna de travez
        #*/
        l_dDAT = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_tTrvz )
        #l_log.info ( "[%s] l_dDAT: [%f]" % ( self._oAtv.getIdent (), l_dDAT ))

        #l_log.info ( "( l_dDAT + 2. ) > ( l_dDAB + l_dDBT ): (%f) > (%f)" % (( l_dDAT + 2. ), ( l_dDAB + l_dDBT )))
        #l_log.info ( "( l_dDAB + 2. ) > ( l_dDAT + l_dDBT ): (%f) > (%f)" % (( l_dDAB + 2. ), ( l_dDAT + l_dDBT )))

        #** ---------------------------------------------------------------------------------------
        #*  aeronave a esquerda da perna base ? 
        #*/
        if (( l_dDAT + 2. ) > ( l_dDAB + l_dDBT )):

            #** -----------------------------------------------------------------------------------
            #*  ok para pouso na cabeceira 0  
            #*/
            l_iSetor = 0

        #** ---------------------------------------------------------------------------------------
        #*  aeronave a direita da perna de travez ? 
        #*/
        elif (( l_dDAB + 2. ) > ( l_dDAT + l_dDBT )):

            #** -----------------------------------------------------------------------------------
            #*  ok para pouso na cabeceira 1  
            #*/
            l_iSetor = 1

        #** ---------------------------------------------------------------------------------------
        #*  aeronave entre a perna base e a perna de travez ? 
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  ok para pouso na cabeceira 1  
            #*/
            l_iSetor = 2

        #** ---------------------------------------------------------------------------------------
        #*/
        #l_log.info ( "[%s] setor: [%d]" % ( self._oAtv.getIdent (), l_iSetor ))

        #** ---------------------------------------------------------------------------------------
        #*/
        """
        #for l_iY in xrange ( 960 ):

            #l_szLin = "%03d !" % l_iY
            
            #for l_iX in xrange ( 960 ):

                #l_tClick = viewUtils.device2Scale (( l_iX, l_iY ))
                #l_tClick = viewUtils.unormalizeXY ( l_tClick )
                #l_log.info ( "[%s] l_tClick: [%f]" % ( self._oAtv.getIdent (), str ( l_tClick ))

                #l_dDAB = cineCalc.distanciaPontoRetaABS ( l_tClick, l_tBase )
                #l_dDAT = cineCalc.distanciaPontoRetaABS ( l_tClick, l_tTrvz )

                #l_log.info ( "( l_dDAT + 2. ) > ( l_dDAB + l_dDBT ): (%f) > (%f)" % (( l_dDAT + 2. ), ( l_dDAB + l_dDBT )))
                #l_log.info ( "( l_dDAB + 2. ) > ( l_dDAT + l_dDBT ): (%f) > (%f)" % (( l_dDAB + 2. ), ( l_dDAT + l_dDBT )))

                #if   (( l_dDAT + 2. ) > ( l_dDAB + l_dDBT )): l_szLin += '0'
                #elif (( l_dDAB + 2. ) > ( l_dDAT + l_dDBT )): l_szLin += '1'
                #else:                                         l_szLin += ' '

            #l_log.info ( "[%s] %s" % ( self._oAtv.getIdent (), l_szLin ))
        """

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_iSetor )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::obtemSituacao
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  nos testes a seguir, é somado 2 a algumas distâncias de modo a evitar erros de
    #*          arredondamento. Assim, está garantido que as aeronaves encontram-se exatamente na
    #*          situação determinada.
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemSituacao ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::obtemSituacao"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: [%f]" % ( self._oAtv.getIdent (), l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "l_iCkt: [%d]" % ( self._oAtv.getIdent (), l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( l_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 1 (perna do vento)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 0 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância da perna do vento
        #*/
        l_dDPV = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_oSeg._tSegReta )
        #l_log.info ( "l_dDPV: [%f]" % ( self._oAtv.getIdent (), l_dDPV ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o angulo entre a aeronave e a perna do vento
        #*/
        l_dAngV = ( 360. + self._oAtv._dDirAtu - l_oSeg._dSegDir ) % 360.
        #l_log.info ( "l_dAngV: [%f]" % ( self._oAtv.getIdent (), l_dAngV ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 2 (perna base)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 1 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a distância entre a perna do vento e a do contra-vento
        #*/
        l_dDVC = l_oSeg._dSegDist
        #l_log.info ( "l_dDVC: [%f]" % ( self._oAtv.getIdent (), l_dDVC ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento 3 (perna do contra-vento)
        #*/
        l_oSeg = l_oCkt.getCktSeg ( 2 )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância da perna do contra-vento
        #*/
        l_dDPC = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, l_oSeg._tSegReta )
        #l_log.info ( "l_dDPC: [%f]" % ( self._oAtv.getIdent (), l_dDPC ))

        #** ---------------------------------------------------------------------------------------
        #*  está na direção da perna do vento ?
        #*/
        if ( 0 == int ( round ( l_dAngV ))):

            #** -----------------------------------------------------------------------------------
            #*  está nas proximidades da perna do vento ou do contra-vento ?
            #*/
            if ( l_dDPV <= 50. ):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 14

            #** -----------------------------------------------------------------------------------
            #*/
            elif ( int ( round ( l_dDPV )) == int ( round ( l_dDVC ))):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 15

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dDPC + 2. ) > ( l_dDPV + l_dDVC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 5

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dDVC + 2. ) > ( l_dDPV + l_dDPC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 12

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 9

        #** ---------------------------------------------------------------------------------------
        #*  o angulo entre aeronave e perna do vento < 180 ?
        #*/
        elif ( l_dAngV < 180. ):

            #** -----------------------------------------------------------------------------------
            #*/
            if (( l_dDPC + 2. ) > ( l_dDPV + l_dDVC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 6

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dDVC + 2. ) > ( l_dDPV + l_dDPC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 7

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 8

        #** ---------------------------------------------------------------------------------------
        #*  o angulo entre aeronave e perna do vento > 180 ?
        #*/
        elif ( l_dAngV > 180. ):

            #** -----------------------------------------------------------------------------------
            #*/
            if (( l_dDPC + 2. ) > ( l_dDPV + l_dDVC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 3

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dDVC + 2. ) > ( l_dDPV + l_dDPC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 2

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 1

        #** ---------------------------------------------------------------------------------------
        #*  está na direção da perna do vento ?
        #*/
        else:  #* l_dAngV = 180.

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_dDPV <= 50. ):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 13

            #** -----------------------------------------------------------------------------------
            #*/
            elif ( int ( round ( l_dDPV )) == int ( round ( l_dDVC ))):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 16

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dDPC + 2. ) > ( l_dDPV + l_dDVC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 4

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dDVC + 2. ) > ( l_dDPV + l_dDPC )):

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 11

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_iSit = 10

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_iSit )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::trataSituacao02
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def trataSituacao02 ( self, f_oSeg ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::trataSituacao02"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oSeg )

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
        #*  obtém a proa do segmento
        #*/
        l_dSegProa = ( 30. + f_oSeg._dSegProa ) % 360.
        #l_log.info ( "Proa do segmento: " % ( self._oAtv.getIdent (), l_dSegProa ))

        #** ---------------------------------------------------------------------------------------
        #*  converte a proa em direção
        #*/
        l_dDir = cineCalc.convProa2Direcao (( l_dSegProa, self._oAer.getDifDeclinacao ()))
        #l_log.info ( "Direção do segmento: " % ( self._oAtv.getIdent (), l_dDir ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o sentido de menor rotação
        #*/
        l_cSent = cineCalc.sentidoRotacao ( self._oAtv._dDirAtu, l_dDir )
        #l_log.info ( "l_cSent: " % ( str ( l_cSent ))

        #** ---------------------------------------------------------------------------------------
        #*  sentido de rotação diferente do atual ?
        #*/
        if ( 'I' != l_cSent ):

            #** -----------------------------------------------------------------------------------
            #*  sentido anti-horario ?
            #*/
            if ( 'A' == l_cSent ):

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

            #** -----------------------------------------------------------------------------------
            #*  sentido horario ?
            #*/
            elif ( 'H' == l_cSent ):

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

            #** -----------------------------------------------------------------------------------
            #*  altera sentido de curva
            #*/
            self._oAtv._cSentidoCurva = l_cSent

            #** -----------------------------------------------------------------------------------
            #*  proa do segmento
            #*/
            self._oAtv._dProaDem = l_dSegProa

            #** -----------------------------------------------------------------------------------
            #*  enquanto está curvando...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                   ( self._oAtv._dProa != self._oAtv._dProaDem )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #l_log.info ( "Fim da primeira curva na situação 2" )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( not (( glbData.g_bKeepRun ) and
                  ( self._oAtv._bActive ) and
                  ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ))):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*/
        l_bFlag = True

        #** ---------------------------------------------------------------------------------------
        #*  obtém a situação da aeronave
        #*/
        l_iSit = self.obtemSituacao ()
        #l_log.info ( "Nova situação (apos curva): " + str ( l_iSit ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira 1 ?
        #*/
        if ( 0 == l_iCab ):

            #** -----------------------------------------------------------------------------------
            #*  entrando no circuito pela perna do vento ?
            #*/
            if ( 'V' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  passei para o outro lado da perna
                #*/
                l_bFlag = not ( l_iSit in [ 3, 4, 5, 6, 13 ] )

            #** -----------------------------------------------------------------------------------
            #*  senão, entrando no circuito por outro ponto
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_bFlag = not ( l_iSit in [ 1, 8, 9, 10, 15 ] )

        #** ---------------------------------------------------------------------------------------
        #*  senão, cabeceira 2
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  entrando no circuito pela perna do vento ?
            #*/
            if ( 'V' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  passei para o outro lado da perna
                #*/
                l_bFlag = not ( l_iSit in [ 1, 8, 9, 10, 15 ] )

            #** -----------------------------------------------------------------------------------
            #*  senão, entrando no circuito por outro ponto
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_bFlag = not ( l_iSit in [ 3, 4, 5, 6, 13 ] )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância do inicio da curva
        #*/
        l_dDIC = cineCalc.distanciaInicioCurva ( self._oAtv._dDirAtu,
                                                 f_oSeg._dSegDir,
                                                 self._oAtv.getRaioCurva ())
        #l_log.info ( "Situação 2: DIC: " + str ( l_dDIC ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância da aeronave ao segmento
        #*/
        l_dDPS = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, f_oSeg._tSegReta )
        #l_log.info ( "Situação 2: DPS(1): " + str ( l_dDPS ))

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( l_bFlag ):

            #** -----------------------------------------------------------------------------------
            #*  enquanto não atingir o ponto de inicio da curva...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                   ( l_dDPS > l_dDIC )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  calcula a distância da aeronave ao segmento
                #*/
                l_dDPS = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, f_oSeg._tSegReta )
                #l_log.info ( "Situação 2: DPS(2): " + str ( l_dDPS ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  keep going ?
            #*/
            if (( glbData.g_bKeepRun ) and
                ( self._oAtv._bActive ) and
                ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] )):

                #** -------------------------------------------------------------------------------
                #*  curva pela esquerda
                #*/
                self._oAtv._cSentidoCurva = 'E'

                #** -------------------------------------------------------------------------------
                #*  proa do segmento
                #*/
                self._oAtv._dProaDem = f_oSeg._dSegProa

                #** -------------------------------------------------------------------------------
                #*  enquanto estiver curvando...
                #*/
                while (( glbData.g_bKeepRun ) and
                       ( self._oAtv._bActive ) and
                       ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                       ( self._oAtv._dProa != self._oAtv._dProaDem )):

                    #** ---------------------------------------------------------------------------
                    #*  obtém o tempo inicial em segundos
                    #*/
                    l_lNow = time.time ()
                    #l_log.info ( "l_lNow: " + str ( l_lNow ))

                    #** ---------------------------------------------------------------------------
                    #*  vôo normal
                    #*/
                    self.procVooNormal ()

                    #** ---------------------------------------------------------------------------
                    #*  obtém o tempo final em segundos e calcula o tempo decorrido
                    #*/
                    l_lDif = time.time () - l_lNow
                    #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                    #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                    #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                    #** ---------------------------------------------------------------------------
                    #*  está adiantado ?
                    #*/
                    if ( glbDefs.xTIM_Wait > l_lDif ):
                                                        
                        #** -----------------------------------------------------------------------
                        #*  permite o scheduler (1/10th)
                        #*/
                        time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  senão, not l_bFlag
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                   ( l_dDPS < ( l_dDIC + 300. ))):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  calcula a distância da aeronave ao segmento
                #*/
                l_dDPS = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, f_oSeg._tSegReta )
                #l_log.info ( "l_dDPS(3): " + str ( l_dDPS ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  keep going ?
            #*/
            if (( glbData.g_bKeepRun ) and
                ( self._oAtv._bActive ) and
                ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] )):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao06 ( f_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::trataSituacao06
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def trataSituacao06 ( self, f_oSeg ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::trataSituacao06"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oSeg )

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
        #*  obtém a proa do segmento
        #*/
        l_dSegProa = ( 330. + f_oSeg._dSegProa ) % 360.
        #l_log.info ( "l_dSegProa: " + str ( l_dSegProa ))

        #** ---------------------------------------------------------------------------------------
        #*  converte a proa em direção
        #*/
        l_dDir = cineCalc.convProa2Direcao (( l_dSegProa, self._oAer.getDifDeclinacao ()))
        #l_log.info ( "l_dDir: " + str ( l_dDir ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o sentido de menor rotação
        #*/
        l_cSent = cineCalc.sentidoRotacao ( self._oAtv._dDirAtu, l_dDir )
        #l_log.info ( "l_cSent: " + str ( l_cSent ))

        #** ---------------------------------------------------------------------------------------
        #*  sentido de rotação diferente do atual ?
        #*/
        if ( 'I' != l_cSent ):

            #** -----------------------------------------------------------------------------------
            #*  sentido anti-horario ?
            #*/
            if ( 'A' == l_cSent ):

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

            #** -----------------------------------------------------------------------------------
            #*  sentido horario ?
            #*/
            elif ( 'H' == l_cSent ):

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

            #** -----------------------------------------------------------------------------------
            #*  altera sentido de curva
            #*/
            self._oAtv._cSentidoCurva = l_cSent

            #** -----------------------------------------------------------------------------------
            #*  proa do segmento
            #*/
            self._oAtv._dProaDem = l_dSegProa

            #** -----------------------------------------------------------------------------------
            #*  enquanto faz a curva...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                   ( self._oAtv._dProa != self._oAtv._dProaDem )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( not (( glbData.g_bKeepRun ) and
                  ( self._oAtv._bActive ) and
                  ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ))):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*/
        l_bFlag = True

        #** ---------------------------------------------------------------------------------------
        #*  obtém a situação da aeronave
        #*/
        l_iSit = self.obtemSituacao ()
        #l_log.info ( "l_iSit: " + str ( l_iSit ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira 1 ?
        #*/
        if ( 0 == l_iCab ):

            #** -----------------------------------------------------------------------------------
            #*  entrando no circuito pela perna do vento ?
            #*/
            if ( 'V' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  passei para o outro lado da perna
                #*/
                l_bFlag = not ( l_iSit in [ 1, 2, 7, 8, 9, 10, 11, 12, 15 ] )

            #** -----------------------------------------------------------------------------------
            #*  senão, entrando no circuito por outro ponto
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_bFlag = not ( l_iSit in [ 2, 3, 4, 5, 6, 7, 11, 12, 13 ] )

        #** ---------------------------------------------------------------------------------------
        #*  senão, cabeceira 2
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  entrando no circuito pela perna do vento ?
            #*/
            if ( 'V' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  passei para o outro lado da perna
                #*/
                l_bFlag = not ( l_iSit in [ 2, 3, 4, 5, 6, 7, 11, 12, 13 ] )

            #** -----------------------------------------------------------------------------------
            #*  senão, entrando no circuito por outro ponto
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*/
                l_bFlag = not ( l_iSit in [ 1, 2, 7, 8, 9, 10, 11, 12, 15 ] )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância ao inicio da curva
        #*/
        l_dDIC = cineCalc.distanciaInicioCurva ( self._oAtv._dDirAtu,
                                                 f_oSeg._dSegDir,
                                                 self._oAtv.getRaioCurva ())
        #l_log.info ( "l_dDIC: " + str ( l_dDIC ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância da aeronave ao segmento
        #*/
        l_dDPS = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, f_oSeg._tSegReta )
        #l_log.info ( "l_dDPS(1): " + str ( l_dDPS ))

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( l_bFlag ):

            #** -----------------------------------------------------------------------------------
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                   ( l_dDPS > l_dDIC )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*/
                l_dDPS = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, f_oSeg._tSegReta )
                #l_log.info ( "l_dDPS(2): " + str ( l_dDPS ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_dDPS <= l_dDIC ):

                #** -------------------------------------------------------------------------------
                #*  curva pela direita
                #*/
                self._oAtv._cSentidoCurva = 'D'

                #** -------------------------------------------------------------------------------
                #*  proa do segmento
                #*/
                self._oAtv._dProaDem = f_oSeg._dSegProa

                #** -------------------------------------------------------------------------------
                #*  enquanto faz a curva...
                #*/
                while (( glbData.g_bKeepRun ) and
                       ( self._oAtv._bActive ) and
                       ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                       ( self._oAtv._dProa != self._oAtv._dProaDem )):

                    #** ---------------------------------------------------------------------------
                    #*  obtém o tempo inicial em segundos
                    #*/
                    l_lNow = time.time ()
                    #l_log.info ( "l_lNow: " + str ( l_lNow ))

                    #** ---------------------------------------------------------------------------
                    #*  vôo normal
                    #*/
                    self.procVooNormal ()

                    #** ---------------------------------------------------------------------------
                    #*  obtém o tempo final em segundos e calcula o tempo decorrido
                    #*/
                    l_lDif = time.time () - l_lNow
                    #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                    #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                    #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                    #** ---------------------------------------------------------------------------
                    #*  está adiantado ?
                    #*/
                    if ( glbDefs.xTIM_Wait > l_lDif ):
                                                        
                        #** -----------------------------------------------------------------------
                        #*  permite o scheduler (1/10th)
                        #*/
                        time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  senão, not l_bFlag
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] ) and
                   ( l_dDPS < ( l_dDIC + 300. ))):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*/
                l_dDPS = cineCalc.distanciaPontoRetaABS ( self._oAtv._tPosicao, f_oSeg._tSegReta )
                #l_log.info ( "l_dDPS(3): " + str ( l_dDPS ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_dDPS >= ( l_dDIC + 300. )):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao02 ( f_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  CALLBACKS
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::cbkNavAlt
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAlt - a nova altitude em pes
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkNavAlt ( self, f_iAlt ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::cbkNavAlt"


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
        #*  aeronave está voando ?
        #*/
        if ( not self._oAtv._bSolo ):

            #** -----------------------------------------------------------------------------------
            #*  salva a nova demanda em metros
            #*/
            self._oAtv._dAltDem = ( f_iAlt * glbDefs.xCNV_ft2M )

            #** -----------------------------------------------------------------------------------
            #*  aeronave está na final ?
            #*/
            if ( 'F' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  evita que aeronaves, na final, mudem algum item de navegação e continue
                #*  com os outros ativos. Mudando proa ou velocidade, a aeronave poderia pousar
                #*  fora da pista, pois a altitude de demanda continuaria a do aerodromo.
                #*  Assim, qualquer mudanca em atributos de navegação leva o StatusVoo para 'N'
                #*/
                self._oAtv._dProaDem = self._oAtv._dProa
                self._oAtv._dVelDem  = self._oAtv._dVeloc

                #** -------------------------------------------------------------------------------
                #*  apaga os dados de navegação de demanda da strip
                #*/
                #guiStrip.apagaDemanda ( l_iAtv )

                #** -------------------------------------------------------------------------------
                #*  coloca em vôo normal
                #*/
                self._oAtv.setStatusVoo ( 'N' )

        #** ---------------------------------------------------------------------------------------
        #*  senão, aeronave está no solo
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  exibe uma mensagem de erro
            #*/
            #guiPiloto.escreveMsg ( [ "Aeronave selecionada está inativa ou no solo !" ], glbDefs.xCOR_Yellow )
            pass

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::cbkNavCurva
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkNavCurva ( self, f_cSent, f_iProa ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::cbkNavCurva"


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
        #*  aeronave está voando ?
        #*/
        if ( not self._oAtv._bSolo ):

            #** -----------------------------------------------------------------------------------
            #*  aeronave está na final ?
            #*/
            if ( 'F' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  evita que aeronaves, na final, mudem algum item de navegação e continue
                #*  com os outros ativos. Mudando proa ou velocidade, a aeronave poderia pousar
                #*  fora da pista, pois a altitude de demanda continuaria a do aerodromo.
                #*  Assim, qualquer mudanca em atributos de navegação leva o StatusVoo para 'N'
                #*/
                self._oAtv._dVelDem = self._oAtv._dVeloc
                self._oAtv._dAltDem = self._oAtv._dAltitude

                #** -------------------------------------------------------------------------------
                #*  apaga os dados de navegação de demanda da strip
                #*/
                #guiStrip.apagaDemanda ( l_iAtv )

                #** -------------------------------------------------------------------------------
                #*  coloca em vôo normal
                #*/
                self._oAtv.setStatusVoo ( 'N' )

            #** -----------------------------------------------------------------------------------
            #*  permite que seja possivel uma curva de 360, em qualquer sentido
            #*/
            if ( f_iProa == int ( round ( self._oAtv._dProa ))):

                #** -------------------------------------------------------------------------------
                #*  curva a direita ?
                #*/
                if ( 'D' == f_cSent ):

                    l_dVal = +0.01

                #** -------------------------------------------------------------------------------
                #*  senão, curva a esquerda
                #*/
                else:

                    l_dVal = -0.01

                #** -------------------------------------------------------------------------------
                #*/
                self._oAtv._dProa += l_dVal

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  coloca em vôo normal. Permite que apenas curvas de 360 sejam possiveis
                #*  quando uma aeronave está no circuito
                #*/
                self._oAtv.setStatusVoo ( 'N' )

            #** -----------------------------------------------------------------------------------
            #*  configura sentido de curva
            #*/
            self._oAtv._cSentidoCurva = f_cSent

            #** -----------------------------------------------------------------------------------
            #*  configura proa desejada
            #*/
            self._oAtv._dProaDem = f_iProa

        #** ---------------------------------------------------------------------------------------
        #*  senão, aeronave está no solo
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  exibe uma mensagem de erro
            #*/
            #guiPiloto.escreveMsg ( [ "Aeronave inativa ou no solo !" ], glbDefs.xCOR_Yellow )
            pass

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::cbkNavVel
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_dVel - velocidade selecionada em knots
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkNavVel ( self, f_dVel ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::cbkNavVel"


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
        #*  aeronave está voando ?
        #*/
        if ( not self._oAtv._bSolo ):

            #** -----------------------------------------------------------------------------------
            #*  converte knots para 'metros por centesimos de segundo'
            #*/
            self._oAtv._dVelDem = ( f_dVel * glbDefs.xCNV_Knots2Ms )

            #** -----------------------------------------------------------------------------------
            #*  aeronave está na final ?
            #*/
            if ( 'F' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  evita que aeronaves, na final, mudem algum item de navegação e continue com os
                #*  outros ativos. Mudando proa ou velocidade, a aeronave poderia pousar fora da
                #*  pista, pois a altitude de demanda continuaria a do aerodromo. Assim, qualquer
                #*  mudanca em atributos de navegação leva o StatusVoo para 'N'
                #*/
                self._oAtv._dProaDem = self._oAtv._dProa
                self._oAtv._dAltDem  = self._oAtv._dAltitude

                #** -------------------------------------------------------------------------------
                #*  apaga os dados de navegação de demanda da strip
                #*/
                #guiStrip.apagaDemanda ( l_iAtv )

                #** -------------------------------------------------------------------------------
                #*  coloca em vôo normal
                #*/
                self._oAtv.setStatusVoo ( 'N' )

        #** ---------------------------------------------------------------------------------------
        #*  senão, aeronave está no solo
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  exibe uma mensagem de erro
            #*/
            #guiMessage.addMsg ( [ "Aeronave inativa ou no solo !" ], glbDefs.xCOR_Yellow )
            pass

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  PROCEDURES LEVEL 2
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execCktPernaContraVento
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  o que difere está procedure da outra (...PernaVento)
    #*          é o segmento de entrada e a ordem da situação.  Por
    #*          exemplo, o que ocorre com a perna do vento na situação 2,
    #*          é o mesmo que ocorre com a perna contra o vento na
    #*          situação 7
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execCktPernaContraVento ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execCktPernaContraVento"


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
        #*/
        l_iSit = self.obtemSituacao ()
        #l_log.info ( "l_iSit: " + str ( l_iSit ))

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "l_iCkt: " + str ( l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento inicial do circuito
        #*/
        if ( 0 == l_iCab ):

            l_iSeg = 2

        else:

            l_iSeg = 0

        #l_log.info ( "l_iSeg: " + str ( l_iSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( l_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento
        #*/
        l_oSeg = l_oCkt.getCktSeg ( l_iSeg )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira 1 ?
        #*/
        if ( 0 == l_iCab ):

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_iSit in [ 1, 8, 9, 10, 15 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao06 ( l_oSeg )

            #** -----------------------------------------------------------------------------------
            #*/
            elif ( l_iSit in [ 2, 3, 4, 5, 6, 7, 11, 12, 13, 14 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao02 ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  senão, cabeceira 2
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_iSit in [ 1, 2, 7, 8, 9, 10, 11, 12, 15, 16 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao02 ( l_oSeg )

            #** -----------------------------------------------------------------------------------
            #*/
            elif ( l_iSit in [ 3, 4, 5, 6, 13 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao06 ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  keep moving ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] )):

            #** -----------------------------------------------------------------------------------
            #*  muda o status do vôo para 'em circuito'
            #*/
            self._oAtv.setStatusVoo ( 'C' )

            #** -----------------------------------------------------------------------------------
            #*/
            self.execEntrarNoCircuito ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execCktPernaVento
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  o que difere está procedure da outra (PernaContraVento)
    #*          é o segmento de entrada e a ordem da situação.  Por
    #*          exemplo, o que ocorre com a perna do vento na situação 2,
    #*          é o mesmo que ocorre com a perna contra o vento na
    #*          situação 7
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execCktPernaVento ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execCktPernaVento"


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
        #*/
        l_iSit = self.obtemSituacao ()
        #l_log.info ( "l_iSit: " + str ( l_iSit ))

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "l_iCkt: " + str ( l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento inicial do circuito
        #*/
        if ( 0 == l_iCab ):

            l_iSeg = 0

        else:

            l_iSeg = 2

        #l_log.info ( "l_iSeg: " + str ( l_iSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( l_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento
        #*/
        l_oSeg = l_oCkt.getCktSeg ( l_iSeg )
        assert ( l_oSeg )
        assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira 1 ?
        #*/
        if ( 0 == l_iCab ):

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_iSit in [ 3, 4, 5, 6, 13 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao06 ( l_oSeg )

            #** -----------------------------------------------------------------------------------
            #*/
            elif ( l_iSit in [ 1, 2, 7, 8, 9, 10, 11, 12, 15, 16 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao02 ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  senão, cabeceira 2
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            if ( l_iSit in [ 2, 3, 4, 5, 6, 7, 11, 12, 13, 14 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao02 ( l_oSeg )

            #** -----------------------------------------------------------------------------------
            #*/
            elif ( l_iSit in [ 1, 8, 9, 10, 15 ] ):

                #** -------------------------------------------------------------------------------
                #*/
                self.trataSituacao06 ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  keep going ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( self._oAtv.getStatusVoo () in [ 'K', 'V' ] )):

            #** -----------------------------------------------------------------------------------
            #*  muda o status do vôo para 'em circuito'
            #*/
            self._oAtv.setStatusVoo ( 'C' )

            #** -----------------------------------------------------------------------------------
            #*  entra no circuito
            #*/
            self.execEntrarNoCircuito ( l_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execEntrarForaDaPerna
    #*  -------------------------------------------------------------------------------------------
    #*  trata das aeronaves que entram no circuito fora do retangulo formado pelas quatro pernas
    #*  -------------------------------------------------------------------------------------------
    #*  @param  self - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execEntrarForaDaPerna ( self, f_oSeg ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execEntrarForaDaPerna"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oSeg )

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
        #*  curva a esquerda
        #*/
        self._oAtv._cSentidoCurva = 'E'

        #** ---------------------------------------------------------------------------------------
        #*  altera demanda
        #*/
        self._oAtv._dProaDem = ( 270. + f_oSeg._dSegProa ) % 360.   #* 270 = 360 - 90

        #** ---------------------------------------------------------------------------------------
        #*  enquanto estiver curvando no circuito...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'C' == self._oAtv.getStatusVoo ()) and
               ( self._oAtv._dProa != self._oAtv._dProaDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  continua ativa e no circuito ?
        #*/
        if ( not (( glbData.g_bKeepRun ) and
                  ( self._oAtv._bActive ) and
                  ( 'C' == self._oAtv.getStatusVoo ()))):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*  obtém o numero do segmento atual
        #*/
        l_iSeg1 = f_oSeg._iSegNum
        #l_log.info ( "l_iSeg: " + str ( l_iSeg1 ))

        assert (( l_iSeg1 >= 0 ) and ( l_iSeg1 < locDefs.xMAX_Segmentos ))

        #** ---------------------------------------------------------------------------------------
        #*  encontra o segundo segmento seguinte
        #*/
        l_iSeg1 = ( l_iSeg1 + 1 ) % locDefs.xMAX_Segmentos
        l_iSeg2 = ( l_iSeg1 + 1 ) % locDefs.xMAX_Segmentos

        #** ---------------------------------------------------------------------------------------
        #*  salva o numero do segmento atual
        #*/
        self._oAtv._tCktAtual = ( self._oAtv.getCktPst (), self._oAtv.getCktCab (), l_iSeg1 )
        assert ( self._oAtv._tCktAtual )

        #** ---------------------------------------------------------------------------------------
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "l_iCkt: " + str ( l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( l_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento seguinte
        #*/
        l_oSeg2 = l_oCkt.getCktSeg ( l_iSeg2 )
        assert ( l_oSeg2 )
        assert ( isinstance ( l_oSeg2, clsPst.clsSeg ))

        #** -----------------------------------------------------------------------------------
        #*  obtém os coeficientes da reta que define o segmento
        #*/
        l_tReta = l_oSeg2._tSegReta

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posico atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre eles
        #*/
        l_dDist = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tReta )
        #l_log.info ( "l_dDist: " + str ( l_dDist ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o raio de curvatura da aeronave
        #*/
        l_dRaio = self._oAtv.getRaioCurva ()
        #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

        #** ---------------------------------------------------------------------------------------
        #*  voa ate atingir o ponto para iniciar a curva
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'C' == self._oAtv.getStatusVoo ()) and
               ( l_dDist > l_dRaio )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém a posição atual da aeronave
            #*/
            l_tAnv = self._oAtv._tPosicao
            assert ( l_tAnv )

            #** -----------------------------------------------------------------------------------
            #*  calcula a distância entre eles
            #*/
            l_dDist = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tReta )
            #l_log.info ( "l_dDist: " + str ( l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o raio de curvatura da aeronave
            #*/
            l_dRaio = self._oAtv.getRaioCurva ()
            #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  ja bloqueou o ponto de curva ?
        #*/
        if ( l_dDist <= l_dRaio ):

            #** -----------------------------------------------------------------------------------
            #*  move a aeronave pelo circuito
            #*/
            self.moveNoCircuito ( l_iPst, l_iCkt )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execEntrarNaPerna
    #*  -------------------------------------------------------------------------------------------
    #*  trata das aeronaves que entram no circuito pelo retangulo formado pelas quatro pernas
    #*  -------------------------------------------------------------------------------------------
    #*  @param  self - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execEntrarNaPerna ( self, f_oSeg ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execEntrarNaPerna"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oSeg )

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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "l_iCkt: " + str ( l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o numero do segmento atual
        #*/
        l_iSeg = f_oSeg._iSegNum
        #l_log.info ( "l_iSeg: " + str ( l_iSeg ))

        assert (( l_iSeg >= 0 ) and ( l_iSeg < locDefs.xMAX_Segmentos ))

        #** ---------------------------------------------------------------------------------------
        #*  salva o numero do segmento atual
        #*/
        self._oAtv._tCktAtual = ( l_iPst, self._oAtv.getCktCab (), l_iSeg )
        assert ( self._oAtv._tCktAtual )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o raio de curvatura da aeronave
        #*/
        l_dRaio = self._oAtv.getRaioCurva ()
        #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o ponto final do segmento
        #*/
        l_tFim = f_oSeg._tSegFim
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posico atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre eles
        #*/
        l_dDist = cineCalc.distanciaEntrePontos ( l_tAnv, l_tFim )
        #l_log.info ( "l_dDist: " + str ( l_dDist ))

        #** ---------------------------------------------------------------------------------------
        #*  enquanto não atingir o ponto para iniciar a curva...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'C' == self._oAtv.getStatusVoo ()) and
               ( l_dDist > l_dRaio )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém a posição atual da aeronave
            #*/
            l_tAnv = self._oAtv._tPosicao
            assert ( l_tAnv )

            #** -----------------------------------------------------------------------------------
            #*  calcula a distância entre eles
            #*/
            l_dDist = cineCalc.distanciaEntrePontos ( l_tAnv, l_tFim )
            #l_log.info ( "l_dDist: " + str ( l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o raio de curvatura da aeronave
            #*/
            l_dRaio = self._oAtv.getRaioCurva ()
            #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  ja bloqueou o ponto de curva ?
        #*/
        if ( l_dDist <= l_dRaio ):

            #** -----------------------------------------------------------------------------------
            #*  move a aeronave pelo circuito
            #*/
            self.moveNoCircuito ( l_iPst, l_iCkt )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execEntrarNoCircuito
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execEntrarNoCircuito ( self, f_oSeg ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execEntrarNoCircuito"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oSeg )
        assert ( isinstance ( f_oSeg, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o raio de curvatura da aeronave
        #*/
        l_dRaio = self._oAtv.getRaioCurva ()
        #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o ponto de inicio do segmento
        #*/
        l_tIni = f_oSeg._tSegIni
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o ponto final do segmento
        #*/
        l_tFim = f_oSeg._tSegFim
        assert ( l_tFim )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre o inicio do segmento e a aeronave
        #*/
        l_dDIA = cineCalc.distanciaEntrePontos ( l_tIni, l_tAnv )
        #l_log.info ( "l_dDIA: " + str ( l_dDIA ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre a aeronave e o ponto final do segmento
        #*/
        l_dDAF = cineCalc.distanciaEntrePontos ( l_tAnv, l_tFim )
        #l_log.info ( "l_dDAF: " + str ( l_dDAF ))

        #** ---------------------------------------------------------------------------------------
        #*/
        if ((( l_dDIA + 2. ) > ( f_oSeg._dSegDist + l_dDAF )) or ( l_dDAF < l_dRaio )):

            #** -----------------------------------------------------------------------------------
            #*  entra no circuito por fora da perna
            #*/
            self.execEntrarForaDaPerna ( f_oSeg )

        else:

            #** -----------------------------------------------------------------------------------
            #*  entra no circuito pela perna
            #*/
            self.execEntrarNaPerna ( f_oSeg )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execFrearAteParar
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execFrearAteParar ( self ):

        #/ nome do método (logger)
        #/ -----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execFrearAteParar"


        #** ----------------------------------------------------------------------------------------
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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira da pista
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o ponto de inicio da cabeceira do circuito
        #*/
        l_tCabIni = l_oCab._tCabIni
        assert ( l_tCabIni )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ----------------------------------------------------------------------------------------
        #*  aeronave no solo
        #*/
        self._oAtv._bSolo = True

        #** ----------------------------------------------------------------------------------------
        #*  muda o status para aeronave parando apos o pouso
        #*/
        self._oAtv.setStatusSolo ( 'S' )

        #** ----------------------------------------------------------------------------------------
        #*  monta o percurso de saida da pista para a aeronave
        #*/
        self._oAer.montarPercurso ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  exibe o percurso de saida da pista
        #*/
        self._oAtv.setShowPercurso ( True )

        #** ----------------------------------------------------------------------------------------
        #*  diminui para velocidade de taxi
        #*/
        self._oAtv._dVelDem = self._oAtv.getVelocidadeTaxi () * glbDefs.xCNV_Knots2Ms

        #** ---------------------------------------------------------------------------------------
        #*  enquanto não atinge a velocidade de taxi...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'S' == self._oAtv.getStatusSolo ()) and
               ( self._oAtv._dVeloc > self._oAtv._dVelDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ----------------------------------------------------------------------------------------
        #*  aeronave ainda parando apos o pouso ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'S' == self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  ajusta velocidade para a demanda
            #*/
            self._oAtv._dVeloc = self._oAtv._dVelDem

            #** -----------------------------------------------------------------------------------
            #*  calcula a distância entre o ponto de toque e a posição da aeronave
            #*/
            l_dDst = cineCalc.distanciaEntrePontos ( l_tCabIni, self._oAtv._tPosicao )

            #** -----------------------------------------------------------------------------------
            #*  aeronave pousou fora da pista ?
            #*/
            if ( l_dDst > l_oPst.getPstCmp ()):

                #** -------------------------------------------------------------------------------
                #*  muda o status para aeronave acidentada
                #*/
                self._oAtv.setStatusSolo ( 'A' )

            #** -----------------------------------------------------------------------------------
            #*  senão, parou ok
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtém fator de pane no pouso
                #*/
                l_btPane = self._oExe.getPanePouso ()
                #l_log.info ( "l_btPane: " + str ( l_btPane ))

                #** -------------------------------------------------------------------------------
                #*  pane no pouso ?
                #*/
                if ( 0 != l_btPane ):

                    #** ---------------------------------------------------------------------------
                    #*  gera pane no pouso ?
                    #*/
                    if ( 0 == random.randrange ( 101 - l_btPane )):

                        #** -----------------------------------------------------------------------
                        #*  fator de pane > 10 ?
                        #*/
                        if ( l_btPane > 10 ):

                            #** -------------------------------------------------------------------
                            #*  salva novo fator de pane no pouso
                            #*/
                            self._oExe.setPanePouso ( l_btPane - 10 )

                        #** -----------------------------------------------------------------------
                        #*  muda o status para aeronave aguardando ser rebocada
                        #*/
                        self._oAtv.setStatusSolo ( 'R' )

                    #** ---------------------------------------------------------------------------
                    #*  senão, pouso normal
                    #*/
                    else:

                        #** -----------------------------------------------------------------------
                        #*  muda o status para aeronave em taxi
                        #*/
                        self._oAtv.setStatusSolo ( 'T' )

                #** -------------------------------------------------------------------------------
                #*  senão, pouso normal
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave em taxi
                    #*/
                    self._oAtv.setStatusSolo ( 'T' )

        #** ---------------------------------------------------------------------------------------
        #*  oculta o percurso de saida da pista
        #*/
        self._oAtv.setShowPercurso ( False )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave aguardando reboque ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'R' == self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*/
            l_iI = 1

            #** -----------------------------------------------------------------------------------
            #*  aguarda 4 minutos pelo reboque... (300 p/min)
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( l_iI < 1200 )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  incrementa o contador
                #*/
                l_iI += 1

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  aeronave continua ativa ?
            #*/
            if (( glbData.g_bKeepRun ) and
                ( self._oAtv._bActive )):

                #** -------------------------------------------------------------------------------
                #*  muda o status para em taxi, porem em pane
                #*/
                self._oAtv.setStatusSolo ( 'B' )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execPousar
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_iAtv - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execPousar ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execPousar"


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
        #*  muda o status para 'frear ate parar'
        #*/
        self._oAtv.setStatusVoo ( 'F' )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a razao de pouso
        #*/
        self.calcRazaoPouso ( 0 )

        #** ---------------------------------------------------------------------------------------
        #*  altitude do aerodromo
        #*/
        self._oAtv._dAltDem = self._oAer.getAltitude () * glbDefs.xCNV_ft2M

        #** ---------------------------------------------------------------------------------------
        #*  enquanto corrige a rampa das aeronaves que entram na final com velocidade acima da
        #*  velocidade de aproximação
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'F' == self._oAtv.getStatusVoo ()) and
               ( self._oAtv._dVeloc != self._oAtv._dVelDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  keep going ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'F' == self._oAtv.getStatusVoo ())):

            #** -----------------------------------------------------------------------------------
            #*  calcula a razao de pouso
            #*/
            self.calcRazaoPouso ( self._oExe.getAcidente ())

            #** -----------------------------------------------------------------------------------
            #*  ate tocar o solo...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'F' == self._oAtv.getStatusVoo ()) and
                   ( self._oAtv._dAltitude != self._oAtv._dAltDem )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ----------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execPousoDireto
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execPousoDireto ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execPousoDireto"


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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        logger.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        logger.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        logger.info ( "l_iCkt: " + str ( l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a direção da cabeceira
        #*/
        l_dCabDir = l_oCab._dCabDir
        logger.info ( "l_dCabDir: " + str ( l_dCabDir ))

        #** ---------------------------------------------------------------------------------------
        #*  converte a direção em proa
        #*/
        l_dCabProa = cineCalc.convProa2Direcao (( l_dCabDir, self._oAer.getDifDeclinacao ()))
        logger.info ( "l_dCabProa: " + str ( l_dCabProa ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o setor atual da aeronave
        #*/
        l_iSetor = self.obtemSetor ( l_iCkt )
        logger.info ( "l_iSetor: " + str ( l_iSetor ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula o angulo entre a direção da aeronave e a cabeceira
        #*/
        l_dAng = abs ( self._oAtv._dDirAtu - l_dCabDir )
        logger.info ( "self._oAtv._dDirAtu: " + str ( self._oAtv._dDirAtu ))
        logger.info ( "l_dCabDir...........: " + str ( l_dCabDir ))
        logger.info ( "l_dAng: " + str ( l_dAng ))

        #** ---------------------------------------------------------------------------------------
        #*/
        l_bFinal = False

        #** ---------------------------------------------------------------------------------------
        #*  setor 0 ? (cabeceira 1, acima da final)
        #*/
        if ( 0 == l_iSetor ):

            #** -----------------------------------------------------------------------------------
            #*/
            if ( 270 == int ( round ( l_dAng ))):

                #** -------------------------------------------------------------------------------
                #*  mantem o sentido de curva
                #*/
                l_cSent = 'I'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 90.

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dAng < 90. ) or ( l_dAng > 270. )):

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 90.

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 90.

        #** ---------------------------------------------------------------------------------------
        #*  setor 1 ? (cabeceira 2, acima da final)
        #*/
        elif ( 1 == l_iSetor ):

            #** -----------------------------------------------------------------------------------
            #*/
            if ( 270. == int ( round ( l_dAng ))):

                #** -------------------------------------------------------------------------------
                #*  mantem o sentido de curva
                #*/
                l_cSent = 'I'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 270.

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dAng > 90. ) and ( l_dAng < 270. )):

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 270.

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 270.

        #** ---------------------------------------------------------------------------------------
        #*  setor 2 ? (cabeceira 0, abaixo da final)
        #*/
        elif ( 2 == l_iSetor ):

            #** -----------------------------------------------------------------------------------
            #*/
            if ( 90. == int ( round ( l_dAng ))):

                #** -------------------------------------------------------------------------------
                #*  mantem o sentido de curva
                #*/
                l_cSent = 'I'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 270.

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dAng < 90. ) or ( l_dAng > 270. )):

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 270.

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 270.

        #** ---------------------------------------------------------------------------------------
        #*  setor 3 ? (cabeceira 2, abaixo da final)
        #*/
        elif ( 3 == l_iSetor ):

            #** -----------------------------------------------------------------------------------
            #*/
            if ( 90. == int ( round ( l_dAng ))):

                #** -------------------------------------------------------------------------------
                #*  mantem o sentido de curva
                #*/
                l_cSent = 'I'

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( l_dAng > 90. ) and ( l_dAng < 270. )):

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

            #** -----------------------------------------------------------------------------------
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

            #** -----------------------------------------------------------------------------------
            #*  angulo da curva
            #*/
            l_dCurva = 90.

        #** ---------------------------------------------------------------------------------------
        #*  setor 4 ? (na final)
        #*/
        elif ( 4 == l_iSetor ):

            #** -----------------------------------------------------------------------------------
            #*  aeronave na direção da cabeceira ?
            #*/
            if ( l_dAng < 3. ):

                #** -------------------------------------------------------------------------------
                #*/
                self.ajustaNaFinal ( l_iPst, l_iCab )

                #** -------------------------------------------------------------------------------
                #*  mantem o sentido de curva
                #*/
                l_cSent = 'I'

                #** -------------------------------------------------------------------------------
                #*/
                l_bFinal = True

            #** -----------------------------------------------------------------------------------
            #*  aeronave a 180 graus com a cabeceira. Isso permite que aeronaves que acabaram
            #*  de decolar possam pousar na cabeceira oposta a decolagem, isto é, permite que
            #*  aeronaves que ja passaram a linha da Perna Base possam fazer uma manobra tipo
            #*  bolha e pousar.
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                self._oAtv._cSentidoCurva = 'D'

                #** -------------------------------------------------------------------------------
                #*  atualiza a demanda
                #*/
                self._oAtv._dProaDem = ( self._oAtv._dProa + 90. ) % 360.

                #** -------------------------------------------------------------------------------
                #*  faz uma curva de 90 graus a direita
                #*/
                while (( glbData.g_bKeepRun ) and
                       ( self._oAtv._bActive ) and
                       ( 'D' == self._oAtv.getStatusVoo ()) and
                       ( self._oAtv._dProaDem != self._oAtv._dProa )):

                    #** ---------------------------------------------------------------------------
                    #*  obtém o tempo inicial em segundos
                    #*/
                    l_lNow = time.time ()
                    #l_log.info ( "l_lNow: " + str ( l_lNow ))

                    #** ---------------------------------------------------------------------------
                    #*  vôo normal
                    #*/
                    self.procVooNormal ()

                    #** ---------------------------------------------------------------------------
                    #*  obtém o tempo final em segundos e calcula o tempo decorrido
                    #*/
                    l_lDif = time.time () - l_lNow
                    #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                    #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                    #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                    #** ---------------------------------------------------------------------------
                    #*  está adiantado ?
                    #*/
                    if ( glbDefs.xTIM_Wait > l_lDif ):
                                                        
                        #** -----------------------------------------------------------------------
                        #*  permite o scheduler (1/10th)
                        #*/
                        time.sleep ( glbDefs.xTIM_Wait - l_lDif )

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 90.

        #** ---------------------------------------------------------------------------------------
        #*  mudou o sentido ?
        #*/
        if ( 'I' != l_cSent ):

            #** -----------------------------------------------------------------------------------
            #*  altera sentido de curva
            #*/
            self._oAtv._cSentidoCurva = l_cSent

            #** -----------------------------------------------------------------------------------
            #*  altera a demanda
            #*/
            self._oAtv._dProaDem = ( l_dCurva + l_dCabProa ) % 360.

        #** ---------------------------------------------------------------------------------------
        #*  altitude de circuito
        #*/
        self._oAtv._dAltDem = ( self._oAtv.getAltitudeCircuito () + self._oAer.getAltitude ()) * glbDefs.xCNV_ft2M

        #** ---------------------------------------------------------------------------------------
        #*  velocidade de pouso
        #*/
        self._oAtv._dVelDem = self._oAtv.getVelocidadeArr () * glbDefs.xCNV_Knots2Ms

        #** ---------------------------------------------------------------------------------------
        #*  enquanto não chega a altitude de circuito e velocidade de pouso...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'D' == self._oAtv.getStatusVoo ()) and
               ( self._oAtv._dProa != self._oAtv._dProaDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  salva o setor atual
        #*/
        l_iSetorAnt = l_iSetor

        #** ---------------------------------------------------------------------------------------
        #*  obtém o setor atual
        #*/
        l_iSetor = self.obtemSetor ( l_iCkt )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a final da cabeceira
        #*/
        l_tFinal = l_oCab._tFinalReta
        assert ( l_tFinal )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre os dois
        #*/
        l_dDist = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tFinal )
        #l_log.info ( "l_dDist: " + str ( l_dDist ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o raio de curvatura da aeronave
        #*/
        l_dRaio = self._oAtv.getRaioCurva ()
        #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

        #** ---------------------------------------------------------------------------------------
        #*/
        if ((( l_iSetor != l_iSetorAnt ) or ( l_dDist < l_dRaio )) and ( not l_bFinal )):

            #** -----------------------------------------------------------------------------------
            #*  enquanto se aproxima da final...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'D' == self._oAtv.getStatusVoo ()) and
                   ( l_dDist < ( l_dRaio + 300. ))):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém a posição atual da aeronave
                #*/
                l_tAnv = self._oAtv._tPosicao
                assert ( l_tAnv )

                #** -------------------------------------------------------------------------------
                #*  calcula a distância entre a aeronave e a final
                #*/
                l_dDist = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tFinal )
                #l_log.info ( "l_dDist: " + str ( l_dDist ))

                #** -------------------------------------------------------------------------------
                #*  obtém o raio de curvatura da aeronave
                #*/
                l_dRaio = self._oAtv.getRaioCurva ()
                #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  pois posso ter mudado de setor somente apos a entrada no while anterior.
            #*/
            l_iSetor = self.obtemSetor ( l_iCkt )
            #l_log.info ( "l_iSetor: " + str ( l_iSetor ))

            #** -----------------------------------------------------------------------------------
            #*  setor 0 ou setor 3 ? (acima da final)
            #*/
            if ( l_iSetor in [ 0, 3 ] ):

                #** -------------------------------------------------------------------------------
                #*  curva a esquerda
                #*/
                l_cSent = 'E'

                #** -------------------------------------------------------------------------------
                #*  angulo da curva
                #*/
                l_dCurva = 90.

            #** -----------------------------------------------------------------------------------
            #*  setor 1 ou setor 2 ? (abaixo da final)
            #*/
            elif ( l_iSetor in [ 1, 2 ] ):

                #** -------------------------------------------------------------------------------
                #*  curva a direita
                #*/
                l_cSent = 'D'

                #** -------------------------------------------------------------------------------
                #*  sentido e angulo da curva
                #*/
                l_dCurva = 270.

            #** -----------------------------------------------------------------------------------
            #*  altera sentido de curva
            #*/
            self._oAtv._cSentidoCurva = l_cSent

            #** -----------------------------------------------------------------------------------
            #*  altera demanda
            #*/
            self._oAtv._dProaDem = ( l_dCurva + l_dCabProa ) % 360.
            #l_log.info ( "Proa: " + str ( self._oAtv._dProaDem ))

            #** -----------------------------------------------------------------------------------
            #*  enquanto faz a curva...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'D' == self._oAtv.getStatusVoo ()) and
                   ( self._oAtv._dProa != self._oAtv._dProaDem )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  keep going ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'D' == self._oAtv.getStatusVoo ())):

            #** -----------------------------------------------------------------------------------
            #*  coloca em modo de pouso
            #*/
            self._oAtv.setStatusVoo ( 'P' )

            #** -----------------------------------------------------------------------------------
            #*  ainda não está na final (4 != l_iSetor) ou mudou sentido ('I' != l_cSent) ?
            #*/
            if (( 4 != l_iSetor ) or ( 'I' != l_cSent )):

                #** -------------------------------------------------------------------------------
                #*  aproa a final
                #*/
                self.aproaFinal ( l_iPst, l_iCab )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execPousoForaDaPista
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execPousoForaDaPista ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execPousoForaDaPista"


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
        #*  enquanto não alcanca a altitude correta...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'A' == self._oAtv.getStatusVoo ()) and
               ( self._oAtv._dAltitude != self._oAtv._dAltDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  keep going ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'A' == self._oAtv.getStatusVoo ())):

            #** -----------------------------------------------------------------------------------
            #*/
            #ApagaAviao ( self.PosicaoAnterior.X, self.PosicaoAnterior.Y )

            #** -----------------------------------------------------------------------------------
            #*  aeronave no solo
            #*/
            self._oAtv._bSolo = True

            #** -----------------------------------------------------------------------------------
            #*  muda status para acidente no pouso
            #*/
            self._oAtv.setStatusSolo ( 'A' )

            #** -----------------------------------------------------------------------------------
            #*/
            #ApagaNavegacao ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execPousoPeloCircuito
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execPousoPeloCircuito ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execPousoPeloCircuito"


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
        #*  pista do circuito
        #*/
        l_iPst = self._oAtv.getCktPst ()
        #l_log.info ( "l_iPst: " + str ( l_iPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a pista
        #*/
        l_oPst = self._oAer.getPista ( l_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira do circuito
        #*/
        l_iCab = self._oAtv.getCktCab ()
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a cabeceira da pista
        #*/
        l_oCab = l_oPst.getPstCab ( l_iCab )
        assert ( l_oCab )
        assert ( isinstance ( l_oCab, clsCab.clsCab ))

        #** ---------------------------------------------------------------------------------------
        #*  verifica qual segmento é a perna base
        #*/
        if ( 0 == l_iCab ):

            #** -----------------------------------------------------------------------------------
            #*  para a cabeceira 1, o segmento é o 2
            #*/
            l_iBase = 1

        else:

            #** -----------------------------------------------------------------------------------
            #*  para a cabeceira 2, o segmento é o 4
            #*/
            l_iBase = 3

        #** ---------------------------------------------------------------------------------------
        #*  segmento do circuito
        #*/
        l_iSeg1 = self._oAtv.getCktSeg ()
        #l_log.info ( "l_iSeg1: " + str ( l_iSeg1 ))

        #** ---------------------------------------------------------------------------------------
        #*  proximo segmento
        #*/
        l_iSeg2 = ( l_iSeg1 + 1 ) % locDefs.xMAX_Segmentos
        #l_log.info ( "l_iSeg2: " + str ( l_iSeg2 ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o raio de curvatura da aeronave
        #*/
        l_dRaio = self._oAtv.getRaioCurva ()
        #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a posição atual da aeronave
        #*/
        l_tAnv = self._oAtv._tPosicao
        assert ( l_tAnv )

        #** ---------------------------------------------------------------------------------------
        #*  circuito padrao da aeronave (tabela performance)
        #*/
        l_iCkt = self._oAtv.getCircuito ()
        #l_log.info ( "l_iCkt: " + str ( l_iCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito
        #*/
        l_oCkt = l_oPst.getPstCkt ( l_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o segmento seguinte
        #*/
        l_oSeg2 = l_oCkt.getCktSeg ( l_iSeg2 )
        assert ( l_oSeg2 )
        assert ( isinstance ( l_oSeg2, clsPst.clsSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém a reta que define o segmento
        #*/
        l_tPerna = l_oSeg2._tSegReta
        assert ( l_tPerna )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a reta final
        #*/
        l_tFinal = l_oCab._tFinalReta
        assert ( l_tFinal )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a distância entre eles
        #*/
        l_dDAP = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tPerna )
        l_dDAF = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tFinal )

        #** ---------------------------------------------------------------------------------------
        #*  está na perna base e consegue fazer a curva ( l_dDAF > l_dRaio ) ?
        #*/
        if (( l_iSeg1 == l_iBase ) and ( l_dDAF > l_dRaio )):

            #** -----------------------------------------------------------------------------------
            #*  velocidade de pouso
            #*/
            self._oAtv._dVelDem = self._oAtv.getVelocidadeArr () * glbDefs.xCNV_Knots2Ms

            #** -----------------------------------------------------------------------------------
            #*  aproa a final
            #*/
            self.aproaFinal ( l_iPst, l_iCab )

        #** ---------------------------------------------------------------------------------------
        #*  senão, não está na perna base ou não consegue fazer a curva
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  enquanto consegue fazer a curva...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'P' == self._oAtv.getStatusVoo ()) and
                   ( l_dDAP > l_dRaio )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém a posição atual da aeronave
                #*/
                l_tAnv = self._oAtv._tPosicao
                assert ( l_tAnv )

                #** -------------------------------------------------------------------------------
                #*  calcula a distância ate a perna
                #*/
                l_dDAP = cineCalc.distanciaPontoRetaABS ( l_tAnv, l_tPerna )

                #** -------------------------------------------------------------------------------
                #*  obtém o raio de curvatura da aeronave
                #*/
                l_dRaio = self._oAtv.getRaioCurva ()
                #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  keep going ?
            #*/
            if (( glbData.g_bKeepRun ) and
                ( self._oAtv._bActive ) and
                ( 'P' == self._oAtv.getStatusVoo ())):

                #** -------------------------------------------------------------------------------
                #*  proximo segmento
                #*/
                l_iSeg = l_iSeg2

                #** -------------------------------------------------------------------------------
                #*  enquanto não estiver na perna base...
                #*/
                while (( glbData.g_bKeepRun ) and
                       ( self._oAtv._bActive ) and
                       ( 'P' == self._oAtv.getStatusVoo ()) and
                       ( l_iSeg != l_iBase )):

                    #** ---------------------------------------------------------------------------
                    #*  obtém o segmento seguinte
                    #*/
                    l_oSeg = l_oCkt.getCktSeg ( l_iSeg )
                    assert ( l_oSeg )
                    assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

                    #** ---------------------------------------------------------------------------
                    #*  obtém a proa do segmento
                    #*/
                    l_dProa = l_oSeg._dSegProa

                    #** ---------------------------------------------------------------------------
                    #*  curva pela esquerda
                    #*/
                    self._oAtv._cSentidoCurva = 'E'

                    #** ---------------------------------------------------------------------------
                    #*  altera a proa
                    #*/
                    self._oAtv._dProaDem = l_dProa

                    #** ---------------------------------------------------------------------------
                    #*  obtém a posição atual da aeronave
                    #*/
                    l_tAnv = self._oAtv._tPosicao
                    assert ( l_tAnv )

                    #** ---------------------------------------------------------------------------
                    #*  obtém a posição final do segmento
                    #*/
                    l_tFim = l_oSeg._tSegFim
                    assert ( l_tFim )

                    #** ---------------------------------------------------------------------------
                    #*  calcula a distância entre eles
                    #*/
                    l_dDist = cineCalc.distanciaEntrePontos ( l_tFim, l_tAnv )

                    #** ---------------------------------------------------------------------------
                    #*  enquanto consegue fazer a curva...
                    #*/
                    while (( glbData.g_bKeepRun ) and
                           ( self._oAtv._bActive ) and
                           ( 'P' == self._oAtv.getStatusVoo ()) and
                           ( l_dDist > l_dRaio )):

                        #** -----------------------------------------------------------------------
                        #*  obtém o tempo inicial em segundos
                        #*/
                        l_lNow = time.time ()
                        #l_log.info ( "l_lNow: " + str ( l_lNow ))

                        #** -----------------------------------------------------------------------
                        #*  vôo normal
                        #*/
                        self.procVooNormal ()

                        #** -----------------------------------------------------------------------
                        #*  obtém a posição atual da aeronave
                        #*/
                        l_tAnv = self._oAtv._tPosicao
                        assert ( l_tAnv )

                        #** -----------------------------------------------------------------------
                        #*  calcula a distância entre eles
                        #*/
                        l_dDist = cineCalc.distanciaEntrePontos ( l_tFim, l_tAnv )

                        #** -----------------------------------------------------------------------
                        #*  obtém o raio de curvatura da aeronave
                        #*/
                        l_dRaio = self._oAtv.getRaioCurva ()
                        #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

                        #** -----------------------------------------------------------------------
                        #*  obtém o tempo final em segundos e calcula o tempo decorrido
                        #*/
                        l_lDif = time.time () - l_lNow
                        #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                        #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                        #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                        #** -----------------------------------------------------------------------
                        #*  está adiantado ?
                        #*/
                        if ( glbDefs.xTIM_Wait > l_lDif ):
                                                            
                            #** -------------------------------------------------------------------
                            #*  permite o scheduler (1/10th)
                            #*/
                            time.sleep ( glbDefs.xTIM_Wait - l_lDif )

                    #** ---------------------------------------------------------------------------
                    #*  keep going ?
                    #*/
                    if (( glbData.g_bKeepRun ) and
                        ( self._oAtv._bActive ) and
                        ( 'P' == self._oAtv.getStatusVoo ())):

                        #** -----------------------------------------------------------------------
                        #*  proximo segmento
                        #*/
                        l_iSeg = ( l_iSeg + 1 ) % locDefs.xMAX_Segmentos

                #** -------------------------------------------------------------------------------
                #*  está na perna base ?
                #*/
                if ( l_iSeg == l_iBase ):

                    #** ---------------------------------------------------------------------------
                    #*  obtém a perna base
                    #*/
                    l_oSeg = l_oCkt.getCktSeg ( l_iBase )
                    assert ( l_oSeg )
                    assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

                    #** ---------------------------------------------------------------------------
                    #*  obtém a proa do segmento
                    #*/
                    l_dProa = l_oSeg._dSegProa

                    #** ---------------------------------------------------------------------------
                    #*  altera a navegação
                    #*/
                    self._oAtv._cSentidoCurva = 'E'

                    #** ---------------------------------------------------------------------------
                    #*  altera a demanda
                    #*/
                    self._oAtv._dProaDem = l_dProa

                    #** ---------------------------------------------------------------------------
                    #*  velocidade de pouso
                    #*/
                    self._oAtv._dVelDem = self._oAtv.getVelocidadeArr () * glbDefs.xCNV_Knots2Ms

                    #** ---------------------------------------------------------------------------
                    #*  enquanto faz a curva...
                    #*/
                    while (( glbData.g_bKeepRun ) and
                           ( self._oAtv._bActive ) and
                           ( 'P' == self._oAtv.getStatusVoo ()) and
                           ( self._oAtv._dProa != self._oAtv._dProaDem )):

                        #** -----------------------------------------------------------------------
                        #*  obtém o tempo inicial em segundos
                        #*/
                        l_lNow = time.time ()
                        #l_log.info ( "l_lNow: " + str ( l_lNow ))

                        #** -----------------------------------------------------------------------
                        #*  vôo normal
                        #*/
                        self.procVooNormal ()

                        #** -----------------------------------------------------------------------
                        #*  obtém o tempo final em segundos e calcula o tempo decorrido
                        #*/
                        l_lDif = time.time () - l_lNow
                        #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                        #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                        #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                        #** -----------------------------------------------------------------------
                        #*  está adiantado ?
                        #*/
                        if ( glbDefs.xTIM_Wait > l_lDif ):
                                                            
                            #** -------------------------------------------------------------------
                            #*  permite o scheduler (1/10th)
                            #*/
                            time.sleep ( glbDefs.xTIM_Wait - l_lDif )

                    #** ---------------------------------------------------------------------------
                    #*  aproa a final
                    #*/
                    self.aproaFinal ( l_iPst, l_iCab )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::execTocarArremeter
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def execTocarArremeter ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::execTocarArremeter"


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
        #*  enquanto não alcanca a altitude correta...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'T' == self._oAtv.getStatusVoo ()) and
               ( self._oAtv._dAltitude != self._oAtv._dAltDem )):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial em segundos
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  vôo normal
            #*/
            self.procVooNormal ()

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final em segundos e calcula o tempo decorrido
            #*/
            l_lDif = time.time () - l_lNow
            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  está adiantado ?
            #*/
            if ( glbDefs.xTIM_Wait > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  keep going ?
        #*/
        if (( glbData.g_bKeepRun ) and
            ( self._oAtv._bActive ) and
            ( 'T' == self._oAtv.getStatusVoo ())):

            #** -----------------------------------------------------------------------------------
            #*  reduz a velocidade em 5%
            #*/
            self._oAtv._dVelDem = 0.95 * self._oAtv._dVeloc

            #** -----------------------------------------------------------------------------------
            #*  enquanto não alcanca a velocidade correta...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'T' == self._oAtv.getStatusVoo ()) and
                   ( self._oAtv._dVeloc != self._oAtv._dVelDem )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

            #** -----------------------------------------------------------------------------------
            #*  keep going ?
            #*/
            if (( glbData.g_bKeepRun ) and
                ( self._oAtv._bActive ) and
                ( 'T' == self._oAtv.getStatusVoo ())):

                #** -------------------------------------------------------------------------------
                #*  aeronave no solo
                #*/
                self._oAtv._bSolo = True

                #** -------------------------------------------------------------------------------
                #*  muda status para acidente no pouso
                #*/
                self._oAtv.setStatusSolo ( 'D' )

                #** -------------------------------------------------------------------------------
                #*  obtém a cinematica de solo da aeronave
                #*/
                l_cs = self._fe.getCineSolo ()
                assert ( l_cs )

                #** -------------------------------------------------------------------------------
                #*  decola a aeronave
                #*/
                l_cs.execDecolar ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  PROCEDURES
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::procArremeter
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
        #l_szMetodo = "cineVoo::procArremeter"


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
        #*  X - arremeter em emergencia ?
        #*/
        if ( 'X' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  altera a demanda
            #*/
            self._oAtv._dAltDem = ( self._oAtv.getAltitudeCircuito () + self._oAer.getAltitude ()) * glbDefs.xCNV_ft2M
            self._oAtv._dVelDem = self._oAtv.getVelocidadeDep () * glbDefs.xCNV_Knots2Ms

            #** -----------------------------------------------------------------------------------
            #*  coloca em vôo normal
            #*/
            self._oAtv.setStatusVoo ( 'N' )

        #** ---------------------------------------------------------------------------------------
        #*  Y - toque e arremetida ?
        #*/
        elif ( 'Y' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  muda status para toque e arremetida (T)
            #*/
            self._oAtv.setStatusVoo ( 'T' )

            #** -----------------------------------------------------------------------------------
            #*  executa o procedimento de toque e arremetida
            #*/
            self.execTocarArremeter ()

        #** ---------------------------------------------------------------------------------------
        #*  Z - arremeter para a perna do vento
        #*/
        elif ( 'Z' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  pegar a perna do vento
            #*/
            self._oAtv.setStatusVoo ( 'V' )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::procCircuito
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def procCircuito ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::procCircuito"


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
        #*  altitude de circuito
        #*/
        self._oAtv._dAltDem = ( self._oAtv.getAltitudeCircuito () + self._oAer.getAltitude ()) * glbDefs.xCNV_ft2M
        #l_log.info ( "_dAltDem: " + str ( self._oAtv._dAltDem ))

        #** ---------------------------------------------------------------------------------------
        #*  velocidade de circuito
        #*/
        self._oAtv._dVelDem = self._oAtv.getVelocidadeCircuito () * glbDefs.xCNV_Knots2Ms
        #l_log.info ( "_dVelDem: " + str ( self._oAtv._dVelDem ))

        #** ---------------------------------------------------------------------------------------
        #*  circuito pela perna do vento ?
        #*/
        if ( 'V' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  executa o procedimento de entrada no circuito pela perna do vento
            #*/
            self.execCktPernaVento ()

        #** ---------------------------------------------------------------------------------------
        #*  circuito pela perna do contra vento ?
        #*/
        elif ( 'K' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  executa o procedimento de entrada no circuito pela perna do contra-vento
            #*/
            self.execCktPernaContraVento ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::procPeelOff
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def procPeelOff ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::procPeelOff"


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
        #*  curva a esquerda
        #*/
        self._oAtv._cSentidoCurva = 'E'

        #** ---------------------------------------------------------------------------------------
        #*/
        l_dProa = self._oAtv._dProa - 45.

        if ( l_dProa < 0. ):

            #** -----------------------------------------------------------------------------------
            #*/
            l_dProa += 360.

        #** ---------------------------------------------------------------------------------------
        #*  se quizer aproar a pista sem a necessidade de estár a 45 graus com a sua direção, sera
        #*  necessario saber qual a pista e qual a cabeceira se quer fazer o PeelOff, e usar o
        #*  comando abaixo. Nestá primeira versao deve-se exigir que a aeronave entre a 45 graus
        #*  com a direção da pista.
        #*  l_dProa = _oPst [ x ]._oCab [ 0 ]._dCabDir
        #*/

        #** ---------------------------------------------------------------------------------------
        #*  altera demanada
        #*/
        self._oAtv._dProaDem = l_dProa

        #** ---------------------------------------------------------------------------------------
        #*  altitude de esquadrilha
        #*/
        self._oAtv._dAltDem = ( self._oAer.getAltitude () + 1200. + ( self._oAtv._btNumero * 300. )) * glbDefs.xCNV_ft2M

        #** ---------------------------------------------------------------------------------------
        #*  velocidade da esquadrilha
        #*/
        self._oAtv._dVelDem = 300. * glbDefs.xCNV_Knots2Ms

        #** ---------------------------------------------------------------------------------------
        #*  coloca em vôo normal
        #*/
        self._oAtv.setStatusVoo ( 'N' )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::procPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def procPouso ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::procPouso"


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
        #*  pouso direto ?
        #*/
        if ( 'D' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  faz o pouso direto
            #*/
            self.execPousoDireto ()

        #** ---------------------------------------------------------------------------------------
        #*  pouso pelo circuito ?
        #*/
        elif ( 'P' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  faz o pouso pelo circuito
            #*/
            self.execPousoPeloCircuito ()

        #** ---------------------------------------------------------------------------------------
        #*  pouso acidentado ?
        #*/
        elif ( 'A' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  faz o pouso fora da pista
            #*/
            self.execPousoForaDaPista ()

        #** ---------------------------------------------------------------------------------------
        #*  pouso normal ?
        #*/
        if ( 'P' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  executa o procedimento de pouso normal
            #*/
            self.execPousar ()

        #** ---------------------------------------------------------------------------------------
        #*  frear ate parar ?
        #*/
        if ( 'F' == self._oAtv.getStatusVoo ()):

            #** -----------------------------------------------------------------------------------
            #*  executa o procedimento de frear a aeronave ate parar
            #*/
            self.execFrearAteParar ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::procVooNormal
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def procVooNormal ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::procVooNormal"


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
            return ( False )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a hora atual em segundos
        #*/
        l_lTempoAtu = self._st.obtemHoraSim ()
        #l_log.info ( "l_lTempoAtu: %d" % ( l_lTempoAtu ))

        #** ---------------------------------------------------------------------------------------
        #*  calcula a variação de tempo desde a ultima atualização
        #*/
        l_lDeltaT = l_lTempoAtu - self._oAtv._lTempoAnt
        #l_log.info ( "l_lDeltaT: " + str ( l_lDeltaT ))

        #** ---------------------------------------------------------------------------------------
        #*  checa se passou algum tempo (1/10th)
        #*/
        if ( l_lDeltaT < .1 ):

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*  cai fora...
            #*/
            return ( False )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a nova proa
        #*/
        l_bProa = self.atualizaProa ( l_lDeltaT )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a nova velocidade e a velocidade media do percurso
        #*/
        l_dVelMed, l_bVel = self.atualizaVelocidade ( l_lDeltaT )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a nova altitude e a variação de altitude
        #*/
        l_dAlfa, l_bAlt = self.atualizaAltitude ( l_lDeltaT, l_dVelMed )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a direção atual
        #*/
        l_dDirAtu = self._oAtv._dDirAtu
        #l_log.info ( "Direção atual: " + str ( l_dDirAtu ))

        #** ---------------------------------------------------------------------------------------
        #*  atualiza a posição da aeronave
        #*/
        self.atualizaPosicao ( l_lDeltaT, l_dVelMed, l_dAlfa, l_dDirAtu )

        #** ---------------------------------------------------------------------------------------
        #*  salva a hora atual
        #*/
        self._oAtv._lTempoAnt = l_lTempoAtu

        #** ---------------------------------------------------------------------------------------
        #*  envia os dados para o controle
        #*/
        self.sendData ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( True )

    #** ===========================================================================================
    #*  MOVES
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  cineVoo::moveNoCircuito
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  self - posição na tabela de ativas
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def moveNoCircuito ( self, f_iPst, f_iCkt ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "cineVoo::moveNoCircuito"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert (( f_iPst >= 0 ) and ( f_iPst < locDefs.xMAX_Pistas ))
        assert (( f_iCkt >= 0 ) and ( f_iCkt < locDefs.xMAX_Circuitos ))

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
        #*  obtém a pista do aerodromo
        #*/
        l_oPst = self._oAer.getPista ( f_iPst )
        assert ( l_oPst )
        assert ( isinstance ( l_oPst, clsPst.clsPst ))

        #** ---------------------------------------------------------------------------------------
        #*  obtém o circuito da pista
        #*/
        l_oCkt = l_oPst.getPstCkt ( f_iCkt )
        assert ( l_oCkt )
        assert ( isinstance ( l_oCkt, clsPst.clsCkt ))

        #** ---------------------------------------------------------------------------------------
        #*  segmento do circuito
        #*/
        l_iSeg = self._oAtv.getCktSeg ()
        #l_log.info ( "l_iSeg: " + str ( l_iSeg ))

        #** ---------------------------------------------------------------------------------------
        #*  enquanto estiver dentro do circuito...
        #*/
        while (( glbData.g_bKeepRun ) and
               ( self._oAtv._bActive ) and
               ( 'C' == self._oAtv.getStatusVoo ())):

            #** -----------------------------------------------------------------------------------
            #*  obtém o proximo segmento
            #*/
            l_iSeg = ( l_iSeg + 1 ) % locDefs.xMAX_Segmentos
            #l_log.info ( "l_iSeg: " + str ( l_iSeg ))

            #** -----------------------------------------------------------------------------------
            #*  salva o segmento do circuito
            #*/
            self._oAtv._tCktAtual = ( f_iPst, self._oAtv.getCktCab (), l_iSeg )
            assert ( self._oAtv._tCktAtual )

            #** -----------------------------------------------------------------------------------
            #*  obtém o segmento
            #*/
            l_oSeg = l_oCkt.getCktSeg ( l_iSeg )
            assert ( l_oSeg )
            assert ( isinstance ( l_oSeg, clsPst.clsSeg ))

            #** -----------------------------------------------------------------------------------
            #*  obtém a proa do segmento
            #*/
            l_dProa = l_oSeg._dSegProa
            #l_log.info ( "l_dProa: " + str ( l_dProa ))

            #** -----------------------------------------------------------------------------------
            #*  altera a navegação da aeronave
            #*/
            self._oAtv._cSentidoCurva = 'E'

            #** -----------------------------------------------------------------------------------
            #*  altera a demanda da aeronave
            #*/
            self._oAtv._dProaDem = l_dProa

            #** -----------------------------------------------------------------------------------
            #*  obtém o raio de curvatura da aeronave
            #*/
            l_dRaio = self._oAtv.getRaioCurva ()
            #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

            #** -----------------------------------------------------------------------------------
            #*  obtém o ponto final do segmento
            #*/
            l_tFim = l_oSeg._tSegFim
            assert ( l_tFim )

            #** -----------------------------------------------------------------------------------
            #*  obtém a posição atual da aeronave
            #*/
            l_tAnv = self._oAtv._tPosicao
            assert ( l_tAnv )

            #** -----------------------------------------------------------------------------------
            #*  calcula a distância entre eles
            #*/
            l_dDist = cineCalc.distanciaEntrePontos ( l_tAnv, l_tFim )
            #l_log.info ( "l_dDist: " + str ( l_dDist ))

            #** -----------------------------------------------------------------------------------
            #*  enquanto não atingir o ponto para iniciar a curva...
            #*/
            while (( glbData.g_bKeepRun ) and
                   ( self._oAtv._bActive ) and
                   ( 'C' == self._oAtv.getStatusVoo ()) and
                   ( l_dDist > l_dRaio )):

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo inicial em segundos
                #*/
                l_lNow = time.time ()
                #l_log.info ( "l_lNow: " + str ( l_lNow ))

                #** -------------------------------------------------------------------------------
                #*  vôo normal
                #*/
                self.procVooNormal ()

                #** -------------------------------------------------------------------------------
                #*  obtém a posição atual da aeronave
                #*/
                l_tAnv = self._oAtv._tPosicao
                assert ( l_tAnv )

                #** -------------------------------------------------------------------------------
                #*  calcula a distância entre eles
                #*/
                l_dDist = cineCalc.distanciaEntrePontos ( l_tAnv, l_tFim )
                #l_log.info ( "l_dDist: " + str ( l_dDist ))

                #** -------------------------------------------------------------------------------
                #*  obtém o raio de curvatura da aeronave
                #*/
                l_dRaio = self._oAtv.getRaioCurva ()
                #l_log.info ( "l_dRaio: " + str ( l_dRaio ))

                #** -------------------------------------------------------------------------------
                #*  obtém o tempo final em segundos e calcula o tempo decorrido
                #*/
                l_lDif = time.time () - l_lNow
                #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
                #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_Wait ))
                #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_Wait - l_lDif ))

                #** -------------------------------------------------------------------------------
                #*  está adiantado ?
                #*/
                if ( glbDefs.xTIM_Wait > l_lDif ):
                                                    
                    #** ---------------------------------------------------------------------------
                    #*  permite o scheduler (1/10th)
                    #*/
                    time.sleep ( glbDefs.xTIM_Wait - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "cineVoo" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
