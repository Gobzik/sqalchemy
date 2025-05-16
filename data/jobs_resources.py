from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs
from data.jobs_parser import make_jobs_parser

parser = make_jobs_parser()


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'users': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'start_date', 'end_date',
                  'is_finished', 'collaborators'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Job {job_id} deleted'
        })


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'start_date', 'end_date',
                  'is_finished', 'collaborators')
        ) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            is_finished=args['is_finished'],
            collaborators=args['collaborators']
        )
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})
