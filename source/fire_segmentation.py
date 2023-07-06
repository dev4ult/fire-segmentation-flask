import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from matplotlib import cm


def apply_threshold(image, thresh_val):
    _, thresholded = cv2.threshold(image, thresh_val, 255, cv2.THRESH_BINARY)
    return thresholded


def combinate_hsv_threshold(image):
    # convert the image in hsv
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h_channel, s_channel, v_channel = cv2.split(hsv_image)

    h_thresholded = apply_threshold(h_channel, 163)
    s_thresholded = apply_threshold(s_channel, 163)
    v_thresholded = apply_threshold(v_channel, 163)

    # Merging the thresholded channel
    thresholded_merged_channel = cv2.merge(
        (h_thresholded, s_thresholded, v_thresholded)
    )

    # Apply thresholding
    thresholded = apply_threshold(hsv_image, 163)

    return thresholded


def combinate_grayscale_threshold(image):
    # panggil method combinate_hsv_threshold
    hsv_threshold = combinate_hsv_threshold(image)

    # Convert HSV to grayscale
    grayscale_image = cv2.cvtColor(hsv_threshold, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    thresholded = apply_threshold(grayscale_image, 163)

    return thresholded


def contour(image):
    # panggil method combinate_grayscale_threshold
    grayscale_threshold = combinate_grayscale_threshold(image)

    # Find contours
    contours, _ = cv2.findContours(
        grayscale_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw contours on the image
    contour_image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    return contour_image


def open_morphology(image):
    # panggil method combinate_grayscale_threshold
    grayscale_threshold = combinate_grayscale_threshold(image)

    # Remove noise by median blur
    filtered_image = cv2.medianBlur(grayscale_threshold, 3)
    combined = filtered_image

    # Noise removal
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    opening = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel, iterations=2)

    return opening


def distance_transform(image):
    # panggil method morphologi_terbuka
    morfologi = open_morphology(image)

    # Sure foreground area
    dist_transform = cv2.distanceTransform(morfologi, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.01 * dist_transform.max(), 255, 0)

    sure_bg = cv2.subtract(morfologi, sure_fg.astype(np.uint8))

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # panggil method combinate_grayscale_threshold
    thresholded_image = combinate_grayscale_threshold(image)

    # Perform distance transform on the binary image
    distance_transform = cv2.distanceTransform(thresholded_image, cv2.DIST_L2, 3)

    return distance_transform


def segmentasi_watershed(image):
    # panggil method transformasi_jarak
    distance_transform = distance_transform(image)

    # panggil method combinate_grayscale_threshold
    thresholded_image = combinate_grayscale_threshold(image)

    # Find peaks in the distance transform
    # coordinates = peak_local_max(distance_transform, min_distance=9, labels=thresholded_image)
    coordinates = peak_local_max(
        distance_transform, min_distance=10, labels=thresholded_image
    )

    # Create markers for watershed segmentation
    markers = np.zeros(thresholded_image.shape, dtype=np.int32)
    for i in range(len(coordinates)):
        # markers[coordinates[i][0], coordinates[i][1]] = i + 1
        markers[coordinates[i][0], coordinates[i][1]] = i + 15

    # Perform watershed segmentation
    labels = watershed(-distance_transform, markers, mask=thresholded_image)

    # Tentukan rentang warna dari merah ke biru
    color_map = cm.get_cmap("cool")

    # Assign warna ke setiap piksel segmentasi berdasarkan jarak transformasi
    segmentation_color = np.zeros(image.shape, dtype=np.uint8)
    for i in range(np.max(labels)):
        color = color_map(i / np.max(labels))[:3]  # Ambil komponen RGB dari colormap
        color = tuple(int(c * 255) for c in color)  # Konversi nilai 0-1 ke 0-255
        x, y = np.where(
            labels == i + 1
        )  # Dapatkan koordinat piksel dengan label yang sesuai
        segmentation_color[x, y] = color

    # Berikan warna pada latar belakang
    background_color = (188, 159, 42)  # Warna kuning untuk latar belakang (format BGR)
    background_pixels = np.where(
        labels == 0
    )  # Dapatkan koordinat piksel latar belakang
    segmentation_color[background_pixels] = background_color

    return segmentation_color


def merged(image):
    # panggil method segmentasi_watershed
    segmentation_color = segmentasi_watershed(image)

    # panggil method segmentasi_watershed
    image_contour = contour(image)

    # Resize or crop image_contour to match the size of segmentation_color
    image_contour = cv2.resize(
        image_contour, (segmentation_color.shape[1], segmentation_color.shape[0])
    )

    # Gabungkan citra contour dengan citra segmentasi warna
    merged_image = cv2.addWeighted(segmentation_color, 0.7, image_contour, 0.3, 0)

    return merged_image
