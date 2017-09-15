#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grgsm import arfcn
from math import pi
from optparse import OptionParser
import grgsm
import osmosdr
import pmt
import time
import sh
from grgsm_livemon_headless import grgsm_livemon_headless

def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--args", dest="args", type="string", default="",
        help="Set Device Arguments [default=%default]")
    parser.add_option(
        "", "--collector", dest="collector", type="string", default="localhost",
        help="Set IP or DNS name of collector point [default=%default]")
    parser.add_option(
        "", "--collectorport", dest="collectorport", type="string", default="4729",
        help="Set UDP port number of collector [default=%default]")
    parser.add_option(
        "-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set RF Gain [default=%default]")
    parser.add_option(
        "", "--osr", dest="osr", type="intx", default=4,
        help="Set OverSampling Ratio [default=%default]")
    parser.add_option(
        "-p", "--ppm", dest="ppm", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set Clock frequency offset in ppms (1/1e6 parts) [default=%default]")
    parser.add_option(
        "-T", "--rec-len", dest="rec_len", type="eng_float", default=eng_notation.num_to_str(1000000),
        help="Set Recording length in seconds [default=%default]")
    parser.add_option(
        "-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(2000000.052982),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "", "--serverport", dest="serverport", type="string", default="4729",
        help="Set UDP server listening port [default=%default]")
    parser.add_option(
        "-o", "--shiftoff", dest="shiftoff", type="eng_float", default=eng_notation.num_to_str(400e3),
        help="Set Frequency Shiftoff [default=%default]")
    parser.add_option(
        "-f", "--fc", dest="fc", type="eng_float", default=eng_notation.num_to_str(957e6),
        help="Set GSM channel's central frequency [default=%default]")
    return parser



def main(top_block_cls=grgsm_livemon_headless, options=None):

    freq_list = []
    Kal = sh.Command("../src/kal")
    output = str(Kal('-s', 'GSM850', '-a', '-p'))
    for line in output.split('\n'):
        if ',' not in line: continue
        parts = line.split(',')
        freq_list.append(parts[1])
    if options is None:
        options, _ = argument_parser().parse_args()
    print("Frequency list: %s" % (str(freq_list))
    tb = top_block_cls(args=options.args, collector=options.collector, collectorport=options.collectorport, gain=options.gain, osr=options.osr, ppm=options.ppm, rec_len=options.rec_len, samp_rate=options.samp_rate, serverport=options.serverport, shiftoff=options.shiftoff, fc=freq_list[0])

    for freq in freq_list:
        tb.set_fc(freq)
        tb.start()
        time.sleep(5)
        tb.stop()

if __name__ == '__main__':
    main()
