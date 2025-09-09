# video_capture.py
from odoo import models, fields, api
import base64

class SurveyVideoCapture(models.Model):
    _name = 'survey.video.capture'
    _description = 'Survey Video Capture'

    survey_id = fields.Many2one('survey.survey', string='Survey')
    participant_id = fields.Many2one('survey.user_input', string='Participant')
    video_data = fields.Binary(string='Captured Video')
    filename = fields.Char(string='Filename')
    user_id = fields.Many2one('res.users', string="User", required=True)
    video_data = fields.Binary(string="Captured Video")
    filename = fields.Char(string="Filename")

    focus_lost_count = fields.Integer(string="Focus Lost Count", default=0)
    copy_paste_attempts = fields.Integer(string="Copy-Paste Attempts", default=0)
    last_focus_lost = fields.Datetime(string="Last Focus Lost Time")
    last_copy_paste_attempt = fields.Datetime(string="Last Copy-Paste Attempt Time")

    video_url = fields.Char(string="Video URL", compute="_compute_video_url")

    @api.depends('video_data')
    def _compute_video_url(self):
        for record in self:
            if record.video_data:
                record.video_url = f"data:video/mp4;base64,{record.video_data.decode()}"
            else:
                record.video_url = ''

class SurveyVideoCapture(models.Model):
    _inherit = 'survey.user_input'
    
    survey_actions = fields.One2many('survey.video.capture','participant_id',string="Actions")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    title_1 = fields.Selection([
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('dr', 'Dr'),
        ('prof', 'Prof'),
        ('miss', 'Miss')], 
        string="Title"
    )
    surname_1 = fields.Char(string="Surname")
    id_number = fields.Char(string="ID Number")
    geographical_location = fields.Selection([
        ('urban', 'Urban'),
        ('peri-urban', 'Peri-Urban'),
        ('rural-village', 'Rural Area - Villages'),
        ('rural-farm', 'Rural Area - Farms'),
        ('informal-settlement', 'Informal Settlement')], 
        string="Geographical Location"
    )
    cell_number_1 = fields.Char(string="Cell Number")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], 
        string="Gender"
    )
    level_of_education = fields.Selection([
        ('below_grade_8', 'Below Grade 8'),
        ('below_grade_12', 'Below Grade 12/Matric'),
        ('matric', 'Matric (Grade 12)'),
        ('short_course', 'Short Course Certificate'),
        ('high_certificate', 'High Certificate'),
        ('diploma', 'Diploma'),
        ('degree', 'Degree/Honors/Doctorate')], 
        string="Level of Education"
    )
    population_group = fields.Selection([
        ('african', 'African'),
        ('colored', 'Colored'),
        ('white', 'White'),
        ('indian', 'Indian'),
        ('asian', 'Asian')], 
        string="Population Group"
    )
    province = fields.Selection([
        ('Eastern Cape', 'Eastern Cape'),
        ('Free State', 'Free State'),
        ('Gauteng', 'Gauteng'),
        ('KwaZulu-Natal', 'KwaZulu-Natal'),
        ('Limpopo', 'Limpopo'),
        ('Mpumalanga', 'Mpumalanga'),
        ('North West', 'North West'),
        ('Northern Cape', 'Northern Cape'),
        ('Western Cape', 'Western Cape')], 
        string="Province"
    )
    physical_address_1 = fields.Text(string="Physical Address")
    popia_consent = fields.Boolean(string="POPIA Concent")
