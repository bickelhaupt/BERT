# Natural Language Processing with Bi-directional Encoder Representation of Transformers (BERT) & Applications of Twitter Stock Movement Prediction

# Keras Final Model:
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_word_ids (InputLayer)     [(None, 157)]        0                                            
__________________________________________________________________________________________________
input_mask (InputLayer)         [(None, 157)]        0                                            
__________________________________________________________________________________________________
segment_ids (InputLayer)        [(None, 157)]        0                                            
__________________________________________________________________________________________________
keras_layer (KerasLayer)        [(None, 768), (None, 177853441   input_word_ids[0][0]             
                                                                 input_mask[0][0]                 
                                                                 segment_ids[0][0]                
__________________________________________________________________________________________________
additional_feature (InputLayer) [(None, 7)]          0                                            
__________________________________________________________________________________________________
pooled_with_additional (Concate (None, 775)          0           keras_layer[0][0]                
                                                                 additional_feature[0][0]         
__________________________________________________________________________________________________
dropout (Dropout)               (None, 775)          0           pooled_with_additional[0][0]     
__________________________________________________________________________________________________
output (Dense)                  (None, 2)            1552        dropout[0][0]                    
==================================================================================================
Total params: 177,854,993
Trainable params: 177,854,992
Non-trainable params: 1


# Data Source:
       https://www.tensorflow.org/datasets/catalog/sentiment140

# Model Source:
        https://github.com/adam0ling/twitter_sentiment/blob/main/4_MODIFIED_BERT.ipynb

# Application (WebAPI) Data Source
       https://github.com/eramoska1/CapstoneProject       

