import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify, url_for
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.enum import project_status
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', required=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('owner_id', type=int, location='json', required=True)
parser.add_argument('kind_id', type=int, location='json', required=True)

resource_fields = {'project': itemStatus(attribute='status')}
resource_fields['list']={}
resource_fields['list']['sublist']={}

user_fields = {
    'projectName': fields.String,
    'projectKinds':fields.String
}

class ProjectView():
    def __init__(self, projectName, projectKinds=None):
        self.projectName = projectName
        self.projectKinds = projectKinds

data = {}
class Profile(Resource):
    # @marshal_with(user_fields)
    def get(self):
        str_list = []

        project = ProjectModel.query.get(1)
        # for name, fullname in db.session.query(User.name, User.fullname).filter(User.fullname=='Ed Jones'):
        #     print(name, fullname)
        # projectKinds = ','.join(project.kinds)
        # project = db.session.query(ProjectModel, ).first()
        # print project.kinds
        for kind in project.kinds:
            str_list.append(kind.name)

        # return ProjectView(project.name,','.join(str_list))
        return jsonify({
            'projectName':project.name,
            'projectKinds':','.join(str_list),
            'url':url_for('.userep', _external=True, userid=1),
            })
