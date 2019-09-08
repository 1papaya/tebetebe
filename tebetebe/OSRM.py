#!/usr/bin/env python3

import logging
import atexit
import sys
import sh

from . import defaults

class OSRM():
    """
    Base class wrapper around all the osrm-* binaries. All functions accept
    additional **kwargs to be passed upon execution. This class is used in
    the background and need not be initialized directly.

    Parameters
    ----------
    verbose: bool
        Output stdout from osrm commands.
    """

    def __init__(self, verbose=defaults.VERBOSE):
        self.log = logging.getLogger(defaults.LOGGER)
        self.verbose = verbose
        self.processes = []

        ## Make sure all OSRM are killed upon script exit
        atexit.register(self._kill_all_osrm)

        try:
            self._osrm_extract = sh.Command("osrm-extract")
            self._osrm_contract = sh.Command("osrm-contract")
            self._osrm_routed = sh.Command("osrm-routed")
            self._osrm_partition = sh.Command("osrm-partition")
            self._osrm_customize = sh.Command("osrm-customize")
            self._osrm_datastore = sh.Command("osrm-datastore")

        except CommandNotFound as err:
            self.log.error("OSRM binary not found: {}".format(err))

    def extract(self, osm_path, profile_path, **kwargs):
        '''
        Call `osrm-extract` with a path to the osm route network and lua profile. 
        '''

        defaults = {"_bg": True,
                    "_out": sys.stdout if self.verbose else None}

        proc = self._osrm_extract(osm_path, "-p", profile_path, **{**defaults, **kwargs})

        self._log_cmd(proc)
        self.processes.append(proc)

        return proc

    def partition(self, osrm_file, **kwargs):
        '''Call `osrm-partition` for a .osrm file'''
      
        defaults = {"_bg": True,
                    "_out": sys.stdout if self.verbose else None}

        proc = self._osrm_partition(osrm_file, **{**defaults, **kwargs})

        self._log_cmd(proc)
        self.processes.append(proc)

        return proc

    def customize(self, osrm_file, **kwargs):
        '''Call `osrm-customize` on a .osrm file'''
      
        defaults = {"_bg": True,
                    "_out": sys.stdout if self.verbose else None}

        proc = self._osrm_customize(osrm_file, **{**defaults, **kwargs})

        self._log_cmd(proc)
        self.processes.append(proc)

        return proc

    def contract(self, osrm_file, **kwargs):
        '''Call `osrm-contract` on a .osrm file'''

        defaults = {"_bg": True,
                    "_out": sys.stdout if self.verbose else None}

        proc = self._osrm_contract(osrm_file, **{**defaults, **kwargs})

        self._log_cmd(proc)
        self.processes.append(proc)

        return proc

    def routed(self, osrm_file, ready_callback, done_callback, verbose=False, **kwargs):
        '''
        Call `osrm-routed` on a .osrm file

        Parameters
        ----------
        osrm_file : str
            Path to *.osrm
        ready_callback : function
            Function to be called when osrm-routed is ready for HTTP requests
        done_callback : function
            Function to be called when osrm-routed has exited
        verbose : bool
            `osrm-routed` output is so verbose it is default off even if the parent class `verbose=True`. Set this to true if you want to see `osrm-routed` output anyway.
        **kwargs
            Any additional parameters to be passed to osrm-routed
        '''

        ## Parse OSRM output line by line and exec callback when server is running
        def parse_output(line, stdin, process):
            if line.find("running and waiting for requests"):
                ready_callback(process)
                return True ## Returning True stops executing this function each line

        def parse_output_verbose(line, stdin, process):
            if line.find("running and waiting for requests"):
                ready_callback(process)

            print(line)

        defaults = {"_bg": True, "_bg_exc": False,
                    "verbosity": "INFO", "ip": "127.0.0.1",
                    "_out": parse_output_verbose if verbose else parse_output,
                    "_done": done_callback}

        proc = self._osrm_routed(osrm_file, **{**defaults, **kwargs})

        self._log_cmd(proc)
        self.processes.append(proc)

        return proc

    def get_version(self):
        '''Return OSRM binaries version'''
        return self._osrm_extract("--version")

    def _log_cmd(self, proc):
        '''Log command text in a debug log output'''
        cmd = " ".join([b.decode('utf-8') for b in proc.cmd])

        self.log.debug("Executing: {}".format(cmd))

    def _kill_all_osrm(self):
        '''
        Send kill signal to all osrm processes spawned under this module. This will
        be executed upon script exit to ensure that there's no processes left behind
        '''

        for proc in self.processes:
            try:
                proc.kill()
            except:
                continue
