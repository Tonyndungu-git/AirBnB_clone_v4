#!/usr/bin/python3

"""
Create a new view for State objects
that handles all default RESTFul API actions
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object of id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ deletes a state with certain id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new state """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates a certain state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
