"""
The Hysteresis code was adapted from the sample code associated with the book Automating the Analysis
of Spatial Grids by Valliapa Lakshmanan. The original Java code can be found at:
https://github.com/lakshmanok/asgbook/blob/master/src/edu/ou/asgbook/segmentation/HysteresisSegmenter.java
"""

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('agg')
import numpy as np
from scipy.ndimage import label, maximum, gaussian_filter, find_objects


class Hysteresis(object):
    """
    Object segmentation method that identifies objects as contiguous areas with all pixels above a low
    threshold and contain at least one pixel above a high threshold.

    :param low_thresh: lower threshold value
    :param high_thresh: higher threshold value
    """
    def __init__(self, low_thresh, high_thresh):
        self.low_thresh = low_thresh
        self.high_thresh = high_thresh
        return

    def label(self, input_grid):
        """
        Label input grid with hysteresis method.

        :param input_grid: 2D array of values.
        :return: Labeled output grid.
        """
        unset = 0 
        high_labels, num_labels = label(input_grid > self.high_thresh)
        region_ranking = np.argsort(maximum(input_grid, high_labels, index=np.arange(1, num_labels + 1)))[::-1]
        output_grid = np.zeros(input_grid.shape,dtype=int)
        stack = []
        for rank in region_ranking:
            label_num = rank + 1
            label_i, label_j = np.where(high_labels == label_num)
            for i in range(label_i.size):
                if output_grid[label_i[i],label_j[i]] == unset:
                    stack.append((label_i[i], label_j[i]))
            while len(stack) > 0:
                index = stack.pop()
                output_grid[index] = label_num
                for i in range(index[0] - 1, index[0] + 2):
                    for j in range(index[1] - 1, index[1] + 2):
                        if (input_grid[i, j] > self.low_thresh) and (output_grid[i, j] == unset):
                            stack.append((i, j))
        return output_grid

    def size_filter(self, labeled_grid, min_size):
        """
        Remove labeled objects that do not meet size threshold criteria.

        :param labeled_grid: 2D output from label method.
        :param min_size: minimum size of object in pixels. 
        :return: labeled grid with smaller objects removed.
        """
        out_grid = np.zeros(labeled_grid.shape,dtype=int)
        slices = find_objects(labeled_grid)
        j = 1
        for i,s in enumerate(slices):
            box = labeled_grid[s]
            size = np.count_nonzero(box.flatten()==i+1)
            if size >= min_size and box.shape[0] > 1 and box.shape[1] > 1:
                out_grid[np.nonzero(labeled_grid==i+1)] = j
                j += 1
        return out_grid
