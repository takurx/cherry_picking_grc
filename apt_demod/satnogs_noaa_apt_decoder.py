#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NOAA APT Decoder
# Author: Manolis Surligas, George Vardakis
# Description: A NOAA APT Decoder with automatic image synchronization
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt
import satnogs
import sip
import sys
from gnuradio import qtgui


class satnogs_noaa_apt_decoder(gr.top_block, Qt.QWidget):

    def __init__(self, antenna=satnogs.not_set_antenna, bb_gain=satnogs.not_set_rx_bb_gain, decoded_data_file_path='/home/mocha/.satnogs/data/noaa', dev_args=satnogs.not_set_dev_args, doppler_correction_per_sec=20, enable_iq_dump=0, file_path='/tmp/test.ogg', flip_images=0, if_gain=satnogs.not_set_rx_if_gain, iq_file_path='/tmp/iq.dat', lo_offset=100e3, ppm=0, rf_gain=satnogs.not_set_rx_rf_gain, rigctl_port=4532, rx_freq=137.812e6, rx_sdr_device='rtlsdr', sync=1, waterfall_file_path='/tmp/waterfall.dat'):
        gr.top_block.__init__(self, "NOAA APT Decoder")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NOAA APT Decoder")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "satnogs_noaa_apt_decoder")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


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
        self.waterfall_file_path = waterfall_file_path

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_rx = samp_rate_rx = satnogs.hw_rx_settings[rx_sdr_device]['samp_rate']
        self.first_stage_decimation = first_stage_decimation = 4

        self.noaa_filter_taps = noaa_filter_taps = firdes.low_pass(1.0, samp_rate_rx /first_stage_decimation, 16.5e3, 4e3, firdes.WIN_HAMMING, 6.76)

        self.initial_bandwidth = initial_bandwidth = 100e3

        self.first_stage_filter_taps = first_stage_filter_taps = firdes.low_pass(1.0, 1.0, 0.2, 0.1, firdes.WIN_HAMMING, 6.76)

        self.audio_decimation = audio_decimation = 2

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_ogg_encoder_0 = satnogs.ogg_encoder(file_path, 48000, 0.8)
        self.rational_resampler_xxx_2_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth))),
                decimation=int(samp_rate_rx /first_stage_decimation),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=48000,
                decimation=int(samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)) / audio_decimation),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rx_freq, #fc
        	samp_rate_rx, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(int(samp_rate_rx/ first_stage_decimation / initial_bandwidth), (noaa_filter_taps), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate_rx,True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.008, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.008, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/mocha/Desktop/1912_December/iq_NOAA_18_20191016T101359_137812000Hz_IQ.wav', False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_char*1, 1)
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((-127, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((127, ))
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate_rx/ ( first_stage_decimation  * int(samp_rate_rx/ first_stage_decimation / initial_bandwidth)),
        	audio_decimation=audio_decimation,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_deinterleave_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.rational_resampler_xxx_2_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.satnogs_ogg_encoder_0, 0))
        self.connect((self.rational_resampler_xxx_2_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "satnogs_noaa_apt_decoder")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate_rx)

    def get_rx_sdr_device(self):
        return self.rx_sdr_device

    def set_rx_sdr_device(self, rx_sdr_device):
        self.rx_sdr_device = rx_sdr_device
        self.set_samp_rate_rx(satnogs.hw_rx_settings[self.rx_sdr_device]['samp_rate'])

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync

    def get_waterfall_file_path(self):
        return self.waterfall_file_path

    def set_waterfall_file_path(self, waterfall_file_path):
        self.waterfall_file_path = waterfall_file_path

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.samp_rate_rx)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_rx)

    def get_first_stage_decimation(self):
        return self.first_stage_decimation

    def set_first_stage_decimation(self, first_stage_decimation):
        self.first_stage_decimation = first_stage_decimation

    def get_noaa_filter_taps(self):
        return self.noaa_filter_taps

    def set_noaa_filter_taps(self, noaa_filter_taps):
        self.noaa_filter_taps = noaa_filter_taps
        self.fft_filter_xxx_0.set_taps((self.noaa_filter_taps))

    def get_initial_bandwidth(self):
        return self.initial_bandwidth

    def set_initial_bandwidth(self, initial_bandwidth):
        self.initial_bandwidth = initial_bandwidth

    def get_first_stage_filter_taps(self):
        return self.first_stage_filter_taps

    def set_first_stage_filter_taps(self, first_stage_filter_taps):
        self.first_stage_filter_taps = first_stage_filter_taps

    def get_audio_decimation(self):
        return self.audio_decimation

    def set_audio_decimation(self, audio_decimation):
        self.audio_decimation = audio_decimation


def argument_parser():
    description = 'A NOAA APT Decoder with automatic image synchronization'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--antenna", dest="antenna", type="string", default=satnogs.not_set_antenna,
        help="Set antenna [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(satnogs.not_set_rx_bb_gain),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--decoded-data-file-path", dest="decoded_data_file_path", type="string", default='/home/mocha/.satnogs/data/noaa',
        help="Set decoded_data_file_path [default=%default]")
    parser.add_option(
        "", "--dev-args", dest="dev_args", type="string", default=satnogs.not_set_dev_args,
        help="Set rtl=00000002 [default=%default]")
    parser.add_option(
        "", "--doppler-correction-per-sec", dest="doppler_correction_per_sec", type="intx", default=20,
        help="Set doppler_correction_per_sec [default=%default]")
    parser.add_option(
        "", "--enable-iq-dump", dest="enable_iq_dump", type="intx", default=0,
        help="Set enable_iq_dump [default=%default]")
    parser.add_option(
        "", "--file-path", dest="file_path", type="string", default='/tmp/test.ogg',
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
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(137.812e6),
        help="Set rx_freq [default=%default]")
    parser.add_option(
        "", "--rx-sdr-device", dest="rx_sdr_device", type="string", default='rtlsdr',
        help="Set rx_sdr_device [default=%default]")
    parser.add_option(
        "", "--sync", dest="sync", type="intx", default=1,
        help="Set sync [default=%default]")
    parser.add_option(
        "", "--waterfall-file-path", dest="waterfall_file_path", type="string", default='/tmp/waterfall.dat',
        help="Set waterfall_file_path [default=%default]")
    return parser


def main(top_block_cls=satnogs_noaa_apt_decoder, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(antenna=options.antenna, bb_gain=options.bb_gain, decoded_data_file_path=options.decoded_data_file_path, dev_args=options.dev_args, doppler_correction_per_sec=options.doppler_correction_per_sec, enable_iq_dump=options.enable_iq_dump, file_path=options.file_path, flip_images=options.flip_images, if_gain=options.if_gain, iq_file_path=options.iq_file_path, lo_offset=options.lo_offset, ppm=options.ppm, rf_gain=options.rf_gain, rigctl_port=options.rigctl_port, rx_freq=options.rx_freq, rx_sdr_device=options.rx_sdr_device, sync=options.sync, waterfall_file_path=options.waterfall_file_path)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
