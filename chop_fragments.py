import os
import glob
import shutil
# from scipy.ndimage import binary_fill_holes
import itertools
import numpy as np
import dippykit as dip
import matplotlib.pyplot as plt

from tqdm import tqdm

import cv2
from cv2 import INTER_AREA
from skimage import filters
from scipy.spatial import ConvexHull
from scipy.ndimage.morphology import binary_erosion


sin = lambda ang: np.sin(ang * np.pi / 180)
cos = lambda ang: np.cos(ang * np.pi / 180)
tan = lambda ang: sin(ang) / cos(ang)
default_frag_size = (128, 128)

dir_in = f'fragments/'
dir_out = f'chopped/'
if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

out_img = lambda img_id: f'{dir_out}/{img_id}.png'
out_frag = lambda img_id, n_frag: f'{dir_out}/frag_{img_id}_{n_frag}.jpg'

n_fragments = 10

_pix2pix_counter = 1
_pix2pix_marker_size = 5
_pix2pix_outsize = (256, 256)
_pix2pix_dir = 'data/processed/pix2pix_vase_fragments/train/'
out_pix2pix = lambda img_id, n_frag: f'{_pix2pix_dir}/frag_{img_id}_{n_frag}.jpg'
os.makedirs(_pix2pix_dir, exist_ok=True)


def contiguous(point, shape, range=1):
    # p_x = [point[0]-1, point[0], point[0]+1]
    # p_y = [point[1]-1, point[1], point[1]+1]

    p_x = np.ones((2*range+1), dtype=np.int32)*point[0]
    p_x += np.arange(-range, range+1)

    p_y = np.ones((2*range+1), dtype=np.int32)*point[1]
    p_y += np.arange(-range, range+1)

    p_x = [p for p in p_x if 0 <= p < shape[0]]
    p_y = [p for p in p_y if 0 <= p < shape[1]]
    points = list(itertools.product(p_x, p_y))
    return points


def space_fill(img, start=None, ):
    if start is None:
        start = img.shape[0] // 2, img.shape[1] // 2

    # mask = np.zeros(img.shape, dtype=int) - 1
    # max_count = 10
    # mask[start] = max_count

    thresh = np.percentile(img, 95)

    # mask2 = np.zeros(img.shape, dtype=bool)
    # details = img > thresh
    # mask2[details] = 1
    mask = img > thresh

    # trim = 25
    # make this general to image shape, not just 512x512
    trim = img.shape[0] // 20
    mask[:trim, :] = 0
    mask[-trim:, :] = 0
    mask[:, :trim] = 0
    mask[:, -trim:] = 0

    mask_inds = np.argwhere(mask)
    m_min = np.min(mask_inds[:, 0])
    m_max = np.max(mask_inds[:, 0])
    n_min = np.min(mask_inds[:, 1])
    n_max = np.max(mask_inds[:, 1])
    print(m_min, m_max, n_min, n_max)
    return mask, m_min, m_max, n_min, n_max

    # this takes awhile, I can do simpler
    # max_range = 10
    # final_mask = np.zeros(img.shape, dtype=bool)
    # for m, n in np.ndindex(mask.shape):
    #     for i, j in contiguous((m, n), mask.shape, max_range):
    #         if mask[i, j]:
    #             final_mask[m, n] = 1
    #             break

    # final_mask = binary_fill_holes(final_mask)
    # return final_mask

def mark_image_box(img, m_min, m_max, n_min, n_max):
    new_img = np.copy(img)
    thick=5
    for m in m_min, m_max:
        # new_img[m-thick:m+thick, n_min:n_max, :] = (255, 0, 0)
        new_img[m-thick:m+thick, n_min:n_max] = 255
    for n in n_min, n_max:
        # new_img[m_min:m_max, n-thick:n+thick, :] = (255, 0, 0)
        new_img[m_min:m_max, n-thick:n+thick] = 255
    return new_img


def isInHull(P,hull):
    '''
    Datermine if the list of points P lies inside the hull
    :return: list
    List of boolean where true means that the point is inside the convex hull
    '''
    A = hull.equations[:,0:-1]
    b = np.transpose(np.array([hull.equations[:,-1]]))
    isInHull = np.all((A @ np.transpose(P)) <= np.tile(-b,(1,len(P))),axis=0)
    return isInHull


def main_site_vasegen():
    for f_img in tqdm(glob.glob(dir_in + '/*')):
        try:
            img = dip.imread(f_img)
        except:
            continue
        img_id = int(os.path.split(f_img)[-1].split('.')[0])
        # img_out = dip.resize(img, _pix2pix_outsize, interpolation=INTER_AREA)
        print(f_img, img.shape)
        if len(img.shape) == 3:
            gray = np.mean(img, axis=-1)
        else:
            # gray = img
            continue
        grad = dip.transforms.edge_detect(gray)
        mask, m_min, m_max, n_min, n_max = space_fill(grad)
        trimx = grad.shape[0] // 20
        trimy = grad.shape[1] // 20
        grad[:trimx, :] = 0
        grad[-trimx:, :] = 0
        grad[:, :trimy] = 0
        grad[:, -trimy:] = 0
        markerx = _pix2pix_marker_size * (grad.shape[0]) // _pix2pix_outsize[0] // 2
        markery = _pix2pix_marker_size * (grad.shape[1]) // _pix2pix_outsize[1] // 2

        grad_top = grad > np.percentile(grad, 99)
        border_inds = np.argwhere(grad_top)
        hull = ConvexHull(border_inds)
        _frag_context = np.zeros_like(grad_top)

        mm = list(np.ndindex(_frag_context.shape[:2]))
        out_hull = isInHull(mm, hull)
        mm = np.array(mm)[out_hull]
        # print(mm)
        # input(out_hull)
        _frag_context = np.stack([255*~_frag_context]*3 + [_frag_context], axis=-1).astype(np.uint8)
        _frag_context[mm[:, 0], mm[:, 1], :3] = img[mm[:, 0], mm[:, 1]]
        _frag_context[mm[:, 0], mm[:, 1], 3] = 255
        dip.im_write(_frag_context, out_img(img_id))

        # plt.imshow(_frag_context)
        # plt.show()

if __name__ == '__main__':
    main_site_vasegen()
