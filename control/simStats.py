#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------------------
# pSiPAR
# Copyright (c) 2008, Milton Abrunhosa
# -----------------------------------------------------------------------------------------------
# Package..: pSiPAR
# Classe...: Piloto
#
# Descrição: this class holds the code to keep score during the game. It
#            uses the game engine's list of flights to calculate no. of
#            NearMisses, no. of commands, and other parameters
# -----------------------------------------------------------------------------------------------
# Detalhes de Alteração
# -----------------------------------------------------------------------------------------------
# mlabru   2008/jun/20  version started
# -----------------------------------------------------------------------------------------------
# Detalhes de Versão
# -----------------------------------------------------------------------------------------------
# start    2008/jun/20  version started
# 1.0-0.1  2008/jun/20  DOCUMENT ME!
# -----------------------------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------------------------
# includes
# -----------------------------------------------------------------------------------------------
#

# Python library
# ------------------------------------------------------------------------------------------------
#import string

# log4Py (logger)
# ------------------------------------------------------------------------------------------------
import logging

# -----------------------------------------------------------------------------------------------
# variáveis globais
# -----------------------------------------------------------------------------------------------
#

# logging level
# ------------------------------------------------------------------------------------------------
#w_logLvl = logging.INFO
w_logLvl = logging.DEBUG

# -----------------------------------------------------------------------------------------------
# simStats::simStats
# -----------------------------------------------------------------------------------------------
# keeps score during the game. The score is calculated based on a number of parameters, e.g. no.
# of near misses, no. of commands given, etc
# -----------------------------------------------------------------------------------------------
#
class simStats:

    # -------------------------------------------------------------------------------------------
    # simStats::__init__
    # -------------------------------------------------------------------------------------------
    # initializes the display
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def __init__ ( self, numPixels = 600.0, numMiles = 50.0, noFlights = 0 ):

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::__init__"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        #
        # Calculate the buffer distance
        # equals numPix / numMiles * 5 miles
        self.safetyBuffer = numPixels / numMiles * 5
        self.crashZone = numPixels / numMiles * .4

        self.noNearMiss = 0       # Holds the number of near misses
        self.noCollision = 0      # Holds the number of collisions
        self.noCommands = 0       # Holds the number of commands given
        self.noMissHandOff = 0    # No. of missed hand-off's

        self.noFlights = noFlights
        self.noProcFlights = 0    # No. of processed flights
        self.noHandOff = 0        # Successfull hand.off's
        self.totalFlightTime = 0  # Total time flights spend in the air.

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::drawAirports
    # -------------------------------------------------------------------------------------------
    # draws the airports and the beacons from ge's beacon list
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def checkProximity(self, flight1, flight2):
        """Calculates the proximity of the flights in the flight pair.

        This should be run everytime new positions are calculated by the
        game engine. If two flights are within 5 miles horizontically and
        at the same level or at the same position and (above 29000 ft)
        within 2000 ft or (under 29000 ft) within 1000 ft vertically a
        danger situation has occured.
        This code also gives proximity warnings to the user.
        """

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::__init__"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        # lista de aeronaves ativas
        #
        # *** This is basically a join of all flights and the gaussian distance
        # *** calculated for all pairs.
        pos1 = flight1.getPos()
        pos2 = flight2.getPos()

        # Calc horizontal distance
        hDist = ( (pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2 )**0.5
        vDist = abs( pos1[2]-pos2[2] )


        if vDist < 100 and hDist < self.crashZone:
            # The planes have crashed
            self.noCollision = self.noCollision + 1
            return 2

        # Check for near miss
        if (pos1[2] < 29000 or pos2[2] < 29000):
            if vDist < 1000 and hDist < self.safetyBuffer:
                return 1
        else:
            if vDist < 2000 and hDist < self.safetyBuffer:
                return 1

        return 0

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::drawAirports
    # -------------------------------------------------------------------------------------------
    # draws the airports and the beacons from ge's beacon list
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def missHandoff(self):

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::__init__"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        # lista de aeronaves ativas
        #
        self.noMissHandOff = self.noMissHandOff + 1

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::drawAirports
    # -------------------------------------------------------------------------------------------
    # draws the airports and the beacons from ge's beacon list
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def handOff(self, flightX, currentTime, autoHandOff):
        """Code to be run when a handoff is successfully completed."""

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::__init__"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        # lista de aeronaves ativas
        #
        # Calculate time
        self.totalFlightTime = self.totalFlightTime + (currentTime - flightX.getTime())
        self.totalFlightTime = self.totalFlightTime - flightX.pauseTime

        if autoHandOff:
            self.noMissHandOff = self.noMissHandOff + 1
        else:
            self.noHandOff = self.noHandOff + 1

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::drawAirports
    # -------------------------------------------------------------------------------------------
    # draws the airports and the beacons from ge's beacon list
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def flightDrop(self, flightX, currentTime):

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::__init__"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        # this flight is somehow dead - most likely dropped off the side of the scope
        #
        self.totalFlightTime = self.totalFlightTime + (currentTime - flightX.getTime())
        self.totalFlightTime = self.totalFlightTime - flightX.pauseTime


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::addAlert
    # -------------------------------------------------------------------------------------------
    # DOCUMENT ME!
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def addAlert ( self ):

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::addAlert"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        #
        self.noNearMiss += 1

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::addCommand
    # -------------------------------------------------------------------------------------------
    # DOCUMENT ME!
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def addCommand ( self ):

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::addCommand"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        # lista de aeronaves ativas
        #
        self.noCommands += 1

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

    # -------------------------------------------------------------------------------------------
    # simStats::printsimStats
    # -------------------------------------------------------------------------------------------
    # prints the score of the player
    # -------------------------------------------------------------------------------------------
    # @param  DOCUMENT ME!
    #
    # @return nenhum
    # -------------------------------------------------------------------------------------------
    #
    def printsimStats ( self ):

        # nome do método (logger)
        # ----------------------------------------------------------------------------------------
        #l_szMetodo = "simStats::printsimStats"


        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log = logging.getLogger ( l_szMetodo )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">> " )

        # ---------------------------------------------------------------------------------------
        #
#       print ''
#       print 'Succesful hand-off\'s    ' + string.rjust(str(self.noHandOff),5)
#       print 'Processed flights       ' + string.rjust(str(self.noProcFlights),5)
#       print 'Total no. of flights    ' + string.rjust(str(self.noFlights),5)
#       print ''
#       print 'Near Misses             ' + string.rjust(str(self.noNearMiss),5)
#       print 'Collisions              ' + string.rjust(str(self.noCollision),5)
#       print 'Commands given          ' + string.rjust(str(self.noCommands),5)
#       print 'Missed Hand-off\'s       ' + string.rjust(str(self.noMissHandOff),5)
#       print 'Total time of flights   ' + string.rjust(str(self.totalFlightTime / 1000),5)
#       print ''
        pass

        # ---------------------------------------------------------------------------------------
        # m.poirot logger
        #
        #l_log.debug ( "<< " )

# -----------------------------------------------------------------------------------------------
#
logger = logging.getLogger ( "simStats" )

# -----------------------------------------------------------------------------------------------
#
logger.setLevel ( w_logLvl )

# ----------------------------------------------------------------------------------------------- *#
