import json
import base64
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class SurveyTrackingController(http.Controller):

    @http.route('/survey/focus_loss', type='json', auth='user')
    def record_focus_loss(self):
        user = request.env.user
        data = json.loads(request.httprequest.data)  # Correct way to get JSON data
        assessment_id = data.get('assessment_id')  # Get assessment_id from JSON
        _logger.info("Method reached")
        _logger.info("----------------"+str(assessment_id))
        survey_record = request.env['survey.user_input'].sudo().search([('access_token', '=', assessment_id['assessment_id'])], limit=1)

        survey_id = request.env['survey.video.capture'].sudo().search([('participant_id','=',survey_record.id)],limit=1)
        if survey_id :
            survey_id.focus_lost_count += 1 # Starts at 1 for a new record
            survey_id.last_focus_lost = datetime.now()
        else:
            survey_id = request.env['survey.video.capture'].sudo().create({
                            'user_id': user.id,
                            'participant_id': survey_record.id,
                            'focus_lost_count': 1,  # Starts at 1 for a new record
                            'last_focus_lost': datetime.now(),
                        })
        _logger.info("----------------"+str(survey_id))

        

        

        return {"status": "success"}

    @http.route('/survey/copy_paste_attempt', type='json', auth='user')
    def record_copy_paste_attempt(self):
        user = request.env.user
        data = json.loads(request.httprequest.data)  # Correct way to get JSON data
        assessment_id = data.get('assessment_id')  # Get assessment_id from JSON
        _logger.info("Method reached")
        _logger.info("----------------"+str(assessment_id))
        survey_record = request.env['survey.user_input'].sudo().search([('access_token', '=', assessment_id['assessment_id'])], limit=1)

        # Create a new record for each attempt
        survey_id = request.env['survey.video.capture'].sudo().search([('participant_id','=',survey_record.id)],limit=1)
        if survey_id :
            survey_id.copy_paste_attempts += 1 # Starts at 1 for a new record
            survey_id.last_copy_paste_attempt = datetime.now()
        else:
            survey_id = request.env['survey.video.capture'].sudo().create({
                'user_id': user.id,
                'participant_id': survey_record.id,
                'copy_paste_attempts': 1,  # Tracks each instance separately
                'last_copy_paste_attempt': datetime.now(),
            })
        _logger.info("----------------"+str(survey_id))

        return {"status": "success"}

    @http.route('/survey/video_capture', type='json', auth='user', methods=['POST'])
    def record_video_capture(self):
        user = request.env.user
        data = json.loads(request.httprequest.data)  # Correct way to get JSON data
        
        video_data = data.get('video_data')  # Base64 encoded video
        _logger.info("++++++++++++++++++++++++++++++++++++++++"+str(type(video_data)))
        filename = data.get('filename', f'survey_video_{datetime.now().strftime("%Y%m%d%H%M%S")}.webm')
        assessment_id = data.get('assessment_id')  # Ensure frontend sends this
        survey_record = request.env['survey.user_input'].sudo().search([('access_token', '=', assessment_id['assessment_id'])], limit=1)
        #_logger.info("-------AA---------"+str(video_data))
        # if not video_data:
        #     return {"status": "error", "message": "No video data received"}

        # Store in Odoo model
        _logger.info("---------------->>>>")
        survey_id = request.env['survey.video.capture'].sudo().search([('participant_id','=',survey_record.id)],limit=1)
        _logger.info("---------------->>>>")
        # if isinstance(video_data, str):
        #     # Convert string to bytes (UTF-8 encoding might not work for binary data)
        #     video_data = video_data.encode('utf-8')
        if survey_id :
            survey_id.video_data = video_data.encode() # Starts at 1 for a new record
            survey_id.filename = filename
        else:
            survey_id = request.env['survey.video.capture'].sudo().create({
                            'user_id': user.id,
                            'participant_id': survey_record.id,
                            'video_data': video_data.encode(), 
                            'filename': filename,
                        })
        _logger.info("---------AA------->>>>"+str(video_data.encode()))
            
        _logger.info("---------LAST-------"+str(survey_id))
        

        return {"status": "success", "message": "Video recorded successfully"}
