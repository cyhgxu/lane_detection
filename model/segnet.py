"""
Implement Lane Detection Model
"""
import tensorflow as tf

from config import global_config
from model import segnet_back_end
from model import segnet_front_end
from semantic_segmentation_zoo import cnn_basenet

CFG = global_config.cfg


class SegNet(cnn_basenet.CNNBaseModel):
    """

    """
    def __init__(self, phase, net_flag='vgg', reuse=False):
        """

        """
        super(SegNet, self).__init__()
        self._net_flag = net_flag
        self._reuse = reuse

        self._frontend = segnet_front_end.SegNetFrondEnd(
            phase=phase, net_flag=net_flag
        )
        self._backend = segnet_back_end.SegNetDataFeeder(
            phase=phase
        )

    def inference(self, input_tensor, name):
        """

        :param input_tensor:
        :param name:
        :return:
        """
        with tf.variable_scope(name_or_scope=name, reuse=self._reuse):
            # first extract image features
            extract_feats_result = self._frontend.build_model(
                input_tensor=input_tensor,
                name='{:s}_frontend'.format(self._net_flag),
                reuse=self._reuse
            )

            # second apply backend process
            binary_seg_prediction = self._backend.inference(
                binary_seg_logits=extract_feats_result['binary_segment_logits']['data'],
                name='{:s}_backend'.format(self._net_flag),
                reuse=self._reuse
            )

            if not self._reuse:
                self._reuse = True

        return binary_seg_prediction

    def compute_loss(self, input_tensor, binary_label, name):
        """
        calculate segmentation loss for training
        :param input_tensor:
        :param binary_label:
        :param name:
        :return:
        """
        with tf.variable_scope(name_or_scope=name, reuse=self._reuse):
            # first extract image features
            extract_feats_result = self._frontend.build_model(
                input_tensor=input_tensor,
                name='{:s}_frontend'.format(self._net_flag),
                reuse=self._reuse
            )

            # second apply backend process
            calculated_losses = self._backend.compute_loss(
                binary_seg_logits=extract_feats_result['binary_segment_logits']['data'],
                binary_label=binary_label,
                name='{:s}_backend'.format(self._net_flag),
                reuse=self._reuse
            )

            if not self._reuse:
                self._reuse = True

        return calculated_losses
