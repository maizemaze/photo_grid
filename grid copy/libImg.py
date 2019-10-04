from scipy.signal import convolve2d
from scipy.signal import find_peaks
import numpy as np

def doKMeans(img, k=3, features=[0]):
    """
    ----------
    Parameters
    ----------
    """

    # data type conversion for opencv
    ## select features
    img = img[:, :, features].copy()
    ## standardize
    img_max, img_min = img.max(axis=(0, 1)), img.min(axis=(0, 1))-(1e-8)
    img = (img-img_min)/(img_max-img_min)
    ## convert to float32
    img_z = img.reshape((-1, img.shape[2])).astype(np.float32)
    
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
    param_k = dict(data=img_z,
                   K=k,
                   bestLabels=None,
                   criteria=criteria,
                   attempts=30,
                   flags=cv2.KMEANS_PP_CENTERS)
    
    # KMEANS_RANDOM_CENTERS
    _, img_k_temp, center = cv2.kmeans(**param_k)
    
    # Convert back
    img_k = img_k_temp.astype(np.uint8).reshape((img.shape[0], -1))
    
    # return
    return img_k, center

def smoothImg(image, n):
    """
    ----------
    Parameters
    ----------
    """

    kernel = np.array((
            [1, 4, 1],
            [4, 9, 4],
            [1, 4, 1]), dtype='int')/29
   
    for i in range(n):
        image = convolve2d(image, kernel, mode='same')

    return image

def binarizeSmImg(image, cutoff=0.5):
    """
    ----------
    Parameters
    ----------
    """
    imgOut = image.copy()
    imgOut[image > cutoff] = 1
    imgOut[image <= cutoff] = 0

    return imgOut.astype(np.int)

def cropImg(img, pts):
    """
    ----------
    Parameters
    ----------
    img : str
          path to the image file 
    pts : list of 2-tuple
          each tuple is a coordinate (x, y)
    -------
    Returns
    -------
    npImg : 3-d ndarray encoded in UINT8

    """

    # convert to opencv cpmatitable
    pts = np.array(pts).astype(np.float32)
    # find four corners
    token = True
    while token:
        try:
            order_x = np.argsort([pts[i, 0] for i in range(4)])
            order_y = np.argsort([pts[i, 1] for i in range(4)])
            pt_NW = pts[order_x[:2][np.isin(order_x[:2], order_y[:2])][0]]
            pt_SW = pts[order_x[:2][np.isin(order_x[:2], order_y[2:])][0]]
            pt_NE = pts[order_x[2:][np.isin(order_x[2:], order_y[:2])][0]]
            pt_SE = pts[order_x[2:][np.isin(order_x[2:], order_y[2:])][0]]
            token = False
        except:
            pts = rotatePts(pts, 15)
    # generate sorted source point
    pts = np.array([pt_NW, pt_NE, pt_SW, pt_SE])
    # estimate output dimension
    img_W = (sum((pt_NE-pt_NW)**2)**(1/2)+sum((pt_SE-pt_SW)**2)**(1/2))/2
    img_H = (sum((pt_SE-pt_NE)**2)**(1/2)+sum((pt_SW-pt_NW)**2)**(1/2))/2
    while (img_W > 1500):
        img_W /= 2
        img_H /= 2
    shape = (int(img_W), int(img_H))
    # generate target point
    pts2 = np.float32(
        [[0, 0], [shape[0], 0], [0, shape[1]], [shape[0], shape[1]]])
    # transformation
    M = cv2.getPerspectiveTransform(pts, pts2)
    dst = cv2.warpPerspective(img, M, (shape[0], shape[1]))
    dst = np.array(dst).astype(np.uint8)

    return dst

def rotatePts(pts, angle):
    """
    ----------
    Parameters
    ----------
    """
    ptx = np.array([pts[i, 0] for i in range(len(pts))])
    pty = np.array([pts[i, 1] for i in range(len(pts))])
    qx = math.cos(math.radians(angle))*(ptx) - \
        math.sin(math.radians(angle))*(pty)
    qy = math.sin(math.radians(angle))*(ptx) + \
        math.cos(math.radians(angle))*(pty)
    qpts = [[qx[i], qy[i]] for i in range(len(pts))]
    return np.array(qpts)

def findPeaks(img, nPeaks=0, axis=0, nSmooth=100):
    """
    ----------
    Parameters
    ----------
    """
    
    # compute 1-D signal
    signal = img.mean(axis=(not axis)*1) # 0:nrow
    # gaussian smooth 
    for i in range(nSmooth):
        signal = np.convolve(
            np.array([1, 2, 4, 2, 1])/10, signal, mode='same')
    peaks, _ = find_peaks(signal)
    if nPeaks != 0:
        if len(peaks) > nPeaks:
            while len(peaks) > nPeaks:
                ls_diff = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
                idx_diff = np.argmin(ls_diff)
                idx_kick = idx_diff if (
                    signal[peaks[idx_diff]] < signal[peaks[idx_diff+1]]) else (idx_diff+1)
                peaks = np.delete(peaks, idx_kick)
        elif len(peaks) < nPeaks:
            while len(peaks) < nPeaks:
                ls_diff = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
                idx_diff = np.argmax(ls_diff)
                peak_insert = (peaks[idx_diff]+peaks[idx_diff+1])/2
                peaks = np.sort(np.append(peaks, int(peak_insert)))

    return peaks, signal
