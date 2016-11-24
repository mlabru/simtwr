#!/usr/bin/env python
# -*- coding: utf-8 -*-
#** -----------------------------------------------------------------------------------------------
#*  pyACME
#*  Copyright (c) 2008, Milton Abrunhosa
#*  -----------------------------------------------------------------------------------------------
#*  Package..: SICAD
#*  Classe...: Dijkstra's algorithm for shortest paths
#*
#*  Descricao: find shortest paths from the start vertex to all vertices nearer than or equal
#*             to the end. The input graph G is assumed to have the following representation:
#*             A vertex can be any object that can be used as an index into a dictionary.
#*             G is a dictionary, indexed by vertices. For any vertex v, G [v] is itself
#*             a dictionary, indexed by the neighbors of v.
#*             For any edge v->w, G [v][w] is the length of the edge. This is related to the
#*             representation in <http://www.python.org/doc/essays/graphs.html> where Guido van
#*             Rossum suggests representing graphs as dictionaries mapping vertices to lists of
#*             neighbors, however dictionaries of edges have many advantages over lists:
#*             they can store extra information (here, the lengths), they support fast existence
#*             tests, and they allow easy modification of the graph by edge insertion and removal.
#*             Such modifications are not needed here but are important in other graph algorithms.
#*             Since dictionaries obey iterator protocol, a graph represented as described here 
#*             could be handed without modification to an algorithm using Guido's representation.
#*             Of course, G and G[v] need not be Python dict objects; they can be any other object
#*             that obeys dict protocol, for instance a wrapper in which vertices are URLs and a
#*             call to G [v] loads the web page and finds its links.
#*             The output is a pair (D,P) where D[v] is the distance from start to v and P[v] is
#*             the predecessor of v along the shortest path from s to v.
#*             Dijkstra's algorithm is only guaranteed to work correctly when all edge lengths are
#*             positive. This code does not verify this property for all edges (only the edges seen
#*             before the end vertex is reached), but will correctly compute shortest paths even
#*             for some graphs with negative edges, and will raise an exception if it discovers
#*             that a negative edge has caused it to make a mistake.
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

#/ log4Py (logger)
#/ ------------------------------------------------------------------------------------------------
import logging

#/ 
#/ ------------------------------------------------------------------------------------------------
import priorityDictionary as priorityDictionary

#** -----------------------------------------------------------------------------------------------
#*  variaveis globais
#*  -----------------------------------------------------------------------------------------------
#*/

#** -----------------------------------------------------------------------------------------------
#*  shortestPath::Dijkstra
#*  -----------------------------------------------------------------------------------------------
#*  determine the path to a file in the data directory
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*/
def Dijkstra ( G, start, end = None ):

    #/ nome do metodo (logger)
    #/ --------------------------------------------------------------------------------------------
    #l_szMetodo = "shortestPath::Dijkstra"


    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #l_log = logging.getLogger ( l_szMetodo )
    #l_log.setLevel ( logging.INFO )
    #l_log.debug ( ">> " )

    #** -------------------------------------------------------------------------------------------
    #*  dictionary of final distances
    #*/
    D = {}

    #** -------------------------------------------------------------------------------------------
    #*  dictionary of predecessors
    #*/
    P = {}

    #** -------------------------------------------------------------------------------------------
    #*  estimated distance of non-final vertices
    #*/
    Q = priorityDictionary.priorityDictionary ()
    #assert ( Q )

    #** -------------------------------------------------------------------------------------------
    #*/
    Q [ start ] = 0
    
    #** -------------------------------------------------------------------------------------------
    #*/
    for v in Q:

        #** ---------------------------------------------------------------------------------------
        #*/
        D [ v ] = Q [ v ]

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( v == end ):

            #** -----------------------------------------------------------------------------------
            #*/
            break
        
        #** ---------------------------------------------------------------------------------------
        #*/
        for w in G [ v ]:

            #** -----------------------------------------------------------------------------------
            #*/
            vwLength = D [ v ] + G [ v ][ w ]
            #l_log.info ( "vwLength: " + str ( vwLength ))

            #** -----------------------------------------------------------------------------------
            #*/
            if ( w in D ):

                #** -------------------------------------------------------------------------------
                #*/
                if ( vwLength < D [ w ] ):

                    #** ---------------------------------------------------------------------------
                    #*/
                    raise ValueError, "Dijkstra: found better path to already-final vertex"

            #** -----------------------------------------------------------------------------------
            #*/
            elif (( w not in Q ) or ( vwLength < Q [ w ] )):

                #** -------------------------------------------------------------------------------
                #*/
                Q [ w ] = vwLength
                #l_log.info ( "Q [ w ]: " + str ( Q [ w ] ))

                #** -------------------------------------------------------------------------------
                #*/
                P [ w ] = v
                #l_log.info ( "P [ w ]: " + str ( P [ w ] ))
    
    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*/
    return ( D, P )
            
#** -----------------------------------------------------------------------------------------------
#*  shortestPath::shortestPath
#*  -----------------------------------------------------------------------------------------------
#*  find a single shortest path from the given start vertex to the given end vertex.
#*  -----------------------------------------------------------------------------------------------
#*  @param  DOCUMENT ME!
#*
#*  @return nenhum
#*  -----------------------------------------------------------------------------------------------
#*  @notes  (1) - The input has the same conventions as Dijkstra().
#*  @notes  (2) - The output is a list of the vertices in order along the shortest path.
#*  -----------------------------------------------------------------------------------------------
#*/
def shortestPath ( G, start, end ):

    #/ nome do metodo (logger)
    #/ --------------------------------------------------------------------------------------------
    #l_szMetodo = "shortestPath::shortestPath"


    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #l_log = logging.getLogger ( l_szMetodo )
    #l_log.setLevel ( logging.INFO )
    #l_log.debug ( ">> " )

    #** -------------------------------------------------------------------------------------------
    #*/
    D, P = Dijkstra ( G, start, end )
    #l_log.info ( "D: " + str ( D ))
    #l_log.info ( "P: " + str ( P ))

    #** -------------------------------------------------------------------------------------------
    #*/
    Path = []
    #l_log.info ( "Path: " + str ( Path ))

    #** -------------------------------------------------------------------------------------------
    #*/
    while ( True ):

        #** ---------------------------------------------------------------------------------------
        #*/
        Path.append ( end )
        #l_log.info ( "Path: " + str ( Path ))

        #** ---------------------------------------------------------------------------------------
        #*/
        if ( end == start ):

            break

        #** ---------------------------------------------------------------------------------------
        #*/
        end = P [ end ]
        #l_log.info ( "end: " + str ( end ))

    #** -------------------------------------------------------------------------------------------
    #*/
    Path.reverse ()
    #l_log.info ( "Path: " + str ( Path ))

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    #l_log.debug ( "<< " )

    #** -------------------------------------------------------------------------------------------
    #*/
    return ( Path )
    
#** -----------------------------------------------------------------------------------------------
#*/
logger = logging.getLogger ( "shortestPath" )

#** -----------------------------------------------------------------------------------------------
#*/
logger.setLevel ( logging.INFO )

#** -----------------------------------------------------------------------------------------------
#*  this is the bootstrap process
#*/
if ( '__main__' == __name__ ):

    #** -------------------------------------------------------------------------------------------
    #*  m.poirot logger
    #*/
    logging.basicConfig ()

    #** -------------------------------------------------------------------------------------------
    #*
    G = { 1 : { 2 : 10., 4 : 5. },
          2 : { 3 :  1., 4 : 2. },
          3 : { 5 :  4. },
          4 : { 2 :  3., 3 : 9., 5 : 2. },
          5 : { 1 :  7., 3 : 6. }
        }

    #** -------------------------------------------------------------------------------------------
    #*
    for x in G:
    
        #l_log.info ( "key: " + str ( x ) + " value: " + str ( G [ x ] ))

        for y in G [ x ]: 

            #l_log.info ( "key: " + str ( y ) + " value: " + str ( G [ x ][ y ] ))

            #l_log.info ( "distancia de: " + str ( x ) + " ate: " + str ( y ) + " = " + str ( G [ x ][ y ] ))

            pass
            
    #** -------------------------------------------------------------------------------------------
    #*
    #l_log.info ( str ( shortestPath ( G, 1, 5 )))

#** ----------------------------------------------------------------------------------------------- *#
    