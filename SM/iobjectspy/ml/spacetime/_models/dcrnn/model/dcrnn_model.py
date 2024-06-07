# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\model\dcrnn_model.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 10215 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import torch
import torch.nn as nn
from model.dcrnn_cell import DCGRUCell
import random
from ..base import BaseModel

class DCRNNEncoder(BaseModel):

    def __init__(self, input_dim, adj_mat, max_diffusion_step, hid_dim, num_nodes, num_rnn_layers):
        super(DCRNNEncoder, self).__init__()
        self.hid_dim = hid_dim
        self._num_rnn_layers = num_rnn_layers
        encoding_cells = list()
        encoding_cells.append(DCGRUCell(input_dim=input_dim, num_units=hid_dim, adj_mat=adj_mat, max_diffusion_step=max_diffusion_step,
          num_nodes=num_nodes))
        for _ in range(1, num_rnn_layers):
            encoding_cells.append(DCGRUCell(input_dim=hid_dim, num_units=hid_dim, adj_mat=adj_mat, max_diffusion_step=max_diffusion_step,
              num_nodes=num_nodes))

        self.encoding_cells = nn.ModuleList(encoding_cells)

    def forward(self, inputs, initial_hidden_state):
        seq_length = inputs.shape[0]
        batch_size = inputs.shape[1]
        inputs = torch.reshape(inputs, (seq_length, batch_size, -1))
        current_inputs = inputs
        output_hidden = []
        for i_layer in range(self._num_rnn_layers):
            hidden_state = initial_hidden_state[i_layer]
            output_inner = []
            for t in range(seq_length):
                _, hidden_state = self.encoding_cells[i_layer](current_inputs[(t, ...)], hidden_state)
                output_inner.append(hidden_state)

            output_hidden.append(hidden_state)
            current_inputs = torch.stack(output_inner, dim=0)
            if torch.cuda.device_count() > 0:
                current_inputs = current_inputs.cuda()

        return (output_hidden, current_inputs)

    def init_hidden(self, batch_size):
        init_states = []
        for i in range(self._num_rnn_layers):
            init_states.append(self.encoding_cells[i].init_hidden(batch_size))

        return torch.stack(init_states, dim=0)


class DCGRUDecoder(BaseModel):

    def __init__(self, input_dim, adj_mat, max_diffusion_step, num_nodes, hid_dim, output_dim, num_rnn_layers):
        super(DCGRUDecoder, self).__init__()
        self.hid_dim = hid_dim
        self._num_nodes = num_nodes
        self._output_dim = output_dim
        self._num_rnn_layers = num_rnn_layers
        cell = DCGRUCell(input_dim=hid_dim, num_units=hid_dim, adj_mat=adj_mat,
          max_diffusion_step=max_diffusion_step,
          num_nodes=num_nodes)
        cell_with_projection = DCGRUCell(input_dim=hid_dim, num_units=hid_dim, adj_mat=adj_mat,
          max_diffusion_step=max_diffusion_step,
          num_nodes=num_nodes,
          num_proj=output_dim)
        decoding_cells = list()
        decoding_cells.append(DCGRUCell(input_dim=input_dim, num_units=hid_dim, adj_mat=adj_mat,
          max_diffusion_step=max_diffusion_step,
          num_nodes=num_nodes))
        for _ in range(1, num_rnn_layers - 1):
            decoding_cells.append(cell)

        decoding_cells.append(cell_with_projection)
        self.decoding_cells = nn.ModuleList(decoding_cells)

    def forward(self, inputs, initial_hidden_state, teacher_forcing_ratio=0.5):
        """
        :param inputs: shape should be (seq_length+1, batch_size, num_nodes, input_dim)
        :param initial_hidden_state: the last hidden state of the encoder. (num_layers, batch, outdim)
        :param teacher_forcing_ratio:
        :return: outputs. (seq_length, batch_size, num_nodes*output_dim) (12, 50, 207*1)
        """
        seq_length = inputs.shape[0]
        batch_size = inputs.shape[1]
        inputs = torch.reshape(inputs, (seq_length, batch_size, -1))
        outputs = torch.zeros(seq_length, batch_size, self._num_nodes * self._output_dim)
        current_input = inputs[0]
        for t in range(1, seq_length):
            next_input_hidden_state = []
            for i_layer in range(0, self._num_rnn_layers):
                hidden_state = initial_hidden_state[i_layer]
                output, hidden_state = self.decoding_cells[i_layer](current_input, hidden_state)
                current_input = output
                next_input_hidden_state.append(hidden_state)

            initial_hidden_state = torch.stack(next_input_hidden_state, dim=0)
            outputs[t] = output
            teacher_force = random.random() < teacher_forcing_ratio
            current_input = inputs[t] if teacher_force else output

        return outputs


class DCRNNModel(BaseModel):

    def __init__(self, adj_mat, batch_size, enc_input_dim, dec_input_dim, max_diffusion_step, num_nodes, num_rnn_layers, rnn_units, seq_len, output_dim):
        super(DCRNNModel, self).__init__()
        self._batch_size = batch_size
        self._num_nodes = num_nodes
        self._num_rnn_layers = num_rnn_layers
        self._rnn_units = rnn_units
        self._seq_len = seq_len
        self._output_dim = output_dim
        self.GO_Symbol = torch.zeros(1, batch_size, num_nodes * self._output_dim, 1)
        if torch.cuda.device_count() > 0:
            self.GO_Symbol = self.GO_Symbol.cuda()
        self.encoder = DCRNNEncoder(input_dim=enc_input_dim, adj_mat=adj_mat, max_diffusion_step=max_diffusion_step,
          hid_dim=rnn_units,
          num_nodes=num_nodes,
          num_rnn_layers=num_rnn_layers)
        self.decoder = DCGRUDecoder(input_dim=dec_input_dim, adj_mat=adj_mat,
          max_diffusion_step=max_diffusion_step,
          num_nodes=num_nodes,
          hid_dim=rnn_units,
          output_dim=(self._output_dim),
          num_rnn_layers=num_rnn_layers)
        assert self.encoder.hid_dim == self.decoder.hid_dim, "Hidden dimensions of encoder and decoder must be equal!"

    def forward(self, source, target, teacher_forcing_ratio):
        source = torch.transpose(source, dim0=0, dim1=1)
        target = torch.transpose((target[(..., None[:self._output_dim])]), dim0=0, dim1=1)
        target = torch.cat([self.GO_Symbol, target], dim=0)
        init_hidden_state = self.encoder.init_hidden(self._batch_size)
        if torch.cuda.device_count() > 0:
            init_hidden_state = init_hidden_state.cuda()
        context, _ = self.encoder(source, init_hidden_state)
        outputs = self.decoder(target, context, teacher_forcing_ratio=teacher_forcing_ratio)
        return outputs[(1[:None], None[:None], None[:None])]

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def output_dim(self):
        return self._output_dim

    @property
    def num_nodes(self):
        return self._num_nodes

    @property
    def batch_size(self):
        return self._batch_size
