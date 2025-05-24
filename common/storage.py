import uuid
from firebase_admin import storage

def upload_imagem_firebase(imagem, bucket_name: str, path_prefix: str = 'fotos/'):
    """
    Faz upload de uma imagem para o Firebase e retorna a URL pública.
    """
    bucket = storage.bucket(bucket_name)
    filename = f"{uuid.uuid4()}_{imagem.name}"
    blob = bucket.blob(f'{path_prefix}{filename}')
    blob.upload_from_file(imagem, content_type=imagem.content_type)
    blob.make_public()
    return blob.public_url
