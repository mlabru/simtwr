#!/usr/bin/env python2.5
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: configPiloto
#*
#*  Descricao: da inicio ao sistema, inicializar todas as variaveis
#*             globais utilizadas no sistema
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteracao
#*  -----------------------------------------------------------------------------------------------
#*  mlabru   2008/???/??  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versao
#*  -----------------------------------------------------------------------------------------------
#*  start    2008/???/??  version started
#*  1.2-0.1  2008/JUN/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  
#*  -----------------------------------------------------------------------------------------------
#*/
if ( '__main__' == __name__ ):

    #/ Python Library
    #/ --------------------------------------------------------------------------------------------
    import sys

    sys.path.insert ( 0, ".." )

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ pyGame (biblioteca grafica)
#/ ------------------------------------------------------------------------------------------------
#import pygame

#/ Tkinter (gui library)
#/ ------------------------------------------------------------------------------------------------
import Tkinter
import tkFileDialog

#/ SiCAD / model
#/ ------------------------------------------------------------------------------------------------
import model.data as data
import model.simConfig as simConfig

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.dlgConfig as dlgConfig
import view.tkUtils as tkUtils

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  configPiloto::configPiloto
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class configPiloto ( dlgConfig.dlgConfig ):

    #** -------------------------------------------------------------------------------------------
    #*  configPiloto::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self ):

        #/ nome do metodo (logger)
        #/ -----------------------------------------------------------------------------------------
        #l_szMetodo = "configPiloto::__init__"


        #** ----------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger = logging.getLogger ( l_szMetodo )
        #logger.setLevel ( logging.INFO )
        #logger.debug ( ">> " )

        #** ----------------------------------------------------------------------------------------
        #*  inicia a superclass
        #*/
        dlgConfig.dlgConfig.__init__ ( self )

        #** ----------------------------------------------------------------------------------------
        #*  filename entry field
        #*/
        self._txtFileName = 0

        #** ----------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  configPiloto::criaWinCfg
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def criaWinCfg ( self, f_tkRoot ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "configPiloto::criaWinCfg"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger = logging.getLogger ( l_szMetodo )
        #logger.setLevel ( logging.INFO )
        #logger.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  widgets initialization
        #*/
        self._frmM = Tkinter.Frame ( f_tkRoot, bg = "blue" )
        self._frmM.pack ()

        #** ---------------------------------------------------------------------------------------
        #*  labels
        #*/
        l_lbl1 = Tkinter.Label ( self._frmM, background = "#0000ff",
                                             font = "{MS Sans Serif} 20",
                                             foreground = "#ffff00",
                                             text = simConfig.xTXT_Tit )
        l_lbl1.grid ( row = 1, column = 0, columnspan = 4 )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_lbl2 = Tkinter.Label ( self._frmM, background = "#0000ff",
                                             font = "{MS Sans Serif} 16",
                                             foreground = "#ffff00",
                                             text = u"Simulador para Servi\u00E7o de" )
        l_lbl2.grid ( row = 2, column = 0, columnspan = 4 )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_lbl3 = Tkinter.Label ( self._frmM, background = "#0000ff",
                                             font = "{MS Sans Serif} 16",
                                             foreground = "#ffff00",
                                             text = u"Controle de Aer\u00F3dromos," )
        l_lbl3.grid ( row = 3, column = 0, columnspan = 4 )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_lbl4 = Tkinter.Label ( self._frmM, background = "#0000ff",
                                             font = "{MS Sans Serif} 16",
                                             foreground = "#ffff00",
                                             text = "Apoiado por Computadores" )
        l_lbl4.grid ( row = 4, column = 0, columnspan = 4 )

        #** ---------------------------------------------------------------------------------------
        #*/
        l_lbl6 = Tkinter.Label ( self._frmM, background = "#0000ff",
                                             font = "{MS Sans Serif} 14",
                                             foreground = "#ffff00",
                                             text = "(C) ITA - ICEA 2009" )
        l_lbl6.grid ( row = 6, column = 0, columnspan = 4 )

        #** ---------------------------------------------------------------------------------------
        #*  frame select
        #*/
        l_frmSelect = Tkinter.Frame ( self._frmM, bd = 2, relief = Tkinter.RAISED )
        l_frmSelect.pack ()
        l_frmSelect.grid ( column = 0, row = 8, columnspan = 4, sticky = "news" )

        #** ---------------------------------------------------------------------------------------
        #*  text entry (numero do exercicio)
        #*/
        fileButton = Tkinter.Button ( l_frmSelect, width = 16, text = "Navegue", command = self.browseForExercicio )
        fileButton.pack ( side = Tkinter.LEFT, padx = 5, pady = 3 )

        self._txtFileName = Tkinter.Entry ( l_frmSelect, width = 19 )
        self._txtFileName.insert ( 0, "Escolha um exercicio" )
        self._txtFileName.pack ( side = Tkinter.RIGHT, padx = 5 )

        #  self._entry_1.configure ( invalidcommand  = self._entry_1_invalidcommand )
        #  self._entry_1.configure ( validatecommand = self._entry_1_validatecommand )
        #  self._entry_1.configure ( xscrollcommand  = self._entry_1_xscrollcommand )

        #** ---------------------------------------------------------------------------------------
        #*  frame canal
        #*/
        l_frmChannel = Tkinter.Frame ( self._frmM, bd = 2, relief = Tkinter.RAISED )
        l_frmChannel.pack ()
        l_frmChannel.grid ( column = 0, row = 9, columnspan = 4, sticky = "news" )

        #** ---------------------------------------------------------------------------------------
        #*  label canal
        #*/
        #l_lbl7 = Tkinter.Label ( l_frmChannel, width = 16, text = "Canal" )
        #l_lbl7.pack ( side = Tkinter.LEFT, padx = 5 )

        #** ---------------------------------------------------------------------------------------
        #*  button (Canal) (Tkinter.DISABLED)
        #*/
        l_lbl7 = Tkinter.Button ( l_frmChannel, width = 16, text = "Canal", state = Tkinter.NORMAL )
        l_lbl7.pack ( side = Tkinter.LEFT, padx = 5 )

        #** ---------------------------------------------------------------------------------------
        #*  listbox canal
        #*/
        self._lbxCanal = Tkinter.Listbox ( l_frmChannel, height = 2, width = 16 )
        self._lbxCanal.pack ( side = Tkinter.RIGHT, fill = Tkinter.Y, padx = 5 )

        #** ---------------------------------------------------------------------------------------
        #*  listbox populate
        #*/
        for l_iI in xrange ( 3, 93 ): 

            self._lbxCanal.insert ( Tkinter.END, l_iI )

        #** ---------------------------------------------------------------------------------------
        #*  scrollbar canal
        #*/
        l_scl = Tkinter.Scrollbar ( l_frmChannel, command = self._lbxCanal.yview )
        l_scl.pack ( side = Tkinter.RIGHT, fill = Tkinter.Y, padx = 5 )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._lbxCanal.configure ( yscrollcommand = l_scl.set )
        self._lbxCanal.selection_set ( 0 )

        #** ---------------------------------------------------------------------------------------
        #*  frame buttons
        #*/
        l_frmButtons = Tkinter.Frame ( self._frmM, bd = 2, relief = Tkinter.RAISED )
        l_frmButtons.pack ()
        l_frmButtons.grid ( column = 0, row = 10, columnspan = 4, sticky = "news" )

        #** ---------------------------------------------------------------------------------------
        #*  button (Ok)
        #*/
        self._btnOk = Tkinter.Button ( l_frmButtons, width = 16, text = "Ok", state = Tkinter.DISABLED, command = self.doOk )
        self._btnOk.pack ( side = Tkinter.LEFT, padx = 5, pady = 3 )

        #** ---------------------------------------------------------------------------------------
        #*  button (Cancel)
        #*/
        l_btnCancel = Tkinter.Button ( l_frmButtons, width = 16, text = "Cancel", command = self.doCancel )
        l_btnCancel.pack ( side = Tkinter.RIGHT, padx = 5, pady = 3 )

        #** ---------------------------------------------------------------------------------------
        #*  resize behavior (self._frmM)
        #*/
        self._frmM.grid_rowconfigure ( 0, minsize = 20 )
        self._frmM.grid_rowconfigure ( 1, minsize = 40 )
        self._frmM.grid_rowconfigure ( 2, minsize = 40 )
        self._frmM.grid_rowconfigure ( 3, minsize = 40 )
        self._frmM.grid_rowconfigure ( 4, minsize = 40 )
        self._frmM.grid_rowconfigure ( 5, minsize = 20 )
        self._frmM.grid_rowconfigure ( 6, minsize = 40 )
        self._frmM.grid_rowconfigure ( 7, minsize = 20 )

        #** ---------------------------------------------------------------------------------------
        #*/
        f_tkRoot.update ()

        #** ---------------------------------------------------------------------------------------
        #*  center in screen
        #*/
        tkUtils.center_toplevel_in_screen ( f_tkRoot )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  configPiloto::browseForExercicio
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def browseForExercicio ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "configPiloto::browseForExercicio"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger = logging.getLogger ( l_szMetodo )
        #logger.setLevel ( logging.INFO )
        #logger.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  monta o diretorio inicial para busca do exercicio
        #*/
        l_szDir = data.filepath ( simConfig.xDIR_EXE )
        #logger.info ( "Dir for search: " + l_szDir )

        #** ---------------------------------------------------------------------------------------
        #*  browse for an exercicio
        #*/
        l_szFileName = tkFileDialog.askopenfilename ( initialdir = l_szDir,
                                                      title = "Escolha um exercicio" )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._txtFileName.delete ( 0, Tkinter.END )
        self._txtFileName.insert ( 0, l_szFileName )

        #logger.info ( l_szFileName + " prepared for loading" )

        #** ---------------------------------------------------------------------------------------
        #*/
        self._btnOk.configure ( state = Tkinter.NORMAL )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  configPiloto::startConfigPanel
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def startConfigPanel ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "configPiloto::startConfigPanel"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger = logging.getLogger ( l_szMetodo )
        #logger.setLevel ( logging.INFO )
        #logger.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  load Tkinter
        #*/
        l_tkRoot = Tkinter.Tk ()
        l_tkRoot.configure ( bg = "blue" )

        #** ---------------------------------------------------------------------------------------
        #*  terminal de pilotagem ?
        #*/
        l_tkRoot.title ( simConfig.xTXT_Tit + " [Piloto]" )

        #** ---------------------------------------------------------------------------------------
        #*  cria a janela de configuracao
        #*/
        self.criaWinCfg ( l_tkRoot )

        #** ---------------------------------------------------------------------------------------
        #*  processa o dialogo
        #*/
        l_tkRoot.mainloop ()

        #** ---------------------------------------------------------------------------------------
        #*  obtem o nome do arquivo de exercicio selecionado
        #*/
        l_szFileName = self._txtFileName.get ()
        #logger.info ( l_szFileName + " eh o arquivo a abrir..." )

        #** ---------------------------------------------------------------------------------------
        #*  canal selecionado ?
        #*/
        if ( self._lbxCanal.curselection ()):

            #** -----------------------------------------------------------------------------------
            #*  salva o canal selecionado
            #*/
            l_iCanal = int ( self._lbxCanal.curselection () [ 0 ] ) + 3

        #** ---------------------------------------------------------------------------------------
        #*  senao, nenhuma selecao
        #*/
        else: 

            #** -----------------------------------------------------------------------------------
            #*  canal default
            #*/
            l_iCanal = 3

        #logger.info ( "Canal de dados: " + str ( l_iCanal ))

        #** ---------------------------------------------------------------------------------------
        #*  unload Tkinter
        #*/
        l_tkRoot.destroy ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #logger.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*  Ok ?  
        #*/
        if ( self._bOk ):

            #** -----------------------------------------------------------------------------------
            #*/
            return ( self._bOk, l_szFileName, l_iCanal )

        #** ---------------------------------------------------------------------------------------
        #*  senao, usuario cancelou
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            return ( self._bOk, None, -1 )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "configPiloto" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** -----------------------------------------------------------------------------------------------
#*  this is the bootstrap process
#*/
if ( '__main__' == __name__ ):

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    logging.basicConfig ()

    #** -------------------------------------------------------------------------------------------
    #*/
    x = configPiloto ()
    y, z, a = x.startConfigPanel () 
 
    #** -------------------------------------------------------------------------------------------
    #*/
    print x
    print y, z, a

#** ----------------------------------------------------------------------------------------------- *#
