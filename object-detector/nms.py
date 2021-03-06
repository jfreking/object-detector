import numpy as np

def overlapping_area(detection_1, detection_2):
    '''
    Function to calculate overlapping area'si
    `detection_1` and `detection_2` are 2 detections whose area
    of overlap needs to be found out.
    Each detection is list in the format ->
    [x-top-left, y-top-left, confidence-of-detections, width-of-detection, height-of-detection]
    The function returns a value between 0 and 1,
    which represents the area of overlap.
    0 is no overlap and 1 is complete overlap.
    Area calculated from ->
    http://math.stackexchange.com/questions/99565/simplest-way-to-calculate-the-intersect-area-of-two-rectangles
    '''
    # Calculate the x-y co-ordinates of the 
    # rectangles
    x1_tl = detection_1[0]
    x2_tl = detection_2[0]
    
    x1_br = detection_1[0] + detection_1[3]
    x2_br = detection_2[0] + detection_2[3]
    
    y1_tl = detection_1[1]
    y2_tl = detection_2[1]
    
    y1_br = detection_1[1] + detection_1[4]
    y2_br = detection_2[1] + detection_2[4]
    
    # Calculate the overlapping Area
    x_overlap = max(0, min(x1_br, x2_br)-max(x1_tl, x2_tl))
    y_overlap = max(0, min(y1_br, y2_br)-max(y1_tl, y2_tl))
    overlap_area = x_overlap * y_overlap
    area_1 = detection_1[3] * detection_2[4]
    area_2 = detection_2[3] * detection_2[4]
    total_area = area_1 + area_2 - overlap_area
    return overlap_area / float(total_area)

def nms(detections, threshold=.5):
    '''
    This function performs Non-Maxima Suppression.
    `detections` consists of a list of detections.
    Each detection is in the format ->
    [x-top-left, y-top-left, confidence-of-detections, width-of-detection, height-of-detection]
    If the area of overlap is greater than the `threshold`,
    the area with the lower confidence score is removed.
    The output is a list of detections.
    '''
    if len(detections) == 0:
	    return []
    detections = np.array(detections)
    
    x1 = detections[:,0]
    y1 = detections[:,1]
    x2 = detections[:,3]
    y2 = detections[:,4]
	
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    # Sort the detections based on confidence score
    #detections = sorted(detections, key=lambda detections: detections[2],reverse=True)
    
    idxs = np.argsort(y2)
    # Unique detections will be appended to this list
    new_detections=[]
    
    # Append the first detection
    #new_detections.append(detections[0])
    
    # Remove the detection from the original list
    #del detections[0]
    
    # For each detection, calculate the overlapping area
    # and if area of overlap is less than the threshold set
    # for the detections in `new_detections`, append the 
    # detection to `new_detections`.
    
    # In either case, remove the detection from `detections` list.
    while len(idxs) >= 0:
        last = len(idxs)-1
        i = idxs[last]
        new_detections.append(i)
        
        # find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
 
		# compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
 
		# delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],np.where(overlap > threshold)[0])))
 
	# return only the bounding boxes that were picked using the
	# integer data type
	return detections[new_detections].astype("int")
        
    """
    for index, detection in enumerate(detections):
        for new_detection in new_detections:
            if overlapping_area(detection, new_detection) > threshold:
                del detections[index]
                break
        else:
            new_detections.append(detection)
            del detections[index]
    return new_detections
    """
if __name__ == "__main__":
    # Example of how to use the NMS Module
    detections = [[31, 31, .9, 10, 10], [31, 31, .12, 10, 10], [100, 34, .8,10, 10]]
    print "Detections before NMS = {}".format(detections)
    print "Detections after NMS = {}".format(nms(detections))
