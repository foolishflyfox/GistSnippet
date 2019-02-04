# 对一幅灰度图像进行直方图均衡化
def myhisteq(im, nbr_bins=256):
    """
    @im: PIL.Image.Image, mode is L
    @return: PIL.Image.Image
    """
    np_im = np.asarray(im)
    imhist, bins = np.histogram(np_im.flatten(), nbr_bins)
    csum = np.cumsum(imhist)
    csum = 255 * csum / csum[-1]
    new_np_im = np.interp(np_im.flatten(), bins[:-1], csum)
    return Image.fromarray(new_np_im.reshape(np_im.shape).astype(np.uint8))
  
  