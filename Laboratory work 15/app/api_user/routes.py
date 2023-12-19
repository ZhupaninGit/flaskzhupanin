from flask import jsonify,request
from flask_restful import Resource,abort
from app.api_user.schemas import UserSchema,UserPutSchema
from app.models import User
from app import db
from marshmallow import ValidationError


user_schema = UserSchema(exclude=("password",))
users_schema = UserSchema(many=True,exclude=("password",))

class UserApi(Resource):
    def get(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            result = user_schema.dump(user)
            return jsonify(result)
        else:
            abort(404, message="User not found")
    
    def delete(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": f"User `{user.username}` deleted successfully"})
        else:
            abort(404, message="User not found")

    def put(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            try:
                user_put_schema = UserPutSchema()
                data = user_put_schema.load(request.json)
                isProvided = False
                if data.get("username"):
                    user.username = data.get("username")
                    isProvided = True

                if data.get("email"):
                    user.email = data.get("email")
                    isProvided = True

                if not isProvided:
                    abort(404, message="Data not provided")
                    
                db.session.commit()
                result = user_put_schema.dump(user)
                return result 

            

            except ValidationError as error:
                return {"error": error.messages}
        else:
            abort(404, message="User not found")


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        result = users_schema.dump(users)
        return jsonify(result)

    def post(self):
        try:
            user_schema = UserSchema()
            result = user_schema.load(request.json)

            new_user = User(
                username=result.get("username"),
                email=result.get("email"),
                password=result.get("password")
            )

            db.session.add(new_user)
            db.session.commit()

            return {
                "message":"user created",
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }, 201 
            
        except ValidationError as err:
            return {"errors": err.messages}, 400