# twitter-classifier

modified this line fewiufweuyfwefi

Take in a post from twitter/facebook/ and other social-media platforms and train the model to classify the text with an “importance scale”.  If the input consists of images, we add a tag with appropriate detail to the text input and hope the classifier rates the image tag higher.  Example tag [IMAGE, 1080x400, name of pic].
After we classify a text/post we can filter the collection of tweets and display the posts that are worth reading.
Input: text and other meta-data of the post
Output: either a Yes vs No or a numerical scale for how important the post is.


https://console.cloud.google.com/bigquery