from flask_restful import reqparse


def make_jobs_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('team_leader', type=int, required=True)
    parser.add_argument('job', required=True)
    parser.add_argument('work_size', required=True, type=int)
    parser.add_argument('is_finished', required=True, type=bool)
    parser.add_argument('collaborators', required=True)