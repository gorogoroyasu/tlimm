class Processor:
    def __init__(self, image, boxes, labels, internal, cut_size=(300, 300)):
        self.image = image
        self.boxes = boxes
        self.labels = labels
        self.internal = internal
        self.cut_size = cut_size
        self.cut_image()
        self.cut_images = self.cut_image()
        self.cut_bboxes, self.cut_labels = self.bboxes_and_labels()
        self.cis, self.cbs, self.cls = self.drop_empty_pictures

    @property
    def cut_image_with_info(self):
        for i, _ in enumerate(self.cis):
            yield self.cis[i], self.cbs[i], self.cls[i]

    def drop_empty_pictures(self):
        # cut images
        cis = []
        # cut bboxes
        cbs = []
        # cut labels
        cls = []
        assert len(self.cut_labels) == len(self.cut_bboxes) == len(self.cut_images)
        for i, b in enumerate(self.cut_labels):
            if len(b) != 0:
                cis.append(self.cut_images[i])
                cbs.append(self.cut_bboxes[i])
                cls.append(self.cut_labels[i])

        return cis, cbs, cls

    def image_cut_rules(self):
        h, w, _ = self.image.shape
        cut_h, cut_w = self.cut_size

        for dh in range((h // cut_h) - 1):
            for dw in range((w // cut_w) - 1):
                ch = dh * cut_h
                cw = dw * cut_w
                yield ch, ch + dh, cw, cw + dw

    def cut_image(self):
        """
        cut image
        :return:
        """
        cut_img = dict()
        for count, (ch, ch_next, cw, cw_next) in enumerate(self.image_cut_rules()):
            if count not in cut_img.keys():
                cut_img[count] = []
            cut_img[count] = self.image[ch:ch_next, cw:cw_next]

        return cut_img

    def bboxes_and_labels(self):
        """
        cut bboxes and labels
        TODO: should be better
        :return:
        """

        box = {}
        label = {}
        for count, picture_coordinate in enumerate(self.image_cut_rules()):
            for boxes, labels in zip(self.boxes, self.labels):
                bx1, bx2, by1, by2 = boxes['x1'], boxes['x2'], boxes['y1'], boxes['y2']

                if self.in_cur_picture(picture_coordinate, (bx1, bx2, by1, by2)):
                    if count not in box.keys():
                        box[count] = []
                        label[count] = []
                    box[count].append(boxes)
                    label[count].append(labels)

        return box, label

    @staticmethod
    def between(p1, p2, target):
        return p1 <= target, p2

    def in_cur_picture(self, picture_position, bbox_coordinate):
        px1, px2, py1, py2 = picture_position
        bx1, bx2, by1, by2 = bbox_coordinate

        if self.internal:
            """
            (px1, py1)
            |----------------------|
            |    (bx1, by1)        |
            |         |---|        |
            |         |   |        |
            |         |   |        |
            |         |   |        |
            |         |---|        |
            |          (bx2, by2)  |
            |                      |
            |----------------------| (px2, py2)
            
            """
            if bx1 <= px1:
                return False
            if bx2 >= px2:
                return False
            if by1 <= py1:
                return False
            if by2 >= py2:
                return False

            return True
        """
        (px1, py1)
        |----------------------|
        |                      |
        |               (bx1, by1)
        |                  |-------|
        |                  |       |
        |                  |       |
        |                  |       |
        |                  |       |
        |                  |       |
        |                  |-------|
        |                      |    (bx2, by2)
        |                      |
        |----------------------| (px2, py2)
        """

        if self.between(px1, px2, bx1) and self.between(py1, py2, by1):
            return True

        if self.between(px1, px2, bx1) and self.between(py1, py2, by2):
            return True

        if self.between(px1, px2, bx2) and self.between(py1, py2, by1):
            return True

        if self.between(px1, px2, bx2) and self.between(py1, py2, by2):
            return True

        return False
