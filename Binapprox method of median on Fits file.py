import 'Wilford's Method.py' as running_stats
from numpy import *
from astropy.io import fits
# Write your median_bins_fits and median_approx_fits here:
def median_bins_fits(imgs, b):
  mean, std = running_stats(imgs)
  dim = mean.shape
  left_bin = zeros(dim)
  bins = zeros((dim[0], dim[1], b))
  bin_width = (2 * std) / b
  
  for i in imgs:
    hsulist = fits.open(i)
    data = hsulist[0].data
    for i in range(dim[0]):
      for j in range(dim[1]):
        val = data[i,j]
        val_mean = mean[i,j]
        val_std = std[i,j]
        
        if val < val_mean - val_std :
          left_bin[i,j] += 1
        elif val >= val_mean - val_std and val < val_mean + val_std:
          bin = int((val - (val_mean - val_std))/bin_width[i,j])
          bins[i,j,bin] += 1
  return mean,std, left_bin, bins 

def median_approx_fits(imgs, b):
  mean, std, left_bin, bins = median_bins_fits(imgs, b)
  dim = mean.shape
  N = len(imgs)
  mid = (N+1)/2
  bin_width = (2*std)/b
  
  median = zeros(dim)
  for i in range(dim[0]):
    for j in range(dim[1]):
      count = left_bin[i,j]
      for k, kcount in enumerate(bins[i,j]):
        count += kcount
        if count >= mid:
          break
      median[i,j] = mean[i,j] - std[i,j] + bin_width[i,j]*(k+0.5)
  return median 
