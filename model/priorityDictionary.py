#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SiCAD
#*  Classe...: priorityDictionary
#*
#*  Descricao: priority dictionary using binary heaps
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Alteracao
#*  -----------------------------------------------------------------------------------------------
#*  correa   1997/fev/12  version started
#*  mlabru   2008/nov/20  version started
#*  -----------------------------------------------------------------------------------------------
#*  Detalhes de Versao
#*  -----------------------------------------------------------------------------------------------
#*  start    1997/fev/12  version started
#*  2.08.11  2008/nov/20  DOCUMENT ME!
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  includes
#*  -----------------------------------------------------------------------------------------------
#*/

#/ Python library
#/ ------------------------------------------------------------------------------------------------
from __future__ import generators

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  priorityDictionary::priorityDictionary
#*  -----------------------------------------------------------------------------------------------
#*  the object holding all information concerning a priorityDictionary
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
class priorityDictionary ( dict ):

    #** -------------------------------------------------------------------------------------------
    #*  priorityDictionary::__init__
    #*  -------------------------------------------------------------------------------------------
    #*  initialize priorityDictionary by creating binary heap of pairs (value, key).
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  changing or removing a dict entry will not remove the old pair from the heap until
    #*          it is found by smallest() or until the heap is rebuilt.
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __init__ ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "priorityDictionary::__init__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        self.__heap = []

        #** ---------------------------------------------------------------------------------------
        #*/
        dict.__init__ ( self )

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  priorityDictionary::smallest
    #*  -------------------------------------------------------------------------------------------
    #*  find smallest item after removing deleted items from heap
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def smallest ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "priorityDictionary::smallest"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( 0 == len ( self )):

            #** -----------------------------------------------------------------------------------
            #*/
            raise IndexError, "smallest of empty priorityDictionary"

        #** ---------------------------------------------------------------------------------------
        #*/
        heap = self.__heap

        #** ---------------------------------------------------------------------------------------
        #*/
        while (( heap [ 0 ][ 1 ] not in self ) or ( self [ heap [ 0 ][ 1 ]] != heap [ 0 ][ 0 ] )):

            #** -----------------------------------------------------------------------------------
            #*/
            lastItem = heap.pop ()

            #** -----------------------------------------------------------------------------------
            #*/
            insertionPoint = 0

            #** -----------------------------------------------------------------------------------
            #*/
            while ( True ):

                #** -------------------------------------------------------------------------------
                #*/
                smallChild = 2 * insertionPoint + 1

                #** -------------------------------------------------------------------------------
                #*/
                if (( smallChild + 1 < len ( heap )) and ( heap [ smallChild ] > heap [ smallChild + 1 ] )):

                    #** ---------------------------------------------------------------------------
                    #*/
                    smallChild += 1

                #** -------------------------------------------------------------------------------
                #*/
                if (( smallChild >= len ( heap )) or ( lastItem <= heap [ smallChild ] )):

                    #** ---------------------------------------------------------------------------
                    #*/
                    heap [ insertionPoint ] = lastItem

                    #** ---------------------------------------------------------------------------
                    #*/
                    break

                #** -------------------------------------------------------------------------------
                #*/
                heap [ insertionPoint ] = heap [ smallChild ]

                #** -------------------------------------------------------------------------------
                #*/
                insertionPoint = smallChild

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( heap [ 0 ][ 1 ] )

    #** -------------------------------------------------------------------------------------------
    #*  priorityDictionary::__iter__
    #*  -------------------------------------------------------------------------------------------
    #*  Create destructive sorted iterator of priorityDictionary
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __iter__ ( self ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "priorityDictionary::__iter__"


        #** ---------------------------------------------------------------------------------------
        #*  __iter__::iterfn
        #*  ---------------------------------------------------------------------------------------
        #*  Create destructive sorted iterator of priorityDictionary
        #*  ---------------------------------------------------------------------------------------
        #*  @param  DOCUMENT ME!
        #*
        #*  @return nenhum
        #*  ---------------------------------------------------------------------------------------
        #*/
        def iterfn ():

            #/ nome do metodo (logger)
            #/ ------------------------------------------------------------------------------------
            #l_szMetodo = "__iter__::iterfn"


            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log = logging.getLogger ( l_szMetodo )
            #l_log.setLevel ( logging.INFO )
            #l_log.debug ( ">> " )

            #** -----------------------------------------------------------------------------------
            #*/
            while ( len ( self ) > 0 ):

                #** -------------------------------------------------------------------------------
                #*/
                x = self.smallest ()

                #** -------------------------------------------------------------------------------
                #*/
                yield x

                #** -------------------------------------------------------------------------------
                #*/
                del self [ x ]

            #** -----------------------------------------------------------------------------------
            #*  m.poirot logger
            #*/
            #l_log.debug ( "<< " )

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
        return ( iterfn ())

    #** -------------------------------------------------------------------------------------------
    #*  priorityDictionary::__setitem__
    #*  -------------------------------------------------------------------------------------------
    #*  change value stored in dictionary and add corresponding pair to heap
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*  @notes  rebuilds the heap if the number of deleted items grows too large, to avoid memory
    #*          leakage
    #*  -------------------------------------------------------------------------------------------
    #*/
    def __setitem__(self,key,val):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "priorityDictionary::__setitem__"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        dict.__setitem__ ( self, key, val )

        #** ---------------------------------------------------------------------------------------
        #*/
        heap = self.__heap

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( len ( heap ) > 2 * len ( self )):

            #** -----------------------------------------------------------------------------------
            #*/
            self.__heap = [ ( v, k ) for k, v in self.iteritems () ]

            #** -----------------------------------------------------------------------------------
            #*  builtin sort likely faster than O(n) heapify
            #*/
            self.__heap.sort ()

        #** ---------------------------------------------------------------------------------------
        #*/
        else:

            #** -----------------------------------------------------------------------------------
            #*/
            newPair = ( val, key )

            #** -----------------------------------------------------------------------------------
            #*/
            insertionPoint = len ( heap )

            #** -----------------------------------------------------------------------------------
            #*/
            heap.append ( None )

            #** -----------------------------------------------------------------------------------
            #*/
            while (( insertionPoint > 0 ) and ( newPair < heap [ ( insertionPoint - 1 ) // 2 ] )):

                #** -------------------------------------------------------------------------------
                #*/
                heap [ insertionPoint ] = heap [ ( insertionPoint - 1 ) // 2 ]

                #** -------------------------------------------------------------------------------
                #*/
                insertionPoint = ( insertionPoint - 1 ) // 2

            #** -----------------------------------------------------------------------------------
            #*/
            heap [ insertionPoint ] = newPair

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*  priorityDictionary::setdefault
    #*  -------------------------------------------------------------------------------------------
    #*  reimplement setdefault to call our customized __setitem__
    #*  -------------------------------------------------------------------------------------------
    #*  @param  DOCUMENT ME!
    #*
    #*  @return nenhum
    #*  -------------------------------------------------------------------------------------------
    #*/
    def setdefault ( self, key, val ):

        #/ nome do metodo (logger)
        #/ ----------------------------------------------------------------------------------------
        #l_szMetodo = "priorityDictionary::setdefault"


        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( logging.INFO )
        #l_log.debug ( ">> " )

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( key not in self ):

            #** -----------------------------------------------------------------------------------
            #*/
            self [ key ] = val

        #** ---------------------------------------------------------------------------------------
        #*  m.poirot logger
        #*/
        #l_log.debug ( "<< " )

        #** ---------------------------------------------------------------------------------------
        #*/
        return ( self [ key ] )

#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "priorityDictionary" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.DEBUG )

#** -----------------------------------------------------------------------------------------------
#*  this is the bootstrap process
#*/
#if ( '__main__' == __name__ ):

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #logging.basicConfig ()

#** ----------------------------------------------------------------------------------------------- *#
        