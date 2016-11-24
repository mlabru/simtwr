#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: guiMenu
#*
#*  Descrição: this class takes care of all interaction with the user
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
import random

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
import model.clsAnv as clsAnv
import model.clsAtv as clsAtv
import model.clsTrj as clsTrj

import model.glbDefs as glbDefs
import model.locDefs as locDefs

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.dialog.Tk.dlgPercurso as dlgPercurso
import view.dialog.Tk.dlgSelect as dlgSelect
import view.dialog.Tk.tkDialogs as tkDialogs
import view.viewUtils as viewUtils

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG


( xN_Esq, xN_Dir, xN_Vel, xN_Niv,
  xN_PVt, xN_PCV, xN_Emg, xN_Tok,
  xN_KlS, xN_KlV, xN_Ext, xN_Arr,
  xN_Aut, xN_Man, xN_Dep, xN_Frz,  
  xN_Can, xN_ZZZ ) = xrange ( 18 )

#** -----------------------------------------------------------------------------------------------
#*  guiMenu::guiMenu
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class guiMenu:

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the scope area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_cm, f_bg, f_guiApp, f_tNW, f_tWH ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_bg )
        assert ( f_cm )

        assert ( f_guiApp )

        assert ( f_tNW )
        assert ( f_tWH )

        #** ---------------------------------------------------------------------------------------
        #*  salva o control manager
        #*/
        self._cm = f_cm

        #** ---------------------------------------------------------------------------------------
        #*  obtem o flight control
        #*/
        self._fc = f_cm.getFC ()
        assert ( self._fc )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o model manager
        #*/
        self._mm = f_cm.getMM ()
        assert ( self._mm )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o aerodromo
        #*/
        self._oAer = self._mm.getAerodromo ()
        assert ( self._oAer )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o exercicio
        #*/
        self._oExe = self._mm.getExercicio ()
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  cria a fonte
        #*/
        self._font = pygame.font.Font ( glbDefs.xFNT_MENU, 12 )
        assert ( self._font )

        #** ---------------------------------------------------------------------------------------
        #*  salva a interface grafica
        #*/
        self._guiApp = f_guiApp

        #** ---------------------------------------------------------------------------------------
        #*  posição da area de menus
        #*/
        self._tNW = f_tNW

        #** ---------------------------------------------------------------------------------------
        #*  largura e altura da caixa
        #*/
        self._tWH = f_tWH

        #** ---------------------------------------------------------------------------------------
        #*  altura do header
        #*/
        self._iHeaderHeight = locDefs.xSCR_HDR_Height

        #** ---------------------------------------------------------------------------------------
        #*  posição da area de menus
        #*/
        self._tNW = f_tNW

        #** ---------------------------------------------------------------------------------------
        #*  cria a area de menus
        #*/
        l_srfMenu = pygame.Surface ( self._tWH )
        assert ( l_srfMenu )
         
        l_srfMenu.set_colorkey ( l_srfMenu.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        self.makeHeader ( l_srfMenu )

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        f_bg.blit ( l_srfMenu, self._tNW )

        #** ---------------------------------------------------------------------------------------
        #*  ajusta a posição da area de menus
        #*/
        self._tMenuPos = ( f_tNW [ 0 ], f_tNW [ 1 ] + self._iHeaderHeight )
        assert ( self._tMenuPos )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave ativa
        #*/
        self._oAtv = None

        #** ---------------------------------------------------------------------------------------
        #*/
        self._msgBox = None

        #** ---------------------------------------------------------------------------------------
        #*  cria os botoes
        #*/
        self._btn = [ None for x in xrange ( xN_ZZZ ) ]

        #** ---------------------------------------------------------------------------------------
        #*/
        self._vbxMenu = None

        #** ---------------------------------------------------------------------------------------
        #*  cria o menu dummy
        #*/
        self._vbxDummy = self.makeMenuDummy ()
        assert ( self._vbxDummy )

        #** ---------------------------------------------------------------------------------------
        #*  cria o menu solo
        #*/
        self._vbxSolo = self.makeMenuSolo ()
        assert ( self._vbxSolo )

        #** ---------------------------------------------------------------------------------------
        #*  cria o menu voo
        #*/
        self._vbxVoo = self.makeMenuVoo ()
        assert ( self._vbxVoo )

        #** ---------------------------------------------------------------------------------------
        #*  cria o menu inicial
        #*/
        self.makeMenu ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkApxEmergencia
    #*  -------------------------------------------------------------------------------------------
    #*  arremeter em emergencia
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkApxEmergencia ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkApxEmergencia"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave na final ou flag acidente de pouso ?
        #*/
        if ( self._oAtv.getStatusVoo () in [ 'A', 'F' ] ):

            #** -----------------------------------------------------------------------------------
            #*  arremeter em emergencia
            #*/
            self._oAtv.setStatusVoo ( 'X' )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave nao esta na final
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave nao esta na final
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "nao esta na final", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkApxPVento
    #*  -------------------------------------------------------------------------------------------
    #*  arremeter para a perna do vento
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkApxPVento ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkApxPVento"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave na final ou flag acidente de pouso ?
        #*/
        if ( self._oAtv.getStatusVoo () in [ 'A', 'F' ] ):

            #** -----------------------------------------------------------------------------------
            #*  arremeter para a perna do vento
            #*/
            self._oAtv.setStatusVoo ( 'Z' )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave nao esta na final
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave nao esta na final
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "nao esta na final", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkApxPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkApxPouso ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkApxPouso"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave no circuito ou em voo normal ?
        #*/
        if ( self._oAtv.getStatusVoo () in [ 'C', 'N' ] ):

            #** -----------------------------------------------------------------------------------
            #*  aeronave em voo normal ?
            #*/
            if ( 'N' == self._oAtv.getStatusVoo ()):

                #** -------------------------------------------------------------------------------
                #*  obtem a cabeceira para o pouso
                #*/
                l_bOk, l_iPst, l_iCab = self.obtemCabeceira ()

                #** -------------------------------------------------------------------------------
                #*  cabeceira Ok ?
                #*/
                if ( l_bOk ):

                    #** ---------------------------------------------------------------------------
                    #*/
                    assert (( l_iPst >= 0 ) and ( l_iPst < locDefs.xMAX_Pistas )) 
                    assert (( l_iCab >= 0 ) and ( l_iCab < locDefs.xMAX_Cabeceiras )) 

                    #** ---------------------------------------------------------------------------
                    #*  salva cabeceira e pista para o pouso
                    #*/
                    self._oAtv.setCktAtual (( l_iPst, l_iCab, 0 ))

                    #** ---------------------------------------------------------------------------
                    #*  ativa pouso direto ?
                    #*/
                    if ( self.checkPousoDireto ()):

                        #** -----------------------------------------------------------------------
                        #*  destino do pouso valido ?
                        #*/
                        if ( self.obtemDestinoPouso ()):

                            #** -------------------------------------------------------------------
                            #*  ha necessidade de se verificar novamente a rampa e a velocidade,
                            #*  pois durante a determinação do ponto de parada apos o pouso,
                            #*  pode ser que a aeronave mude de setor ou passe para uma posição
                            #*  em que nao eh mais possivel um pouso direto
                            #*/
                            if ( self.checkPousoDireto ()):
                            
                                #** ---------------------------------------------------------------
                                #*  muda o status para pouso direto
                                #*/
                                self._oAtv.setStatusVoo ( 'D' ) 

            #** -----------------------------------------------------------------------------------
            #*  senao, aeronave no circuito
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  destino do pouso valido ?
                #*/
                if ( self.obtemDestinoPouso ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status do voo
                    #*/
                    self._oAtv.setStatusVoo ( 'P' )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave em pouso
        #*/
        elif ( self._oAtv.getStatusVoo () in [ 'D', 'P' ] ):

            #** -----------------------------------------------------------------------------------
            #*  erro, aviao em procedimento de pouso
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "em procedimento de pouso", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave em outro modo
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, momento inadequado ao pedido
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "situação inadequada ao pedido", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )
 
    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkApxToque
    #*  -------------------------------------------------------------------------------------------
    #*  toque e arremetida
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkApxToque ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkApxToque"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave na final ou flag acidente de pouso ?
        #*/
        if ( self._oAtv.getStatusVoo () in [ 'A', 'F' ] ):

            #** -----------------------------------------------------------------------------------
            #*  toque e arremetida 
            #*/
            self._oAtv.setStatusVoo ( 'Y' )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave nao esta na final
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave nao esta na final
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "nao esta na final", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkCktCircuito
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkCktCircuito ( self, f_cPerna ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkCktCircuito"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_cPerna in [ 'K', 'V' ] )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a pista/cabeceira do circuito
        #*/
        l_bOk, l_iPst, l_iCab = self.obtemCabeceira ()

        #** ---------------------------------------------------------------------------------------
        #*  pista/cabeceira ok ?
        #*/
        if ( l_bOk ):

            #** -----------------------------------------------------------------------------------
            #*  aeronave ja esta em circuito ?
            #*/
            if ( self._oAtv.getStatusVoo () in locDefs.xSET_StatusCircuitos ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave ja esta em circuito
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "ja esta em circuito", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave nao esta em circuito
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  muda o status do voo
                #*/
                self._oAtv.setStatusVoo ( f_cPerna )

                #** -------------------------------------------------------------------------------
                #*/
                assert (( l_iPst >= 0 ) and ( l_iPst < locDefs.xMAX_Pistas )) 
                assert (( l_iCab >= 0 ) and ( l_iCab < locDefs.xMAX_Cabeceiras )) 

                #** -------------------------------------------------------------------------------
                #*  configura o circuito de trafego a realizar
                #*/
                self._oAtv.setCktAtual (( l_iPst, l_iCab, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkCktExit
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkCktExit ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkCktExit"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o status do voo
        #*/
        l_cStat = self._oAtv.getStatusVoo ()
        
        #** ---------------------------------------------------------------------------------------
        #*  checa se o voo esta em circuito
        #*/
        if (( l_cStat in locDefs.xSET_StatusCircuitos ) or ( 'P' == l_cStat )):

            #** -----------------------------------------------------------------------------------
            #*  volta ao voo normal
            #*/
            self._oAtv.setNavProaDem ( self._oAtv.getNavProa ())
            self._oAtv.setNavAltDem ( self._oAtv.getNavAlt ())
            self._oAtv.setNavVelDem ( self._oAtv.getNavVel ())

            #** -----------------------------------------------------------------------------------
            #*  muda o status do voo
            #*/
            self._oAtv.setStatusVoo ( 'N' )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave nao esta no circuito
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave nao esta no circuito
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "nao esta em circuito", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkDoNothing
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkDoNothing ( self ): pass

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkExeAtiva
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkExeAtiva ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkExeAtiva"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._fc )
        assert ( self._oExe )

        #** ---------------------------------------------------------------------------------------
        #*  verifica se ja estao ativas todas as aeronaves do exercicio
        #*/
        if ( len ( self._fc.getListFlight ()) >= len ( self._oExe.getAeronaves ())):

            #** -----------------------------------------------------------------------------------
            #*  avisa que nao existem aeronaves a ativar
            #*/
            self._msgBox.addMsg ( "SiCAD", "nenhuma aeronave a ativar", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  recria o menu principal
            #*/
            self.makeMenu ()

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*/
            return

        #** ---------------------------------------------------------------------------------------
        #*  lista de retorno
        #*/
        l_lstIdent = []

        #** ---------------------------------------------------------------------------------------
        #*  percorre as aeronaves do exercicio
        #*/
        for l_oAnv in self._oExe.getAeronaves ():

            #** -----------------------------------------------------------------------------------
            #*  verifica aeronave
            #*/
            assert ( isinstance ( l_oAnv, clsAnv.clsAnv ))

            #** -----------------------------------------------------------------------------------
            #*  coloca o call sign da aeronave na lista de identificadores
            #*/
            l_lstIdent.append ( l_oAnv.getIdent ())

        #** ---------------------------------------------------------------------------------------
        #*  lista de aeronaves do exercicio
        #*/
        #l_log.info ( "lista de aeronaves do exercicio(1): " + str ( l_lstIdent ))        

        #** ---------------------------------------------------------------------------------------
        #*  percorre as aeronaves ativas e as retira da lista
        #*/
        for l_fe in self._fc.getListFlight ():

            #** -----------------------------------------------------------------------------------
            #*  verifica aeronave
            #*/
            l_oAtv = l_fe.getAtv ()
            assert ( l_oAtv )
            assert ( isinstance ( l_oAtv, clsAtv.clsAtv ))

            #** -----------------------------------------------------------------------------------
            #*  retira da lista
            #*/
            l_lstIdent.remove ( l_oAtv.getIdent ())

        #** ---------------------------------------------------------------------------------------
        #*  ordena a lista de aeronaves do exercicio
        #*/
        l_lstIdent.sort ()

        #** ---------------------------------------------------------------------------------------
        #*  lista de aeronaves do exercicio
        #*/
        #l_log.info ( "lista de aeronaves do exercicio(2): " + str ( l_lstIdent ))        

        #** ---------------------------------------------------------------------------------------
        #*  cria o dialogo "seleciona aeronave a ativar" e seleciona uma aeronave
        #*/
        l_bOk, l_iI = dlgSelect.askList ( locDefs.xTXT_Tit, "Aeronave:", l_lstIdent )
        #l_log.info ( "Opção: " + str ( l_iI ))

        #** ---------------------------------------------------------------------------------------
        #*  Ok ?
        #*/
        if ( l_bOk ):

            #** -----------------------------------------------------------------------------------
            #*  obtem a aeronave selecionada
            #*/
            l_szId = l_lstIdent [ l_iI ]
            #l_log.info ( "Selecionada (%d): [%s]" % ( l_iI, l_szId ))

            #** -----------------------------------------------------------------------------------
            #*  percorre as aeronaves do exercicio
            #*/
            for l_oAnv in self._oExe.getAeronaves ():

                #** -------------------------------------------------------------------------------
                #*  verifica aeronave
                #*/
                assert ( isinstance ( l_oAnv, clsAnv.clsAnv ))

                #** -------------------------------------------------------------------------------
                #*  eh a aeronave a ativar ?
                #*/
                if ( l_szId == l_oAnv.getIdent ()):

                    #** ---------------------------------------------------------------------------
                    #*  modifica a hora de ativação
                    #*/
                    l_oAnv.setHora (( 0, 0 ))

                    #** ---------------------------------------------------------------------------
                    #*  verifica tempo de ativação
                    #*/
                    self._fc.runCheck ()

                    #** ---------------------------------------------------------------------------
                    #*  cai fora
                    #*/
                    break

        #** ---------------------------------------------------------------------------------------
        #*  recria o menu principal
        #*/
        #self.makeMenu ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkExeElimina
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkExeElimina ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkExeElimina"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._fc )
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o flight engine da aeronave
        #*/
        l_fe = self._oAtv.getFE ()
        assert ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  deseleciona o voo
        #*/
        self.deselectFlight ()
        
        #** ---------------------------------------------------------------------------------------
        #*  retira a aeronave da lista de aeronaves ativas
        #*/
        self._fc.cbkElimina ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  recria o menu principal
        #*/
        #self.makeMenu ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkExeEscala
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkExeEscala ( self, f_iEsc ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkExeEscala"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_iEsc in locDefs.xSET_EscalasValidas )
        
        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oExe )
        
        #** ---------------------------------------------------------------------------------------
        #*  verifica se mudou a escala
        #*/
        if ( self._oExe.getEscala () != f_iEsc ):

            #** -----------------------------------------------------------------------------------
            #*  configura a nova escala
            #*/
            self._oExe.setEscala ( f_iEsc )

            #** -----------------------------------------------------------------------------------
            #*  avisa que houve mudanca de escala
            #*/
            self._oExe.setMudouEscala ( True )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkExePeelOff
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkExePeelOff ( self ): pass

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkExePeelOff"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  peel-off
        #*/
        #for l_iAnv in xrange ( self._oExe.getQtdeAnvPeelOff ()):

            #** -----------------------------------------------------------------------------------
            #*  peel-off
            #*/
            #self._oAtv.setStatusVoo ( 'O' )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkNavCurva
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkNavCurva ( self, f_cSent ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkNavCurva"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( self._oAtv )
        assert ( f_cSent in locDefs.xSET_SentidosValidos )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a proa atual
        #*/
        l_iProa = int ( self._oAtv.getNavProa ())

        #** ---------------------------------------------------------------------------------------
        #*  obtem o novo nivel
        #*/
        l_iProa = tkDialogs.askinteger ( locDefs.xTXT_Prg, "Proa:", valIni = l_iProa,
                                                                       valMin = 0,
                                                                       valMax = 360 )

        #** ---------------------------------------------------------------------------------------
        #*  resposta valida ?
        #*/
        if ( None != l_iProa ):
         
            #** -----------------------------------------------------------------------------------
            #*  normaliza a proa
            #*/
            l_iProa = l_iProa % 360

            #** -----------------------------------------------------------------------------------
            #*  obtem o flight engine da aeronave
            #*/
            l_fe = self._oAtv.getFE ()
            assert ( l_fe ) 

            #** -----------------------------------------------------------------------------------
            #*  obtem a cinematica de voo da aeronave
            #*/
            l_cv = l_fe.getCineVoo ()
            assert ( l_cv )

            #** -----------------------------------------------------------------------------------
            #*  muda a proa da aeronave
            #*/
            l_cv.cbkNavCurva ( f_cSent, l_iProa )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkNavNiv
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkNavNiv ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkNavNiv"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a altitude atual em metros e converte em nivel
        #*/
        l_iNiv = int (( self._oAtv.getNavAlt () * glbDefs.xCNV_M2ft ) / 100. )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a altitude minima em pes e converte em nivel
        #*/
        l_iMin = int ( self._oAtv.getAltitudeMinima () / 100. )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a altitude maxima em pes e converte em nivel
        #*/
        l_iMax = int ( self._oAtv.getAltitudeMaxima () / 100. )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o novo nivel
        #*/
        l_iNiv = tkDialogs.askinteger ( locDefs.xTXT_Prg, "Nivel:", valIni = l_iNiv,
                                                                       valMin = l_iMin,
                                                                       valMax = l_iMax )

        #** ---------------------------------------------------------------------------------------
        #*  resposta valida ?
        #*/
        if ( None != l_iNiv ):
         
            #** -----------------------------------------------------------------------------------
            #*  obtem o flight engine da aeronave
            #*/
            l_fe = self._oAtv.getFE ()
            assert ( l_fe ) 

            #** -----------------------------------------------------------------------------------
            #*  obtem a cinematica de voo da aeronave
            #*/
            l_cv = l_fe.getCineVoo ()
            assert ( l_cv )

            #** -----------------------------------------------------------------------------------
            #*  muda o nivel da aeronave
            #*/
            l_cv.cbkNavAlt ( l_iNiv * 100 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkNavVel
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkNavVel ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkNavVel"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade atual em m/ms e converte para knots
        #*/
        l_iVel = int ( round ( self._oAtv.getNavVel () * glbDefs.xCNV_Ms2Knots ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade minima em knots
        #*/
        l_iMin = self._oAtv.getVelocidadeMinima ()

        #** ---------------------------------------------------------------------------------------
        #*  obtem a velocidade maxima em knots
        #*/
        l_iMax = self._oAtv.getVelocidadeMaxima ()

        #** ---------------------------------------------------------------------------------------
        #*  obtem o novo nivel
        #*/
        l_iVel = tkDialogs.askinteger ( locDefs.xTXT_Prg, "Vel:", valIni = l_iVel,
                                                                  valMin = l_iMin,
                                                                  valMax = l_iMax )

        #** ---------------------------------------------------------------------------------------
        #*  resposta valida ?
        #*/
        if ( None != l_iVel ):
         
            #** -----------------------------------------------------------------------------------
            #*  obtem o flight engine da aeronave
            #*/
            l_fe = self._oAtv.getFE ()
            assert ( l_fe ) 

            #** -----------------------------------------------------------------------------------
            #*  obtem a cinematica de voo da aeronave
            #*/
            l_cv = l_fe.getCineVoo ()
            assert ( l_cv )

            #** -----------------------------------------------------------------------------------
            #*  muda a velocidade da aeronave
            #*/
            l_cv.cbkNavVel ( l_iVel )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxAuto
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxAuto ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxAuto"

        #// return code
        #// ---------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*/
        if (( self._oAtv.isActive ()) and
            ( self._oAtv.getSolo ()) and
            ( 'Y' != self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  aeronave acidentada ? 
            #*/
            if ( self._oAtv.getStatusSolo () in [ 'A', 'X' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave acidentada
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "acidentada", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave aguardando reboque ?
            #*/
            elif ( 'R' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave aguardando reboque
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "aguardando reboque", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave ja em taxi ?
            #*/
            elif ( self._oAtv.getStatusSolo in [ 'B', 'T' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave ja esta em taxi
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "ja esta em taxi", glbDefs.xCOR_yellow )
                
            #** -----------------------------------------------------------------------------------
            #*  ok, aeronave em condicoes de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  salva a escala atual
                #*/
                l_iEsc = self._oExe.getEscala ()
                assert ( l_iEsc in locDefs.xSET_EscalasValidas )

                #** -------------------------------------------------------------------------------
                #*  vai para a escala 1
                #*/
                self.cbkExeEscala ( 1 )

                #** -------------------------------------------------------------------------------
                #*  apagar o percurso inicial que a aeronave desenvolveria, caso fosse aceito,
                #*  apos a parada no pouso
                #*/
                if ( 'S' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  exibe o percurso da aeronave
                    #*/
                    self._oAtv.setShowPercurso ( True )

                #** -------------------------------------------------------------------------------
                #*  obtem o destino do taxi
                #*/
                l_bRC = self.obtemDestinoTaxi ()

                #** -------------------------------------------------------------------------------
                #*  aeronave parando apos o pouso ?
                #*/
                if (( 'S' == self._oAtv.getStatusSolo ()) and ( l_bRC )):

                    #** ---------------------------------------------------------------------------
                    #*  oculta o percurso da aeronave
                    #*/
                    self._oAtv.setShowPercurso ( False )

                #** -------------------------------------------------------------------------------
                #*  volta a escala anterior
                #*/
                self.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  senao, erro
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave inativa, em DEP ou em voo
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "inativa, em DEP ou em voo", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxCancela
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxCancela ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxPara"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._oExe )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*/
        if (( self._oAtv.isActive ()) and
            ( self._oAtv.getSolo ()) and
            ( 'Y' != self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  aeronave acidentada ? 
            #*/
            if ( self._oAtv.getStatusSolo () in [ 'A', 'X' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave acidentada
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "acidentada", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave aguardando reboque ?
            #*/
            elif ( 'R' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave aguardando reboque
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "aguardando reboque", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  ok, aeronave em condicoes de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  salva a escala atual
                #*/
                l_iEsc = self._oExe.getEscala ()
                assert ( l_iEsc in locDefs.xSET_EscalasValidas )

                #** -------------------------------------------------------------------------------
                #*  vai para a escala 1
                #*/
                self.cbkExeEscala ( 1 )

                #** -------------------------------------------------------------------------------
                #*  aeronave em taxi, porem em pane ? 
                #*/
                if ( 'B' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para parada 
                    #*/
                    self._oAtv.setStatusSolo ( 'G' )
                    #EXIT

                #** -------------------------------------------------------------------------------
                #*  aeronave em taxi ? 
                #*/
                elif ( self._oAtv.getStatusSolo () in [ 'C', 'D', 'T' ] ):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para ...
                    #*/
                    self._oAtv.setStatusSolo ( 'P' )
                    #EXIT

                #** -------------------------------------------------------------------------------
                #*  senao, aeronave nao esta em taxi
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  erro, cancelamento impossivel
                    #*/
                    self._msgBox.addMsg ( self._oAtv.getIdent (), "cancelamento impossivel", glbDefs.xCOR_yellow )

                #** -------------------------------------------------------------------------------
                #*  volta a escala anterior
                #*/
                self.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  senao, erro
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave inativa, em DEP ou em voo
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "inativa, em DEP ou em voo", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxCongela
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxCongela ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxCongela"

        #// return code
        #// ---------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._oExe )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*/
        if (( self._oAtv.isActive ()) and
            ( self._oAtv.getSolo ()) and
            ( 'Y' != self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  aeronave acidentada ? 
            #*/
            if ( self._oAtv.getStatusSolo () in [ 'A', 'X' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave acidentada
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "acidentada", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave aguardando reboque ?
            #*/
            elif ( 'R' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave aguardando reboque
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "aguardando reboque", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  ok, aeronave em condicoes de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  salva a escala atual
                #*/
                l_iEsc = self._oExe.getEscala ()
                assert ( l_iEsc in locDefs.xSET_EscalasValidas )

                #** -------------------------------------------------------------------------------
                #*  vai para a escala 1
                #*/
                self.cbkExeEscala ( 1 )

                #** -------------------------------------------------------------------------------
                #*  aeronave em taxi, porem em pane ? 
                #*/
                if ( 'B' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para parada e em pane, porem nao necessita de reboque
                    #*/
                    self._oAtv.setStatusSolo ( 'G' )

                    #** ---------------------------------------------------------------------------
                    #*  Ok
                    #*/
                    l_bRC = True

                #** -------------------------------------------------------------------------------
                #*  aeronave em taxi para a posição de decolagem ? 
                #*/
                elif ( 'D' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para congelada durante o taxi para decolagem
                    #*/
                    self._oAtv.setStatusSolo ( 'E' )

                    #** ---------------------------------------------------------------------------
                    #*  Ok
                    #*/
                    l_bRC = True

                #** -------------------------------------------------------------------------------
                #*  aeronave em taxi ? 
                #*/
                elif ( 'T' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para congelado
                    #*/
                    self._oAtv.setStatusSolo ( 'C' )

                    #** ---------------------------------------------------------------------------
                    #*  Ok
                    #*/
                    l_bRC = True

                #** -------------------------------------------------------------------------------
                #*  senao, aeronave nao esta em taxi
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  erro, congelamento impossivel
                    #*/
                    self._msgBox.addMsg ( self._oAtv.getIdent (), "congelamento impossivel", glbDefs.xCOR_yellow )

                #** -------------------------------------------------------------------------------
                #*  volta a escala anterior
                #*/
                self.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  senao, erro
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave inativa, em DEP ou em voo
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "inativa, em DEP ou em voo", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxDeparture
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxDeparture ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxDeparture"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave ativa e no solo ? 
        #*/
        if (( self._oAtv.isActive ()) and
            ( self._oAtv.getSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  aeronave acidentada ou em pane ? 
            #*/
            if ( self._oAtv.getStatusSolo () in [ 'A', 'B', 'G', 'X' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave acidentada ou em pane
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "acidentada ou em pane", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave congelada ? 
            #*/
            elif ( 'C' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave congelada
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "congelada", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave decolando ? 
            #*/
            elif ( self._oAtv.getStatusSolo () in [ 'D', 'E', 'Y' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave decolando
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "decolando", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave pousando ? 
            #*/
            elif ( 'S' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave pousando
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "pousando", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave em taxi ? 
            #*/
            elif ( 'T' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave em taxi
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "em taxi", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  senao, ok para decolar
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  obtem os dados para a decolagem
                #*/
                self.obtemDadosDecolagem ()

        #** ---------------------------------------------------------------------------------------
        #*  senao, erro
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave inativa, em DEP ou em voo
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "inativa, em DEP ou em voo", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxDescongela
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxDescongela ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxDescongela"

        #// return code
        #// ---------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._oExe )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*/
        if (( self._oAtv.isActive ()) and
            ( self._oAtv.getSolo ()) and
            ( 'Y' != self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  aeronave acidentada ? 
            #*/
            if ( self._oAtv.getStatusSolo () in [ 'A', 'X' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave acidentada
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "acidentada", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave aguardando reboque ?
            #*/
            elif ( 'R' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave aguardando reboque
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "aguardando reboque", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  ok, aeronave em condicoes de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  salva a escala atual
                #*/
                l_iEsc = self._oExe.getEscala ()
                assert ( l_iEsc in locDefs.xSET_EscalasValidas )

                #** -------------------------------------------------------------------------------
                #*  vai para a escala 1
                #*/
                self.cbkExeEscala ( 1 )

                #** -------------------------------------------------------------------------------
                #*  aeronave congelada ? 
                #*/
                if ( 'C' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para aeronave em taxi
                    #*/
                    self._oAtv.setStatusSolo ( 'T' )

                    #** ---------------------------------------------------------------------------
                    #*  Ok
                    #*/
                    l_bRC = True

                #** -------------------------------------------------------------------------------
                #*  aeronave congelada durante o taxi para decolagem ? 
                #*/
                elif ( 'E' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda status para aeronave em taxi para a posição de decolagem
                    #*/
                    self._oAtv.setStatusSolo ( 'D' )

                    #** ---------------------------------------------------------------------------
                    #*  Ok
                    #*/
                    l_bRC = True

                #** -------------------------------------------------------------------------------
                #*  senao, erro
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  erro, taxi nao esta congelado
                    #*/
                    self._msgBox.addMsg ( self._oAtv.getIdent (), "taxi nao esta congelado", glbDefs.xCOR_yellow )

                #** -------------------------------------------------------------------------------
                #*  volta a escala anterior
                #*/
                self.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  senao, erro
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave inativa, em DEP ou em voo
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "inativa, em DEP ou em voo", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxManual
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxManual ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxManual"

        #// return code
        #// ---------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._oExe )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  condicoes de execução ok ?
        #*/
        if (( self._oAtv.isActive ()) and
            ( self._oAtv.getSolo ()) and
            ( 'Y' != self._oAtv.getStatusSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  aeronave acidentada ? 
            #*/
            if ( self._oAtv.getStatusSolo () in [ 'A', 'X' ] ):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave acidentada
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "acidentada", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  aeronave aguardando reboque ?
            #*/
            elif ( 'R' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  erro, aeronave aguardando reboque
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "aguardando reboque", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  ok, aeronave em condicoes de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  aeronave ja esta em taxi ? 
                #*/
                if ( self._oAtv.getStatusSolo () in [ 'T', 'B' ] ):

                    #** ---------------------------------------------------------------------------
                    #*  erro, congelamento impossivel
                    #*/
                    self._msgBox.addMsg ( self._oAtv.getIdent (), "ja esta em taxi", glbDefs.xCOR_yellow )

                #** -------------------------------------------------------------------------------
                #*  senao, aeronave nao esta em taxi
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  salva a escala atual
                    #*/
                    l_iEsc = self._oExe.getEscala ()
                    assert ( l_iEsc in locDefs.xSET_EscalasValidas )

                    #** ---------------------------------------------------------------------------
                    #*  vai para a escala 1
                    #*/
                    self.cbkExeEscala ( 1 )

                    #** ---------------------------------------------------------------------------
                    #*  obtem o percurso do taxi
                    #*/
                    l_bRC = self.obtemPercursoTaxi ()

                    #** ---------------------------------------------------------------------------
                    #*  volta a escala anterior
                    #*/
                    self.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  senao, erro
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, aeronave inativa, em DEP ou em voo
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "inativa, em DEP ou em voo", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::cbkTaxSwitch
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def cbkTaxSwitch ( self, l_bVal ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::cbkTaxSwitch"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  get taxi status
        #*/
        l_bVal = self._oAtv.getTaxStatus ()

        #** ---------------------------------------------------------------------------------------
        #*  taxi descongelado ? 
        #*/
        if ( l_bVal ):

            #** -----------------------------------------------------------------------------------
            #*  congela o taxi
            #*/
            if ( self.cbkTaxCongela ()):
            
                #** -------------------------------------------------------------------------------
                #*  congela o taxi
                #*/
                self._btn [ xN_Frz ].value = "Desc"
            
        #** ---------------------------------------------------------------------------------------
        #*  senao, taxi congelado
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  descongela o taxi
            #*/
            if ( self.cbkTaxDescongela ()):
            
                #** -------------------------------------------------------------------------------
                #*  congela o taxi
                #*/
                self._btn [ xN_Frz ].value = "Cong"
            
        #** ---------------------------------------------------------------------------------------
        #*  switch status value
        #*/
        self._oAtv.setTaxStatus ( not l_bVal )
        
        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::checkBoolLogic  
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def checkBoolLogic ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::checkBoolLogic  "


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._btn )

        #** ---------------------------------------------------------------------------------------
        #*  desabilita todas as opcoes
        #*/
        for l_btn in self._btn:  

            if ( None != l_btn ): l_btn.disabled = True
            
        #** ---------------------------------------------------------------------------------------
        #*  aeronave selecionada ?
        #*/
        if ( None != self._oAtv ):
        
            #** -----------------------------------------------------------------------------------
            #*  aeronave no solo ?
            #*/
            if ( self._oAtv.getSolo ()):

                #** -------------------------------------------------------------------------------
                #*  habilita opcoes globais
                #*/
                if ( None != self._btn [ xN_KlS ] ): self._btn [ xN_KlS ].disabled = False

                #** -------------------------------------------------------------------------------
                #*  habilita opcoes de Taxi
                #*/
                if ( None != self._btn [ xN_Aut ] ): self._btn [ xN_Aut ].disabled = False
                if ( None != self._btn [ xN_Can ] ): self._btn [ xN_Can ].disabled = False
                if ( None != self._btn [ xN_Dep ] ): self._btn [ xN_Dep ].disabled = False
                if ( None != self._btn [ xN_Man ] ): self._btn [ xN_Man ].disabled = False

                #** -------------------------------------------------------------------------------
                #*/
                if ( None != self._btn [ xN_Frz ] ):

                    #** ---------------------------------------------------------------------------
                    #*  obtem o status de congelamento do taxi desta aeronave
                    #*/
                    self._btn [ xN_Frz ].value = self.getTaxStatus ( False )
                    self._btn [ xN_Frz ].disabled = False
                
            #** -----------------------------------------------------------------------------------
            #*  senao, aeronave em voo
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  habilita opcoes globais
                #*/
                if ( None != self._btn [ xN_KlV ] ): self._btn [ xN_KlV ].disabled = False

                #** -------------------------------------------------------------------------------
                #*  habilita opcoes de Aproximação
                #*/
                if ( None != self._btn [ xN_Arr ] ): self._btn [ xN_Arr ].disabled = False
                if ( None != self._btn [ xN_Emg ] ): self._btn [ xN_Emg ].disabled = False
                if ( None != self._btn [ xN_Tok ] ): self._btn [ xN_Tok ].disabled = False

                #** -------------------------------------------------------------------------------
                #*  habilita opcoes de Circuito
                #*/
                if ( None != self._btn [ xN_Ext ] ): self._btn [ xN_Ext ].disabled = False
                if ( None != self._btn [ xN_PCV ] ): self._btn [ xN_PCV ].disabled = False
                if ( None != self._btn [ xN_PVt ] ): self._btn [ xN_PVt ].disabled = False

                #** -------------------------------------------------------------------------------
                #*  habilita opcoes de Navegação
                #*/
                if ( None != self._btn [ xN_Dir ] ): self._btn [ xN_Dir ].disabled = False
                if ( None != self._btn [ xN_Esq ] ): self._btn [ xN_Esq ].disabled = False
                if ( None != self._btn [ xN_Niv ] ): self._btn [ xN_Niv ].disabled = False
                if ( None != self._btn [ xN_Vel ] ): self._btn [ xN_Vel ].disabled = False

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::checkPousoDireto
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def checkPousoDireto ( self ):

        #// nome do método (logger)
        #// ---------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::checkPousoDireto"

        #// return code
        #// ---------------------------------------------------------------------------------------
        l_iRC = 0


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )
        assert ( self._msgBox )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira da pista
        #*/
        l_iCab = self._oAtv.getCktCab ()
        assert (( l_iCab >= 0 ) and ( l_iCab < locDefs.xMAX_Cabeceiras ))

        #** ---------------------------------------------------------------------------------------
        #*  obtem o flight engine da aeronave
        #*/
        l_fe = self._oAtv.getFE ()
        assert ( l_fe )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cinematica de voo da aeronave
        #*/
        l_cv = l_fe.getCineVoo ()
        assert ( l_cv )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o setor de pouso
        #*/
        l_iSetor = l_cv.obtemSetorPouso ()
        assert (( l_iSetor >= 0 ) and ( l_iSetor <= 2 ))

        #l_log.info ( "Anv: [%s] setor de pouso: [%d] cabeceira: [%d]" % ( self._oAtv.getIdent (), l_iSetor, l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  cabeceira eh o setor de pouso ?
        #*/
        if ( l_iCab == l_iSetor ):

            #** -----------------------------------------------------------------------------------
            #*  checa a rampa e a velocidade de aproximação
            #*/
            l_iRC = l_cv.checkRampaVelocidade ()

            #** -----------------------------------------------------------------------------------
            #*  codigo de erro 1 ?
            #*/
            if ( 1 == l_iRC ):
            
                #** -------------------------------------------------------------------------------
                #*  erro, velocidade muito alta
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "velocidade muito alta", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  codigo de erro 2 ?
            #*/
            elif ( 2 == l_iRC ):
            
                #** -------------------------------------------------------------------------------
                #*  erro, rampa maior que a permitida
                #*/
                self._msgBox.addMsg ( self._oAtv.getIdent (), "rampa maior que a permitida", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  senao, cabeceira nao eh o setor de pouso
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  erro, momento inadequado
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "setor inadequado", glbDefs.xCOR_yellow )

            #** -----------------------------------------------------------------------------------
            #*  return code: cabeceira nao eh o setor de pouso
            #*/
            l_iRC = 3
            
        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( 0 == l_iRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::deselectFlight
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def deselectFlight ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::deselectFlight"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave nao selecionada
        #*/
        self._oAtv = None

        #** ---------------------------------------------------------------------------------------
        #*  recria o menu principal
        #*/
        self.makeMenu ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::doRedraw
    #*  -------------------------------------------------------------------------------------------
    #*  initializes the scope area
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def doRedraw ( self, f_bg ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::doRedraw"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_bg )

        #** ---------------------------------------------------------------------------------------
        #*  cria a area de menus
        #*/
        l_srfMenu = pygame.Surface ( self._tWH )
        assert ( l_srfMenu )
         
        l_srfMenu.set_colorkey ( l_srfMenu.get_at (( 1, 1 )))

        #** ---------------------------------------------------------------------------------------
        #*  cria o header
        #*/
        self.makeHeader ( l_srfMenu )

        #** ---------------------------------------------------------------------------------------
        #*  copia no background
        #*/
        f_bg.blit ( l_srfMenu, self._tNW )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::getTaxStatus
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getTaxStatus ( self, f_bOpt ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::getTaxStatus"

        #/ status do taxi
        #/ ----------------------------------------------------------------------------------------
        l_bVal = True


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( None != self._oAtv ): 

            #** -----------------------------------------------------------------------------------
            #*/
            l_bVal = self._oAtv.getTaxStatus ()

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( f_bOpt ): 

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

            #** -----------------------------------------------------------------------------------
            #*/
            return ( l_bVal )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( l_bVal ): 

            #** -----------------------------------------------------------------------------------
            #*  congela o taxi
            #*/
            l_szVal = "Cong"

        #** ---------------------------------------------------------------------------------------
        #*/
        else:
            
            #** -----------------------------------------------------------------------------------
            #*  descongela o taxi
            #*/
            l_szVal = "Desc"

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_szVal )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::makeHeader
    #*  -------------------------------------------------------------------------------------------
    #*  create a strip icon
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeHeader ( self, f_surf ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::makeHeader"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_surf )

        #** ---------------------------------------------------------------------------------------
        #*  retangulo que define a area de strips
        #*/
        l_retArea = ( 0, 0 ), self._tWH

        #** ---------------------------------------------------------------------------------------
        #*  desenha a moldura externa da area de strips
        #*/
        pygame.draw.rect ( f_surf, locDefs.xCOR_Header, l_retArea, 1 )

        #** ---------------------------------------------------------------------------------------
        #*  cria o header da lista de strips
        #*/
        l_srfHdr = pygame.Surface (( self._tWH [ 0 ], self._iHeaderHeight ))
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
        l_szTxt = l_font.render ( "menu", 1, glbDefs.xCOR_SGrey )
        assert ( l_szTxt )

        #** ---------------------------------------------------------------------------------------
        #*  calcula a posição do texto
        #*/
        l_txtPos = l_szTxt.get_rect ()
        assert ( l_txtPos )

        l_txtPos.center = ( self._tWH [ 0 ] / 2, ( self._iHeaderHeight / 2 ) - 1 )

        #** ---------------------------------------------------------------------------------------
        #*  transfere o texto para o header
        #*/
        l_srfHdr.blit ( l_szTxt, l_txtPos )

        #** ---------------------------------------------------------------------------------------
        #*  transfere o header para a tela
        #*/
        f_surf.blit ( l_srfHdr, ( 0, 0 ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::makeMenu
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeMenu ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::makeMenu"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicies de execução
        #*/
        assert ( self._guiApp )

        #** ---------------------------------------------------------------------------------------
        #*  flag que habilita/desabilita os menus
        #*/
        self.checkBoolLogic ()

        #** ---------------------------------------------------------------------------------------
        #*  aeronave selecionada ?
        #*/
        if ( None != self._oAtv ):
        
            #** -----------------------------------------------------------------------------------
            #*  aeronave no solo ?
            #*/
            if ( self._oAtv.getSolo ()):

                #** -------------------------------------------------------------------------------
                #*  ja existe um menu na aplicação ?
                #*/
                if ( self._vbxMenu != self._vbxSolo ):
                
                    #** ---------------------------------------------------------------------------
                    #*  ja existe um menu na aplicação ?
                    #*/
                    if ( None != self._vbxMenu ):
                    
                        #** -----------------------------------------------------------------------
                        #*  remove it to our app
                        #*/
                        self._guiApp.remove ( self._vbxMenu )

                    #** ---------------------------------------------------------------------------
                    #*  cria menu com opcoes de aeronave no solo
                    #*/
                    self._vbxMenu = self._vbxSolo
                    #self._vbxMenu = self.makeMenuSolo ()
                    assert ( self._vbxMenu )

                    #** ---------------------------------------------------------------------------
                    #*  and add it to our app
                    #*/
                    self._guiApp.add ( self._vbxMenu )

            #** -----------------------------------------------------------------------------------
            #*  senao, aeronave em voo
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  ja existe um menu na aplicação ?
                #*/
                if ( self._vbxMenu != self._vbxVoo ):
                
                    #** ---------------------------------------------------------------------------
                    #*  ja existe um menu na aplicação ?
                    #*/
                    if ( None != self._vbxMenu ):
                    
                        #** -----------------------------------------------------------------------
                        #*  remove it to our app
                        #*/
                        self._guiApp.remove ( self._vbxMenu )

                    #** ---------------------------------------------------------------------------
                    #*  cria menu com opcoes de aeronave em voo
                    #*/
                    self._vbxMenu = self._vbxVoo
                    assert ( self._vbxMenu )
            
                    #** ---------------------------------------------------------------------------
                    #*  and add it to our app
                    #*/
                    self._guiApp.add ( self._vbxMenu )

        #** ---------------------------------------------------------------------------------------
        #*  senao, nenhuma aeronave selecionada
        #*/
        else:
        
            #** -----------------------------------------------------------------------------------
            #*  ja existe um menu na aplicação ?
            #*/
            if ( self._vbxMenu != self._vbxDummy ):
            
                #** -------------------------------------------------------------------------------
                #*  ja existe um menu na aplicação ?
                #*/
                if ( None != self._vbxMenu ):
                
                    #** ---------------------------------------------------------------------------
                    #*  remove it to our app
                    #*/
                    self._guiApp.remove ( self._vbxMenu )

                #** -------------------------------------------------------------------------------
                #*  cria menu com opcoes gerais
                #*/
                self._vbxMenu = self._vbxDummy
                assert ( self._vbxMenu )

                #** -------------------------------------------------------------------------------
                #*  and add it to our app
                #*/
                self._guiApp.add ( self._vbxMenu )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::makeMenuDummy
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeMenuDummy ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::makeMenuDummy"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a primeira linha do menu
        #*/
        l_btnD01 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD01.connect ( CLICK, self.cbkDoNothing )

        l_btnD02 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD02.connect ( CLICK, self.cbkDoNothing )

        l_btnD03 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD03.connect ( CLICK, self.cbkDoNothing )

        l_btnD04 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD04.connect ( CLICK, self.cbkDoNothing )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL1 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL1 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL1.add ( l_btnD01, l_btnD02, l_btnD03, l_btnD04 )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a segunda linha do menu
        #*/
        l_btnD05 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD05.connect ( CLICK, self.cbkDoNothing )

        l_btnD06 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD06.connect ( CLICK, self.cbkDoNothing )

        l_btnD07 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD07.connect ( CLICK, self.cbkDoNothing )

        l_btnD08 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD08.connect ( CLICK, self.cbkDoNothing )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL2 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL2 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL2.add ( l_btnD05, l_btnD06, l_btnD07, l_btnD08 )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a terceira linha do menu (Anv)
        #*/
        l_btnAtv = gooeypy.Button ( "Ini", width = 62 )
        l_btnAtv.connect ( CLICK, self.cbkExeAtiva )

        l_btnD09 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD09.connect ( CLICK, self.cbkDoNothing )

        l_btnD10 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD10.connect ( CLICK, self.cbkDoNothing )

        l_btnD11 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD11.connect ( CLICK, self.cbkDoNothing )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL3 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL3 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL3.add ( l_btnAtv, l_btnD09, l_btnD10, l_btnD11 )

        #** ---------------------------------------------------------------------------------------
        #*  make a VBox, which will automatically position widgets inside of it vertically
        #*/
        l_vbxMenu = gooeypy.VBox ( x = self._tMenuPos [ 0 ],
                                   y = self._tMenuPos [ 1 ], padding = 1, spacing = 1 )
        assert ( l_vbxMenu )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "vertical box"
        #*/
        l_vbxMenu.add ( l_hbxL1, l_hbxL2, l_hbxL3 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_vbxMenu )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::makeMenuSolo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeMenuSolo ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::makeMenuSolo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a primeira linha do menu (Tax)
        #*/
        self._btn [ xN_Aut ] = gooeypy.Button ( "Auto", width = 62 )
        self._btn [ xN_Aut ].connect ( CLICK, self.cbkTaxAuto )

        self._btn [ xN_Man ] = gooeypy.Button ( "Man", width = 62 )
        self._btn [ xN_Man ].connect ( CLICK, self.cbkTaxManual )

        self._btn [ xN_Dep ] = gooeypy.Button ( "Dep", width = 62 )
        self._btn [ xN_Dep ].connect ( CLICK, self.cbkTaxDeparture )

        self._btn [ xN_Frz ] = gooeypy.Button ( self.getTaxStatus ( False ), width = 62 )
        self._btn [ xN_Frz ].connect ( CLICK, self.cbkTaxSwitch, self.getTaxStatus ( True ))

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL1 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL1 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL1.add ( self._btn [ xN_Aut ], self._btn [ xN_Man ], self._btn [ xN_Dep ], self._btn [ xN_Frz ] )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a segunda linha do menu
        #*/
        l_btnD01 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD01.connect ( CLICK, self.cbkDoNothing )

        l_btnD02 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD02.connect ( CLICK, self.cbkDoNothing )

        l_btnD03 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD03.connect ( CLICK, self.cbkDoNothing )

        l_btnD04 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD04.connect ( CLICK, self.cbkDoNothing )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL2 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL2 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL2.add ( l_btnD01, l_btnD02, l_btnD03, l_btnD04 )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a terceira linha do menu (Anv)
        #*/
        l_btnAtv = gooeypy.Button ( "Ini", width = 62 )
        l_btnAtv.connect ( CLICK, self.cbkExeAtiva )

        self._btn [ xN_KlS ] = gooeypy.Button ( "Elim", width = 62 )
        self._btn [ xN_KlS ].connect ( CLICK, self.cbkExeElimina )

        self._btn [ xN_Can ] = gooeypy.Button ( "Cnl", width = 62 )
        self._btn [ xN_Can ].connect ( CLICK, self.cbkTaxCancela )

        l_btnD05 = gooeypy.Button ( " ", width = 62, disabled = True )
        l_btnD05.connect ( CLICK, self.cbkDoNothing )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL3 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL3 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL3.add ( l_btnAtv, self._btn [ xN_KlS ], self._btn [ xN_Can ], l_btnD05 )

        #** ---------------------------------------------------------------------------------------
        #*  make a VBox, which will automatically position widgets inside of it vertically
        #*/
        l_vbxMenu = gooeypy.VBox ( x = self._tMenuPos [ 0 ],
                                   y = self._tMenuPos [ 1 ], padding = 1, spacing = 1 )
        assert ( l_vbxMenu )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "vertical box"
        #*/
        l_vbxMenu.add ( l_hbxL1, l_hbxL2, l_hbxL3 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_vbxMenu )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::makeMenuVoo
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeMenuVoo ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::makeMenuVoo"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a primeira linha do menu (Nav)
        #*/
        self._btn [ xN_Esq ] = gooeypy.Button ( "<<", width = 62 )
        self._btn [ xN_Esq ].connect ( CLICK, self.cbkNavCurva, 'E' )

        #self._btn [ xN_Esq ].stylesets [ "disabled" ][ "bgcolor" ] = ( 128, 255, 255 )
        #self._btn [ xN_Esq ].stylesets [ "focused" ] [ "bgcolor" ] = (   0, 128, 255 )
        #self._btn [ xN_Esq ].stylesets [ "default" ] [ "bgcolor" ] = (   0, 128, 192 )
        #self._btn [ xN_Esq ].stylesets [ "down" ]    [ "bgcolor" ] = (   0,   0, 255 )
        #self._btn [ xN_Esq ].stylesets [ "hover" ]   [ "bgcolor" ] = (   0,   0, 160 )

        self._btn [ xN_Dir ] = gooeypy.Button ( ">>", width = 62 )
        self._btn [ xN_Dir ].connect ( CLICK, self.cbkNavCurva, 'D' )

        self._btn [ xN_Vel ] = gooeypy.Button ( "Vel", width = 62 )
        self._btn [ xN_Vel ].connect ( CLICK, self.cbkNavVel )

        self._btn [ xN_Niv ] = gooeypy.Button ( "Niv", width = 62 )
        self._btn [ xN_Niv ].connect ( CLICK, self.cbkNavNiv )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL1 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL1 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL1.add ( self._btn [ xN_Esq ], self._btn [ xN_Dir ], self._btn [ xN_Vel ], self._btn [ xN_Niv ] )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a segunda linha do menu (Ckt/Apx)
        #*/
        self._btn [ xN_PVt ] = gooeypy.Button ( "PerV", width = 62 )
        self._btn [ xN_PVt ].connect ( CLICK, self.cbkCktCircuito, 'V' )

        self._btn [ xN_PCV ] = gooeypy.Button ( "PerC", width = 62 )
        self._btn [ xN_PCV ].connect ( CLICK, self.cbkCktCircuito, 'K' )

        self._btn [ xN_Emg ] = gooeypy.Button ( "APer", width = 62 )
        self._btn [ xN_Emg ].connect ( CLICK, self.cbkApxEmergencia )

        self._btn [ xN_Tok ] = gooeypy.Button ( "Tque", width = 62 )
        self._btn [ xN_Tok ].connect ( CLICK, self.cbkApxToque )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL2 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL2 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL2.add ( self._btn [ xN_PVt ], self._btn [ xN_PCV ], self._btn [ xN_Emg ], self._btn [ xN_Tok ] )

        #** ---------------------------------------------------------------------------------------
        #*  cria botoes para a terceira linha do menu (Anv)
        #*/
        l_btnAtv = gooeypy.Button ( "Ini", width = 62 )
        l_btnAtv.connect ( CLICK, self.cbkExeAtiva )

        self._btn [ xN_KlV ] = gooeypy.Button ( "Elim", width = 62 )
        self._btn [ xN_KlV ].connect ( CLICK, self.cbkExeElimina )

        self._btn [ xN_Ext ] = gooeypy.Button ( "Cnl", width = 62 )
        self._btn [ xN_Ext ].connect ( CLICK, self.cbkCktExit )

        self._btn [ xN_Arr ] = gooeypy.Button ( "Arr", width = 62 )
        self._btn [ xN_Arr ].connect ( CLICK, self.cbkApxPouso )

        #** ---------------------------------------------------------------------------------------
        #*  make a HBox, which will automatically position widgets inside of it horizontally
        #*/
        l_hbxL3 = gooeypy.HBox ( spacing = 1 )
        assert ( l_hbxL3 )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "horizontal box"
        #*/
        l_hbxL3.add ( l_btnAtv, self._btn [ xN_KlV ], self._btn [ xN_Ext ], self._btn [ xN_Arr ] )

        #** ---------------------------------------------------------------------------------------
        #*  make a VBox, which will automatically position widgets inside of it vertically
        #*/
        l_vbxMenu = gooeypy.VBox ( x = self._tMenuPos [ 0 ],
                                   y = self._tMenuPos [ 1 ], padding = 1, spacing = 1 )
        assert ( l_vbxMenu )

        #** ---------------------------------------------------------------------------------------
        #*  coloca os botoes na "vertical box"
        #*/
        l_vbxMenu.add ( l_hbxL1, l_hbxL2, l_hbxL3 )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_vbxMenu )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemCabeceira
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemCabeceira ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::obtemCabeceira"

        #/ flag Ok
        #/ ----------------------------------------------------------------------------------------
        l_bOk = False

        #/ indice de cabeceira
        #/ ----------------------------------------------------------------------------------------
        l_iCab = 0

        #/ indice de pista
        #/ ----------------------------------------------------------------------------------------
        l_iPst = 0


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  lista de pista/cabeceiras
        #*/
        l_lstIdent = []
        l_lstPouso = []

        #** ---------------------------------------------------------------------------------------
        #*  percorre todas as pistas do aerodromo...
        #*/
        for l_oPst in self._oAer.getPistas ():

            #** -----------------------------------------------------------------------------------
            #*  inicia o indice de cabeceiras
            #*/
            l_iCab = 0
            
            #** -----------------------------------------------------------------------------------
            #*  percorre todas as cabeceiras da pista...
            #*/
            for l_oCab in l_oPst.getPstCabs ():

                #** -------------------------------------------------------------------------------
                #*  obtem o nome da cabeceira
                #*/
                l_lstIdent.append ( l_oCab.getCabNome ())
                l_lstPouso.append (( l_iPst, l_iCab ))

                #** -------------------------------------------------------------------------------
                #*  incrementa o indice de cabeceiras
                #*/
                l_iCab += 1

            #** -----------------------------------------------------------------------------------
            #*  incrementa o indice de pistas
            #*/
            l_iPst += 1
            
        #l_log.info ( "Lista de cabeceiras: " + str ( l_lstIdent ))
        #l_log.info ( "Lista de cabeceiras: " + str ( l_lstPouso ))

        #** ---------------------------------------------------------------------------------------
        #*  limpa indices
        #*/
        l_iCab = 0
        l_iPst = 0

        #** ---------------------------------------------------------------------------------------
        #*  cria o dialogo "seleciona cabeceira" e seleciona uma cabeceira
        #*/
        l_bOk, l_iI = dlgSelect.askList ( locDefs.xTXT_Tit, "Cabeceira:", l_lstIdent )
        #l_log.info ( "Opção: " + str ( l_iI ))

        #** ---------------------------------------------------------------------------------------
        #*  Ok ?
        #*/
        if ( l_bOk ):

            #** -----------------------------------------------------------------------------------
            #*  obtem a pista selecionada
            #*/
            l_iPst = l_lstPouso [ l_iI ][ 0 ]
            assert (( l_iPst >= 0 ) and ( l_iPst < locDefs.xMAX_Pistas )) 

            #** -----------------------------------------------------------------------------------
            #*  obtem a cabeceira selecionada
            #*/
            l_iCab = l_lstPouso [ l_iI ][ 1 ]
            assert (( l_iCab >= 0 ) and ( l_iCab < locDefs.xMAX_Cabeceiras )) 

            #l_log.info ( "[%s] - Pista: [%d] Cab: [%d]" % ( l_lstIdent [ l_iI ], l_iPst, l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bOk, l_iPst, l_iCab )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemClick
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemClick ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::obtemClick"

        #/ posição do click do mouse
        #/ ----------------------------------------------------------------------------------------
        l_tClick = None


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  loop do mouse
        #*/
        while ( 1 ):

            #** -----------------------------------------------------------------------------------
            #*  obtem um unico evento da fila 
            #*/
            l_event = pygame.event.wait ()
            #l_log.info ( "evento: " + str ( l_event ))

            #** -----------------------------------------------------------------------------------
            #*  clicou botao do mouse dentro da area de scope ?
            #*/
            if (( MOUSEBUTTONDOWN == l_event.type ) and
                ( l_event.pos [ 0 ] <= glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 1 ][ 0 ] )):

                #** -------------------------------------------------------------------------------
                #*  botao esquerdo ?
                #*/
                if ( 1 == l_event.button ):

                    #** ---------------------------------------------------------------------------
                    #*  ponto de destino
                    #*/
                    l_tClick = l_event.pos
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(Pto): " + str ( l_tClick ))
                    
                    #** ---------------------------------------------------------------------------
                    #*  converte de coodenadas de tela para normalizada
                    #*/
                    l_tClick = viewUtils.device2Scale ( l_tClick )
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(D2S): " + str ( l_tClick ))

                    #** ---------------------------------------------------------------------------
                    #*  desnormaliza as coodenadas
                    #*/
                    l_tClick = viewUtils.unormalizeXY ( l_tClick )
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(UXY): " + str ( l_tClick ))

                    #** ---------------------------------------------------------------------------
                    #*  cai fora...
                    #*/
                    break

                #** -------------------------------------------------------------------------------
                #*  botao direito ?
                #*/
                elif ( 3 == l_event.button ):

                    #** ---------------------------------------------------------------------------
                    #*  cai fora...
                    #*/
                    break

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_tClick )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemDadosDecolagem
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemDadosDecolagem ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::doRedraw"

        #/ flag Ok
        #/ ----------------------------------------------------------------------------------------
        l_bFlag = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        #assert ( f_bg )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a cabeceira de dep
        #*/
        l_bOk, l_iPst, l_iCab = self.obtemCabeceira ()

        #l_log.info ( "l_iPst: " + str ( l_iPst ))
        #l_log.info ( "l_iCab: " + str ( l_iCab ))

        #** ---------------------------------------------------------------------------------------
        #*  dados de pista e cabeceira ok ?
        #*/
        if ( l_bOk ):

            #** -----------------------------------------------------------------------------------
            #*/
            assert (( l_iPst >= 0 ) and ( l_iPst < locDefs.xMAX_Pistas )) 
            assert (( l_iCab >= 0 ) and ( l_iCab < locDefs.xMAX_Cabeceiras )) 

            #** -----------------------------------------------------------------------------------
            #*  pista e cabeceira, no momento da decolagem
            #*/
            self._oAtv.setCktAtual (( l_iPst, l_iCab, 0 ))

            #** -----------------------------------------------------------------------------------
            #*  obtem fator de pane na decolagem
            #*/
            l_btPane = self._oExe.getPaneDecolagem ()
            #l_log.info ( "l_btPane: " + str ( l_btPane ))

            #** -----------------------------------------------------------------------------------
            #*  pane na decolagem ?
            #*/
            if ( 0 != l_btPane ):

                #** -------------------------------------------------------------------------------
                #*  gera pane na decolagem ?
                #*/
                if ( 0 == random.randrange ( 101 - l_btPane )):

                    #** ---------------------------------------------------------------------------
                    #*  fator de pane > 10 ?
                    #*/
                    if ( l_btPane > 10 ):

                        #** -----------------------------------------------------------------------
                        #*  salva novo fator de pane na decolagem
                        #*/
                        self._oExe.setPaneDecolagem ( l_btPane - 10 )

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave parada e em pane, porem nao necessita de reboque
                    #*/
                    self._oAtv.setStatusSolo ( 'G' )

                    #** ---------------------------------------------------------------------------
                    #*  avisa sobre a pane na decolagem
                    #*/
                    self._msgBox.addMsg ( self._oAtv.getIdent (), "Pane. Impossivel decolar", glbDefs.xCOR_yellow )

                #** -------------------------------------------------------------------------------
                #*  senao, decolagem normal
                #*/
                else:

                    #** ---------------------------------------------------------------------------
                    #*  monta o percurso a ser percorrido ate a cabeceira da pista
                    #*/
                    self._oAer.montarPercursoAteCabeceira ( self._oAtv, l_iPst, l_iCab )

                    #** ---------------------------------------------------------------------------
                    #*  exibe o percurso da aeronave
                    #*/
                    self._oAtv.setShowPercurso ( True )
                    #l_log.info ( "setShowPercurso ( True )" )

                    #** ---------------------------------------------------------------------------
                    #*  cria o dialogo "confirma o percurso"
                    #*/
                    l_dlg = dlgPercurso.dlgPercurso ()
                    assert ( l_dlg )

                    #** ---------------------------------------------------------------------------
                    #*  confirma o percurso
                    #*/
                    l_bConfirme = l_dlg.startPanel ()

                    #** ---------------------------------------------------------------------------
                    #*  cria o dialogo "confirma o percurso" e confirma o percurso
                    #*/
                    #l_bConfirme = dlgConfirm.askConfirm ( locDefs.xTXT_Tit, "Confirma o percurso ?" )

                    #** ---------------------------------------------------------------------------
                    #*  oculta o percurso da aeronave
                    #*/
                    self._oAtv.setShowPercurso ( False )
                    #l_log.info ( "setShowPercurso ( False )" )

                    #** ---------------------------------------------------------------------------
                    #*  aceitou o percurso ?
                    #*/
                    if ( l_bConfirme ):

                        #** -----------------------------------------------------------------------
                        #*  muda o status para aeronave em taxi para posição de decolagem
                        #*/
                        self._oAtv.setStatusSolo ( 'D' )

                        #** -----------------------------------------------------------------------
                        #*/
                        l_bFlag = True

                #** -------------------------------------------------------------------------------
                #*  avisa que mudou o status
                #*/
                self._oAtv.setMudouStatus ( True )

            #** -----------------------------------------------------------------------------------
            #*  senao, decolagem normal
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  monta o percurso a ser percorrido ate a cabeceira da pista
                #*/
                self._oAer.montarPercursoAteCabeceira ( self._oAtv, l_iPst, l_iCab )
                #l_log.info ( "monta percurso ate cabeceira" )

                #** -------------------------------------------------------------------------------
                #*  exibe o percurso da aeronave
                #*/
                self._oAtv.setShowPercurso ( True )
                #l_log.info ( "setShowPercurso ( True )" )

                #** -------------------------------------------------------------------------------
                #*  cria o dialogo "confirma o percurso"
                #*/
                l_dlg = dlgPercurso.dlgPercurso ()
                assert ( l_dlg )

                #** -------------------------------------------------------------------------------
                #*  confirma o percurso
                #*/
                l_bConfirme = l_dlg.startPanel ()

                #** -------------------------------------------------------------------------------
                #*  cria o dialogo "confirma o percurso" e confirma o percurso
                #*/
                #l_bConfirme = dlgConfirm.askConfirm ( locDefs.xTXT_Tit, "Confirma o percurso ?" )

                #** -------------------------------------------------------------------------------
                #*  oculta o percurso da aeronave
                #*/
                self._oAtv.setShowPercurso ( False )
                #l_log.info ( "setShowPercurso ( False )" )

                #** -------------------------------------------------------------------------------
                #*  aceitou o percurso ?
                #*/
                if ( l_bConfirme ):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave em taxi para posição de decolagem
                    #*/
                    self._oAtv.setStatusSolo ( 'D' )

                    #** ---------------------------------------------------------------------------
                    #*/
                    l_bFlag = True

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bFlag )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemDestinoPouso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemDestinoPouso ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::obtemDestinoPouso"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  obtem a escala atual
        #*/
        l_iEsc = self._oExe.getEscala ()
        assert ( l_iEsc in locDefs.xSET_EscalasValidas )

        #** ---------------------------------------------------------------------------------------
        #*  vai para a escala 1
        #*/
        self.cbkExeEscala ( 1 )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o destino do pouso
        #*/
        self._msgBox.addMsg ( self._oAtv.getIdent (), "direito  = cancela", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "esquerdo = destino", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "selecione o destino do pouso", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o destino do pouso
        #*/
        l_tClick = self.obtemClick ()

        #** ---------------------------------------------------------------------------------------
        #*  aceitou o click ?
        #*/
        if ( None != l_tClick ):

            #** -----------------------------------------------------------------------------------
            #*  configura o destino do taxi
            #*/
            self._oAtv.setTaxDestino ( l_tClick )

        #** ---------------------------------------------------------------------------------------
        #*  volta a escala anterior
        #*/
        self.cbkExeEscala ( l_iEsc )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( True ) # Cond

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemDestinoTaxi
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemDestinoTaxi ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::obtemDestinoTaxi"

        #/ return code
        #/ ----------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAer )
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o destino do pouso
        #*/
        self._msgBox.addMsg ( self._oAtv.getIdent (), "direito  = cancela", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "esquerdo = destino", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "selecione o destino do taxi", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o destino do pouso
        #*/
        l_tClick = self.obtemClick ()
        #l_log.info ( "Posição do click: " + str ( l_tClick ))

        #** ---------------------------------------------------------------------------------------
        #*  aceitou o click ?
        #*/
        if ( None != l_tClick ):

            #** -----------------------------------------------------------------------------------
            #*  salva o ponto definido como destino do taxi
            #*/
            self._oAtv.setTaxDestino ( l_tClick )
            #l_log.info ( "salva o ponto definido como destino do taxi" )

            #** -----------------------------------------------------------------------------------
            #*  monta o menor percurso possivel da posição da aeronave ao destino do taxi
            #*/
            self._oAer.montarPercurso ( self._oAtv )
            #l_log.info ( "monta percurso" )

            #** -----------------------------------------------------------------------------------
            #*  aeronave parando apos o pouso ?
            #*/
            if ( 'S' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  nao necessita de confirmação
                #*/
                l_bConfirme = False

                #** -------------------------------------------------------------------------------
                #*/
                l_bRC = True

            #** -----------------------------------------------------------------------------------
            #*  senao, outra condição de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  exibe o percurso da aeronave
                #*/
                self._oAtv.setShowPercurso ( True )
                #l_log.info ( "setShowPercurso ( True )" )

                #** -------------------------------------------------------------------------------
                #*  cria o dialogo "confirma o percurso"
                #*/
                l_dlg = dlgPercurso.dlgPercurso ()
                assert ( l_dlg )

                #** -------------------------------------------------------------------------------
                #*  confirma o percurso
                #*/
                l_bConfirme = l_dlg.startPanel ()

                #** -------------------------------------------------------------------------------
                #*  cria o dialogo "confirma o percurso" e confirma o percurso
                #*/
                #l_bConfirme = dlgConfirm.askConfirm ( locDefs.xTXT_Tit, "Confirma o percurso ?" )

                #** -------------------------------------------------------------------------------
                #*  oculta o percurso da aeronave
                #*/
                self._oAtv.setShowPercurso ( False )
                #l_log.info ( "setShowPercurso ( False )" )

            #** -----------------------------------------------------------------------------------
            #*  aceitou o percurso ?
            #*/
            if ( l_bConfirme ):

                #** -------------------------------------------------------------------------------
                #*  aeronave parada ? 
                #*/
                if ( 'P' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave em taxi
                    #*/
                    self._oAtv.setStatusSolo ( 'T' )

                #** -------------------------------------------------------------------------------
                #*  aeronave parada e em pane ? 
                #*/
                elif ( 'G' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave em taxi porem em pane
                    #*/
                    self._oAtv.setStatusSolo ( 'B' )

                #** -------------------------------------------------------------------------------
                #*/
                l_bRC = True

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemPercurso
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemPercurso ( self, f_lstEtapa ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::obtemPercurso"

        #/ return code
        #/ ----------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( not f_lstEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  verifica condicoes de execução
        #*/
        assert ( self._oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  aeronave deslocando apos o pouso ?
        #*/
        if ( 'S' == self._oAtv.getStatusSolo ()):

            #** -----------------------------------------------------------------------------------
            #*  obtem a posição do ponto de pouso (wrl.coord)
            #*/
            l_tIni = self._oAtv.getParadaPouso ()
            assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  senao, aeronave no solo
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*  obtem a posição da aeronave (wrl.coord)
            #*/
            l_tIni = self._oAtv.getPosicao ()
            assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  salva o ultimo ponto do percurso como destino do taxi (wrl.coord)
        #*/
        self._oAtv.setTaxDestino ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  cria uma etapa do percurso
        #*/
        l_oEtapa = clsTrj.Etapa ( 0, l_tIni, ( 0., 0. ))
        assert ( l_oEtapa ) 

        #** ---------------------------------------------------------------------------------------
        #*  coloca a etapa no percurso
        #*/
        f_lstEtapa.append ( l_oEtapa )

        #** ---------------------------------------------------------------------------------------
        #*  normaliza as coodenadas. coloca no range (0, 1)
        #*/
        l_tIni = viewUtils.normalizeXY ( l_tIni )
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  converte de normalizada para coodenadas de tela
        #*/
        l_tIni = viewUtils.scale2Device ( l_tIni )
        assert ( l_tIni )

        #** ---------------------------------------------------------------------------------------
        #*  salva o ponto inicial (scr.coord)
        #*/
        l_tAnt = l_tIni

        #** ---------------------------------------------------------------------------------------
        #*  fica no rubber-band
        #*/
        while ( True ):

            #** -----------------------------------------------------------------------------------
            #*  torna o mouse visivel
            #*/
            #pygame.mouse.set_visible ( True )

            #** -----------------------------------------------------------------------------------
            #*  obtem um unico evento da fila 
            #*/
            l_event = pygame.event.wait ()
            #l_log.info ( "evento: " + str ( l_event ))

            #** -----------------------------------------------------------------------------------
            #*  clicou botao do mouse dentro da area de scope ?
            #*/
            if (( MOUSEBUTTONDOWN == l_event.type ) and
                ( l_event.pos [ 0 ] >=   glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ][ 0 ] ) and
                ( l_event.pos [ 0 ] <= ( glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ][ 0 ] +
                                         glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 1 ][ 0 ] ))):

                #l_log.info ( "evento: " + str ( l_event ))

                #** -------------------------------------------------------------------------------
                #*  marca um ponto no percurso (botao esquerdo) ?
                #*/
                if ( 1 == l_event.button ):

                    #** ---------------------------------------------------------------------------
                    #*  ponto de destino (scr.coord)
                    #*/
                    l_tClick = l_event.pos
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(Pto): " + str ( l_tClick ))
                    
                    #** ---------------------------------------------------------------------------
                    #*  calcula o delta de deslocamento do mouse
                    #*/
                    l_iDltX = abs ( l_tClick [ 0 ] - l_tAnt [ 0 ] )
                    l_iDltY = abs ( l_tClick [ 1 ] - l_tAnt [ 1 ] )

                    #** ---------------------------------------------------------------------------
                    #*  deslocamento de pelo menos 5 pixels ?
                    #*/
                    if (( l_iDltX > 5 ) or ( l_iDltY > 5 )):

                        #** -----------------------------------------------------------------------
                        #*  salva o click anterior (scr.coord)
                        #*/
                        l_tAnt = l_tClick

                        #** -----------------------------------------------------------------------
                        #*  converte de coodenadas de tela para normalizada
                        #*/
                        l_tClick = viewUtils.device2Scale ( l_tClick )
                        assert ( l_tClick ) 

                        #l_log.info ( "l_tClick(D2S): " + str ( l_tClick ))

                        #** -----------------------------------------------------------------------
                        #*  desnormaliza as coodenadas
                        #*/
                        l_tClick = viewUtils.unormalizeXY ( l_tClick )
                        assert ( l_tClick ) 

                        #l_log.info ( "l_tClick(UXY): " + str ( l_tClick ))

                        #** -----------------------------------------------------------------------
                        #*  indice da etapa anterior
                        #*/
                        l_iIdx = len ( f_lstEtapa ) - 1

                        #** -----------------------------------------------------------------------
                        #*  obtem a distancia e a direção entre a posição anterior e o ponto atual (wrl.coord)
                        #*/
                        l_dDist, l_dAng = cineCalc.distanciaDirecao ( f_lstEtapa [ l_iIdx ]._tPos, l_tClick )
                        #l_log.info ( "l_dDist: [%f], l_dAng: [%f] " % ( l_dDist, l_dAng ))

                        #** -----------------------------------------------------------------------
                        #*  salva o trecho da etapa anterior
                        #*/
                        f_lstEtapa [ l_iIdx ]._tTrecho = ( l_dDist, l_dAng )

                        #** -----------------------------------------------------------------------
                        #*  cria uma nova etapa do percurso
                        #*/
                        l_oEtapa = clsTrj.Etapa ( l_iIdx + 1, l_tClick, ( 0., l_dAng ))
                        assert ( l_oEtapa ) 

                        #** -----------------------------------------------------------------------
                        #*  coloca a nova etapa no percurso
                        #*/
                        f_lstEtapa.append ( l_oEtapa )

                        #** -----------------------------------------------------------------------
                        #*  salva o ultimo ponto do percurso como destino do taxi (wrl.coord)
                        #*/
                        self._oAtv.setTaxDestino ( l_tClick )
                        #l_log.info ( "posição destino (%d)(1): [%s]" % ( l_iCont, str ( l_tClick )))

                #** -------------------------------------------------------------------------------
                #*  termina o percurso (botao central) ?
                #*/
                elif ( 2 == l_event.button ):

                    #** ---------------------------------------------------------------------------
                    #*  ponto de destino (scr.coord)
                    #*/
                    l_tClick = l_event.pos
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(Pto): " + str ( l_tClick ))
                    
                    #** ---------------------------------------------------------------------------
                    #*  converte de coodenadas de tela para normalizada
                    #*/
                    l_tClick = viewUtils.device2Scale ( l_tClick )
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(D2S): " + str ( l_tClick ))

                    #** ---------------------------------------------------------------------------
                    #*  desnormaliza as coodenadas
                    #*/
                    l_tClick = viewUtils.unormalizeXY ( l_tClick )
                    assert ( l_tClick ) 

                    #l_log.info ( "l_tClick(UXY): " + str ( l_tClick ))

                    #** ---------------------------------------------------------------------------
                    #*  indice da etapa anterior
                    #*/
                    l_iIdx = len ( f_lstEtapa ) - 1

                    #** ---------------------------------------------------------------------------
                    #*  obtem a distancia e a direção entre a posição anterior e o ponto atual (wrl.coord)
                    #*/
                    l_dDist, l_dAng = cineCalc.distanciaDirecao ( f_lstEtapa [ l_iIdx ]._tPos, l_tClick )
                    #l_log.info ( "l_dDist: [%f], l_dAng: [%f] " % ( l_dDist, l_dAng ))

                    #** ---------------------------------------------------------------------------
                    #*  salva o trecho da etapa anterior
                    #*/
                    f_lstEtapa [ l_iIdx ]._tTrecho = ( l_dDist, l_dAng )

                    #** ---------------------------------------------------------------------------
                    #*  cria uma nova etapa do percurso
                    #*/
                    l_oEtapa = clsTrj.Etapa ( l_iIdx + 1, l_tClick, ( 0., l_dAng ))
                    assert ( l_oEtapa ) 

                    #** ---------------------------------------------------------------------------
                    #*  coloca a nova etapa no percurso
                    #*/
                    f_lstEtapa.append ( l_oEtapa )

                    #** ---------------------------------------------------------------------------
                    #*  salva o ultimo ponto do percurso como destino do taxi (wrl.coord)
                    #*/
                    self._oAtv.setTaxDestino ( l_tClick )
                    #l_log.info ( "posição destino (%d)(1): [%s]" % ( l_iCont, str ( l_tClick )))

                    #** ---------------------------------------------------------------------------
                    #*/
                    #for l_oEtapa in f_lstEtapa :

                        #l_log.info ( "--------------" )
                        #l_log.info ( "Percurso(Pto): " + str ( l_oEtapa._iPto ))
                        #l_log.info ( "Percurso(Pos): " + str ( l_oEtapa._tPos ))
                        #l_log.info ( "Percurso(Cmp): " + str ( l_oEtapa._tTrecho [ 0 ] ))
                        #l_log.info ( "Percurso(Dir): " + str ( l_oEtapa._tTrecho [ 1 ] ))

                    #** ---------------------------------------------------------------------------
                    #*  flag operação Ok
                    #*/
                    l_bRC = True

                    #** ---------------------------------------------------------------------------
                    #*  cai fora...
                    #*/
                    break

                #** -------------------------------------------------------------------------------
                #*  cancela o percurso (botao direito) ?
                #*/
                elif ( 3 == l_event.button ):

                    #** ---------------------------------------------------------------------------
                    #*  flag de cancelamento da operação
                    #*/
                    l_bRC = False

                    #** ---------------------------------------------------------------------------
                    #*  cai fora...
                    #*/
                    break

            #** -----------------------------------------------------------------------------------
            #*  moveu o mouse dentro da area de scope ?
            #*/
            elif (( MOUSEMOTION == l_event.type ) and
                  ( l_event.pos [ 0 ] >=   glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ][ 0 ] ) and
                  ( l_event.pos [ 0 ] <= ( glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 0 ][ 0 ] +
                                           glbDefs.xSCR_POS [ glbDefs.xSCR_Scope ][ 1 ][ 0 ] ))):

                #** -------------------------------------------------------------------------------
                #*  ponto de destino (scr.coord)
                #*/
                l_tMouse = l_event.pos
                assert ( l_tMouse ) 

                #l_log.info ( "l_tMouse(Pto): " + str ( l_tMouse ))
                        
                #** -------------------------------------------------------------------------------
                #*  converte de coodenadas de tela para normalizada
                #*/
                l_tMouse = viewUtils.device2Scale ( l_tMouse )
                assert ( l_tMouse ) 

                #l_log.info ( "l_tMouse(D2S): " + str ( l_tMouse ))

                #** -------------------------------------------------------------------------------
                #*  desnormaliza as coodenadas
                #*/
                l_tMouse = viewUtils.unormalizeXY ( l_tMouse )
                assert ( l_tMouse ) 

                #l_log.info ( "l_tMouse(UXY): " + str ( l_tMouse ))

                #** -------------------------------------------------------------------------------
                #*  salva o ultimo ponto do percurso como destino do taxi (wrl.coord)
                #*/
                self._oAtv.setTaxDestino ( l_tMouse )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ----------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )
        
    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::obtemPercursoTaxi 
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def obtemPercursoTaxi ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::obtemPercursoTaxi"

        #/ return code
        #/ ----------------------------------------------------------------------------------------
        l_bRC = False


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  obtem o destino do pouso
        #*/
        self._msgBox.addMsg ( self._oAtv.getIdent (), "direito  = cancela", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "central  = termina", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "esquerdo = marca", glbDefs.xCOR_yellow )
        self._msgBox.addMsg ( self._oAtv.getIdent (), "selecione o percurso do taxi", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  cria um percurso
        #*/
        l_lstEtapa = []
        #assert ( l_lstEtapa )
                                        
        #** ---------------------------------------------------------------------------------------
        #*  salva o percurso na aeronave
        #*/
        self._oAtv.setPercurso ( l_lstEtapa )
        #l_log.info ( "l_lstEtapa...........: " + str ( l_lstEtapa ))
        #l_log.info ( "self._oAtv._lstEtapa: " + str ( self._oAtv._lstEtapa ))

        #** ---------------------------------------------------------------------------------------
        #*  exibe o percurso da aeronave
        #*/
        self._oAtv.setShowPercurso ( True )
        #l_log.info ( "ShowPercurso: " + str ( self._oAtv.getShowPercurso ()))

        #** ---------------------------------------------------------------------------------------
        #*  obtem o percurso do taxi
        #*/
        l_bOk = self.obtemPercurso ( l_lstEtapa )
        #assert ( l_lstEtapa ) 

        #** ---------------------------------------------------------------------------------------
        #*  percurso ok ?
        #*/
        if (( l_bOk ) and ( len ( l_lstEtapa ) > 0 )):

            #** -----------------------------------------------------------------------------------
            #*  aeronave parando apos o pouso ?
            #*/
            if ( 'S' == self._oAtv.getStatusSolo ()):

                #** -------------------------------------------------------------------------------
                #*  nao necessita de confirmação
                #*/
                l_bConfirme = False

                #** -------------------------------------------------------------------------------
                #*/
                l_bRC = True

            #** -----------------------------------------------------------------------------------
            #*  senao, outra condição de taxi
            #*/
            else:

                #** -------------------------------------------------------------------------------
                #*  cria o dialogo "confirma o percurso"
                #*/
                l_dlg = dlgPercurso.dlgPercurso ()
                assert ( l_dlg )

                #** -------------------------------------------------------------------------------
                #*  confirma o percurso
                #*/
                l_bConfirme = l_dlg.startPanel ()

                #** -------------------------------------------------------------------------------
                #*  cria o dialogo "confirma o percurso" e confirma o percurso
                #*/
                #l_bConfirme = dlgConfirm.askConfirm ( locDefs.xTXT_Tit, "Confirma o percurso ?" )

            #** -----------------------------------------------------------------------------------
            #*  aceitou o percurso ?
            #*/
            if ( l_bConfirme ):

                #** -------------------------------------------------------------------------------
                #*  aeronave parada ? 
                #*/
                if ( 'P' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave em taxi
                    #*/
                    self._oAtv.setStatusSolo ( 'T' )

                #** -------------------------------------------------------------------------------
                #*  aeronave parada e em pane ? 
                #*/
                elif ( 'G' == self._oAtv.getStatusSolo ()):

                    #** ---------------------------------------------------------------------------
                    #*  muda o status para aeronave em taxi porem em pane
                    #*/
                    self._oAtv.setStatusSolo ( 'B' )

                #** -------------------------------------------------------------------------------
                #*/
                l_bRC = True

        #** ---------------------------------------------------------------------------------------
        #*  percurso zerado ?
        #*/
        elif (( not l_lstEtapa ) and ( self._oAtv.getSolo ())):

            #** -----------------------------------------------------------------------------------
            #*  erro, percurso invalido
            #*/
            self._msgBox.addMsg ( self._oAtv.getIdent (), "percurso invalido", glbDefs.xCOR_yellow )

        #** ---------------------------------------------------------------------------------------
        #*  oculta o percurso da aeronave
        #*/
        self._oAtv.setShowPercurso ( False )
        #l_log.info ( "setShowPercurso ( False )" )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( l_bRC )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::selectFlight
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def selectFlight ( self, f_oAtv ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::selectFlight"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  verifica parametros de entrada
        #*/
        assert ( f_oAtv )

        #** ---------------------------------------------------------------------------------------
        #*  salva aeronave selecionada
        #*/
        self._oAtv = f_oAtv

        #** ---------------------------------------------------------------------------------------
        #*  recria o menu principal
        #*/
        self.makeMenu ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** ===========================================================================================
    #*  acesso a area de dados do objeto
    #*  ===========================================================================================
    #*/

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::setMsgBox
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setMsgBox ( self, f_Val ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::setMsgBox"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  salva a message box
        #*/
        self._msgBox = f_Val

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  guiMenu::setViewAer
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    #def setViewAer ( self, f_Val ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "guiMenu::setViewAer"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  salva o viewAer
        #*/
        #self._viewAer = f_Val

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "guiMenu" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( w_logLvl )

#** ----------------------------------------------------------------------------------------------- *#
