import numpy as np
import torch
from torch import nn
import pytorch_lightning as pl
from .soft_attention import Attention



class lstm_crossattn_tl(pl.LightningModule):
    '''
    Standard PyTorch Lightning module:
    https://pytorch-lightning.readthedocs.io/en/latest/lightning_module.html
    '''
    def __init__(self, 
                 hidden_size, 
                 batch_size,
                 num_layers, 
                 dropout, 
                 output_size,
                 learning_rate,
                 criterion_ht, criterion_tl,
                 mse_female, mae_female, mse_male, mae_male,
                 seq_len = 800,
                 n_features = 83):
        super(lstm_crossattn_tl, self).__init__()
        self.n_features = n_features
        self.hidden_size = hidden_size
        self.seq_len = seq_len
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.criterion_ht = criterion_ht
        self.criterion_tl = criterion_tl
        self.learning_rate = learning_rate
        self.mse_female = mse_female
        self.mae_female = mae_female
        self.mse_male = mse_male
        self.mae_male = mae_male

        self.lstm = nn.LSTM(input_size=n_features, 
                            hidden_size=hidden_size,
                            num_layers=num_layers, 
                            dropout=dropout, 
                            batch_first=True,
                            bidirectional=False)
        self.attention_time = Attention(n_channels=hidden_size)
        self.attention_units = Attention(n_channels=seq_len)
        self.dropout = nn.Dropout(dropout)
        self.linear_ht = nn.Linear(hidden_size + seq_len, output_size)
        self.linear_n = nn.Linear(hidden_size + seq_len, output_size)
        self.relu_ht= nn.ReLU()
        
    def forward(self, x):

        x = x.float()
        lstm_out, _ = self.lstm(x)

        attn_t = self.attention_time(lstm_out)
        attn_u = self.attention_units(lstm_out.permute(0,2,1))
        attn_cross = torch.cat((attn_t, attn_u), axis=1)
        
        drop = self.dropout(attn_cross)
        out_ht = self.linear_ht(drop)
        out_n = self.linear_n(drop)
        out_ht = self.relu_ht(out_ht)
        
        return out_ht, attn_cross
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    def training_step(self, batch, batch_idx):
        anchor, positive, negative, target = batch
        
        ht_hat, anchor_embd = self(anchor)
        _, positive_embd = self(positive)
        _, negative_embd = self(negative)
        
        loss_ht = self.criterion_ht(torch.squeeze(ht_hat).float(), target.float())
        loss_tl = self.criterion_tl(torch.squeeze(anchor_embd).float(), torch.squeeze(positive_embd).float(), torch.squeeze(negative_embd).float())
        loss = loss_ht + 30*loss_tl
        #result = pl.TrainResult(loss)
        self.log('train_loss', loss)
        return loss
    
    def validation_step(self, batch, batch_idx):
        anchor, target = batch
        
        ht_hat, _ = self(anchor)
        
        loss_ht = self.criterion_ht(torch.squeeze(ht_hat).float(), target.float())
        # loss_n = self.criterion_tl(torch.squeeze(n_hat).float(), n.float())
        # loss = 3*loss_ht + loss_n
        #result = pl.EvalResult(checkpoint_on=loss)
        self.log('val_loss', loss_ht)
        return loss_ht
    
    def test_step(self, batch, batch_idx):
        anchor, target, gender = batch
        ht_hat, _ = self(anchor)
        loss_ht = self.criterion_ht(torch.squeeze(ht_hat).float(), target.float())
        # loss_n = self.criterion_n(torch.squeeze(n_hat).float(), n.float())
        # loss = 3*loss_ht + loss_n
        for i in range(ht_hat.shape[0]):
            #print(i, ht_hat[i], y_ht[i])
            if gender[i].item() == 1:
                mse_error_f = mse_female(torch.squeeze(ht_hat[i]), target[i])
                mae_error_f = mae_female(torch.squeeze(ht_hat[i]), target[i])
                
            if gender[i].item() == 0:
                mse_error_m = mse_male(torch.squeeze(ht_hat[i]), target[i])
                mae_error_m = mae_male(torch.squeeze(ht_hat[i]), target[i])
                
        #result = pl.EvalResult()
        self.log('test_loss', loss_ht)
        return loss_ht