# Revisiting Underwater Image Enhancement for Object Detection: A Unified Quality–Detection Evaluation Framework

**Abstract:** Underwater images often suffer from severe color distortion, low contrast, and reduced visibility, motivating the widespread use of image enhancement as a preprocessing step for downstream computer vision tasks. However, recent studies have questioned whether enhancement actually improves object detection performance. In this work, we conduct a comprehensive and rigorous evaluation of nine state-of-the-art enhancement methods and their interactions with modern object detectors. We propose a unified evaluation framework that integrates (1) a distribution-level quality assessment using a composite quality index (Q-index), (2) a fine-grained per-image detection protocol based on COCO-style mAP, and (3) a mixed-set upper-bound analysis that quantifies the theoretical performance achievable through ideal selective enhancement. Our findings reveal that traditional image quality metrics do not reliably predict detection performance, and that dataset-level conclusions often overlook substantial image-level variability. Through per-image evaluation, we identify numerous cases in which enhancement significantly improves detection accuracy—primarily for low-quality inputs—while also demonstrating conditions under which enhancement degrades performance. The mixed-set analysis shows that selective enhancement can yield substantial gains over both original and fully enhanced datasets, establishing a new direction for designing enhancement models optimized for downstream vision tasks. This study provides the most comprehensive evidence to date that underwater image enhancement can be beneficial for object detection when evaluated at the appropriate granularity and guided by informed selection strategies. The data generated and code developed are publicly available.

**Codes:**

* Q-index_final MATLAB file: to calculate the Quality Index (Q-index) using some image enhancement metrics, outlier removal, and global rescaling.
* Q-mAp-Grid-images Python file: to generate a figure of random images belonging to different quality bins from different enhancers.
* Dashed_rectangle_YOLO_addition Python file: to visualize the ground truth (as dashed lines) alongside the detections in the SuperGradients library for YOLO.

**Data links:**

* Enhanced versions of the CUPDD dataset using 9 underwater image enhancement algorithms:
  * https://drive.google.com/file/d/1yX86I6AM_Dqts5oevFtF7tSzImbU-mzz/view?usp=sharing

* Enhanced versions of the RUOD dataset using 9 underwater image enhancement algorithms:
  * [https://drive.google.com/open?id=1-w-HB9AdblaEbr_1cP1sz59EFBgG6QM5&usp=drive_fs](https://drive.google.com/file/d/1wG7nW_5ol1w7SUJjKdfFsDw64qDa7RLn/view?usp=sharing)

* Trained YOLO-NAS object detection models on the CUPDD dataset (1 on the original images + 9 using enhanced versions) (please use the SuperGrdainet implementation with the Large YOLO architecture):
  * https://drive.google.com/drive/folders/1jlwfmiuMJ_zIlTRDHhZRAARzekmSf7hS?usp=sharing

* Trained YOLO-NAS object detection models on the RUOD dataset (1 on the original images + 9 using enhanced versions) (please use the SuperGrdainet implementation with the Large YOLO architecture):
  * [https://drive.google.com/file/d/1-wE2tpK9-Hx-L0aFYTjasN01bXKBm-ig/view?usp=drive_link](https://drive.google.com/drive/folders/12LFugM50L-r1wmVgZMvJrplAllEr7oTF?usp=sharing)

**Some figures:**

![](Figs/Q_index_Alg.png) Fig.1 The algorithm for calculating the Q-index.

![](Figs/Enh_RUOD.jpeg) Fig.2 Randomly selected Original images from each available quality bin of RUOD dataset. The corresponding Q-index values are color-mapped and placed under each image.

![](Figs/Max_Enh_RUOD.jpeg) Fig.3 Cases where enhancers revealed hidden objects that went unnoticed by the human annotator on RUOD dataset. The ground truth bounding boxes are visualized on each image as dotted bounding boxes. The color-mapped values next to images represent Q-index.

**Please cite this paper reference:**

@Article{jimaging12010018,
AUTHOR = {Awad, Ali and Saleem, Ashraf and Paheding, Sidike and Lucas, Evan and Al-Ratrout, Serein and Havens, Timothy C.},
TITLE = {Revisiting Underwater Image Enhancement for Object Detection: A Unified Quality–Detection Evaluation Framework},
JOURNAL = {Journal of Imaging},
VOLUME = {12},
YEAR = {2026},
NUMBER = {1},
ARTICLE-NUMBER = {18},
URL = {https://www.mdpi.com/2313-433X/12/1/18},
ISSN = {2313-433X},
DOI = {10.3390/jimaging12010018}
}





