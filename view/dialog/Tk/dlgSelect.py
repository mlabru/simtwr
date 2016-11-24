#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: dlgSelect
#*
#*  Descrição: da inicio ao sistema, inicializar todas as variaveis globais utilizadas no sistema
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteração
#*  -----------------------------------------------------------------------------------------------
#*  mlabru   2008/jun/20  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versão
#*  -----------------------------------------------------------------------------------------------
#*  start    2008/jun/20  version started
#*  1.2-0.1  2008/jun/20  DOCUMENT ME!
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

#/ Tkinter (gui library)
#/ ------------------------------------------------------------------------------------------------
import Tkinter

#/ SiCAD / view
#/ ------------------------------------------------------------------------------------------------
import view.dialog.Tk.tkDialogs as tkDialogs

#** -----------------------------------------------------------------------------------------------
#*  variáveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#/ logging level
#/ ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

#** -----------------------------------------------------------------------------------------------
#*  dlgSelect::dlgSelect
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/
class dlgSelect ( tkDialogs.tkDialogs ):

    #** -------------------------------------------------------------------------------------------
    #*  dlgSelect::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self, f_title, f_prompt, f_lstOpc ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "dlgSelect::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  indice de opções
        #*/
        self._szPrompt = f_prompt
        assert ( self._szPrompt )

        #** ---------------------------------------------------------------------------------------
        #*  indice de opções
        #*/
        self._iOpc = None

        #** ---------------------------------------------------------------------------------------
        #*  lista de opções
        #*/
        self._lstOpc = f_lstOpc
        assert ( self._lstOpc )

        #** ---------------------------------------------------------------------------------------
        #*  lista de widgets
        #*/
        self._wOpc = [ x for x in xrange ( len ( f_lstOpc )) ]
        assert ( self._wOpc )

        #** ---------------------------------------------------------------------------------------
        #*  inicia a superclass
        #*/
        tkDialogs.tkDialogs.__init__ ( self, f_title )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  dlgSelect::getResult
    #*  -------------------------------------------------------------------------------------------
    #*  obtem o campo de entrada de dados convertido para inteiro
    #*  -------------------------------------------------------------------------------------------
    #*  @param  nenhum
    #*
    #*  @return o campo de entrada de dados convertido para inteiro
    #*  -------------------------------------------------------------------------------------------
    #*/
    def getResult ( self ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "dlgSelect::getResult"


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
        #*  retorna o campo de entrada de dados e o flag Ok
        #*/
        return ( self._bOk, self._iOpc.get ())

    #** -------------------------------------------------------------------------------------------
    #*  dlgSelect::makeBody
    #*  -------------------------------------------------------------------------------------------
    #*  DOCUMENT ME!
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def makeBody ( self, f_frmM ):

        #/ nome do método (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "dlgSelect::makeBody"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*  labels
        #*/
        l_lbl1 = Tkinter.Label ( f_frmM, font = "{MS Sans Serif} 10",
                                         text = self._szPrompt )
        l_lbl1.grid ( column = 1, row = 1, columnspan = 2, sticky = "news" )

        #** ---------------------------------------------------------------------------------------
        #*  frame opções
        #*/
        l_frmCabs = Tkinter.Frame ( f_frmM, bd = 2 )
        l_frmCabs.pack ()
        l_frmCabs.grid ( column = 1, row = 2, columnspan = 2, sticky = "news" )

        #** ---------------------------------------------------------------------------------------
        #*  prepara variavel de resposta
        #*/
        self._iOpc = Tkinter.IntVar ()

        #** ---------------------------------------------------------------------------------------
        #*  percorre a lista de opções...
        #*/
        for l_iOpc in xrange ( len ( self._lstOpc )):

            #** -----------------------------------------------------------------------------------
            #*  cria os radio buttons
            #*/
            self._wOpc [ l_iOpc ] = Tkinter.Radiobutton ( l_frmCabs,
                                                          value = l_iOpc,
                                                          variable = self._iOpc,
                                                          text = self._lstOpc [ l_iOpc ] )
            self._wOpc [ l_iOpc ].pack ()

        #** ---------------------------------------------------------------------------------------
        #*  seleciona o primeiro
        #*/
        self._wOpc [ 0 ].select ()

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

#** ===============================================================================================
#*  convenience dialogues
#*  ===============================================================================================
#*/

#** -----------------------------------------------------------------------------------------------
#*  dlgSelect::askList
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
def askList ( f_title, f_prompt, f_list, **kw ):

    #/ nome do método (logger)
    #/ --------------------------------------------------------------------------------------------
    #l_szMetodo = "dlgSelect::askList"


    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #l_log = logging.getLogger ( l_szMetodo )
    #l_log.setLevel ( w_logLvl )
    #l_log.debug ( ">> " )

    #** -------------------------------------------------------------------------------------------
    #*/
    l_dlg = apply ( dlgSelect, ( f_title, f_prompt, f_list ), kw )
    assert ( l_dlg )

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*/
    return ( l_dlg.getResult ())

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "dlgSelect" )

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
    #*/
    b, v = askList ( "@T@", u"Teste de Seleção:", [ "10", "28" ] )
 
    #** -------------------------------------------------------------------------------------------
    #*/
    print b
    print v

#** ----------------------------------------------------------------------------------------------- *#
