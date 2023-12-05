from google.cloud import vision


# This function is a modified starter code from Google, directly.
# It takes an image, processes it (surprisingly quick too!) then generates a
# a string for the alt text the images can use.
def analyze_box_art(file_url) -> vision.EntityAnnotation:

    # If the image is actually real (not titled with nocover.png), we can
    # have the AI process the image and provide labels
    if "nocover.png" not in file_url:
        
        # Instantiates a client. This happens in a unique way. GCP can do this
        # natively no problem, but local debugging requires an addition key to
        # successfully make that handshake with the Vision AI.
        client = vision.ImageAnnotatorClient()

        image = vision.Image()
        image.source.image_uri = file_url

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        label_arr = []
        for label in labels:
            label_arr.append(label.description)

        # Eventually, we can make one big string for the images to use instead
        # of struggling to parse an array of strings in the jinja template.
        label_arr = ", ".join(label_arr)
        
        # return it to be used! It gets inserted into the cover json property
        # for each game
        return label_arr 
    else:
        return "No alt text available"
    