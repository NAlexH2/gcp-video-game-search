from google.cloud import vision

def analyze_box_art(file_url) -> vision.EntityAnnotation:

    if "nocover.png" not in file_url:
        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        image = vision.Image()
        image.source.image_uri = file_url

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        label_arr = []
        for label in labels:
            label_arr.append(label.description)

        label_arr = ", ".join(label_arr)
        return label_arr
    else:
        return "No alt text available"
    