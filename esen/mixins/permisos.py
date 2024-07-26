from rest_framework_simplejwt.authentication import JWTAuthentication
from esen.settings import SECRET_KEY
from jwt import decode


class AutorizacionMixin():

    def identificar(self, request):
        jwtObject = JWTAuthentication()
        header = jwtObject.get_header(request)
        raw_token = jwtObject.get_raw_token(header)
        payload = decode(raw_token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')

        return user_id