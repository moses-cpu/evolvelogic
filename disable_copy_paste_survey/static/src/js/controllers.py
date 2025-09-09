import json
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class SurveyTrackingController(http.Controller):

    # @http.route('/survey/focus_loss', type='json', auth='user')
    # def record_focus_loss(self):
    #     user = request.env.user
    #     assessment_id = request.params.get('assessment_id')  # Ensure assessment_id is passed

    #     # Create a new record instead of updating
    #     # request.env['survey.video.capture'].sudo().create({
    #     #     'user_id': user.id,
    #     #     'assessment_id': assessment_id,
    #     #     'focus_lost_count': 1,  # Starts at 1 for a new record
    #     #     'last_focus_lost': datetime.now(),
    #     # })

    #     return {"status": "success"}

    @http.route('/survey/copy_paste_attempt', type='json', auth='user')
    def record_copy_paste_attempt(self):
        user = request.env.user
        data = json.loads(request.httprequest.data)  # Correct way to get JSON data
        assessment_id = data.get('assessment_id')  # Get assessment_id from JSON
        _logger.info("Method reached")
        _logger.info("----------------"+str(assessment_id))
        # if not assessment_id:
        #     return {"status": "error", "message": "assessment_id is required"}

        # Create a new record for each attempt
        survey_id = request.env['survey.video.capture'].sudo().create({
            'user_id': user.id,
            'participant_id': assessment_id,
            'copy_paste_attempts': 1,  # Tracks each instance separately
            'last_copy_paste_attempt': datetime.now(),
        })
        _logger.info("----------------"+str(survey_id))

        return {"status": "success"}

    # @http.route('/survey/video_capture', type='json', auth='user', methods=['POST'])
    # def record_video_capture(self):
    #     user = request.env.user
    #     data = request.jsonrequest

    #     video_data = data.get('video_data')  # Base64 encoded video
    #     filename = data.get('filename', f'survey_video_{datetime.now().strftime("%Y%m%d%H%M%S")}.webm')
    #     assessment_id = data.get('assessment_id')  # Ensure frontend sends this

    #     if not video_data:
    #         return {"status": "error", "message": "No video data received"}

    #     # Store in Odoo model
    #     request.env['survey.video.capture'].sudo().create({
    #         'user_id': user.id,
    #         'assessment_id': assessment_id,
    #         'video_data': base64.b64encode(video_data.encode()).decode(),  # Convert to base64 for Odoo storage
    #         'filename': filename,
    #         'recorded_at': datetime.now(),
    #     })

    #     return {"status": "success", "message": "Video recorded successfully"}
