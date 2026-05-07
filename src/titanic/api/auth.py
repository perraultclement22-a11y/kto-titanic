import os
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

security = HTTPBearer(auto_error=False)

def verify_token(scope: str):
    async def _verify(credentials: HTTPAuthorizationCredentials = Depends(security)):
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token manquant",
            )

        oauth2_domain = os.getenv("OAUTH2_DOMAIN", "")
        if not oauth2_domain:
            return credentials.credentials

        try:
            jwks_url = f"https://{oauth2_domain}/.well-known/jwks.json"
            import urllib.request, json
            with urllib.request.urlopen(jwks_url) as response:
                jwks = json.loads(response.read())

            token = credentials.credentials
            header = jwt.get_unverified_header(token)
            key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
            if key is None:
                raise HTTPException(status_code=401, detail="Clé invalide")

            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=f"https://{oauth2_domain}/api/v2/",
            )
            return token
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token invalide: {e}")

    return _verify
