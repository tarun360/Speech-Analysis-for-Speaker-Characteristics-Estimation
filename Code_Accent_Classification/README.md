# Code for Accent Classification

## Overview of the Directory

This folder contains the code implementation of different models for Accent Recognition using the dataset of 'Accented speech recognition workshop data’ from DataTang for INTERSPEECH 2020 </br>

Please download the dataset from: [Accent_Data](https://drive.google.com/file/d/1u-MnUn4w0Pu-w7PvWPVQs8QHwH_G-uJu/view?usp=sharing)

The directory also contains augmented features for Training, Validation and Testing Sets. </br>
Number of Accents: 8 (each ~20 hrs)
- American
- British
- Chinese
- Indian
- Japanese
- Korean
- Portuguese
- Russian

The features here include:</br>
- 80 Filter Bank Energy features
- 3 Pitch features </br>

</br>
We have used CMVN normalization as a pre-processing step on the input features.
</br></br>

 

As of now, the following six models have been added in the package here:</br>


- `LSTM + Attention Model`
- `LSTM + Cross Attention (proposed by us) Model`
- `BiLSTM + Cross Attention + Focal Loss Model`
- `LSTM + Cross Attention + Multi-Task Model (Accent & Gender prediction)`
- `LSTM + Cross Attention + Multi-Task + Focal Loss Model (Accent & Gender prediction)`
- `LSTM + Cross Attention + Gender_Pre_Training Model`
</br></br>

## Running the Package:

1. Please ensure that the follwing dependencies are installed in you system:</br>
```
sklearn
kaldiio
keras
tensorflow
numpy
pandas
pickle
```
</br></br>

2. Clone or Download this directory (i.e. `Code_Accent_Classification`). </br></br>

3. Download the dataset from the link given above. Unzip the dataset in the `Code_Accent_Classification` directory. 
Your directory should look like this: </br>
```
/Code_Accent_Classification/
...
   Accent_Data
   modules
   README.md
   run.py
```
  
  </br></br>

4. Excecute the `run.py` file (make sure that your current working directory is `Code_Accent_Classification`):
```
$ python run.py
```

(You may change the model to be used in the `run.py`. If you do not make any changes, `BiLSTM + Cross Attention + Focal Loss Model` shall run by default).


5. Google Colab demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1wB4y3CACGpKi_-S1IBsCHdQ1UeUnqu_U?usp=sharing)

## For Further Details:

For gaining further insight of our work, you may refer the following report compiled by us on this topic:
[Report](https://drive.google.com/file/d/1hcVhcThpI32Fr44aavsi0NXJ9N2NpxGF/view?usp=sharing)
