I initally had problems with loss becoming "nan" and the accuracy dropping to virtually 0,
but I found that the problem could be fixed by changing the activation on the final layer
to "softmax" from "relu".

In terms of pooling and convolution, I found that adding a third layer didn't help too
much and had minimal, if any, impact on the results.

I did a lot of expirementation with adding more layers and the number of units per layer,
and found that generally, more units means a faster learning rate, but does not necessairly 
mean better final results. Generally, the accuracy will plateau at around 95-96%, even after
letting the ai run for up to 30 epochs. Another interesting thing I found was that with more 
layers(4) and given enough time, the trainning accuracy will reach up to 99%, but the testing
data will show much lower results(~93%). I think this is due to overfitting with so many units
involved. Another feature to note is that with more net units(whether it be from more layers or
units/layer, trainning does take longer).

My final neural network consited of 2 layers of 128 units each and was able to consistently 
reach 96% accuracy for the testing results.
