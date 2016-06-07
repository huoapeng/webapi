import datetime
from flask import url_for
from myapi import db
from enum import verify_type, approval_status

class PrivateAuthorisedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    identityID = db.Column(db.String(50))
    identityFrontImage = db.Column(db.String(500))
    identityBackImage = db.Column(db.String(500))
    authorisedDate = db.Column(db.DateTime)

    approval_status = db.Column(db.Integer)
    approvalDate = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, name, identityID, identityFrontImage, identityBackImage):
        self.name = name
        self.identityID = identityID
        self.identityFrontImage = identityFrontImage
        self.identityBackImage = identityBackImage
        self.authorisedDate = datetime.datetime.now()
        self.approval_status = approval_status.start

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'identityID': self.identityID,
            'identityFrontImage': url_for('.imageep', _external=True, \
                userid=self.owner_id, imagetype=2, filename=self.identityFrontImage)\
                if self.identityFrontImage else self.identityFrontImage,
            'identityBackImage': url_for('.imageep', _external=True, \
                userid=self.owner_id, imagetype=3, filename=self.identityBackImage)\
                if self.identityBackImage else self.identityBackImage,
            'authorisedDate': self.authorisedDate,
            'approvalStatus': self.approval_status,
            'approvalDate': self.approvalDate,
            'ownerID': self.owner_id,
            'owner': url_for('.userep', _external=True, userid=self.owner_id),
        }

class CompanyAuthorisedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    businessScope = db.Column(db.Text)
    businessLicenseID = db.Column(db.String(500))
    businessLicenseImage = db.Column(db.String(500))
    contactImage = db.Column(db.String(500))
    verifyType = db.Column(db.Integer)
    bankAccount = db.Column(db.String(100))
    bankName = db.Column(db.String(500))
    bankLocation = db.Column(db.String(200))
    authorisedDate = db.Column(db.DateTime)

    approval_status = db.Column(db.Integer)
    approvalDate = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, name, businessScope, businessLicenseID, verifyType, bankAccount, bankName, bankLocation,
            businessLicenseImage, contactImage):
        self.name = name
        self.businessScope = businessScope
        self.businessLicenseID = businessLicenseID
        self.businessLicenseImage = businessLicenseImage
        self.contactImage = contactImage
        self.verifyType = verifyType
        self.bankAccount = bankAccount
        self.bankName = bankName
        self.bankLocation = bankLocation
        self.authorisedDate = datetime.datetime.now()
        self.approval_status = approval_status.start

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'businessScope': self.businessScope,
            'businessLicenseID':self.businessLicenseID,
            'businessLicenseImage': url_for('.imageep', _external=True, \
                userid=self.owner_id, imagetype=4, filename=self.businessLicenseImage)\
                if self.businessLicenseImage else self.businessLicenseImage,
            'contactImage': url_for('.imageep', _external=True, \
                userid=self.owner_id, imagetype=5, filename=self.contactImage)\
                if self.contactImage else self.contactImage,
            'verifyType': self.verifyType,
            'bankAccount': self.bankAccount,
            'bankName': self.bankName,
            'bankLocation': self.bankLocation,
            'authorisedDate': self.authorisedDate,
            'approvalStatus': self.approval_status,
            'approvalDate': self.approvalDate,
            'ownerID': self.owner_id,
            'owner': url_for('.userep', _external=True, userid=self.owner_id),
        }
