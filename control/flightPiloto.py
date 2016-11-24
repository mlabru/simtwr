#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: flightPiloto
#*
#*  Descrição: this is the actual flight control for SiCAD.
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/jun/20  version started
#*  mlabru   2008/jun/20  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versão
#*  -----------------------------------------------------------------------------------------------
#*  start    2008/jun/20  version started
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

#/ SiCAD / control
#/ ------------------------------------------------------------------------------------------------
import control.flightControl as flightControl
import control.flightEngine as flightEngine

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.cineCalc as cineCalc
import model.clsAnv as clsAnv
import model.clsAtv as clsAtv

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
#*  flightPiloto::flightPiloto
#*  -----------------------------------------------------------------------------------------------
#*  the flight control class generates new flights and handles their movement. It has a list of
#*  flight objects holding all flights that are currently active. The flights are generated when
#*  activation time comes, or quando ja foi ativado na confecção do exercício. Once a flight has
#*  been generated it is handed by the flight engine.
#*  -----------------------------------------------------------------------------------------------
#*/
class flightPiloto ( flightControl.flightControl ):

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the app and prepares everything
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_mm - model manager
    #*  @param  f_st - simulation time
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::__init__"


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
        #*  inicia a super classe
        #*/
        flightControl.flightControl.__init__ ( self, f_cm )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a tabela de performance
        #*/
        self._oPrf = self._mm.getPerformance ()
        assert ( self._oPrf )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o net sender
        #*/
        self._ns = f_cm.getNS ()
        assert ( self._ns )

        #** ---------------------------------------------------------------------------------------
        #*  initialize the list for all active flights
        #*/
        self._lstFlight = []

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::ativaAnv
    #*  -------------------------------------------------------------------------------------------
    #*  descongela as aeronaves
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def ativaAnv ( self, f_oAnv ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::ativaAnv"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_oAnv )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._ns )
        assert ( self._st )
        assert ( self._oAer )
        assert ( self._oExe )
        assert ( self._oPrf )

        #** ---------------------------------------------------------------------------------------
        #*  cria uma nova aeronave ativa
        #*/
        l_oAtv = clsAtv.clsAtv ( self._oExe, self._oAer, self._oPrf, f_oAnv )
        assert ( l_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  cria o flightEngine para a aeronave
        #*/
        l_fe = flightEngine.flightEngine ( self._oAer, l_oAtv, self._st, self._ns )
        assert ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  salva o flight engine da aeronave
        #*/
        l_oAtv.setFE ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  poem a aeronave pra voar
        #*/
        l_fe.start ()
        
        #** ---------------------------------------------------------------------------------------
        #*  marca a aeronave como processada
        #*/
        f_oAnv.setProcessed ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_fe )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::cbkElimina
    #*  -------------------------------------------------------------------------------------------
    #*  descongela as aeronaves
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkElimina ( self, f_fe ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::cbkElimina"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave esta na lista de vôos ativos ?
        #*/
        if ( f_fe in self._lstFlight ):

            #** -----------------------------------------------------------------------------------
            #*  verifica aeronave
            #*/
            assert ( isinstance ( f_fe, flightEngine.flightEngine ))

            #** -----------------------------------------------------------------------------------
            #*  trava a lista de vôos
            #*/
            glbData.g_lckFlight.acquire ()

            #** -----------------------------------------------------------------------------------
            #*  tenta remover o vôo da lista de vôos ativos
            #*/
            try:

                #** -------------------------------------------------------------------------------
                #*  estava, não está mais....
                #*/
                self._lstFlight.remove ( f_fe )

            #** -----------------------------------------------------------------------------------
            #*/
            finally:

                #** -------------------------------------------------------------------------------
                #*  libera a lista de vôos
                #*/
                glbData.g_lckFlight.release ()

        #** ---------------------------------------------------------------------------------------
        #*  get flight data
        #*/
        l_oAtv = f_fe.getAtv ()
        assert ( l_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a identificação da aeronave
        #*/
        l_szIdent = l_oAtv.getIdent ()
        assert ( l_szIdent )

        #** ---------------------------------------------------------------------------------------
        #*  desativa a aeronave (termina a thread)
        #*/
        l_oAtv.setActive ( False )

        #** ---------------------------------------------------------------------------------------
        #*  envia o aviso de eliminação
        #*/
        self._ns.sendData ( str ( glbDefs.xMSG_Vrs ) + glbDefs.xMSG_Sep +
                            str ( glbDefs.xMSG_Kll ) + glbDefs.xMSG_Sep + l_szIdent )
        
        #** ---------------------------------------------------------------------------------------
        #*  aguarda o envio da mensagem    
        #*/
        time.sleep ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::checkProximity
    #*  -------------------------------------------------------------------------------------------
    #*  Calculates the proximity of the flights in the flight pair
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_oAnv - aeronave a verificar o tempo de ativação
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  should be run everytime new positions are calculated by the flight engine. If two
    #*          flights are within 5 miles horizontically and at the same level or at the same
    #*          position and (above 29000 ft) within 2000 ft or (under 29000 ft) within 1000 ft
    #*          vertically a danger situation has occured.
    #*  -------------------------------------------------------------------------------------------
    #*/
    def checkProximity ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::checkProximity"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  obtém o view manager
        #*/
        l_vm = self._cm.getVM ()
        assert ( l_vm )

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de vôos ativos...
        #*/
        for l_fe1 in self._lstFlight:

            #** -----------------------------------------------------------------------------------
            #*  verifica aeronave
            #*/
            assert ( isinstance ( l_fe1, flightEngine.flightEngine ))

            #** -----------------------------------------------------------------------------------
            #*  get flight data
            #*/
            l_oAtv1 = l_fe1.getAtv ()
            assert ( l_oAtv1 )

            #** -----------------------------------------------------------------------------------
            #*  obtém a posição do vôo
            #*/
            l_tPos1 = l_oAtv1.getPosicao ()
            assert ( l_tPos1 )

            #** -----------------------------------------------------------------------------------
            #*  obtém a altitude do vôo em metros
            #*/
            l_dAlt1 = l_oAtv1.getNavAlt ()
            assert ( l_tPos1 )

            #l_log.info ( "------------------------" )
            #l_log.info ( "Anv(1):[%s] em [%s]/[%f]" % ( l_oAtv1.getIdent (), str ( l_tPos1 ), l_dAlt1 ))
             
            #** -----------------------------------------------------------------------------------
            #*  reset proximity alert
            #*/
            l_oAtv1.setAlert ( False )

            #** -----------------------------------------------------------------------------------
            #*  percorre a lista de vôos ativos...
            #*/
            for l_fe2 in self._lstFlight:

                #** -------------------------------------------------------------------------------
                #*  verifica aeronave
                #*/
                assert ( isinstance ( l_fe2, flightEngine.flightEngine ))

                #** -------------------------------------------------------------------------------
                #*  get flight data
                #*/
                l_oAtv2 = l_fe2.getAtv ()
                assert ( l_oAtv2 )

                #** -------------------------------------------------------------------------------
                #*  eh o mesmo vôo ?
                #*/
                if ( l_oAtv1 == l_oAtv2 ):

                    #** ---------------------------------------------------------------------------
                    #*  vai para o próximo vôo
                    #*/
                    continue

                #** -------------------------------------------------------------------------------
                #*  obtém a posição do vôo
                #*/
                l_tPos2 = l_oAtv2.getPosicao ()
                assert ( l_tPos2 )

                #** -------------------------------------------------------------------------------
                #*  obtém a altitude do vôo em metros
                #*/
                l_dAlt2 = l_oAtv2.getNavAlt ()
                assert ( l_tPos2 )

                #l_log.info ( "Anv(2):[%s] em [%s]/[%f]" % ( l_oAtv2.getIdent (), str ( l_tPos2 ), l_dAlt2 ))

                #** -------------------------------------------------------------------------------
                #*  calcula a distância euclidiana entre eles
                #*/
                l_dHrz = cineCalc.distanciaEntrePontos ( l_tPos1, l_tPos2 )

                #** -------------------------------------------------------------------------------
                #*  calcula a separação vertical em metros entre eles
                #*/
                l_dVrt = abs ( l_dAlt1 - l_dAlt2 )

                #l_log.info ( "Distancias: H[%f] V[%f]" % ( l_dHrz, l_dVrt ))

                #** -------------------------------------------------------------------------------
                #*  as duas estão no solo ?
                #*/
                if (( l_oAtv1.getSolo ()) and ( l_oAtv2.getSolo ())):

                    #** ---------------------------------------------------------------------------
                    #*  separação menor que 20m (1s a 20 Kt) ?
                    #*/
                    if ( l_dHrz < 20. ):

                        #** -----------------------------------------------------------------------
                        #*  nova colisão ?
                        #*/
                        if ( 'X' != l_oAtv1.getStatusSolo ()):

                            #** -------------------------------------------------------------------
                            #*  emite o aviso sonoro
                            #*/
                            self._sndExplode.play ()

                            #** -------------------------------------------------------------------
                            #*  gera colisão no solo entre as aeronaves
                            #*/
                            l_vm.geraColisaoSolo ( l_oAtv1, l_oAtv2 )                        

                    #** ---------------------------------------------------------------------------
                    #*  separação menor que 150m (5s a 30 Kt) ?
                    #*/
                    elif ( l_dHrz < 150. ):

                        #** -----------------------------------------------------------------------
                        #*  emite o aviso sonoro
                        #*/
                        self._sndAlert.play ()

                        #** -----------------------------------------------------------------------
                        #*  gera alerta de colisão no solo entre as aeronaves
                        #*/
                        l_oAtv1.setAlert ( True )

                #** -------------------------------------------------------------------------------
                #*  as duas estao em vôo ?
                #*/
                elif (( not l_oAtv1.getSolo ()) and ( not l_oAtv2.getSolo ())):

                    #** ---------------------------------------------------------------------------
                    #*  separação horizontal menor que 300m (1s a 300 Kt) e separação vertical
                    #*  menor que 70m (200ft) ?
                    #*/
                    if (( l_dHrz < 300. ) and ( l_dVrt < 70. )):

                        #l_log.info ( "Distancias: H[%f] V[%f]" % ( l_dHrz, l_dVrt ))

                        #** -----------------------------------------------------------------------
                        #*  emite o aviso sonoro
                        #*/
                        self._sndExplode.play ()

                        #** -----------------------------------------------------------------------
                        #*  gera colisão no ar entre as aeronaves
                        #*/
                        l_vm.geraColisaoAr ( l_oAtv1, l_oAtv2 )                        

                    #** ---------------------------------------------------------------------------
                    #*  separação horizontal menor que 450m (3s a 300 Kt) e separação vertical
                    #*  menor que 150m (300ft)?
                    #*/
                    elif (( l_dHrz < 900. ) and ( l_dVrt < 150. )):

                        #** -----------------------------------------------------------------------
                        #*  emite o aviso sonoro
                        #*/
                        self._sndAlert.play ()

                        #** -----------------------------------------------------------------------
                        #*  gera alerta de colisão no ar entre as aeronaves
                        #*/
                        l_oAtv1.setAlert ( True )

                #** -------------------------------------------------------------------------------
                #*  uma no solo e a outra em vôo
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  separação horizontal menor que 50m (1s a 50 Kt) e separação vertical
                    #*  menor que 25m ?
                    #*/
                    if (( l_dHrz < 50. ) and ( l_dVrt < 25. )):

                        #** -----------------------------------------------------------------------
                        #*  nova colisão ?
                        #*/
                        if ( 'X' != l_oAtv1.getStatusSolo ()):

                            #** -------------------------------------------------------------------
                            #*  emite o aviso sonoro
                            #*/
                            self._sndExplode.play ()

                            #** -------------------------------------------------------------------
                            #*  gera colisão no solo e ar entre as aeronaves
                            #*/
                            l_vm.geraColisaoArSolo ( l_oAtv1, l_oAtv2 )                        

                    #** ---------------------------------------------------------------------------
                    #*  separação horizontal menor que 100m (2s a 50 Kt) e separacão vertical
                    #*  menor que 50m ?
                    #*/
                    elif (( l_dHrz < 100. ) and ( l_dVrt < 50. )):

                        #** -----------------------------------------------------------------------
                        #*  gera colisão no solo e ar entre as aeronaves
                        #*/
                        l_oAtv1.setAlert ( True )

                        #** -----------------------------------------------------------------------
                        #*  emite o aviso sonoro
                        #*/
                        self._sndAlert.play ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::chkTimeIn
    #*  -------------------------------------------------------------------------------------------
    #*  checa se ja deu o tempo de ativação a uma aeronave do exercício
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_oAnv - aeronave a verificar o tempo de ativação
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def chkTimeIn ( self, f_oAnv ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::chkTimeIn"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parâmetros de entrada
        #*/
        assert ( f_oAnv )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condições de execução
        #*/
        assert ( self._st )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a hora da simulação
        #*/
        l_btH, l_btM, l_btS, l_btCs = self._st.obtemHora ()

        #** ---------------------------------------------------------------------------------------
        #*  calcula o tempo da simulação
        #*/
        l_iSim = (( l_btH * 60 ) + l_btM )

        #** ---------------------------------------------------------------------------------------
        #*  obtém a hora de ativação da aeronave
        #*/
        l_oHora = f_oAnv.getHora ()

        #** ---------------------------------------------------------------------------------------
        #*  calcula o tempo da ativação
        #*/
        l_iAtv = (( l_oHora [ 0 ] * 60 ) + l_oHora [ 1 ] )

        #** ---------------------------------------------------------------------------------------
        #*  checa se hora e minuto batem
        #*/
        l_bOk = ( l_iSim >= l_iAtv )

        #l_log.info ( "hora sim: " + str ( l_btH ) + ":" + str ( l_btM ))
        #l_log.info ( "hora atv: " + str ( l_oHora [ 0 ] ) + ":" + str ( l_oHora [ 1 ] ))

        #l_log.info ( "Tempo de entrada ? " + str ( l_bOk ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bOk )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::deselectFlights
    #*  -------------------------------------------------------------------------------------------
    #*  deselects all flights
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def deselectFlights ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::deselectFlights"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de vôos ativos...
        #*/
        for l_fe in self._lstFlight:

            #** -----------------------------------------------------------------------------------
            #*  verifica aeronave
            #*/
            assert ( isinstance ( l_fe, flightEngine.flightEngine ))

            #** -----------------------------------------------------------------------------------
            #*  get flight data
            #*/
            l_oAtv = l_fe.getAtv ()
            assert ( l_oAtv )

            #** -----------------------------------------------------------------------------------
            #*  for each flight, deselect...
            #*/
            l_oAtv.setSelected ( False, False )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::run
    #*  -------------------------------------------------------------------------------------------
    #*  checks whether it's time to created another flight
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def run ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::run"

        #/ contador de voltas
        #/ ----------------------------------------------------------------------------------------
        l_lRound = 0


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  enquanto não inicia...
        #*/
        while ( not glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  aguarda 1 seg
            #*/
            time.sleep ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  loop de exibição do relogio
        #*/
        while ( glbData.g_bKeepRun ):

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo inicial
            #*/
            l_lNow = time.time ()
            #l_log.info ( "l_lNow: " + str ( l_lNow ))

            #** -----------------------------------------------------------------------------------
            #*  check whether there are any more flights coming
            #*/
            #if (( 0 == len ( self._lstFlight )) and
            #    ( self.flightsProcessed >= self_oExe.getQtdeAnvs ())):

                #** -------------------------------------------------------------------------------
                #*  m.poirot logger
                #*/
                #l_log.debug ( "<< " )

                #** -------------------------------------------------------------------------------
                #*/
                #break

            #** -----------------------------------------------------------------------------------
            #*  hora do check de colisão ?
            #*/
            if ( 0 == ( l_lRound % glbDefs.xTIM_Prox )):

                #** -------------------------------------------------------------------------------
                #*  ...check for proximity and call for update of display
                #*/
                self.checkProximity ()

            #** -----------------------------------------------------------------------------------
            #*  hora de enviar a configuração ?
            #*/
            if ( 0 == ( l_lRound % glbDefs.xTIM_Cnfg )):

                #** -------------------------------------------------------------------------------
                #*  envia os dados de exercício
                #*/
                self._oExe.sendExe ( self._ns )

            #** -----------------------------------------------------------------------------------
            #*  hora de enviar a hora ?
            #*/
            if ( 0 == ( l_lRound % glbDefs.xTIM_Hora )):

                #** -------------------------------------------------------------------------------
                #*  envia os dados de hora
                #*/
                self._st.sendHora ( self._ns )

            #** -----------------------------------------------------------------------------------
            #*  hora do check de ativação ?
            #*/
            if ( 0 == ( l_lRound % glbDefs.xTIM_FGen )):

                #** -------------------------------------------------------------------------------
                #*  see if any new flights should be generated this iteration
                #*/
                self.runCheck ()

            #** -----------------------------------------------------------------------------------
            #*  incrementa o contador de voltas
            #*/
            l_lRound += 1

            #** -----------------------------------------------------------------------------------
            #*  obtém o tempo final
            #*/
            l_lDif = time.time () - l_lNow

            #l_log.info ( "l_lDif....(F): " + str ( l_lDif ))        
            #l_log.info ( "xTIM_Wait.(F): " + str ( glbDefs.xTIM_RRbn ))
            #l_log.info ( "Wait/Sleep(F): " + str ( glbDefs.xTIM_RRbn - l_lDif ))

            #** -----------------------------------------------------------------------------------
            #*  esta atrasado ?
            #*/
            if ( glbDefs.xTIM_RRbn > l_lDif ):
                                                
                #** -------------------------------------------------------------------------------
                #*  permite o scheduler (1/10th)
                #*/
                time.sleep ( glbDefs.xTIM_RRbn - l_lDif )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  flightPiloto::runCheck
    #*  -------------------------------------------------------------------------------------------
    #*  checks whether it's time to created another flight
    #*  -------------------------------------------------------------------------------------------
    #*  @param  f_lstFlight - lista de vôos ativos atual
    #*
    #*  @return l_lstAtv - lista de vôos ativados
    #*  -------------------------------------------------------------------------------------------
    #*/
    def runCheck ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "flightPiloto::runCheck"


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
        assert ( self._oPrf )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a lista de retorno
        #*/
        l_lstAtv = []

        #** ---------------------------------------------------------------------------------------
        #*  percorre as aeronaves do exercício
        #*/
        for l_oAnv in self._oExe.getAeronaves ():

            #** -----------------------------------------------------------------------------------
            #*  verifica aeronave
            #*/
            assert ( isinstance ( l_oAnv, clsAnv.clsAnv ))

            #** -----------------------------------------------------------------------------------
            #*  checa se deu o tempo para a ativação
            #*/
            l_bOk = self.chkTimeIn ( l_oAnv )

            #** -----------------------------------------------------------------------------------
            #*  se está no tempo e tem espaço...
            #*/
            if ( l_bOk and ( len ( self._lstFlight ) < locDefs.xMAX_Ativas )):

                #** -------------------------------------------------------------------------------
                #*  cria uma nova aeronave ativa
                #*/
                l_fe = self.ativaAnv ( l_oAnv )
                assert ( l_fe )

                #** -------------------------------------------------------------------------------
                #*  coloca na lista de aeronaves ativas
                #*/
                l_lstAtv.append ( l_fe )

            #** -----------------------------------------------------------------------------------
            #*  se esta no tempo mas não tem espaço...
            #*/
            elif ( l_bOk ):

                #** -------------------------------------------------------------------------------
                #*  atrasa a hora de ativação em um minuto
                #*/
                l_oAnv.atrasaAtivacao ()

        #l_log.info ( "lista de ativação: " + str ( l_lstAtv ))

        #** ---------------------------------------------------------------------------------------
        #*  gerou alguma aeronave ?
        #*/
        if ( [] != l_lstAtv ):

            #** ---------------------------------------------------------------------------
            #*  insere os vôos na lista de ativos
            #*/
            self._lstFlight.extend ( l_lstAtv )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "flightPiloto" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
