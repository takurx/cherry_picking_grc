#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: APT Generic Demodulation
# Author: Manolis Surligas (surligas@gmail.com)
# Description: A generic APT demodulation block
# GNU Radio version: 3.7.13.5
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import math
import pmt
import satnogs


class satnogs_apt_demod_1(gr.top_block):

    def __init__(self, antenna=satnogs.not_set_antenna, bb_gain=satnogs.not_set_rx_bb_gain, decoded_data_file_path='/home/mocha/.satnogs/data/data', dev_args='rtl=00000002', doppler_correction_per_sec=20, enable_iq_dump=0, file_path='/home/mocha/Desktop/test.ogg', flip_images=0, if_gain=satnogs.not_set_rx_if_gain, iq_file_path='/tmp/iq.dat', lo_offset=100e3, ppm=0, rf_gain=satnogs.not_set_rx_rf_gain, rigctl_port=4532, rx_freq=137812000, rx_sdr_device='rtlsdr', sync=1):
        gr.top_block.__init__(self, "APT Generic Demodulation")

        ##################################################
        # Parameters
        ##################################################
        self.antenna = antenna
        self.bb_gain = bb_gain
        self.decoded_data_file_path = decoded_data_file_path
        self.dev_args = dev_args
        self.doppler_correction_per_sec = doppler_correction_per_sec
        self.enable_iq_dump = enable_iq_dump
        self.file_path = file_path
        self.flip_images = flip_images
        self.if_gain = if_gain
        self.iq_file_path = iq_file_path
        self.lo_offset = lo_offset
        self.ppm = ppm
        self.rf_gain = rf_gain
        self.rigctl_port = rigctl_port
        self.rx_freq = rx_freq
        self.rx_sdr_device = rx_sdr_device
        self.sync = sync

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rx = samp_rate_rx = satnogs.hw_rx_settings[rx_sdr_device]['samp_rate']
        self.xlate_filter_taps = xlate_filter_taps = firdes.low_pass(1, samp_rate_rx, 125000, 25000, firdes.WIN_HAMMING, 6.76)

        self.taps = taps = firdes.low_pass(12.0, samp_rate_rx, 100e3, 60000, firdes.WIN_HAMMING, 6.76)

        self.initial_bandwidth = initial_bandwidth = 100e3

        self.first_stage_filter_taps = first_stage_filter_taps = firdes.low_pass(1.0, 1.0, 0.2, 0.1, firdes.WIN_HAMMING, 6.76)

        self.first_stage_decimation = first_stage_decimation = 4
        self.filter_rate = filter_rate = 250000
        self.deviation = deviation = 17000
        self.audio_samp_rate = audio_samp_rate = 48000
        self.audio_decimation = audio_decimation = 2

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_noaa_apt_sink_0 = satnogs.noaa_apt_sink('/tmp/.satnogs/data/test-2.png', 2080, 1800, bool(sync), bool(flip_images))
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_fff(
                interpolation=int(samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation),
                decimation=48000,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=2,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_3 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_2 = filter.rational_resampler_fff(
                interpolation=4*4160,
                decimation=int((samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation)/2),
                taps=None,
                fractional_bw=None,
        )
        self.hilbert_fc_0 = filter.hilbert_fc(65, firdes.WIN_HAMMING, 6.76)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(int(samp_rate_rx/filter_rate), (xlate_filter_taps), lo_offset, samp_rate_rx)
        self.fir_filter_xxx_1 = filter.fir_filter_fff(2, ([0.5, 0.5]))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate_rx,True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.008, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.008, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/mocha/Desktop/1912_December/iq_NOAA_18_20191016T101359_137812000Hz_IQ.wav', False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_char*1, 1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((-127, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((127, ))
        self.blks2_rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=48,
                decimation=125,
                taps=None,
                fractional_bw=None,
        )
        self.band_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	6, samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((2*math.pi*deviation)/96000)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.blks2_rational_resampler_xxx_1, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.rational_resampler_3, 0))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_deinterleave_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.rational_resampler_2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blks2_rational_resampler_xxx_1, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.rational_resampler_2, 0), (self.hilbert_fc_0, 0))
        self.connect((self.rational_resampler_3, 0), (self.satnogs_noaa_apt_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.band_pass_filter_0_0, 0))

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain

    def get_decoded_data_file_path(self):
        return self.decoded_data_file_path

    def set_decoded_data_file_path(self, decoded_data_file_path):
        self.decoded_data_file_path = decoded_data_file_path

    def get_dev_args(self):
        return self.dev_args

    def set_dev_args(self, dev_args):
        self.dev_args = dev_args

    def get_doppler_correction_per_sec(self):
        return self.doppler_correction_per_sec

    def set_doppler_correction_per_sec(self, doppler_correction_per_sec):
        self.doppler_correction_per_sec = doppler_correction_per_sec

    def get_enable_iq_dump(self):
        return self.enable_iq_dump

    def set_enable_iq_dump(self, enable_iq_dump):
        self.enable_iq_dump = enable_iq_dump

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_flip_images(self):
        return self.flip_images

    def set_flip_images(self, flip_images):
        self.flip_images = flip_images

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_iq_file_path(self):
        return self.iq_file_path

    def set_iq_file_path(self, iq_file_path):
        self.iq_file_path = iq_file_path

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.lo_offset)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_rigctl_port(self):
        return self.rigctl_port

    def set_rigctl_port(self, rigctl_port):
        self.rigctl_port = rigctl_port

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq

    def get_rx_sdr_device(self):
        return self.rx_sdr_device

    def set_rx_sdr_device(self, rx_sdr_device):
        self.rx_sdr_device = rx_sdr_device
        self.set_samp_rate_rx(satnogs.hw_rx_settings[self.rx_sdr_device]['samp_rate'])

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate_rx, 125000, 25000, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_rx)
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_xlate_filter_taps(self):
        return self.xlate_filter_taps

    def set_xlate_filter_taps(self, xlate_filter_taps):
        self.xlate_filter_taps = xlate_filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.xlate_filter_taps))

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_initial_bandwidth(self):
        return self.initial_bandwidth

    def set_initial_bandwidth(self, initial_bandwidth):
        self.initial_bandwidth = initial_bandwidth
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_first_stage_filter_taps(self):
        return self.first_stage_filter_taps

    def set_first_stage_filter_taps(self, first_stage_filter_taps):
        self.first_stage_filter_taps = first_stage_filter_taps

    def get_first_stage_decimation(self):
        return self.first_stage_decimation

    def set_first_stage_decimation(self, first_stage_decimation):
        self.first_stage_decimation = first_stage_decimation
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))

    def get_filter_rate(self):
        return self.filter_rate

    def set_filter_rate(self, filter_rate):
        self.filter_rate = filter_rate

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.analog_quadrature_demod_cf_0.set_gain((2*math.pi*self.deviation)/96000)

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate

    def get_audio_decimation(self):
        return self.audio_decimation

    def set_audio_decimation(self, audio_decimation):
        self.audio_decimation = audio_decimation
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(6, self.samp_rate_rx/ ( self.first_stage_decimation  * int(self.samp_rate_rx/ self.first_stage_decimation / self.initial_bandwidth)) / self.audio_decimation, 500, 4.2e3, 200, firdes.WIN_HAMMING, 6.76))


def argument_parser():
    description = 'A generic APT demodulation block'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--antenna", dest="antenna", type="string", default=satnogs.not_set_antenna,
        help="Set antenna [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_bb_gain),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--decoded-data-file-path", dest="decoded_data_file_path", type="string", default='/home/mocha/.satnogs/data/data',
        help="Set decoded_data_file_path [default=%default]")
    parser.add_option(
        "", "--dev-args", dest="dev_args", type="string", default='rtl=00000002',
        help="Set dev_args [default=%default]")
    parser.add_option(
        "", "--doppler-correction-per-sec", dest="doppler_correction_per_sec", type="intx", default=20,
        help="Set doppler_correction_per_sec [default=%default]")
    parser.add_option(
        "", "--enable-iq-dump", dest="enable_iq_dump", type="intx", default=0,
        help="Set enable_iq_dump [default=%default]")
    parser.add_option(
        "", "--file-path", dest="file_path", type="string", default='/home/mocha/Desktop/test.ogg',
        help="Set file_path [default=%default]")
    parser.add_option(
        "", "--flip-images", dest="flip_images", type="intx", default=0,
        help="Set flip_images [default=%default]")
    parser.add_option(
        "", "--if-gain", dest="if_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_if_gain),
        help="Set if_gain [default=%default]")
    parser.add_option(
        "", "--iq-file-path", dest="iq_file_path", type="string", default='/tmp/iq.dat',
        help="Set iq_file_path [default=%default]")
    parser.add_option(
        "", "--lo-offset", dest="lo_offset", type="eng_float", default=eng_notation.num_to_str(100e3),
        help="Set lo_offset [default=%default]")
    parser.add_option(
        "", "--ppm", dest="ppm", type="intx", default=0,
        help="Set ppm [default=%default]")
    parser.add_option(
        "", "--rf-gain", dest="rf_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_rf_gain),
        help="Set rf_gain [default=%default]")
    parser.add_option(
        "", "--rigctl-port", dest="rigctl_port", type="intx", default=4532,
        help="Set rigctl_port [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(137812000),
        help="Set rx_freq [default=%default]")
    parser.add_option(
        "", "--rx-sdr-device", dest="rx_sdr_device", type="string", default='rtlsdr',
        help="Set rx_sdr_device [default=%default]")
    parser.add_option(
        "", "--sync", dest="sync", type="intx", default=1,
        help="Set sync [default=%default]")
    return parser


def main(top_block_cls=satnogs_apt_demod_1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(antenna=options.antenna, bb_gain=options.bb_gain, decoded_data_file_path=options.decoded_data_file_path, dev_args=options.dev_args, doppler_correction_per_sec=options.doppler_correction_per_sec, enable_iq_dump=options.enable_iq_dump, file_path=options.file_path, flip_images=options.flip_images, if_gain=options.if_gain, iq_file_path=options.iq_file_path, lo_offset=options.lo_offset, ppm=options.ppm, rf_gain=options.rf_gain, rigctl_port=options.rigctl_port, rx_freq=options.rx_freq, rx_sdr_device=options.rx_sdr_device, sync=options.sync)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
