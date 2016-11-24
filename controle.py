#!/usr/bin/env python2.5
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: Console
#*
#*  Descricao: this class holds the code for creating a welcome and setup screen for SiCAD.
#*             Furthermore, this class initiates the actual application classes and starts
#*             everything.
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteracao
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/???/??  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versao
#*  -----------------------------------------------------------------------------------------------
#*  start    1997/???/??  version started
#*  1.2-0.1  2008/JUN/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ Python library
#/ ------------------------------------------------------------------------------------------------
import sys

#/ log4Py
#/ ------------------------------------------------------------------------------------------------
import logging

#/ SiCAD
#/ ------------------------------------------------------------------------------------------------
sys.path.insert ( 0, "." )

#/ SiCAD / control
#/ ------------------------------------------------------------------------------------------------
import control.controlConsole as controlConsole

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  console::main
#*  -----------------------------------------------------------------------------------------------
#*  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
def main ():

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    logging.basicConfig ()

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*
    #logger = logging.getLogger ( "console" )

    #** -------------------------------------------------------------------------------------------
    #*  set verbosity to show all messages of severity >= DEBUG
    #*
    #logger.setLevel ( logging.DEBUG )

    #** -------------------------------------------------------------------------------------------
    #*  instancia o controle
    #*
    l_cc = controlConsole.controlConsole ()
    assert ( l_cc )

    #** -------------------------------------------------------------------------------------------
    #*  ativa o controle
    #*
    l_cc.run ()

#** -----------------------------------------------------------------------------------------------
#*  this is the bootstrap process
#*/
if ( '__main__' == __name__ ):

    #** -------------------------------------------------------------------------------------------
    #*  try to load psyco
    #*/
    try:

        #** ---------------------------------------------------------------------------------------
        #*  import Psyco if available
        #*/
        import psyco

        #** ---------------------------------------------------------------------------------------
        #*/
        psyco.log ()
        psyco.full ()
        #psyco.profile ( 0.05 )

    #** -------------------------------------------------------------------------------------------
    #*  psyco not found ?
    #*/
    except ImportError:

        #** ---------------------------------------------------------------------------------------
        #*  get Psyco !
        #*/
        print "Get psyco !"

    #** -------------------------------------------------------------------------------------------
    #*  run application
    #*/
    main ()

#** ----------------------------------------------------------------------------------------------- *#
