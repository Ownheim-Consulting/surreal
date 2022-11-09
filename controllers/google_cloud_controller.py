from flask import jsonify, Blueprint

from utils.google_cloud import generate_signed_url
from utils.constants import GC_AUTH_FILE, GC_BUCKET_NAME

google_cloud_controller_blueprint = Blueprint('google-cloud', __name__)

@google_cloud_controller_blueprint.get("/api/google-cloud/filename/<string:filename>")
def get_google_cloud_signed_url(filename: str):
        """Create a signed URL for a Google Cloud Bucket entity."""
        # The name of the file on Google Cloud
        # filename = "your-filename"
        signed_url = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, filename)

        if signed_url is None:
            raise ResourceNotFound("Could not generate signed URL for filename: {}".format(filename))

        return jsonify({
            "filename": filename,
            "callbackUrl": signed_url,
        })
