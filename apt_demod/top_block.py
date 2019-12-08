#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Description: Ref. https://community.libre.space/t/noaa-apt-slanting-issues/2264
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import satnogs
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


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
        self.satnogs_ogg_source_0 = satnogs.ogg_source('/home/mocha/Desktop/test4windows.ogg', 1, False)
        self.satnogs_noaa_apt_sink_0_0 = satnogs.noaa_apt_sink('/home/mocha/Desktop/test_ogg.png', 2080, 1800, True, True)
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
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_f(
        	2048, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	8000, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
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
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.satnogs_noaa_apt_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.band_pass_filter_0, 0))
        self.connect((self.satnogs_ogg_source_0, 0), (self.rational_resampler_xxx_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
