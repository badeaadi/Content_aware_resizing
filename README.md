# Content_aware_resizing
Seam-carving for content-aware image resizing based on https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf




## Width decrease 

- Original image

![](originals/castel.jpg)

- Width decrease using OpenCV

![](img/castel_openCV.png)

- Width decrease using our algorithm

![](img/castel_micsoreazaLatime.png)

## Height decrease


- Original image

![](originals/praga.jpg)

- Height decrease using OpenCV

![](img/praga_opencv.png)

- Height decrease using our algorithm

![](img/praga_micsoreazaInaltime.png)


## Content amplification (using enlarging and then width/height decrease)

- Original 

![](originals/arcTriumf.jpg)

- Content amplification using our algorithm

![](img/arcTriumf_amplificaContinut.png)


## Object elimination using ROI (Region of interest)

- Original image

![](originals/lac.jpg)

- Examples of object elimination:

![](img/lac_eliminaObiect1.png)

![](img/lac_eliminaObiect2.png)
