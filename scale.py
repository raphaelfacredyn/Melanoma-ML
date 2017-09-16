from PIL import Image
import os
import progressbar

paths = ["validation", "test", "train"]
newSize = (512, 512)

for path in paths:
    dirs = os.listdir(path)

    def scale(image, max_size, method=Image.ANTIALIAS):
        """
        resize 'image' to 'max_size' keeping the aspect ratio
        and place it in center of white 'max_size' image
        """
        im_aspect = float(image.size[0]) / float(image.size[1])
        out_aspect = float(max_size[0]) / float(max_size[1])
        if im_aspect >= out_aspect:
            scaled = image.resize(
                (max_size[0],
                 int((float(max_size[0]) / im_aspect) + 0.5)), method)
        else:
            scaled = image.resize((int((float(max_size[1]) * im_aspect) + 0.5),
                                   max_size[1]), method)

        offset = (((max_size[0] - scaled.size[0]) / 2),
                  ((max_size[1] - scaled.size[1]) / 2))
        back = Image.new("RGB", max_size, "black")
        back.paste(scaled, offset)
        return back

    pbar = progressbar.ProgressBar()
    for item in pbar(dirs):
        if os.path.isfile(path + "/" + item) and ("jpg" in (path + item)
                                                  or "jpeg" in (path + item)
                                                  or "png" in (path + item)):
            im = Image.open(path + "/" + item)
            imResize = scale(im, newSize)
            imResize.save(path + "_resized/" + item, 'JPEG', quality=90)
