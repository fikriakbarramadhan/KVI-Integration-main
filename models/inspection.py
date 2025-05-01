from datetime import datetime
from models.user import db

class Inspection(db.Model):
    __tablename__ = 'tb_inspection'
    
    inspection_id = db.Column(db.Integer, primary_key=True)  # PK
    trx_id = db.Column(db.String(50), nullable=False)  # Transaction ID
    reg_no = db.Column(db.String(50), nullable=False)  # Registration Number
    remark_reg_no = db.Column(db.String(255))  # Remark for Registration Number
    engine_no = db.Column(db.String(50), nullable=False)  # Engine Number
    remark_engine_no = db.Column(db.String(255))  # Remark for Engine Number
    chassis_no = db.Column(db.String(50), nullable=False)  # Chassis Number
    remark_chassis_no = db.Column(db.String(255))  # Remark for Chassis Number
    front_fid = db.Column(db.String(255))  # Front Fid (Could be a file URL or data)
    back_fid = db.Column(db.String(255))  # Back Fid (Could be a file URL or data)
    engine_no_fid = db.Column(db.String(255))  # Engine Number Fid
    chassis_no_fid = db.Column(db.String(255))  # Chassis Number Fid
    
    # New fields for images as base64 encoded strings
    front_image_base64 = db.Column(db.Text)  # Base64 encoded front image
    back_image_base64 = db.Column(db.Text)   # Base64 encoded back image
    engine_no_image_base64 = db.Column(db.Text)  # Base64 encoded engine number image
    chassis_no_image_base64 = db.Column(db.Text)  # Base64 encoded chassis number image
    reg_no_image_base64 = db.Column(db.Text)  # Base64 encoded registration number image
    
    officer = db.Column(db.String(255))  # FK to User (Officer)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of the inspection
    
    def __repr__(self):
        return f"<Inspection {self.inspection_id} for {self.reg_no}>"
