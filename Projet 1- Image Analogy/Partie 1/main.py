import numpy as np
import cv2
import analogy
import time

"""
Frame work for looping through make_analogy
Parameters:
A.jpg, Ap.jpg, B.jpg : Inputs into the framework. Will attempt to create novel image Bp.
remap_A : specifies whether an attempt should be made to normalize the luminance of A and Ap to B. Can help with
            artifacting with images of noticeably different luminance averages.
pyr_levels : number of Gaussian pyramids to iterate along. Increases expression of low frequency features.
kappa : coherence weight, refer to Hertzmann paper for some suggested values
search_method : each works well. Three are implemented: pyflann_kmeans, pyflann_kdtree, and sk_nn. kmeans iterations 
                is set to reach convergence. If you want to speed up kmeans you may want to change it to 7-10. kdtree
                is probably the fastest, sk_nn is the slowest.
type : two types are implemented. The default is luminance since the paper predominantly did its work only in the
        luminance domain. The color setting lets you apply the color from textures and colorize grayscale features.
                 
"""


"""  Start User Defined Inputs  """
remap_A = 1 # est ce que on normalise la luminance ou pas 
pyr_levels = 5
kappa = 0
# method can be pyflann_kmeans, pyflann_kdtree or sk_nn, default:pyflann_kmeans
search_method = 'pyflann_kdtree'
# type can be luminance or color, most effects work with luminance. Texture synthesis works well with color
# default:luminance
type = 'luminance'
additional_pairs = False
# type the path of your images here. You can change the output path at the bottom
imgA, imgAp, imgB = analogy.read_images("Images/A1.jpg", "Images/Ap1.jpg", "Images/B1.jpg")

if additional_pairs:  # add/remove a line for each pair you want to cat to A and Ap for training on a single loop
    imgA, imgAp = analogy.add_pairs(imgA, imgAp, "Images/A2.jpg", "Images/Ap2.jpg")
    imgA, imgAp = analogy.add_pairs(imgA, imgAp, "Images/A3.jpg", "Images/Ap3.jpg")
"""  End User Defined Inputs  """

start_time = time.time()

# initialize pyramids (denoted by _L)
if type == 'luminance': #deja la on a plusieurs img level 
    A_L = analogy.get_pyramid(analogy.rgb2yiq(imgA), pyr_levels)
    B_L = analogy.get_pyramid(analogy.rgb2yiq(imgB, feature='yiq'), pyr_levels)
    Ap_L = analogy.get_pyramid(analogy.rgb2yiq(imgAp, feature='yiq'), pyr_levels)
elif type == 'color':
    A_L = analogy.get_pyramid(imgA, pyr_levels)
    B_L = analogy.get_pyramid(imgB, pyr_levels)
    Ap_L = analogy.get_pyramid(imgAp, pyr_levels)



Bp_L = []
s = []
# this loop initializes Bp_L with empty arrays and s with arrays
#  filled with -1 for each level of the image pyramid. These arrays
#  will later be populated with 
# values as the algorithm progresses through the pyramid levels.

for i in range(len(B_L)): #each level of the pyramide 
    Bp_L.append(np.zeros(B_L[i].shape))
    s.append(np.zeros((B_L[i].shape[0],B_L[i].shape[1],2))-1)

print(Bp_L)

# process pyramid from coursest to finest
for lvl in range(pyr_levels, -1, -1):
    print("Starting Level: ", lvl, "of ", pyr_levels)

    if type == 'luminance':
        Bp_L[lvl] = analogy.make_analogy(lvl, pyr_levels, A_L, Ap_L, B_L, Bp_L, s, kappa, search_method)
        Bp_int = np.uint8(Bp_L[lvl][:, :, 0].copy() * 255)
        cv2.imshow("bp", Bp_int)
        cv2.waitKey(1)
        imgBp = analogy.yiq2rgb(Bp_L[lvl])

    elif type == 'color':
        Bp_L[lvl] = analogy.make_analogy_color(lvl, pyr_levels, A_L, Ap_L, B_L, Bp_L, s, kappa, search_method)
        Bp_int = np.uint8(Bp_L[lvl].copy() * 255)
        cv2.imshow("bp", Bp_int)
        cv2.waitKey(1)
        imgBp = Bp_L[lvl]

    imgBp = imgBp * 255.0
    imgBp[imgBp > 255] = 255
    imgBp[imgBp < 0] = 0
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time} seconds")

    # write_name = 'out/Bp_PyrLvl-'+str(lvl)+'.jpg'
    # cv2.imwrite(write_name, imgBp)
cv2.imwrite("Images/Bp.jpg", imgBp)



