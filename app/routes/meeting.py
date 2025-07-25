from flask import Blueprint, Response, redirect, url_for, request, session, jsonify

meeting_bp = Blueprint('meeting', __name__, url_prefix="/meeting")