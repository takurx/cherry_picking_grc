#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Decode Noaa Apt From Ogg 48K
# Description: Ref. https://community.libre.space/t/noaa-apt-slanting-issues/2264
# GNU Radio version: 3.7.13.5
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import satnogs


class decode_noaa_apt_from_ogg_48k(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Decode Noaa Apt From Ogg 48K")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rx = samp_rate_rx = 500e3
        self.samp_rate = samp_rate = 48000
        self.initial_bandwidth = initial_bandwidth = 100e3
        self.first_stage_decimation = first_stage_decimation = 4
        self.audio_decimation = audio_decimation = 2

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_ogg_source_0 = satnogs.ogg_source('/home/mocha/Desktop/satnogs_1389117_2019-12-17T09-31-56.ogg', 1, False)
        self.satnogs_noaa_apt_sink_0_0 = satnogs.noaa_apt_sink('/home/mocha/Desktop/satnogs_1389117_2019-12-17T09-31-56_ogg.png', 2080, 1800, True, False)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=int(samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation),
                decimation=48000,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=4*4160,
                decimation=int((samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation)/2),
                taps=None,
                fractional_bw=None,
        )
        self.hilbert_fc_0 = filter.hilbert_fc(65, firdes.WIN_HAMMING, 6.76)
        self.fir_filter_xxx_1 = filter.fir_filter_fff(2, ([0.5, 0.5]))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	6, samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))



        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.hilbert_fc_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.satnogs_noaa_apt_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.band_pass_filter_0, 0))
        self.connect((self.satnogs_ogg_source_0, 0), (self.rational_resampler_xxx_1, 0))

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.band_pass_filter_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_initial_bandwidth(self):
        return self.initial_bandwidth

    def set_initial_bandwidth(self, initial_bandwidth):
        self.initial_bandwidth = initial_bandwidth
        self.band_pass_filter_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_first_stage_decimation(self):
        return self.first_stage_decimation

    def set_first_stage_decimation(self, first_stage_decimation):
        self.first_stage_decimation = first_stage_decimation
        self.band_pass_filter_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_audio_decimation(self):
        return self.audio_decimation

    def set_audio_decimation(self, audio_decimation):
        self.audio_decimation = audio_decimation
        self.band_pass_filter_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=decode_noaa_apt_from_ogg_48k, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
