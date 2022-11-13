from flask import Blueprint, jsonify, Response

from utils.constants import GC_AUTH_FILE, GC_BUCKET_NAME
import utils.google_cloud as GC

google_cloud_controller_blueprint = Blueprint('google_cloud', __name__)

@google_cloud_controller_blueprint.get("/filename/<string:filename>")
def get_google_cloud_signed_url(filename: str) -> Response:
        """Create a signed URL for a Google Cloud Bucket entity."""
        # The name of the file on Google Cloud
        # filename = "your-filename"
        signed_url: str = GC.generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, filename)

        if not signed_url:
            raise ResourceNotFound("Could not generate signed URL for filename: {}".format(filename))

        return jsonify({
            "filename": filename,
            "callback_url": signed_url,
        })
