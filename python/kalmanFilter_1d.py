
# Write a program that will iteratively update and
# predict based on the location measurements
# and inferred motions shown below.

#update measurement(mean, var=sigma^2) using previous measurement [mean1, var1] and new measurement [mean2, var2]
def update(mean1, var1, mean2, var2):
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return [new_mean, new_var]

#predict, current belief[mean1, var1] + new motion [mean2, var2]
#
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0
sig = 10000

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

# Insert code here
if len(measurements)!= len(motion):
    raise ValueError,"Error"

for k in range(len(measurements)):
    [mu,sig]=update(mu,sig, measurements[k], measurement_sig)
    print "update ",mu, sig
    [mu,sig]=predict(mu, sig, motion[k], motion_sig)
    print "predict ",mu,sig

print [mu, sig]
