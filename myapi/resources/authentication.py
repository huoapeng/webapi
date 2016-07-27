import datetime
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db
from myapi.model.user import UserModel
from myapi.model.authentication import ApprovalModel, PrivateAuthenticateModel, CompanyAuthenticateModel, BankModel
from myapi.model.enum import authentication_type, verify_type, approval_result

class Approval(Resource):
    def get(self, id):
        approval = ApprovalModel.query.get(id)
        return jsonify(approval.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('authenType', type=int, location='json', required=True)
        post_parser.add_argument('authenID', type=int, location='json', required=True)
        post_parser.add_argument('approvalStatus', type=int, location='json', required=True)
        post_parser.add_argument('userid', type=int, location='json', required=True)
        post_parser.add_argument('adminid', type=int, location='json', required=True)
        post_parser.add_argument('description', type=str, location='json', required=True)
        args = post_parser.parse_args()

        a = ApprovalModel(
            args.authenType, args.authenID, args.approvalStatus, args.userid, args.adminid, args.description)
        db.session.add(a)

        user = UserModel.query.get(args.userid)
        user.authentications.append(a)
        if args.approvalStatus == approval_result.allow:
            user.authenticationType = user.authenticationType | args.authenType

        for key in authentication_type.__dict__:
            if not key.startswith('__') and args.authenType == authentication_type.__dict__[key]:
                p = model[key].query.filter_by(id = args.authenID).one()
                p.approvalStatus = args.approvalStatus
                break;

        db.session.commit()
        return jsonify(a.serialize())
        
class PrivateAuthenticate(Resource):
    def get(self, id):
        authority = PrivateAuthenticateModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('identityid', type=str, location='json', required=True)
        post_parser.add_argument('identityFrontImage', type=str, location='json', required=True)
        post_parser.add_argument('identityBackImage', type=str, location='json', required=True)
        args = post_parser.parse_args()

        p = PrivateAuthenticateModel(args.name, args.identityid, args.identityFrontImage, args.identityBackImage)
        db.session.add(p)

        user = UserModel.query.get(args.ownerid)
        user.privateAuthenHistory.append(p)
        db.session.commit()
        return jsonify(p.serialize())

class CompanyAuthenticate(Resource):
    def get(self, id):
        authority = CompanyAuthenticateModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('businessScope', type=str, location='json', required=True)
        post_parser.add_argument('licenseID', type=str, location='json', required=True)
        post_parser.add_argument('licenseImage', type=str, location='json', required=True)
        post_parser.add_argument('contactImage', type=str, location='json', required=True)
        post_parser.add_argument('verifyType', type=str, location='json', required=True)
        args = post_parser.parse_args()

        c = CompanyAuthenticateModel(args.name, args.businessScope, args.licenseID, 
            args.licenseImage, args.contactImage, args.verifyType)
        db.session.add(c)

        user = UserModel.query.get(args.ownerid)
        user.companyAuthenHistory.append(c)
        db.session.commit()
        return jsonify(c.serialize())

class BankAuthenticate(Resource):
    def get(self, id):
        authority = BankModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('bankAccount', type=str, location='json', required=True)
        post_parser.add_argument('bankName', type=str, location='json', required=True)
        post_parser.add_argument('bankLocation', type=str, location='json', required=True)
        args = post_parser.parse_args()

        b = BankModel(args.name, args.bankAccount, args.bankName, args.bankLocation)
        db.session.add(b)

        user = UserModel.query.get(args.ownerid)
        user.bankAuthenHistory.append(b)
        db.session.commit()
        return jsonify(b.serialize())

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('code', type=str, location='json', required=True)
        args = post_parser.parse_args()

        b = BankModel.query.get(args.id)
        if b.checkCode:
            return jsonify(result='already has check code')
        else:
            b.checkCode = args.code
            db.session.commit()
            return jsonify(b.serialize())

class AuthenticationList(Resource):
    def get(self, kind):
        # for x in dir(authentication_type):
        #     print getattr(authentication_type, str(x))
        for key in authentication_type.__dict__:
            if not key.startswith('__') and kind == authentication_type.__dict__[key]:
                result = model[key].query.filter_by(approvalStatus = None).all()
                return jsonify(kind=kind, data=[e.serialize() for e in result])

        return jsonify(data=[])

model = {
    'private' : PrivateAuthenticateModel,
    'company' : CompanyAuthenticateModel,
    'bank' : BankModel
}

