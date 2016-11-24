# !/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# pSiPAR
# Copyright (c) 2008-2011, Milton Abrunhosa
# -------------------------------------------------------------------------------------------------
# Package..: control
# Classe...: configManager
#
# Descrição: DOCUMENT ME!
# -------------------------------------------------------------------------------------------------
# Detalhes de Versão
# -------------------------------------------------------------------------------------------------
# mlabru   2008/fev  2.0  versão para Linux (2D)
# mlabru   2011/fev  3.0  versão para Linux (3D)
# -------------------------------------------------------------------------------------------------
# Detalhes de Alteração
# -------------------------------------------------------------------------------------------------
# mlabru   2008/jun  2.0  version started
# mlabru   2009/jun  2.09 release 09
# mlabru   2011/jan  2.11 release 11
# mlabru   2011/fev  3.0  version started
# -------------------------------------------------------------------------------------------------

# < imports >--------------------------------------------------------------------------------------

# python library
import ConfigParser
import os

# log4Py (logger)
import logging

# pSiPAR / model
import model.data as data
import model.glbDefs as glbDefs
import model.locDefs as locDefs

# < variáveis globais >-----------------------------------------------------------------------------

# logging level
w_logLvl = logging.ERROR

# < class configManager >--------------------------------------------------------------------------

class configManager ( object ):

    # ---------------------------------------------------------------------------------------------
    # configManager::__init__
    # ---------------------------------------------------------------------------------------------
    def __init__ ( self, f_fdCnfg ):

        """
        inicia o gerente de configuração.

        @param  f_fdCnfg : full path do arquivo de configuração.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::__init__" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # cria o parser par o arquivo de configuração
        self._cp = ConfigParser.SafeConfigParser ()
        assert ( self._cp )

        # abre o arquivo de configuração
        self._cp.readfp ( open ( f_fdCnfg ))

        # load cores section
        # self.loadCores ()

        # load dirs section
        self.loadDirs ()

        # load fonts section
        self.loadFonts ()

        # load rede section
        self.loadRede ()

        # load screen section
        self.loadScreen ()

        # load sounds section
        self.loadSound ()

        # load time section
        self.loadTime ()

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadCores
    # ---------------------------------------------------------------------------------------------
    def loadCores ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadCores" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_Aer = self._cp.get ( "cor", "aerodromo" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_Aer: " + str ( locDefs.xCOR_Aer ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_Congelado = self._cp.get ( "cor", "congelado" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_Congelado: " + str ( locDefs.xCOR_Congelado ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_DeclMag = self._cp.get ( "cor", "declMag" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_DeclMag: " + str ( locDefs.xCOR_DeclMag ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_FlightNo = self._cp.get ( "cor", "flightNo" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_FlightNo: " + str ( locDefs.xCOR_FlightNo ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_Messages = self._cp.get ( "cor", "messages" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_Messages: " + str ( locDefs.xCOR_Messages ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_RangeMark = self._cp.get ( "cor", "rangeMark" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_RangeMark: " + str ( locDefs.xCOR_RangeMark ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_RoseWind = self._cp.get ( "cor", "roseWind" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_RoseWind: " + str ( locDefs.xCOR_RoseWind ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_Hora = self._cp.get ( "cor", "hora" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_Hora: " + str ( locDefs.xCOR_Hora ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_Vers = self._cp.get ( "cor", "vers" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_Vers: " + str ( locDefs.xCOR_Vers ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_Header = self._cp.get ( "cor", "header" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_Header: " + str ( locDefs.xCOR_Header ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_SA = self._cp.get ( "cor", "SA" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_SA: " + str ( locDefs.xCOR_SA ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_SD = self._cp.get ( "cor", "SD" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_SD: " + str ( locDefs.xCOR_SD ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_SP = self._cp.get ( "cor", "SP" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_SP: " + str ( locDefs.xCOR_SP ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_ST = self._cp.get ( "cor", "ST" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_ST: " + str ( locDefs.xCOR_ST ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_VC = self._cp.get ( "cor", "VC" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_VC: " + str ( locDefs.xCOR_VC ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_VD = self._cp.get ( "cor", "VD" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_VD: " + str ( locDefs.xCOR_VD ))

        # load cor de fundo do aerodromo
        try:

            locDefs.xCOR_VN = self._cp.get ( "cor", "VN" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xCOR_VN: " + str ( locDefs.xCOR_VN ))

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadDirs
    # ---------------------------------------------------------------------------------------------
    def loadDirs ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadDirs" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # load aerodromos dir
        try:

            locDefs.xDIR_AER = self._cp.get ( "dir", "aer" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "locDefs.xDIR_AER: " + str ( locDefs.xDIR_AER ))

        # load data dir
        try:

            glbDefs.xDIR_DAT = self._cp.get ( "dir", "data" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_DAT: " + str ( glbDefs.xDIR_DAT ))

        # load exercicios dir
        try:

            glbDefs.xDIR_EXE = self._cp.get ( "dir", "exe" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_EXE: " + str ( glbDefs.xDIR_EXE ))

        # load fontes dir
        try:

            glbDefs.xDIR_FNT = self._cp.get ( "dir", "fnt" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_FNT: " + str ( glbDefs.xDIR_FNT ))

        # load icones dir
        try:

            glbDefs.xDIR_IMG = self._cp.get ( "dir", "img" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_IMG: " + str ( glbDefs.xDIR_IMG ))

        # load PAR's dir
        # try:

            # glbDefs.xDIR_PAR = self._cp.get ( "dir", "par" )

        # except ConfigParser.NoSectionError: pass
        # except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_PAR: " + str ( glbDefs.xDIR_PAR ))

        # load sons dir
        try:

            glbDefs.xDIR_SND = self._cp.get ( "dir", "snd" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_SND: " + str ( glbDefs.xDIR_SND ))

        # load tabelas dir
        try:

            glbDefs.xDIR_TAB = self._cp.get ( "dir", "tab" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xDIR_TAB: " + str ( glbDefs.xDIR_TAB ))

        # monta o diretorio de aerodromos
        locDefs.xDIR_AER = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, locDefs.xDIR_AER ))
        #l_log.info ( "diretorio de aerodromos: " + str ( locDefs.xDIR_AER ))

        # monta o diretorio de exercicios
        glbDefs.xDIR_EXE = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, glbDefs.xDIR_EXE ))
        #l_log.info ( "diretorio de exercicios: " + str ( glbDefs.xDIR_EXE ))

        # monta o diretorio de fontes
        glbDefs.xDIR_FNT = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, glbDefs.xDIR_FNT ))
        #l_log.info ( "diretorio de fontes: " + str ( glbDefs.xDIR_FNT ))

        # monta o diretorio de imagens
        glbDefs.xDIR_IMG = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, glbDefs.xDIR_IMG ))
        #l_log.info ( "diretorio de imagens: " + str ( glbDefs.xDIR_IMG ))

        # monta o diretorio de PAR's
        # glbDefs.xDIR_PAR = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, glbDefs.xDIR_PAR ))
        #l_log.info ( "diretorio de PAR's: " + str ( glbDefs.xDIR_PAR ))

        # monta o diretorio de sons
        glbDefs.xDIR_SND = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, glbDefs.xDIR_SND ))
        #l_log.info ( "diretorio de sons: " + str ( glbDefs.xDIR_SND ))

        # monta o diretorio de tabelas
        glbDefs.xDIR_TAB = data.filepath ( os.path.join ( glbDefs.xDIR_DAT, glbDefs.xDIR_TAB ))
        #l_log.info ( "diretorio de tabelas: " + str ( glbDefs.xDIR_TAB ))

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadFonts
    # ---------------------------------------------------------------------------------------------
    def loadFonts ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadFonts" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # load default font
        try:

            glbDefs.xFNT_None = self._cp.get ( "font", "none" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xFNT_None: " + str ( glbDefs.xFNT_None ))

        # load proportional font
        try:

            glbDefs.xFNT_VARS = self._cp.get ( "font", "vars" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xFNT_VARS: " + str ( glbDefs.xFNT_VARS ))

        # load menu font
        try:

            glbDefs.xFNT_MENU = self._cp.get ( "font", "menu" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xFNT_MENU: " + str ( glbDefs.xFNT_MENU ))

        # load monospaced font
        try:

            glbDefs.xFNT_MONO = self._cp.get ( "font", "mono" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xFNT_MONO: " + str ( glbDefs.xFNT_MONO ))

        # monta o pathname do arquivo de fonte de menu
        glbDefs.xFNT_MENU = data.filepath ( os.path.join ( glbDefs.xDIR_FNT, glbDefs.xFNT_MENU ))
        #l_log.info ( "diretorio de fontes: " + str ( glbDefs.xFNT_MENU ))

        # monta o pathname do arquivo de fonte monoespacadas
        glbDefs.xFNT_MONO = data.filepath ( os.path.join ( glbDefs.xDIR_FNT, glbDefs.xFNT_MONO ))
        #l_log.info ( "diretorio de fontes: " + str ( glbDefs.xFNT_MONO ))

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadRede
    # ---------------------------------------------------------------------------------------------
    def loadRede ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadRede" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # load multicast data address
        try:

            glbDefs.xNET_Addr = self._cp.get ( "net", "addr" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xNET_Addr: " + str ( glbDefs.xNET_Addr ))

        # load multicast config address
        try:

            glbDefs.xNET_Cnfg = self._cp.get ( "net", "cnfg" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xNET_Cnfg: " + str ( glbDefs.xNET_Cnfg ))

        # load multicast address
        try:

            glbDefs.xNET_Data = self._cp.get ( "net", "data" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xNET_Data: " + str ( glbDefs.xNET_Data ))

        # load comm port
        try:

            glbDefs.xNET_Port = self._cp.getint ( "net", "port" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xNET_Port: " + str ( glbDefs.xNET_Port ))

        # load signature
        try:

            glbDefs.xNET_Vers = self._cp.getint ( "net", "vers" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xNET_Vers: " + str ( glbDefs.xNET_Vers ))

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadScreen
    # ---------------------------------------------------------------------------------------------
    def loadScreen ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadScreen" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # load fullscreen flag
        try:

            glbDefs.xSCR_Full = self._cp.getboolean ( "cfg", "full" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xSCR_Full: " + str ( glbDefs.xSCR_Full ))

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadSound
    # ---------------------------------------------------------------------------------------------
    def loadSound ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadSound" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # load alert sound
        try:

            glbDefs.xSND_Alert = self._cp.get ( "snd", "alert" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xSND_Alert: " + str ( glbDefs.xSND_Alert ))

        # load explode sound
        try:

            glbDefs.xSND_Explode = self._cp.get ( "snd", "explode" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xSND_Explode: " + str ( glbDefs.xSND_Explode ))

        # monta o pathname do arquivo de alerta
        glbDefs.xSND_Alert = data.filepath ( os.path.join ( glbDefs.xDIR_SND, glbDefs.xSND_Alert ))
        #l_log.info ( "arquivo de alerta: " + str ( glbDefs.xSND_Alert ))

        # monta o pathname do arquivo de explosão
        glbDefs.xSND_Explode = data.filepath ( os.path.join ( glbDefs.xDIR_SND, glbDefs.xSND_Explode ))
        #l_log.info ( "arquivo de explosão: " + str ( glbDefs.xSND_Explode ))

        # m.poirot logger
        #l_log.debug ( "<<" )

    # ---------------------------------------------------------------------------------------------
    # configManager::loadTime
    # ---------------------------------------------------------------------------------------------
    def loadTime ( self ):

        """
        initializes the display.

        @return none
        """

        # m.poirot logger
        #l_log = logging.getLogger ( "configManager::loadTime" )
        #l_log.setLevel ( w_logLvl )
        #l_log.debug ( ">>" )

        # fast-time simulation acceleration factor
        try:

            glbDefs.xTIM_Accel = self._cp.getfloat ( "time", "accel" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xTIM_Accel: " + str ( glbDefs.xTIM_Accel ))

        # envio de configuração do sistema
        try:

            glbDefs.xTIM_Cnfg = self._cp.getint ( "time", "cnfg" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xTIM_Cnfg: " + str ( glbDefs.xTIM_Cnfg ))

        # ativação das aeronaves
        try:

            glbDefs.xTIM_FGen = self._cp.getint ( "time", "fgen" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xTIM_FGen: " + str ( glbDefs.xTIM_FGen ))

        # colisão entre aeronaves
        try:

            glbDefs.xTIM_Prox = self._cp.getint ( "time", "prox" )

        except ConfigParser.NoSectionError: pass
        except ConfigParser.NoOptionError: pass

        #l_log.info ( "glbDefs.xTIM_Prox: " + str ( glbDefs.xTIM_Prox ))

        # m.poirot logger
        #l_log.debug ( "<<" )

# < the end >-------------------------------------------------------------------------------------- #
