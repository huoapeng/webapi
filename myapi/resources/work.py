import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.work import WorkModel
from myapi.model.user import UserModel
from myapi.model.enum import work_status

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, location='json')
parser.add_argument('title', type=str, location='json')
parser.add_argument('image', type=str, location='json')
parser.add_argument('description', type=str, location='json')
parser.add_argument('userid', type=int, location='json')

class Work(Resource):
    def get(self, workid):
        work = WorkModel.query.get(workid)
        if work:
            return jsonify(work.serialize())
        else:
            return jsonify('{}')

    def post(self):
        args = parser.parse_args()
        work = WorkModel(args.title, args.image, args.description)
        db.session.add(work)

        user = UserModel.query.get(args.userid)
        user.works.append(work)
        db.session.commit()
        return jsonify(work.serialize())

    def put(self):
        pass

    def delete(self):
        args = parser.parse_args()
        work = WorkModel.query.get(args.id)
        work.status = work_status.delete
        db.session.commit()
        return jsonify(result='true')

class UserWorks(Resource):
    def get(self, userid, page):
        works = WorkModel.query.filter_by(owner_id = userid)
        works = works.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = works.total,
            pages = works.pages,
            page = works.page,
            per_page = works.per_page,
            has_next = works.has_next,
            has_prev = works.has_prev,
            next_num = works.next_num,
            prev_num = works.prev_num,
            data=[e.serialize() for e in works.items])

# class SearchTagsByName(Resource):
#     def get(self, keyword):
#         return WorkModel.query.filter(WorkModel.name.contains(keyword)).all()