// Imports the Google Cloud Video Intelligence library
const Video = require("@google-cloud/video-intelligence");
const env = require("dotenv").config();

async function main() {
  // Creates a client
  const video = new Video.VideoIntelligenceServiceClient();

  // Replace this with the URI of your video in Google Cloud Storage
  const gcsUri = "gs://lightworkarabicseason/v.mp4";

  const request = {
    inputUri: gcsUri,
    features: ["TEXT_DETECTION"],
  };

  // Detects text in a video
  const [operation] = await video.annotateVideo(request);
  const results = await operation.promise();

  // Gets annotations for video
  const textAnnotations = results[0].annotationResults[0].textAnnotations;
  textAnnotations.forEach((textAnnotation) => {
    console.log(`${textAnnotation.text} `);
  });
}

// Execute the main function
main().catch(console.error);
